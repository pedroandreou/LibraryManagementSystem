import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def create_connection(db_path):
    conn = None

    try:
        # open db => if does not exist => will be created
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as error:
        print(error)

    return conn


def execute_query(conn, query=None, data=None):
    try:
        c = conn.cursor()

        if query is not None and data is not None:
            c.execute(query, data)
        else:
            c.execute(query)
    except sqlite3.Error as error:
        print(error)
    finally:
        conn.commit()


def create_table(conn, table):
    title = table[0]
    table = table[1:]
    table_len = len(table)

    all_cols = ""
    for counter, col in enumerate(table):
        if table_len == counter + 1:
            # do not add comma => last col of the table
            all_cols += col
            break

        all_cols += col + ","

    create_table = f""" CREATE TABLE IF NOT EXISTS {title} (
                                    {all_cols}
                                ); """

    execute_query(conn, create_table)


def drop_table(conn, table_name):
    drop_table = f"DROP TABLE {table_name};"

    execute_query(conn, drop_table)


def init_db(conn, table_name, file_path=None):
    df = pd.read_csv(file_path, na_values="---")
    df.to_sql(name=table_name, con=conn, if_exists="append", index=False)

    return df


def create_dimension_table(fact_table, col_to_be_normalized, new_cols):
    unique_values_lst = fact_table[col_to_be_normalized].unique()
    ids = list(range(1, 1 + len(unique_values_lst)))

    dim_table = pd.DataFrame(data=list(zip(ids, unique_values_lst)), columns=new_cols)

    return dim_table


def map_vals_to_ids(
    fact_df, fact_col_name, dimension_df, dimension_keycol_name, dimension_refcol_name
):
    """
    This function maps all the values of the fact table from a dimension table
    inspired by: https://stackoverflow.com/questions/53818434/pandas-replacing-values-by-looking-up-in-an-another-dataframe
    """

    # map each col value to an id
    mapping_dict = dimension_df.set_index(dimension_refcol_name)[
        dimension_keycol_name
    ].to_dict()

    # get all the values of the col from the fact table
    col_vals = fact_df.filter(like=fact_col_name)

    # replace all
    fact_df[col_vals.columns] = col_vals.replace(mapping_dict)

    return fact_df


def fill_new_fields(
    df,
    idx,
    transactionTypeMsg,
    isCheckedOutNum,
    checkedOutMemberId,
    isReservedNum,
    reservedMemberId,
    initialDate,
    endRecordDate,
    isActive,
):
    """This function is inserting data to the new fields of the Transactions table"""

    df.loc[idx, "TransactionType"] = transactionTypeMsg
    df.loc[idx, "IsCheckedOut"] = isCheckedOutNum
    df.loc[idx, "CheckedOutMemberId"] = checkedOutMemberId
    df.loc[idx, "IsReserved"] = isReservedNum
    df.loc[idx, "ReservedMemberId"] = reservedMemberId

    reserve_or_checkout_flag = False
    if transactionTypeMsg == "Reserve":
        reserve_or_checkout_flag = True
        num_of_days = 10
    elif transactionTypeMsg == "Checkout":
        reserve_or_checkout_flag = True
        num_of_days = 30

    # Reserve or Checkout
    if reserve_or_checkout_flag == True:
        # convert the string to datetime
        init_date = datetime.strptime(initialDate, "%d/%m/%Y")
        # add days based on the transaction type above
        expiry_date = init_date + timedelta(days=num_of_days)
        # change format
        expiry_date = expiry_date.strftime("%d/%m/%Y")
        # get only the date and not the time
        expiry_date = str(expiry_date).split()[0]
        df.loc[idx, "TransactionTypeExpirationDate"] = expiry_date
    # Return
    else:
        df.loc[idx, "TransactionTypeExpirationDate"] = np.nan

    df.loc[idx, "StartRecordDate"] = initialDate
    df.loc[idx, "EndRecordDate"] = endRecordDate
    df.loc[idx, "IsActive"] = isActive


def deactivateLastTransaction(final_df, row):
    """
    This function is called for deactivating the previous transaction of the specific member id
    In case it is the first transaction of the specific book's copy, then it won't do anything
    """
    allTransactions_of_bookId_df = final_df[
        final_df["BookId"] == row.loc["BookId"]
    ].dropna(axis=0, subset=["IsActive"])

    last_activatedTransactionId = None
    # check that there is an older transaction for the specific book id
    if len(allTransactions_of_bookId_df) >= 1:
        # get last transaction id that belong to the book id
        last_activatedTransactionId = allTransactions_of_bookId_df.iloc[-1][
            "TransactionId"
        ]

        # deactivate the last transaction
        final_df.loc[last_activatedTransactionId - 1, "IsActive"] = 0

    return last_activatedTransactionId


def findLastMemberId_and_deactivateLastTransaction(initial_df, final_df, row):
    """
    This function is called when either Reserve and Checkout happen at the same time
    or all Reserve, Checkout, Return occur in a single transaction.

    As a result, the previous transaction gets deactivated and since Reserve and Checkout are
    always part of either of the two cases above:
    in case there is no previous transaction: both Reserve and Checkout have the same member id
    otherwise, if the function is called for Reserve, then the CheckOutMemberId is the previous transaction's member id
    or if thefunction is called for Checkout, then the ReservedMemberId is the previous transaction's member id
    """
    last_activatedTransactionId = deactivateLastTransaction(final_df, row)

    if last_activatedTransactionId is not None:
        if (
            final_df.loc[last_activatedTransactionId - 1, "TransactionType"]
            == "Checkout"
            or final_df.loc[last_activatedTransactionId - 1, "TransactionType"]
            == "Reserve"
        ):
            # get the last member that checked out
            last_lastMemberId = initial_df.loc[
                last_activatedTransactionId - 1, "MemberId"
            ]
        else:
            last_lastMemberId = None
    else:
        last_lastMemberId = None

    # there was no previous transaction => assigning the same current member id
    if last_lastMemberId is None:
        last_lastMemberId = row.loc["MemberId"]

    # casting => fixed problem with automatically allocating 8 bytes space to the CheckedOutMemberId field where I needed to download each cell's file to see the real value
    return int(last_lastMemberId)


def normalize_data(conn, bookInfo_df, loanReservationHistory_df):

    ### create BookInventory fact table ###
    bookInventory_df = bookInfo_df[["Id", "Genre", "Title", "Author"]].copy()

    # create and fill Genre table with unique values of genres and map the ids
    genre_df = create_dimension_table(
        bookInventory_df, "Genre", ["GenreKey", "GenreRef"]
    )
    bookInventory_df = map_vals_to_ids(
        bookInventory_df, "Genre", genre_df, "GenreKey", "GenreRef"
    )

    # create and fill Title table with unique values of title books and map the ids
    bookTitles_df = create_dimension_table(
        bookInventory_df, "Title", ["BookTitleKey", "BookTitleRef"]
    )
    bookInventory_df = map_vals_to_ids(
        bookInventory_df, "Title", bookTitles_df, "BookTitleKey", "BookTitleRef"
    )

    # create and fill Author table with unique values of author books and map the ids
    bookAuthors_df = create_dimension_table(
        bookInventory_df, "Author", ["BookAuthorKey", "BookAuthorRef"]
    )
    bookInventory_df = map_vals_to_ids(
        bookInventory_df, "Author", bookAuthors_df, "BookAuthorKey", "BookAuthorRef"
    )

    # rename col names
    bookInventory_df.rename(
        columns={
            "Id": "BookId",
            "Genre": "GenreKey",
            "Title": "BookTitleKey",
            "Author": "BookAuthorKey",
        },
        inplace=True,
    )

    # add new column BookCopyKey to fact table and add the ids of book copies
    bookInventory_df["BookCopyKey"] = list(range(1, 1 + len(bookInventory_df)))

    # create new dimension table BookCopies
    data = {
        "BookCopyKey": bookInventory_df["BookCopyKey"],
        "PurchasePrice£": bookInfo_df["PurchasePrice£"],
        "PurchaseDate": bookInfo_df["PurchaseDate"],
    }
    bookCopies_df = pd.DataFrame(data)

    # add all tables to db
    bookInventory_df.to_sql(
        name="BookInventory", con=conn, if_exists="append", index=False
    )
    genre_df.to_sql(name="Genre", con=conn, if_exists="append", index=False)
    bookTitles_df.to_sql(name="BookTitle", con=conn, if_exists="append", index=False)
    bookAuthors_df.to_sql(name="BookAuthor", con=conn, if_exists="append", index=False)
    bookCopies_df.to_sql(name="BookCopies", con=conn, if_exists="append", index=False)

    ### create Transactions fact table ###
    transactions_df = pd.DataFrame()
    data = {
        "TransactionId": loanReservationHistory_df["TransactionId"],
        "BookId": loanReservationHistory_df["BookId"],
        "BookCopyKey": loanReservationHistory_df["BookId"],
        "TransactionType": np.nan,
        "IsCheckedOut": np.nan,
        "CheckedOutMemberId": np.nan,
        "ReservedMemberId": np.nan,
        "IsReserved": np.nan,
        "TransactionTypeExpirationDate": np.nan,
        "StartRecordDate": np.nan,
        "EndRecordDate": np.nan,
        "IsActive": np.nan,
    }
    transactions_df = pd.DataFrame(
        data,
        columns=[
            "TransactionId",
            "BookId",
            "BookCopyKey",
            "TransactionType",
            "IsCheckedOut",
            "CheckedOutMemberId",
            "IsReserved",
            "ReservedMemberId",
            "TransactionTypeExpirationDate",
            "StartRecordDate",
            "EndRecordDate",
            "IsActive",
        ],
    )

    # create values for new fields of Transactions table
    for (idx, row) in loanReservationHistory_df.iterrows():
        if pd.isnull(row.loc["ReservationDate"]) == False:
            # Reserve
            if pd.isnull(row.loc["CheckoutDate"]) and pd.isnull(row.loc["ReturnDate"]):
                deactivateLastTransaction(transactions_df, row)

                fill_new_fields(
                    transactions_df,
                    idx,
                    transactionTypeMsg="Reserve",
                    isCheckedOutNum=0,
                    checkedOutMemberId=np.nan,
                    isReservedNum=1,
                    reservedMemberId=row.loc["MemberId"],
                    initialDate=row.loc["ReservationDate"],
                    endRecordDate=np.nan,
                    isActive=1,
                )
            # Reserve, Checkout at the same time
            elif pd.isnull(row.loc["CheckoutDate"]) == False:
                # Reserve, Checkout at the same time
                if pd.isnull(row.loc["ReturnDate"]):
                    reserve_date = datetime.strptime(
                        row.loc["ReservationDate"], "%d/%m/%Y"
                    )
                    checkout_date = datetime.strptime(
                        row.loc["CheckoutDate"], "%d/%m/%Y"
                    )

                    # it is reserved by a new member even if the book is currently checked out
                    if reserve_date > checkout_date:
                        last_checkedOutMemberId = (
                            findLastMemberId_and_deactivateLastTransaction(
                                loanReservationHistory_df, transactions_df, row
                            )
                        )

                        fill_new_fields(
                            transactions_df,
                            idx,
                            transactionTypeMsg="Reserve",
                            isCheckedOutNum=1,
                            checkedOutMemberId=last_checkedOutMemberId,
                            isReservedNum=1,
                            reservedMemberId=row.loc["MemberId"],
                            initialDate=row.loc["ReservationDate"],
                            endRecordDate=np.nan,
                            isActive=1,
                        )
                    # otherwise, the reservation will be considered that it has already been done in the past => main transaction type will be Checkout
                    else:
                        last_ReservedMemberId = (
                            findLastMemberId_and_deactivateLastTransaction(
                                loanReservationHistory_df, transactions_df, row
                            )
                        )

                        fill_new_fields(
                            transactions_df,
                            idx,
                            transactionTypeMsg="Checkout",
                            isCheckedOutNum=1,
                            checkedOutMemberId=row.loc["MemberId"],
                            isReservedNum=1,
                            reservedMemberId=last_ReservedMemberId,
                            initialDate=row.loc["CheckoutDate"],
                            endRecordDate=np.nan,
                            isActive=1,
                        )
                # All Reserve, Checkout, Return at the same time
                else:
                    last_checkedOutMemberId = (
                        findLastMemberId_and_deactivateLastTransaction(
                            loanReservationHistory_df, transactions_df, row
                        )
                    )

                    reserve_date = datetime.strptime(
                        row.loc["ReservationDate"], "%d/%m/%Y"
                    )
                    return_date = datetime.strptime(row.loc["ReturnDate"], "%d/%m/%Y")

                    # if the reservation date is more recent than the return date => reservation happened latest
                    if reserve_date > return_date:
                        fill_new_fields(
                            transactions_df,
                            idx,
                            transactionTypeMsg="Reserve",
                            isCheckedOutNum=1,
                            checkedOutMemberId=last_checkedOutMemberId,
                            isReservedNum=1,
                            reservedMemberId=row.loc["MemberId"],
                            initialDate=row.loc["ReservationDate"],
                            endRecordDate=np.nan,
                            isActive=1,
                        )
                    # otherwise, the reservation will be considered that it has already been done in the past => main transaction type will be Return
                    else:
                        fill_new_fields(
                            transactions_df,
                            idx,
                            transactionTypeMsg="Return",
                            isCheckedOutNum=1,
                            checkedOutMemberId=last_checkedOutMemberId,
                            isReservedNum=1,
                            reservedMemberId=row.loc["MemberId"],
                            initialDate=row.loc["ReturnDate"],
                            endRecordDate=np.nan,
                            isActive=1,
                        )
        elif (
            pd.isnull(row.loc["ReservationDate"])
            and pd.isnull(row.loc["CheckoutDate"]) == False
        ):
            deactivateLastTransaction(transactions_df, row)

            # just Checkout
            if pd.isnull(row.loc["ReturnDate"]):
                fill_new_fields(
                    transactions_df,
                    idx,
                    transactionTypeMsg="Checkout",
                    isCheckedOutNum=1,
                    checkedOutMemberId=row.loc["MemberId"],
                    isReservedNum=0,
                    reservedMemberId=np.nan,
                    initialDate=row.loc["CheckoutDate"],
                    endRecordDate=np.nan,
                    isActive=1,
                )
            # Checkout and Return at the same time
            else:
                fill_new_fields(
                    transactions_df,
                    idx,
                    transactionTypeMsg="Return",
                    isCheckedOutNum=1,
                    checkedOutMemberId=row.loc["MemberId"],
                    isReservedNum=0,
                    reservedMemberId=np.nan,
                    initialDate=row.loc["ReturnDate"],
                    endRecordDate=np.nan,
                    isActive=1,
                )

    transactions_df.to_sql(
        name="Transactions", con=conn, if_exists="append", index=False
    )

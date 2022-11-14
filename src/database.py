import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class Database:
    def __init__(self, db_path):

        self.db_path = db_path

        def create_connection(path):
            """This function initializes the database connection
               If the databse does not exist, then it will be created

            Args:
                db_path (str): A string containing the path where the database file should be created

            Returns:
                sqlite3.Connection: The established connection with the local SQLite database
            """

            conn = None

            try:
                conn = sqlite3.connect(path)
                return conn
            except sqlite3.Error as error:
                print(error)

            return conn

        self.conn = create_connection(self.db_path)

    def execute_query(self, query=None, get_results=False, get_first_item=False):
        """This function executes the passing query.

        Args:
            query (str, optional): A request for data. Defaults to None.
            get_results (bool, optional): A boolean for deciding whether results from the query should be send back for visualisation or not. Defaults to False.
            get_first_item (bool, optional): A boolean for understanding if only the first element of each tuple from the query's returned list is needed. Defaults to False.

        Returns:
            list: It returns a list of tuples based on the query provided if get_results boolean is set to True.
        """

        try:
            c = self.conn.cursor()

            c.execute(query)

            if query is not None:
                if get_results == True:
                    if get_first_item == True:
                        # convert list of tuples into a list of strings
                        results = [item[0] for item in c.fetchall()]
                    else:
                        # convert list of tuples into a list of strings
                        results = [item for item in c.fetchall()]

                    return results
        except sqlite3.Error as error:
            print(error)
        finally:
            self.conn.commit()

    def create_table(self, table):
        """This function creates a table and pushes it to the SQLite DB.

        Args:
            table (list): A list containing the title of the table, the table columns and their data types.
        """

        title = table[0]
        table = table[1:]
        table_len = len(table)

        all_cols = ""
        for counter, col in enumerate(table):
            if table_len == counter + 1:
                # Do not add comma to the last column of the table
                all_cols += col
                break

            all_cols += col + ","

        create_table = f""" CREATE TABLE IF NOT EXISTS {title} (
                                        {all_cols}
                                    ); """

        self.execute_query(query=create_table)

    def drop_table(self, table_name):
        """This function drops a table using the passing table name.

        Args:
            table_name (str): Name of an existing table.
        """

        drop_table = f"DROP TABLE {table_name};"

        self.execute_query(query=drop_table)

    def init_db(self, table_name, file_path=None):
        """This function initializes the values of the SQLite DB by loading the data from the text files.

        Args:
            table_name (str): The name of the table that the data should be inserted into.
            file_path (str, optional): A string containing the path of the text file. Defaults to None.

        Returns:
            pandas.core.frame.DataFrame: A dataframe containing all the text file's data.
        """

        df = pd.read_csv(file_path, na_values="---")
        df.to_sql(name=table_name, con=self.conn, if_exists="append", index=False)

        return df

    def create_dimension_table(self, fact_table, col_to_be_mapped, new_cols):
        """This function creates a dimension table.

        Args:
            fact_table (pandas.core.frame.DataFrame): The fact table, BookInventory.
            col_to_be_mapped (str): A column from the fact table that should be normalized.
            new_cols (list): A list containing the new columns that should be created and mapped containing ids and the unique values of the columnn that should be mapped.

        Returns:
            pandas.core.frame.DataFrame: The dimension table.
        """

        unique_values_lst = fact_table[col_to_be_mapped].unique()
        ids = list(range(1, 1 + len(unique_values_lst)))

        dim_table = pd.DataFrame(
            data=list(zip(ids, unique_values_lst)), columns=new_cols
        )

        return dim_table

    def map_vals_to_ids(
        self,
        fact_df,
        fact_col_name,
        dimension_df,
        dimension_keycol_name,
        dimension_refcol_name,
    ):
        """This function maps all the values of the fact table from a dimension table.
           Inspired by https://stackoverflow.com/questions/53818434/pandas-replacing-values-by-looking-up-in-an-another-dataframe

        Args:
            fact_df (pandas.core.frame.DataFrame): A dataframe of the fact table.
            fact_col_name (str): The fact table's column which will be mapped.
            dimension_df (pandas.core.frame.DataFrame): A dataframe of the dimension table.
            dimension_keycol_name (str): The dimension table's PK column.
            dimension_refcol_name (str): The dimension table's FK column.

        Returns:
            pandas.core.frame.DataFrame: The fact table with mapped values.
        """

        # Map each col value to an id
        mapping_dict = dimension_df.set_index(dimension_refcol_name)[
            dimension_keycol_name
        ].to_dict()

        # Get all the values of the col from the fact table
        col_vals = fact_df.filter(like=fact_col_name)

        # Replace all
        fact_df[col_vals.columns] = col_vals.replace(mapping_dict)

        return fact_df

    def fill_new_fields(
        self,
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
        gui_flag=False,
        bookId=None,
    ):
        """This function is inserting data to the new fields of the Transactions table.

        Args:
            df (pandas.core.frame.DataFrame): Transactions fact table
            idx (integer): The current index of row when looping through the dataframe of loanReservationHistory_df which is the data of the text file containing the transactions
            transactionTypeMsg (str): A string value of what the main type of the transaction should be, e.g. Reserve/Checkout/Return
            isCheckedOutNum (bool): A boolean value indicating whether the book is checked out in the current transaction
            checkedOutMemberId (integer): A member's id value who checked out the book
            isReservedNum (bool): A boolean value indicating whether the book is reserved in the current transaction
            reservedMemberId (integer): A member's id value who reserved the book
            initialDate (date): A date showing when the transaction opened
            endRecordDate (date): A date showing when the transaction has been closed when the new transaction will be made
            isActive (bool): A boolean value indicating whether the transaction is the latest one or not
        """

        if gui_flag == True:
            df.loc[idx, "TransactionId"] = idx
            df.loc[idx, "BookId"] = bookId

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
            # Convert the string to datetime
            init_date = datetime.strptime(initialDate, "%d/%m/%Y")
            # Ddd days based on the transaction type above
            expiry_date = init_date + timedelta(days=num_of_days)
            # Change format
            expiry_date = expiry_date.strftime("%Y/%m/%d")
            # Get only the date and not the time
            expiry_date = str(expiry_date).split()[0]
            df.loc[idx, "TransactionTypeExpirationDate"] = expiry_date
        # Return
        else:
            df.loc[idx, "TransactionTypeExpirationDate"] = np.nan

        df.loc[idx, "StartRecordDate"] = datetime.strptime(
            initialDate, "%d/%m/%Y"
        ).strftime("%Y/%m/%d")
        # df.loc[idx, "EndRecordDate"] = datetime.strptime(endRecordDate, "%d/%m/%Y").strftime("%Y/%m/%d")
        df.loc[idx, "IsActive"] = isActive

    def deactivateLastTransaction(
        self, final_df, bookId, get_df_of_same_bookIds_via_gui=False
    ):
        """This function deactivates the previous transaction of the specific member id.
           In case it is the first transaction of the specific book's copy, then it won't do anything.

        Args:
            final_df (pandas.core.frame.DataFrame): The dataframe that we need to go through to find the last/previous transaction if possbile
            row (pandas.core.series.Series): The current transaction

        Returns:
            integer: The id of the last activated transaction
        """

        # Get all transactions of the same passing BookId
        allTransactions_of_bookId_df = final_df[final_df["BookId"] == bookId].dropna(
            axis=0, subset=["IsActive"]
        )

        last_activatedTransactionId = None
        # Check that there is an older transaction for the specific book id
        if len(allTransactions_of_bookId_df) >= 1:
            if get_df_of_same_bookIds_via_gui == True:
                return allTransactions_of_bookId_df.iloc[-1]

            # Get last transaction id that belong to the book id
            last_activatedTransactionId = allTransactions_of_bookId_df.iloc[-1][
                "TransactionId"
            ]

            # Deactivate the last transaction
            final_df.loc[last_activatedTransactionId - 1, "IsActive"] = 0

        return last_activatedTransactionId

    def findLastMemberId_and_deactivateLastTransaction(
        self, initial_df, final_df, bookId, memberId, columnOfmemberId="MemberId"
    ):
        """This function finds the member id of the previous transaction and deactivates last transaction by calling the deactivateLastTransaction function.

           It is called when either:
           - Reserve and Checkout happen at the same time.
                                OR
           - All Reserve, Checkout, Return occur in a single transaction.

           As a result, the previous transaction gets deactivated and since Reserve and Checkout are
           always part of either of the two cases above:

           In case there is no previous transaction, then both Reserve and Checkout have the same member id for the new transaction.
           Otherwise, if:
           - the function is called for Reserve, then the CheckOutMemberId is the previous transaction's member id.
           - the function is called for Checkout, then the ReservedMemberId is the previous transaction's member id.

        Args:
            initial_df (pandas.core.frame.DataFrame): The dataframe that will go through
            final_df (pandas.core.frame.DataFrame): The new dataframe that will have the new fields added to it
            row (pandas.core.series.Series): The current transaction

        Returns:
            integer: The id of the member that was part of the last activated transaction
        """

        last_activatedTransactionId = self.deactivateLastTransaction(final_df, bookId)

        last_memberId = None
        if last_activatedTransactionId is not None:

            if (
                final_df.loc[last_activatedTransactionId - 1, "TransactionType"]
                == "Checkout"
            ):
                # Get the last member that checked out
                last_memberId = initial_df.loc[
                    last_activatedTransactionId - 1, columnOfmemberId
                ]

            elif (
                final_df.loc[last_activatedTransactionId - 1, "TransactionType"]
                == "Reserve"
            ):
                # Get the last member that checked out
                last_memberId = initial_df.loc[
                    last_activatedTransactionId - 1, columnOfmemberId
                ]

        # If there was no previous transaction, assign the same current member id
        if last_memberId is None:
            last_memberId = memberId

        # Using casting fixed the problem of automatically allocating 8 bytes of space to the CheckOut Member Id field
        # which needed to be downloaded from each cell's file to see the actual value
        return int(last_memberId)

    def normalize_data(self, bookInfo_df, loanReservationHistory_df):

        ### Create BookInventory fact table ###
        bookInventory_df = bookInfo_df[["Id", "Genre", "Title", "Author"]].copy()

        # Create and fill Genre table with unique values of genres and map the ids
        genre_df = self.create_dimension_table(
            bookInventory_df, "Genre", ["GenreKey", "GenreRef"]
        )
        bookInventory_df = self.map_vals_to_ids(
            bookInventory_df, "Genre", genre_df, "GenreKey", "GenreRef"
        )

        # Create and fill Title table with unique values of book titles and map the ids
        bookTitles_df = self.create_dimension_table(
            bookInventory_df, "Title", ["BookTitleKey", "BookTitleRef"]
        )
        bookInventory_df = self.map_vals_to_ids(
            bookInventory_df, "Title", bookTitles_df, "BookTitleKey", "BookTitleRef"
        )

        # Create and fill Author table with unique values of book authors and map the ids
        bookAuthors_df = self.create_dimension_table(
            bookInventory_df, "Author", ["BookAuthorKey", "BookAuthorRef"]
        )
        bookInventory_df = self.map_vals_to_ids(
            bookInventory_df, "Author", bookAuthors_df, "BookAuthorKey", "BookAuthorRef"
        )

        # Rename col names
        bookInventory_df.rename(
            columns={
                "Id": "BookId",
                "Genre": "GenreKey",
                "Title": "BookTitleKey",
                "Author": "BookAuthorKey",
            },
            inplace=True,
        )

        # Add new column BookCopyKey to fact table and add the ids of book copies
        bookInventory_df["BookCopyKey"] = list(range(1, 1 + len(bookInventory_df)))

        # Create new dimension table BookCopies
        data = {
            "BookCopyKey": bookInventory_df["BookCopyKey"],
            "PurchasePrice£": bookInfo_df["PurchasePrice£"],
            "PurchaseDate": pd.to_datetime(
                bookInfo_df["PurchaseDate"], format="%d/%m/%Y"
            ).dt.strftime("%Y-%m-%d"),
        }
        bookCopies_df = pd.DataFrame(data)

        # Add all tables to db
        bookInventory_df.to_sql(
            name="BookInventory", con=self.conn, if_exists="append", index=False
        )
        genre_df.to_sql(name="Genre", con=self.conn, if_exists="append", index=False)
        bookTitles_df.to_sql(
            name="BookTitle", con=self.conn, if_exists="append", index=False
        )
        bookAuthors_df.to_sql(
            name="BookAuthor", con=self.conn, if_exists="append", index=False
        )
        bookCopies_df.to_sql(
            name="BookCopies", con=self.conn, if_exists="append", index=False
        )

        ### Create Transactions fact table ###
        transactions_df = pd.DataFrame()
        data = {
            "TransactionId": loanReservationHistory_df["TransactionId"],
            "BookId": loanReservationHistory_df["BookId"],
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

        # Create values for new fields of Transactions table
        for (idx, row) in loanReservationHistory_df.iterrows():
            if pd.isnull(row.loc["ReservationDate"]) == False:
                # Reserve
                if pd.isnull(row.loc["CheckoutDate"]) and pd.isnull(
                    row.loc["ReturnDate"]
                ):
                    self.deactivateLastTransaction(transactions_df, row.loc["BookId"])

                    self.fill_new_fields(
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
                        ).strftime("%Y/%m/%d")
                        checkout_date = datetime.strptime(
                            row.loc["CheckoutDate"], "%d/%m/%Y"
                        ).strftime("%Y/%m/%d")

                        # It is reserved by a new member even if the book is currently checked out
                        if reserve_date > checkout_date:
                            last_checkedOutMemberId = (
                                self.findLastMemberId_and_deactivateLastTransaction(
                                    loanReservationHistory_df,
                                    transactions_df,
                                    row.loc["BookId"],
                                    row.loc["MemberId"],
                                )
                            )

                            self.fill_new_fields(
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
                        # Otherwise, the reservation is considered that it has been done in the past, transaction type will be Checkout
                        else:
                            last_ReservedMemberId = (
                                self.findLastMemberId_and_deactivateLastTransaction(
                                    loanReservationHistory_df,
                                    transactions_df,
                                    row.loc["BookId"],
                                    row.loc["MemberId"],
                                )
                            )

                            self.fill_new_fields(
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
                            self.findLastMemberId_and_deactivateLastTransaction(
                                loanReservationHistory_df,
                                transactions_df,
                                row.loc["BookId"],
                                row.loc["MemberId"],
                            )
                        )

                        reserve_date = datetime.strptime(
                            row.loc["ReservationDate"], "%d/%m/%Y"
                        ).strftime("%Y/%m/%d")
                        return_date = datetime.strptime(
                            row.loc["ReturnDate"], "%d/%m/%Y"
                        ).strftime("%Y/%m/%d")

                        # If the reservation date is more recent than the return date, then reservation happened latest
                        if reserve_date > return_date:
                            self.fill_new_fields(
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
                        # Otherwise, the reservation is considered that it has been done in the past, the transaction type will be Return
                        else:
                            self.fill_new_fields(
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
                self.deactivateLastTransaction(transactions_df, row.loc["BookId"])

                # Just Checkout
                if pd.isnull(row.loc["ReturnDate"]):
                    self.fill_new_fields(
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
                    self.fill_new_fields(
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
            name="Transactions", con=self.conn, if_exists="append", index=False
        )

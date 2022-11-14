from tkinter import messagebox
import pandas as pd
import numpy as np
from datetime import datetime


def get_transactions_table_data(conn):
    df = pd.read_sql_query("SELECT * FROM Transactions;", conn)

    return df


class CheckoutBook:
    def __init__(self, databaseObj):
        self.databaseObj = databaseObj
        self.conn = self.databaseObj.conn

        self.transactions_df = get_transactions_table_data(self.conn)

        self.new_df = self.databaseObj.create_empty_transactions_fact_table(
            self.transactions_df
        )

    def checkout_book(self, bookID, memberID):

        self.transactions_df = get_transactions_table_data(self.conn)

        # Do not deactivate for now (that's why I introduced new boolean get_df_of_same_bookIds_via_gui),
        # just try to get the last activated transaction to make sure there is a previous transaction for the specific BookId
        last_activatedTransaction = self.databaseObj.deactivateLastTransaction(
            self.transactions_df, bookID, get_df_of_same_bookIds_via_gui=True
        )

        # No previous transaction for the specific BookId or the previous transaction was Return
        # Just Checkout then
        if (
            last_activatedTransaction is None
            or last_activatedTransaction["TransactionType"] == "Return"
        ):
            messagebox.showinfo(
                "Success",
                f"The book with an ID of {bookID} has successfully been checked out to {memberID} ID member",
            )

            # deactivate last transaction
            self.databaseObj.deactivateLastTransaction(
                self.transactions_df, bookID, get_df_of_same_bookIds_via_gui=False
            )

            self.new_df = self.databaseObj.fill_new_fields(
                self.transactions_df,
                self.transactions_df.shape[0] + 1,
                transactionTypeMsg="Checkout",
                isCheckedOutNum=1,
                checkedOutMemberId=memberID,
                isReservedNum=0,
                reservedMemberId=np.nan,
                initialDate=datetime.today().strftime("%d/%m/%Y"),
                endRecordDate=np.nan,
                isActive=1,
                gui_flag=True,
                bookId=bookID,
                get_df=True,
            )

            self.new_df.tail(1).to_sql(
                "Transactions", self.conn, if_exists="append", index=False
            )

            # Print it to the console for confirming that it works
            print(self.new_df.tail(1))

        elif last_activatedTransaction["TransactionType"] == "Checkout":

            if last_activatedTransaction["CheckedOutMemberId"] == memberID:
                messagebox.showerror(
                    "Error",
                    f"The book with an ID of {bookID} is already checked out by this member",
                )
            else:
                messagebox.showerror(
                    "Error",
                    f"The book with an ID of {bookID} is already checked out by {int(last_activatedTransaction.loc['CheckedOutMemberId'])} ID member. Therefore, it cannot be checked out",
                )

        # Since a previous transaction exists, check if its transactionType was Reserve
        elif last_activatedTransaction["TransactionType"] == "Reserve":

            # Check if the member who tries to check it out is the one who reserves it
            if last_activatedTransaction["ReservedMemberId"] == memberID:

                messagebox.showinfo(
                    "Success",
                    f"""The book with an ID of {bookID} has successfully been checked out to {memberID} ID member
                since the member was already reserving it""",
                )

                # deactivate last transaction
                self.databaseObj.deactivateLastTransaction(
                    self.transactions_df, bookID, get_df_of_same_bookIds_via_gui=False
                )

                last_ReservedMemberId = (
                    self.databaseObj.findLastMemberId_and_deactivateLastTransaction(
                        self.transactions_df,
                        self.new_df,
                        bookID,
                        memberID,
                        columnOfmemberId="ReservedMemberId",
                    )
                )

                self.new_df = self.databaseObj.fill_new_fields(
                    self.transactions_df,
                    self.transactions_df.shape[0] + 1,
                    transactionTypeMsg="Checkout",
                    isCheckedOutNum=1,
                    checkedOutMemberId=memberID,
                    isReservedNum=1,
                    reservedMemberId=last_ReservedMemberId,
                    initialDate=datetime.today().strftime("%d/%m/%Y"),
                    endRecordDate=np.nan,
                    isActive=1,
                    gui_flag=True,
                    bookId=bookID,
                    get_df=True,
                )

                self.new_df.tail(1).to_sql(
                    "Transactions", self.conn, if_exists="append", index=False
                )

                # Print it to the console for confirming that it works
                print(self.new_df.tail(1))

            else:
                messagebox.showerror(
                    "Error",
                    f"The book with an ID of {bookID} is already {last_activatedTransaction.loc['TransactionType']} to the {int(last_activatedTransaction.loc['ReservedMemberId'])} ID member",
                )

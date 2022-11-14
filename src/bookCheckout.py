from tkinter import messagebox
import numpy as np
from datetime import datetime


class CheckoutBook:
    def __init__(self, databaseObj):
        self.databaseObj = databaseObj
        self.conn = self.databaseObj.conn

    def checkout_book(self, transactions_df, bookID, memberID):

        # Do not deactivate for now (that's why I introduced new boolean get_df_of_same_bookIds_via_gui),
        # just try to get the last activated transaction to make sure there is a previous transaction for the specific BookId
        last_activatedTransaction = self.databaseObj.deactivateLastTransaction(
            transactions_df, bookID, get_df_of_same_bookIds_via_gui=True
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

            self.databaseObj.fill_new_fields(
                transactions_df,
                transactions_df.shape[0] + 1,
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
            )

            transactions_df.to_sql(
                "Transactions", self.conn, if_exists="replace", index=False
            )

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

                last_ReservedMemberId = (
                    self.databaseObj.findLastMemberId_and_deactivateLastTransaction(
                        transactions_df,
                        transactions_df,
                        bookID,
                        memberID,
                        columnOfmemberId="CheckedOutMemberId",
                    )
                )

                self.databaseObj.fill_new_fields(
                    transactions_df,
                    transactions_df.shape[0] + 1,
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
                )

                transactions_df.to_sql(
                    "Transactions", self.conn, if_exists="replace", index=False
                )

            else:
                messagebox.showerror(
                    "Error",
                    f"The book with an ID of {bookID} is already {last_activatedTransaction.loc['TransactionType']} to the {int(last_activatedTransaction.loc['ReservedMemberId'])} ID member",
                )

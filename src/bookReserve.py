import numpy as np
from tkinter import messagebox
from datetime import datetime


class ReserveBook:
    def __init__(self, databaseObj):
        self.databaseObj = databaseObj
        self.conn = self.databaseObj.conn

    def reserve_book(self, transactions_df, bookID, memberID):

        # Do not deactivate for now (that's why I introduced new boolean get_df_of_same_bookIds_via_gui),
        # just try to get the last activated transaction to make sure there is a previous transaction for the specific BookId
        last_activatedTransaction = self.databaseObj.deactivateLastTransaction(
            transactions_df, bookID, get_df_of_same_bookIds_via_gui=True
        )

        # No previous transaction for the specific BookId or the previous transaction was Return
        # Just Reserve then
        if (
            last_activatedTransaction is None
            or last_activatedTransaction["TransactionType"] == "Return"
        ):
            messagebox.showinfo(
                "Success",
                f"The book with an ID of {bookID} has successfully been reserved to {memberID} ID member",
            )

            self.databaseObj.fill_new_fields(
                transactions_df,
                transactions_df.shape[0] + 1,  # New index
                transactionTypeMsg="Reserve",
                isCheckedOutNum=0,
                checkedOutMemberId=np.nan,
                isReservedNum=1,
                reservedMemberId=memberID,
                initialDate=datetime.today().strftime("%d/%m/%Y"),
                endRecordDate=np.nan,
                isActive=1,
                gui_flag=True,
                bookId=bookID,
            )

            transactions_df.to_sql(
                "Transactions", self.conn, if_exists="replace", index=False
            )

        # Since a previous transaction exists, check if its transactionType was Reserve
        elif last_activatedTransaction["TransactionType"] == "Reserve":

            if last_activatedTransaction["ReservedMemberId"] == memberID:
                messagebox.showerror(
                    "Error",
                    f"The book with an ID of {bookID} is already reserved by this member",
                )
            else:
                messagebox.showerror(
                    "Error",
                    f"The book with an ID of {bookID} is already reserved to the {int(last_activatedTransaction.loc['ReservedMemberId'])} ID member",
                )

        # Since a previous transaction exists, check if its transactionType was Checkout
        elif last_activatedTransaction["TransactionType"] == "Checkout":
            # If the transactionType is Checkout, then it is known for a fact that today's date is more recent than the previous transaction's date
            # Unlike what it was done during the loading of text files

            messagebox.showinfo(
                "Success",
                f"""The book with an ID of {bookID} has successfully been reserved to {memberID} ID member as it is already checked out by
            {int(last_activatedTransaction.loc['CheckedOutMemberId'])} ID member""",
            )

            last_checkedOutMemberId = (
                self.databaseObj.findLastMemberId_and_deactivateLastTransaction(
                    transactions_df,
                    transactions_df,
                    bookID,
                    memberID,
                    columnOfmemberId="ReservedMemberId",
                )
            )

            self.databaseObj.fill_new_fields(
                transactions_df,
                transactions_df.shape[0] + 1,  # New index
                transactionTypeMsg="Reserve",
                isCheckedOutNum=1,
                checkedOutMemberId=last_checkedOutMemberId,
                isReservedNum=1,
                reservedMemberId=bookID,
                initialDate=datetime.today().strftime("%d/%m/%Y"),
                endRecordDate=np.nan,
                isActive=1,
                gui_flag=True,
                bookId=bookID,
            )

            transactions_df.to_sql(
                "Transactions", self.conn, if_exists="replace", index=False
            )

import numpy as np
from tkinter import messagebox
from datetime import datetime


class ReturnBook:
    def __init__(self, databaseObj):
        self.databaseObj = databaseObj
        self.conn = self.databaseObj.conn

    def return_book(self, transactions_df, bookID, memberID):
        # Do not deactivate for now (that's why I introduced new boolean get_df_of_same_bookIds_via_gui),
        # just try to get the last activated transaction to make sure there is a previous transaction for the specific BookId
        last_activatedTransaction = self.databaseObj.deactivateLastTransaction(
            transactions_df, bookID, get_df_of_same_bookIds_via_gui=True
        )

        # No previous transaction for the specific BookId
        if (
            last_activatedTransaction is None
            or last_activatedTransaction["TransactionType"] == "Reserve"
        ):
            messagebox.showerror(
                "Error",
                f"The book with an ID of {bookID} cannot be returned as it was never checked out",
            )

        elif last_activatedTransaction["TransactionType"] == "Checkout":

            # Check if the individual who tries to return the book is the one who checked it out last
            if last_activatedTransaction["checkedOutMemberId"] == memberID:
                messagebox.showinfo(
                    "Success",
                    f"The book with an ID of {bookID} has successfully been returned",
                )

                self.databaseObj.fill_new_fields(
                    transactions_df,
                    transactions_df.shape[0] + 1,  # New index
                    transactionTypeMsg="Return",
                    isCheckedOutNum=1,
                    checkedOutMemberId=memberID,
                    isReservedNum=0,
                    reservedMemberId=np.nan,
                    initialDate=datetime.today().strftime("%d/%m/%Y"),
                    endRecordDate=np.nan,
                    isActive=1,
                )

                transactions_df.to_sql(
                    "Transactions", self.conn, if_exists="replace", index=False
                )
        else:
            messagebox.showerror(
                "Error",
                f"The book with an ID of {bookID} cannot be returned as the member who checked it out last was {int(last_activatedTransaction.loc['checkedOutMemberId'])}",
            )

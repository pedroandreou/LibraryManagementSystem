from tkinter import Tk
import os
import database as d
import gui


def main():
    repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir_path = os.path.join(repo_path, "data")

    ## database ###
    db_path = f"{data_dir_path}/library.db"
    db_exists_flag = os.path.isfile(db_path)

    database = d.database(db_path)

    # check if db already exists => do not load files or normalize data => already done
    if not db_exists_flag:
        create_book_info = [
            "Book_Info",
            "Id integer PRIMARY KEY",
            "Genre TEXT NOT NULL",
            "Title TEXT NOT NULL",
            "Author TEXT NOT NULL",
            "PurchasePrice£ INTEGER NOT NULL",
            "PurchaseDate DATE NOT NULL",
        ]
        create_loan_reservation_history = [
            "Loan_Reservation_History",
            "TransactionId integer PRIMARY KEY",
            "BookId integer NOT NULL",
            "ReservationDate DATE",
            "CheckoutDate DATE",
            "ReturnDate DATE",
            "MemberId INTEGER NOT NULL",
            "FOREIGN KEY (BookId) REFERENCES Book_Info(BookId)",
        ]

        # create two initial tables
        create_tables = [create_book_info, create_loan_reservation_history]
        for table in create_tables:
            database.create_table(table)

        # fill initial tables with data from the two txt files
        book_info_df = None
        loan_res_hist_df = None
        table_names = [create_book_info[0], create_loan_reservation_history[0]]
        for table_name in table_names:
            file_path = f"{data_dir_path}/data_files/{table_name}.txt"

            # fill each initial table with data
            df = database.init_db(table_name, file_path)

            # store the created df from the txt file to a variable
            if table_name == create_book_info[0]:
                book_info_df = df
            else:
                loan_res_hist_df = df

        # create tables for adding normalized data
        create_book_inventory = [
            "BookInventory",
            "BookId PRIMARY KEY",
            "GenreKey INTEGER",
            "BookTitleKey INTEGER NOT NULL",
            "BookAuthorKey INTEGER NOT NULL",
            "BookCopyKey INTEGER",
            "FOREIGN KEY (GenreKey) REFERENCES Genre(GenreKey)",
            "FOREIGN KEY (BookTitleKey) REFERENCES BookTitle(BookTitleKey)",
            "FOREIGN KEY (BookAuthorKey) REFERENCES BookAuthor(BookAuthorKey)",
            "FOREIGN KEY (BookCopyKey) REFERENCES BookCopies(BookCopyKey)",
        ]
        create_genre = [
            "Genre",
            "GenreKey PRIMARY KEY",
            "GenreRef TEXT NOT NULL",
        ]
        create_bookTitle = [
            "BookTitle",
            "BookTitleKey PRIMARY KEY",
            "BookTitleRef TEXT NOT NULL",
        ]
        create_bookAuthor = [
            "BookAuthor",
            "BookAuthorKey PRIMARY KEY",
            "BookAuthorRef TEXT NOT NULL",
        ]
        create_book_copies = [
            "BookCopies",
            "BookCopyKey PRIMARY KEY",
            "PurchasePrice£ INTEGER NOT NULL",
            "PurchaseDate DATE NOT NULL",
        ]
        create_transactions = [
            "Transactions",
            "TransactionId PRIMARY KEY",
            "BookId INTEGER",
            "BookCopyKey INTEGER",
            "TransactionType TEXT",
            "IsCheckedOut INTEGEGER",
            "CheckedOutMemberId INTEGER",
            "IsReserved INTEGER",
            "ReservedMemberId INTEGER",
            "TransactionTypeExpirationDate DATE",
            "StartRecordDate DATE",
            "EndRecordDate DATE",
            "IsActive INTEGER",
            "FOREIGN KEY (BookId) REFERENCES BookInventory(BookId)",
            "FOREIGN KEY (BookCopyKey) REFERENCES BookCopies(BookCopyKey)",
        ]

        create_tables = [
            create_book_inventory,
            create_genre,
            create_bookTitle,
            create_bookAuthor,
            create_book_copies,
            create_transactions,
        ]
        for table in create_tables:
            database.create_table(table)

        # normalize existing data
        database.normalize_data(book_info_df, loan_res_hist_df)

        # drop the initial tables
        database.drop_table("Book_Info")
        database.drop_table("Loan_Reservation_History")
    else:
        print("DB already exists; no need for creating our tables from scratch again!")

    # create a list of all the book titles that will be used for autocompletion
    book_titles_lst = database.execute_query(
        query="SELECT BookTitleRef FROM BookTitle", book_autocompletion_flag=True
    )

    ## gui ###
    root = Tk()
    gui.app(root, database.conn, data_dir_path, book_titles_lst)
    root.mainloop()

    database.conn.close()


if __name__ == "__main__":
    main()

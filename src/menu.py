import os
from tkinter import Tk
import database as d
import gui


def main():
    repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir_path = os.path.join(repo_path, "data/")

    ## database ###
    db_path = data_dir_path + "library.db"
    conn = d.create_connection(db_path)

    if conn is not None:
        # create initial tables
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

        create_tables = [create_book_info, create_loan_reservation_history]
        for table in create_tables:
            d.create_table(conn, table)

        # insert initial data to tables
        fill_book_info = [
            "Book_Info",
            "Id, Genre, Title, Author, PurchasePrice£, PurchaseDate",
        ]
        fill_loan_reservation_history = [
            "Loan_Reservation_History",
            "TransactionId, BookId, ReservationDate, CheckoutDate, ReturnDate, MemberId",
        ]

        fill_tables = [fill_book_info, fill_loan_reservation_history]
        for table in fill_tables:
            table_name = table[0]
            file_path = f"{data_dir_path}{table_name}.txt"
            d.init_db(conn, table_name, file_path)

        # drop the initial tables
        d.drop_table(conn, "Book_Info")
        d.drop_table(conn, "Loan_Reservation_History")

        # create tables for adding normalized data
        create_book_inventory = [
            "BookInventory",
            "BookId PRIMARY KEY",
            "BookTitle TEXT NOT NULL",
            "BookEdition INTEGER NOT NULL",
            "BookAuthor TEXT NOT NULL",
            "GenreKey INTEGER",
            "BookCopyKey INTEGER",
            "FOREIGN KEY (GenreKey) REFERENCES Genre(GenreKey)",
            "FOREIGN KEY (BookCopyKey) REFERENCES BookCopies(BookCopyKey)",
        ]
        create_genre = ["Genre", "GenreKey PRIMARY KEY", "GenreRef TEXT NOT NULL"]
        create_book_copies = [
            "BookCopies",
            "BookCopyKey PRIMARY KEY",
            "PurchaseDate date",
            "RetiredDate date",
            "isActive INTEGER NOT NULL",
        ]
        create_member = [
            "Member",
            "MemberId PRIMARY KEY",
            "Name TEXT NOT NULL",
            "Surname TEXT NOT NULL",
            "Address TEXT",
            "Phone TEXT",
            "StudentNumber TEXT",
        ]
        create_librarian = [
            "Librarian",
            "LibrarianId PRIMARY KEY",
            "LibrarianName TEXT NOT NULL",
            "LibrarianSurname TEXT NOT NULL",
            "LibrarianAddress TEXT",
            "LIbrarianPhone TEXT",
        ]
        create_transactions = [
            "Transactions",
            "TransactionId PRIMARY KEY",
            "BookId INTEGER",
            "BookCopyKey INTEGER",
            "TransactionType TEXT NOT NULL",
            "IsCheckedOut INTEGEGER NOT NULL",
            "CheckedOutMemberId INTEGER NOT NULL",
            "LibrarianId INTEGER",
            "ReservedMemberId INTEGER",
            "IsReserved INTEGER",
            "TransactionTypeExpirationDate DATE NOT NULL",
            "StartRecordDate DATE NOT NULL",
            "EndRecordDate DATE NOT NULL",
            "IsActive INTEGER NOT NULL",
            "FOREIGN KEY (BookId) REFERENCES BookInventory(BookId)",
            "FOREIGN KEY (BookCopyKey) REFERENCES BookCopies(BookCopyKey)",
            "FOREIGN KEY (LibrarianId) REFERENCES Librarian(LibrarianId)",
            "FOREIGN KEY (ReservedMemberId) REFERENCES Member(MemberId)",
        ]

        create_tables = [
            create_book_inventory,
            create_genre,
            create_book_copies,
            create_member,
            create_librarian,
            create_transactions,
        ]
        for table in create_tables:
            d.create_table(conn, table)

    else:
        print("Error! cannot create the database connection")

    conn.close()

    ## gui ###
    # img_path = data_dir_path + 'gui_bg.png'

    root = Tk()
    gui.app(root)
    root.mainloop()


if __name__ == "__main__":
    main()

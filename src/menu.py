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
            "book_info",
            "id integer PRIMARY KEY",
            "genre text NOT NULL",
            "title text NOT NULL",
            "author text NOT NULL",
            "purchase_price_£ integer NOT NULL",
            "purchase_date date NOT NULL",
        ]
        create_loan_reservation_history = [
            "loan_reservation_history",
            "book_id integer NOT NULL",
            "reservation_date date",
            "checkout_date date",
            "return_date date",
            "member_id integer NOT NULL",
            "PRIMARY KEY (book_id, member_id)",
        ]

        create_tables = [create_book_info, create_loan_reservation_history]
        for table in create_tables:
            d.create_table(conn, table)

        # insert initial data to tables
        fill_book_info = [
            "book_info",
            "id, genre, title, author, purchase_price_£, purchase_date",
        ]
        fill_loan_reservation_history = [
            "loan_reservation_history",
            "book_id, reservation_date, checkout_date, return_date, member_id",
        ]

        fill_tables = [fill_book_info, fill_loan_reservation_history]
        for table in fill_tables:
            # capitalize the first letter and every letter after an underscore => txt file name
            file_name = "_".join(elem.capitalize() for elem in table[0].split("_"))
            file_path = f"{data_dir_path}{file_name}.txt"
            d.init_db(conn, table, file_path)

    else:
        print("Error! cannot create the database connection")

    conn.close()

    ### gui ###
    # img_path = data_dir_path + 'gui_bg.png'

    root = Tk()
    gui.app(root)
    root.mainloop()


if __name__ == "__main__":
    main()

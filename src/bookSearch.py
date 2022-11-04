import sqlite3
from tkinter.constants import END


def find_books(text, conn, tree):
    # clear TreeView
    for i in tree.get_children():
        tree.delete(i)

    # check that input is not only whitespace
    if len(text.strip()) != 0:
        basic_query = f"""SELECT bi.BookId, g.GenreRef, bt.BookTitleRef, ba.BookAuthorRef, bc.PurchasePrice£, bc.PurchaseDate
    FROM BookInventory bi
    INNER JOIN Genre g on g.GenreKey = bi.GenreKey
    INNER JOIN BookTitle bt on bt.BookTitleKey = bi.BookTitleKey
    INNER JOIN BookAuthor ba on ba.BookAuthorKey = bi.BookAuthorKey
    INNER JOIN BookCopies bc on bc.BookCopyKey = bi.BookCopyKey
    WHERE bt.BookTitleRef LIKE '%{text}%';"""

        # query_to_run = '\n'.join([prelude, basic_query, postlude])

        data = []
        try:
            c = conn.cursor()
            c.execute(basic_query)

            for row in c.fetchall():
                data.append(row)
        except sqlite3.Error as error:
            print(error)

        # sort list based on the first element of each tuple, bookId
        sorted_data = sorted(data, key=lambda x: x[0])

        for row_tuple in sorted_data:
            tree.insert("", "end", values=row_tuple)

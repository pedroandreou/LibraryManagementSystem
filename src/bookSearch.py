from treeView import TreeViewClass


def find_books(text, conn, tree):

    # check that input is not only whitespace
    if len(text.strip()) != 0:
        search_query = f"""SELECT bi.BookId, g.GenreRef, bt.BookTitleRef, ba.BookAuthorRef, bc.PurchasePrice£, bc.PurchaseDate
    FROM BookInventory bi
    INNER JOIN Genre g on g.GenreKey = bi.GenreKey
    INNER JOIN BookTitle bt on bt.BookTitleKey = bi.BookTitleKey
    INNER JOIN BookAuthor ba on ba.BookAuthorKey = bi.BookAuthorKey
    INNER JOIN BookCopies bc on bc.BookCopyKey = bi.BookCopyKey
    WHERE bt.BookTitleRef LIKE '%{text}%';"""

        TreeViewClass(conn, tree, search_query)

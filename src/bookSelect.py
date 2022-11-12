from treeView import TreeViewClass


class BookRecommendationSystem:
    def __init__(self, databaseObj):
        self.databaseObj = databaseObj
        self.conn = self.databaseObj.conn

    def most_checkouts_per_copy(self, tree):
        query = f"""SELECT t.BookId, bt.BookTitleRef, COUNT(t.BookId)
   FROM Transactions t
   INNER JOIN BookInventory bi on bi.BookId = t.BookId
   INNER JOIN BookTitle bt on bt.BookTitleKey = bi.BookTitleKey
   WHERE TransactionType = 'Checkout'
   GROUP BY t.BookId
   LIMIT 5;"""

        TreeViewClass(self.databaseObj, tree, query)

    def most_checkouts_per_book(self, tree):
        query = f"""SELECT bt.BookTitleRef, COUNT(bi.BookTitleKey)
   FROM BookInventory bi
   INNER JOIN BookTitle bt on bt.BookTitleKey = bi.BookTitleKey
   INNER JOIN Transactions t on t.BookId = bi.BookId
   WHERE t.TransactionType = 'Checkout'
   GROUP BY bi.BookTitleKey
   LIMIT 5;"""

        TreeViewClass(self.databaseObj, tree, query)

    def total_available_days(self, tree):
        query = f"""SELECT bt.BookTitleRef, COUNT(bi.BookTitleKey), CAST(SUM(JULIANDAY('now') - JULIANDAY(bc.PurchaseDate)) AS INTEGER) AS Available_days
   FROM BookCopies bc
   INNER JOIN BookInventory bi on bi.BookCopyKey = bc.BookCopyKey
   INNER JOIN Transactions t on t.BookId = bi.BookId
   INNER JOIN BookTitle bt on bt.BookTitleKey = bi.BookTitleKey
   WHERE t.TransactionType = 'Checkout'
   GROUP BY bi.BookTitleKey
   LIMIT 5;"""

        TreeViewClass(self.databaseObj, tree, query, True)

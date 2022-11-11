from treeView import TreeViewClass


class BookRecommendationSystem:
    def __init__(self, databaseObj):
        self.databaseObj = databaseObj
        self.conn = self.databaseObj.conn

    def most_checkouts(self, tree):
        most_checkouts_query = f"""SELECT BookId, COUNT(BookId)
   FROM Transactions
   WHERE TransactionType = 'Checkout'
   GROUP BY BookId
   LIMIT 5;"""

        TreeViewClass(self.databaseObj, tree, most_checkouts_query)

    def number_of_copies(self, tree):
        print("Number of copies")

    def total_available_minutes(self, tree):
        print("Total available minutes")

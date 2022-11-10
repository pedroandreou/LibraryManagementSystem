from treeView import TreeViewClass


class BookRecommendationSystem:
    def __init__(self, conn):
        self.conn = conn

    def most_checkouts(self, tree):
        recommend_query = f"""SELECT BookId, COUNT(BookId)
   FROM Transactions
   WHERE TransactionType = 'Checkout'
   GROUP BY BookId
   LIMIT 5;"""

        TreeViewClass(self.conn, tree, recommend_query)

    def number_of_copies(self, tree):
        print("Number of copies")

    def total_available_minutes(self, tree):
        print("Total available minutes")

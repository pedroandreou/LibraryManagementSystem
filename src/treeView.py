import sqlite3


class TreeViewClass:
    def __init__(self, conn, tree, query):
        self.conn = conn
        self.tree = tree
        self.query = query

        self.clear_Treeview()
        self.get_data()
        self.add_data_toTreeview()

    def clear_Treeview(self):
        # clear Treeview
        for i in self.tree.get_children():
            self.tree.delete(i)

    def get_data(self):
        self.data = []

        try:
            c = self.conn.cursor()
            c.execute(self.query)

            for row in c.fetchall():
                self.data.append(row)
        except sqlite3.Error as error:
            print(error)

    def add_data_toTreeview(self):
        # sort list based on the first element of each tuple, bookId
        sorted_data = sorted(self.data, key=lambda x: x[0])

        for row_tuple in sorted_data:
            self.tree.insert("", "end", values=row_tuple)

class TreeViewClass:
    def __init__(self, databaseObj, tree, query):
        self.databaseObj = databaseObj
        self.conn = self.databaseObj.conn
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
        self.data = self.databaseObj.execute_query(
            query=self.query, get_results=True, get_first_item=False
        )

    def add_data_toTreeview(self):
        # sort list based on the first element of each tuple, bookId
        sorted_data = sorted(self.data, key=lambda x: x[0])

        for row_tuple in sorted_data:
            self.tree.insert("", "end", values=row_tuple)

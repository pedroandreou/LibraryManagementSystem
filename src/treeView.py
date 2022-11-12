class TreeViewClass:
    def __init__(self, databaseObj, tree, query, available_days_flag=False):
        self.databaseObj = databaseObj
        self.conn = self.databaseObj.conn
        self.tree = tree
        self.query = query
        self.available_days_flag = available_days_flag

        self.clear_Treeview()
        self.get_data_from_db()
        self.add_data_to_treeview()

    def clear_Treeview(self):
        # clear Treeview
        for i in self.tree.get_children():
            self.tree.delete(i)

    def get_data_from_db(self):
        self.data = self.databaseObj.execute_query(
            query=self.query, get_results=True, get_first_item=False
        )

    def add_data_to_treeview(self):

        if self.available_days_flag == False:
            # get the length of the first tuple from the list
            tuple_len = len(self.data[0])

            # sort tuple based on the numbers of Checkout in a descending order
            self.data.sort(key=lambda elem: elem[tuple_len - 1], reverse=True)
        else:
            # sort tuples by diving the number of checkouts from the available days
            self.data.sort(key=lambda element: (element[2] / element[1]))

        for row_tuple in self.data:
            self.tree.insert("", "end", values=row_tuple)

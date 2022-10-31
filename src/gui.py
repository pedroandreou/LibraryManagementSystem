from tkinter import Label, Entry, Button, Frame, messagebox, CENTER
from tkinter.ttk import Combobox, Treeview
from turtle import width
from bookSearch import find_books


class app:
    def __init__(self, master, conn):
        self.master = master
        self.conn = conn
        self.master.title("Library Management System")
        self.master.geometry("950x750")
        self.master.configure(background="#FFC300")
        self.main_page()

    def destroy_page_widgets(self):
        for i in self.master.winfo_children():
            i.destroy()

    def main_page(self):
        self.master.title("Library Management System")
        self.destroy_page_widgets()

        # Add background image
        # background_image = tk.PhotoImage("images.png")
        # background_label = tk.Label(self.master, image=background_image)
        # background_label.image = background_image
        # background_label.place(x=20, y=20, relwidth=1, relheight=1)

        self.search_bton = Button(
            text="Search Book",
            font="sans 16 bold",
            fg="white",
            bg="black",
            command=self.search_book_page,
        )
        self.search_bton.place(relx=0.5, rely=0.45, anchor=CENTER, height=40, width=300)

        # rcr => reserve, checkout, return
        self.rcr_bton = Button(
            text="Reserve/Checkout/Return\nBook",
            font="sans 16 bold",
            fg="white",
            bg="black",
            command=self.rcr_page,
        )
        self.rcr_bton.place(relx=0.5, rely=0.55, anchor=CENTER, height=60, width=400)

        self.rec_bton = Button(
            text="Find Recommended Books",
            font="sans 16 bold",
            fg="white",
            bg="black",
            command=self.recommendation_page,
        )
        self.rec_bton.place(relx=0.5, rely=0.65, anchor=CENTER, height=40, width=340)

    def create_label_entry_widgets(self, frame, label_text, height):
        self.memberid_label = Label(
            frame, text=label_text, font=("calibre", 10, "bold")
        )
        self.memberid_label.place(
            relx=0.5, rely=height, anchor=CENTER, height=40, width=200
        )

        self.memberid_entry = Entry(frame, font=("calibre", 10, "normal"))
        self.memberid_entry.place(
            relx=0.69, rely=height, anchor=CENTER, height=40, width=220
        )

    def create_bottom_button_widgets(self, frame, curr_page):
        self.go_back_bton = Button(
            frame,
            text="Go Back",
            font="sans 16 bold",
            fg="white",
            bg="black",
            command=self.main_page,
        )
        self.go_back_bton.place(
            relx=0.35, rely=0.9, anchor=CENTER, height=40, width=220
        )

        if curr_page == "search_book":
            self.submit_bton = Button(
                frame,
                text="Submit",
                font="sans 16 bold",
                fg="white",
                bg="black",
                command=lambda: find_books(
                    self.memberid_entry.get(), self.conn, self.tree
                ),
            )
        else:
            self.submit_bton = Button(
                frame,
                text="Submit",
                font="sans 16 bold",
                fg="white",
                bg="black",
            )
        self.submit_bton.place(relx=0.75, rely=0.9, anchor=CENTER, height=40, width=220)

    def search_book_page(self):
        self.master.title("Search Book")
        self.destroy_page_widgets()

        # create new frame for 'search book' page to attach all its widgets
        self.sb_frame = Frame(self.master, bg="#FFC300", height=700, width=1200)

        # widgets for "search book" label and entry for getting user input
        self.create_label_entry_widgets(
            frame=self.sb_frame, label_text="Search Book Title", height=0.1
        )

        # add a Treeview widget
        self.tree = Treeview(
            self.sb_frame,
            columns=[
                "BookId",
                "Genre",
                "Title",
                "Book Author",
                "Purchase Price",
                "Purchase Date",
            ],
            show="headings",
            height=20,
        )
        # define headings
        self.tree.column("# 1", anchor=CENTER, stretch=False, width=120)
        self.tree.heading("# 1", text="Id")
        self.tree.column("# 2", anchor=CENTER, stretch=False, width=140)
        self.tree.heading("# 2", text="Genre")
        self.tree.column("# 3", anchor=CENTER, stretch=False, width=223)
        self.tree.heading("# 3", text="Title")
        self.tree.column("# 4", anchor=CENTER, stretch=False, width=223)
        self.tree.heading("# 4", text="Author")
        self.tree.heading("# 5", text="Purchase Price")
        self.tree.column("# 5", anchor=CENTER, stretch=False, width=140)
        self.tree.heading("# 6", text="Purchase Date")
        self.tree.column("# 6", anchor=CENTER, stretch=False, width=223)
        self.tree.place(x=130, y=140, width=1400)

        self.create_bottom_button_widgets(self.sb_frame, "search_book")

        # show frame with all its widgets
        self.sb_frame.pack()

    def show_diff_widgets_based_on_action_submitted(self):
        if self.rcr_dropdown.get() == "Reserve Book":
            self.create_label_entry_widgets(
                frame=self.rcr_frame, label_text="Book ID", height=0.3
            )

        elif self.rcr_dropdown.get() == "Checkout Book":
            self.create_label_entry_widgets(
                frame=self.rcr_frame, label_text="Member ID", height=0.2
            )
            self.create_label_entry_widgets(
                frame=self.rcr_frame, label_text="Book ID", height=0.3
            )

            # invalid => member ID or book ID is wrong
            messagebox.showerror("error", "Unsuccessful Checkout")

            # valid member ID and book ID
            # if book is available => not on loan or is already reserved
            # checkout the book and update the db

            ### else ###
            # invalid checkout => the book is not available (on loan or reservation)
            # allow user to reserve it
            messagebox.showinfo("success", "Successful Checkout")

        elif self.rcr_dropdown.get() == "Return Book":
            self.create_label_entry_widgets(
                frame=self.rcr_frame, label_text="Book ID", height=0.3
            )

            # if id is invalid or the book is already available
            messagebox.showerror(
                "error",
                "Unsuccessful Return\nEither the Book ID is invalid or the book is available",
            )

            # once it is returned - show a message if the book is pre-reserved by a member

    def rcr_page(self):
        self.master.title("Checkout Book")
        self.destroy_page_widgets()

        # create new frame for the 'rcr' page to attach all its widgets
        self.rcr_frame = Frame(self.master, bg="#FFC300", height=700, width=900)

        # widgets
        self.rcr_dropdown = Combobox(
            self.rcr_frame,
            state="readonly",
            justify="center",
            values=["Reserve Book", "Checkout Book", "Return Book"],
        )
        self.rcr_dropdown.current(0)
        self.rcr_dropdown.place(
            relx=0.53, rely=0.1, anchor=CENTER, height=30, width=500
        )

        self.action_submit_btn = Button(
            self.rcr_frame,
            text="Submit Action",
            command=self.show_diff_widgets_based_on_action_submitted,
        )
        self.action_submit_btn.place(
            relx=0.9, rely=0.10, anchor=CENTER, height=30, width=150
        )

        self.create_bottom_button_widgets(self.rcr_frame, "rcr_page")

        # show frame with all its widgets
        self.rcr_frame.pack(padx=1, pady=1)

    def recommendation_page(self):
        print("")

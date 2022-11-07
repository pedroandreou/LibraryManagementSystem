from tkinter import Text, Label, Entry, Button, Frame, messagebox, CENTER, END
from PIL import Image, ImageTk
from tkinter.ttk import Combobox, Treeview
from bookSearch import find_books
from bookReserve import reserve_book
from bookCheckout import checkout_book
from bookReturn import return_book


class app:
    def __init__(self, master, conn, bs_img_path, rcr_img_path, frb_img_path):
        self.master = master
        self.conn = conn
        self.master.title("Library Management System")
        self.w, self.h = (
            self.master.winfo_screenwidth(),
            self.master.winfo_screenheight(),
        )
        self.master.geometry("%dx%d+0+0" % (self.w, self.h))
        self.master.configure(background="#FFC300")
        self.bs_img_path = bs_img_path
        self.rcr_img_path = rcr_img_path
        self.frb_img_path = frb_img_path
        self.main_page()

    def show_frame(self, frame):
        #  set border color
        frame.config(
            highlightbackground="black", highlightcolor="black", highlightthickness=10
        )
        #  make frame visible to toplevel
        frame.pack(expand=True)

    def hide_frame(self, frame):
        # remove the frame from toplevel
        frame.pack_forget()

    def get_font_fg_bg(self):

        return {"font": "sans 16 bold", "fg": "white", "bg": "black"}

    def get_img_obj(self, img_path):
        label = Label(self.master)
        img = Image.open(img_path)
        label.img = ImageTk.PhotoImage(img)

        return label.img

    def main_page(self):
        self.master.title("Library Management System")

        self.main_frame = Frame(self.master, bg="#FFC300", height=700, width=900)

        # add Text widget
        T = Text(self.main_frame, **self.get_font_fg_bg(), height=5, width=52)
        text = "\nWelcome to Petros's Library Management System"
        T.tag_configure("center", justify="center")
        T.insert(END, text)
        T.tag_add("center", "1.0", END)
        T.place(relx=0.53, rely=0.35, anchor=CENTER, height=80, width=700)

        self.search_bton = Button(
            self.main_frame,
            **self.get_font_fg_bg(),
            image=self.get_img_obj(self.bs_img_path),
            command=lambda: [self.hide_frame(self.main_frame), self.search_book_page()],
        )
        self.search_bton.place(relx=0.5, rely=0.55, anchor=CENTER, height=60, width=400)

        # rcr => reserve, checkout, return
        self.rcr_bton = Button(
            self.main_frame,
            **self.get_font_fg_bg(),
            image=self.get_img_obj(self.rcr_img_path),
            command=lambda: [self.hide_frame(self.main_frame), self.rcr_page()],
        )
        self.rcr_bton.place(relx=0.5, rely=0.65, anchor=CENTER, height=60, width=400)

        self.rec_bton = Button(
            self.main_frame,
            **self.get_font_fg_bg(),
            image=self.get_img_obj(self.frb_img_path),
            command=lambda: [
                self.hide_frame(self.main_frame),
                self.recommendation_page(),
            ],
        )
        self.rec_bton.place(relx=0.5, rely=0.75, anchor=CENTER, height=60, width=400)

        self.show_frame(self.main_frame)

    def create_label_entry_widgets(self, frame, label_text, y, x1=0.48, x2=0.65):
        self.entry_label = Label(frame, text=label_text, font=("calibre", 10, "bold"))
        self.entry_label.place(relx=x1, rely=y, anchor=CENTER, height=40, width=200)

        self.entry_widget = Entry(frame, font=("calibre", 10, "normal"))
        self.entry_widget.place(relx=x2, rely=y, anchor=CENTER, height=40, width=220)

    def call_appropriate_rcr_action(self, member_id, action_submitted):
        if action_submitted == "Reserve Book":
            reserve_book()
        elif action_submitted == "Checkout Book":
            checkout_book()
        else:
            return_book()

    def create_bottom_button_widgets(self, frame, curr_page):
        self.go_back_bton = Button(
            frame,
            text="Go Back",
            **self.get_font_fg_bg(),
            command=lambda: [self.hide_frame(frame), self.main_page()],
        )
        self.go_back_bton.place(
            relx=0.35, rely=0.9, anchor=CENTER, height=40, width=220
        )

        if curr_page == "search_book":
            self.submit_bton = Button(
                frame,
                text="Submit",
                **self.get_font_fg_bg(),
                command=lambda: find_books(
                    self.entry_widget.get(), self.conn, self.tree
                ),
            )
        # rcr page
        else:
            self.submit_bton = Button(
                frame,
                text="Submit",
                **self.get_font_fg_bg(),
                command=lambda: self.call_appropriate_rcr_action(
                    self.entry_widget.get(), self.rcr_dropdown.get()
                ),
            )
        self.submit_bton.place(relx=0.75, rely=0.9, anchor=CENTER, height=40, width=220)

    def define_treeView_heading(self, order_num, width_num, col_name):
        self.tree.column(
            f"# {order_num}", anchor=CENTER, stretch=False, width=width_num
        )
        self.tree.heading(f"# {order_num}", text=col_name)

    def search_book_page(self):
        self.master.title("Search Book")

        # create new frame for 'search book' page to attach all its widgets
        self.sb_frame = Frame(self.master, bg="#FFC300", height=700, width=1400)

        # widgets for "search book" label and entry for getting user input
        self.create_label_entry_widgets(
            frame=self.sb_frame, label_text="Search Book Title", y=0.1
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
        self.define_treeView_heading("1", 120, "Id")
        self.define_treeView_heading("2", 140, "Genre")
        self.define_treeView_heading("3", 223, "Title")
        self.define_treeView_heading("4", 223, "Author")
        self.define_treeView_heading("5", 140, "Purchase Price")
        self.define_treeView_heading("6", 223, "Purchase Date")

        self.tree.place(x=200, y=140)

        self.create_bottom_button_widgets(self.sb_frame, "search_book")

        # show frame with all its widgets
        self.show_frame(self.sb_frame)

    def show_diff_widgets_based_on_action_submitted(self):
        # if self.rcr_dropdown.get() == "Reserve Book":
        self.create_label_entry_widgets(
            frame=self.rcr_frame, label_text="Book ID", y=0.3, x1=0.35, x2=0.55
        )

        self.create_label_entry_widgets(
            frame=self.rcr_frame, label_text="Member ID", y=0.4, x1=0.35, x2=0.55
        )

        # elif self.rcr_dropdown.get() == "Checkout Book":
        #     self.create_label_entry_widgets(
        #         frame=self.rcr_frame, label_text="Book ID", height=0.3
        #     )

        #     self.create_label_entry_widgets(
        #         frame=self.rcr_frame, label_text="Member ID", height=0.2
        #     )

        # # invalid => member ID or book ID is wrong
        # messagebox.showerror("error", "Unsuccessful Checkout")

        # valid member ID and book ID
        # if book is available => not on loan or is already reserved
        # checkout the book and update the db

        ### else ###
        # invalid checkout => the book is not available (on loan or reservation)
        # allow user to reserve it
        # messagebox.showinfo("success", "Successful Checkout")

        # elif self.rcr_dropdown.get() == "Return Book":
        #     self.create_label_entry_widgets(
        #         frame=self.rcr_frame, label_text="Book ID", height=0.3
        #     )

        #     self.create_label_entry_widgets(
        #         frame=self.rcr_frame, label_text="Member ID", height=0.2
        #     )

        #     # if id is invalid or the book is already available
        # messagebox.showerror(
        #         "error",
        #         "Unsuccessful Return\nEither the Book ID is invalid or the book is available",
        #     )

        # once it is returned - show a message if the book is pre-reserved by a member

    def rcr_page(self):
        self.master.title("Checkout Book")

        # create new frame for the 'rcr' page to attach all its widgets
        self.rcr_frame = Frame(self.master, bg="#FFC300", height=700, width=1000)

        # widgets
        self.rcr_dropdown = Combobox(
            self.rcr_frame,
            state="readonly",
            justify="center",
            values=["Reserve Book", "Checkout Book", "Return Book"],
        )
        self.rcr_dropdown.current(0)
        self.rcr_dropdown.place(
            relx=0.45, rely=0.1, anchor=CENTER, height=30, width=500
        )

        self.action_submit_btn = Button(
            self.rcr_frame,
            text="Submit Action",
            command=self.show_diff_widgets_based_on_action_submitted,
        )
        self.action_submit_btn.place(
            relx=0.8, rely=0.10, anchor=CENTER, height=30, width=150
        )

        self.create_bottom_button_widgets(self.rcr_frame, "rcr_page")

        # show frame with all its widgets
        self.show_frame(self.rcr_frame)

    def recommendation_page(self):
        print("Recommendation Page")

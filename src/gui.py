from tkinter import Text, Label, Entry, Button, Frame, Canvas, messagebox, CENTER, END
from ttkwidgets.autocomplete import AutocompleteEntry
from PIL import Image, ImageTk
from tkinter.ttk import Combobox, Treeview
from bookSearch import find_books
from bookReserve import reserve_book
from bookCheckout import checkout_book
from bookReturn import return_book


class app:
    def __init__(self, master, conn, data_dir_path, book_titles_lst):
        self.master = master
        self.conn = conn
        self.master.title("Library Management System")
        self.w, self.h = (
            self.master.winfo_screenwidth(),
            self.master.winfo_screenheight(),
        )
        self.master.geometry("%dx%d+0+0" % (self.w, self.h))
        self.master.configure(background="#FFC300")

        self.bs_img_path = f"{data_dir_path}/imgs/bs_img.png"
        self.rcr_img_path = f"{data_dir_path}/imgs/rcr_img.png"
        self.frb_img_path = f"{data_dir_path}/imgs/frb_img.png"
        self.dbs_img_path = f"{data_dir_path}/imgs/dbs_img.png"
        self.erd_img_path = f"{data_dir_path}/imgs/erd_diagram.png"

        self.book_titles_lst = book_titles_lst

        self.main_page()

    def show_frame(self, frame):
        #  set border color
        frame.config(highlightbackground="black", highlightthickness=10)
        #  make frame visible to toplevel
        frame.pack(expand=True)

    def hide_frame(self, frame):
        # remove the frame from toplevel
        frame.pack_forget()

    def get_font_fg_bg(self):

        return {"font": "sans 16 bold", "fg": "white", "bg": "black"}

    def get_img_obj(self, frame, img_path):
        label = Label(frame)
        img = Image.open(img_path)
        label.img = ImageTk.PhotoImage(img)

        return label.img

    def create_text_widget(self, frame, text, x, y, w):
        # add Text widget
        T = Text(frame, **self.get_font_fg_bg())
        T.tag_configure("center", justify="center")
        T.insert(END, text)
        T.tag_add("center", "1.0", END)
        T.config(state="disabled")
        T.place(relx=x, rely=y, anchor=CENTER, height=80, width=w)

    def main_page(self):
        self.master.title("Library Management System")

        self.main_frame = Frame(self.master, bg="#FFC300", height=700, width=900)

        # add Text widget
        text = "\nWelcome to Petros's Library Management System"
        self.create_text_widget(frame=self.main_frame, text=text, x=0.53, y=0.35, w=700)

        self.search_bton = Button(
            self.main_frame,
            **self.get_font_fg_bg(),
            image=self.get_img_obj(self.main_frame, self.bs_img_path),
            command=lambda: [self.hide_frame(self.main_frame), self.search_book_page()],
        )
        self.search_bton.place(relx=0.5, rely=0.55, anchor=CENTER, height=60, width=400)

        # rcr => reserve, checkout, return
        self.rcr_bton = Button(
            self.main_frame,
            **self.get_font_fg_bg(),
            image=self.get_img_obj(self.main_frame, self.rcr_img_path),
            command=lambda: [self.hide_frame(self.main_frame), self.rcr_page()],
        )
        self.rcr_bton.place(relx=0.5, rely=0.65, anchor=CENTER, height=60, width=400)

        self.rec_bton = Button(
            self.main_frame,
            **self.get_font_fg_bg(),
            image=self.get_img_obj(self.main_frame, self.frb_img_path),
            command=lambda: [
                self.hide_frame(self.main_frame),
                self.recommendation_page(),
            ],
        )
        self.rec_bton.place(relx=0.5, rely=0.75, anchor=CENTER, height=60, width=400)

        self.db_schema_bton = Button(
            self.main_frame,
            **self.get_font_fg_bg(),
            image=self.get_img_obj(self.main_frame, self.dbs_img_path),
            command=lambda: [
                self.hide_frame(self.main_frame),
                self.db_schema_page(),
            ],
        )
        self.db_schema_bton.place(
            relx=0.5, rely=0.85, anchor=CENTER, height=60, width=400
        )

        self.show_frame(self.main_frame)

    def create_label_entry_widgets(
        self, frame, label_text, y, x1=0.48, x2=0.65, autocomplete_widget_flag=False
    ):
        self.entry_label = Label(frame, text=label_text, font=("calibre", 10, "bold"))
        self.entry_label.place(relx=x1, rely=y, anchor=CENTER, height=40, width=200)

        if autocomplete_widget_flag == False:
            self.entry_widget = Entry(frame, font=("calibre", 10, "normal"))
            self.entry_widget.place(
                relx=x2, rely=y, anchor=CENTER, height=40, width=220
            )
        # Search Book page
        else:
            self.entry_widget = AutocompleteEntry(
                frame,
                font=("calibre", 10, "normal"),
                completevalues=self.book_titles_lst,
            )
            self.entry_widget.place(
                relx=x2, rely=y, anchor=CENTER, height=40, width=220
            )

    def call_appropriate_rcr_action(self, member_id, action_submitted):
        if action_submitted == "Reserve Book":
            reserve_book()
        elif action_submitted == "Checkout Book":
            checkout_book()
        else:
            return_book()

    def check_in_which_page_submit_button_was_pressed(self, curr_page):
        if curr_page == "search_book":
            return lambda: find_books(self.entry_widget.get(), self.conn, self.tree)
        elif curr_page == "rcr_page":
            return lambda: self.call_appropriate_rcr_action(
                self.entry_widget.get(), self.rcr_dropdown.get()
            )

    def create_bottom_button_widgets(
        self, frame, curr_page, go_back_bton_x=0.35, go_back_bton_y=0.9
    ):
        self.go_back_bton = Button(
            frame,
            text="Go Back",
            **self.get_font_fg_bg(),
            command=lambda: [self.hide_frame(frame), self.main_page()],
        )
        self.go_back_bton.place(
            relx=go_back_bton_x,
            rely=go_back_bton_y,
            anchor=CENTER,
            height=40,
            width=220,
        )

        # db_schema page should not have a submit button
        if curr_page != "db_schema_page":
            self.submit_bton = Button(
                frame,
                text="Submit",
                **self.get_font_fg_bg(),
                command=self.check_in_which_page_submit_button_was_pressed(curr_page),
            )
            self.submit_bton.place(
                relx=0.75, rely=0.9, anchor=CENTER, height=40, width=220
            )

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
            frame=self.sb_frame,
            label_text="Search Book Title",
            y=0.1,
            autocomplete_widget_flag=True,
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

        self.create_bottom_button_widgets(frame=self.sb_frame, curr_page="search_book")

        # show frame with all its widgets
        self.show_frame(self.sb_frame)

    def show_id_label_entry_widgets(self):
        messagebox.showinfo(
            "Success",
            f"""You are ready to
{self.rcr_dropdown.get().split(' ')[0]} a {self.rcr_dropdown.get().split(' ')[1]}!""",
        )

        self.create_label_entry_widgets(
            frame=self.rcr_frame, label_text="Book ID", y=0.3, x1=0.35, x2=0.55
        )

        self.create_label_entry_widgets(
            frame=self.rcr_frame, label_text="Member ID", y=0.4, x1=0.35, x2=0.55
        )

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
            command=self.show_id_label_entry_widgets,
        )
        self.action_submit_btn.place(
            relx=0.8, rely=0.10, anchor=CENTER, height=30, width=150
        )

        self.create_bottom_button_widgets(frame=self.rcr_frame, curr_page="rcr_page")

        # show frame with all its widgets
        self.show_frame(self.rcr_frame)

    def recommendation_page(self):
        self.master.title("Recommended Books")

        # create new frame for the 'recommendation_page' page to attach all its widgets
        self.rec_frame = Frame(self.master, bg="#FFC300", height=700, width=1000)

        self.create_bottom_button_widgets(frame=self.rec_frame, curr_page="rec_page")

        # show frame with all its widgets
        self.show_frame(self.rec_frame)

    def db_schema_page(self):
        self.master.title("DB Schema")

        # create new frame for the 'db_schema_page' page to attach all its widgets
        self.db_schema_frame = Frame(self.master, bg="#FFC300", height=800, width=1000)

        # add Text widget
        text = "\nMy Database Schema"
        self.create_text_widget(
            frame=self.db_schema_frame, text=text, x=0.515, y=0.1, w=500
        )

        # create canvas and place it on the frame
        canvas = Canvas(
            self.db_schema_frame,
            bg="#FFC300",
            highlightbackground="white",
            highlightthickness=5,
        )

        # load img that shows the db structure
        erd_img = Image.open(self.erd_img_path)
        self.db_schema_frame.logo = ImageTk.PhotoImage(erd_img)

        # place the image as canvas image object directly on the canvas
        canvas.create_image(450, 280, image=self.db_schema_frame.logo, anchor=CENTER)
        canvas.place(relx=0.5, rely=0.55, width=900, height=550, anchor=CENTER)

        self.create_bottom_button_widgets(
            frame=self.db_schema_frame,
            curr_page="db_schema_page",
            go_back_bton_x=0.5,
            go_back_bton_y=0.96,
        )

        # show frame with all its widgets
        self.show_frame(self.db_schema_frame)

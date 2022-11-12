from tkinter import (
    Text,
    Label,
    Entry,
    Button,
    Frame,
    Canvas,
    messagebox,
    Message,
    CENTER,
    END,
)
from tkinter.ttk import Combobox, Treeview, Notebook, Style
from ttkwidgets.autocomplete import AutocompleteEntry
from PIL import Image, ImageTk
from bookSearch import SearchBookTitle
from bookSelect import BookRecommendationSystem
from bookReserve import reserve_book
from bookCheckout import checkout_book
from bookReturn import return_book


class App:
    def __init__(
        self, master, databaseObj, data_dir_path, book_titles_lst, book_ids_lst
    ):
        def create_window(master):
            self.master = master
            self.master.title("Library Management System")
            self.master.configure(background="#FFC300")

        create_window(master)

        self.databaseObj = databaseObj
        self.conn = self.databaseObj.conn

        def set_window_geometry():
            self.w, self.h = (
                self.master.winfo_screenwidth(),
                self.master.winfo_screenheight(),
            )
            self.master.geometry("%dx%d+0+0" % (self.w, self.h))

        set_window_geometry()

        def set_img_paths(data_dir_path):
            self.bs_img_path = f"{data_dir_path}/imgs/bs_img.png"
            self.rcr_img_path = f"{data_dir_path}/imgs/rcr_img.png"
            self.frb_img_path = f"{data_dir_path}/imgs/frb_img.png"
            self.dbs_img_path = f"{data_dir_path}/imgs/dbs_img.png"
            self.erd_img_path = f"{data_dir_path}/imgs/erd_diagram.png"

        set_img_paths(data_dir_path)

        self.book_titles_lst = book_titles_lst
        self.book_ids_lst = book_ids_lst

        def set_colors_to__widgets():
            self.style = Style()

            self.style.theme_create(
                "#FFC300",
                settings={
                    "TCombobox": {
                        "configure": {
                            "background": "black",
                            "fieldbackground": "black",
                            "foreground": "white",
                        },
                    },
                    "TNotebook": {
                        "configure": {
                            "background": "black",
                            "tabmargins": [2, 5, 0, 0],
                        }
                    },
                    "TNotebook.Tab": {
                        "configure": {
                            "background": "black",
                            "foreground": "white",
                            "padding": [10, 2],
                            "font": "white",
                        },
                        "map": {
                            "background": [("selected", "red")],
                            "expand": [("selected", [1, 1, 1, 0])],
                        },
                    },
                },
            )
            self.style.theme_use("#FFC300")

        set_colors_to__widgets()

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

    def create_text_widget(self, frame, text, x, y, w):
        # add Text widget
        T = Text(frame, **self.get_font_fg_bg())
        T.tag_configure("center", justify="center")
        T.insert(END, text)
        T.tag_add("center", "1.0", END)
        T.config(state="disabled")
        T.place(relx=x, rely=y, anchor=CENTER, height=80, width=w)

    def main_page(self):
        def get_img_obj(img_path):
            label = Label(self.main_frame)
            img = Image.open(img_path)
            label.img = ImageTk.PhotoImage(img)

            return label.img

        self.master.title("Library Management System")

        self.main_frame = Frame(self.master, bg="#FFC300", height=700, width=900)

        # add Text widget
        text = "\nWelcome to Petros's Library Management System"
        self.create_text_widget(frame=self.main_frame, text=text, x=0.53, y=0.35, w=700)

        self.search_bton = Button(
            self.main_frame,
            **self.get_font_fg_bg(),
            image=get_img_obj(self.bs_img_path),
            command=lambda: [self.hide_frame(self.main_frame), self.search_book_page()],
        )
        self.search_bton.place(relx=0.5, rely=0.55, anchor=CENTER, height=60, width=400)

        # rcr => reserve, checkout, return
        self.rcr_bton = Button(
            self.main_frame,
            **self.get_font_fg_bg(),
            image=get_img_obj(self.rcr_img_path),
            command=lambda: [self.hide_frame(self.main_frame), self.rcr_page()],
        )
        self.rcr_bton.place(relx=0.5, rely=0.65, anchor=CENTER, height=60, width=400)

        self.rec_bton = Button(
            self.main_frame,
            **self.get_font_fg_bg(),
            image=get_img_obj(self.frb_img_path),
            command=lambda: [
                self.hide_frame(self.main_frame),
                self.recommendation_page(),
            ],
        )
        self.rec_bton.place(relx=0.5, rely=0.75, anchor=CENTER, height=60, width=400)

        self.db_schema_bton = Button(
            self.main_frame,
            **self.get_font_fg_bg(),
            image=get_img_obj(self.dbs_img_path),
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

            return self.entry_widget
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

    def check_in_which_page_submit_button_was_pressed(
        self, curr_page, recommendation_tab=None
    ):
        def call_appropriate_rcr_action():
            bookID = self.book_id.get()
            memberID = self.member_id.get()

            try:
                bookID = int(bookID)
                memberID = int(memberID)
            except ValueError:
                messagebox.showerror("Error", "The IDs need to be integers")
                return

            if (memberID < 1000 or memberID > 9999) and bookID not in self.book_ids_lst:
                messagebox.showerror("Error", "Both provided IDs are invalid")
                return
            elif memberID < 1000 or memberID > 9999:
                messagebox.showerror("Error", "The provided Member ID is invalid")
                return
            elif bookID not in self.book_ids_lst:
                messagebox.showerror("Error", "The provided Book ID is invalid")
                return

            action_submitted = self.rcr_dropdown.get()

            if action_submitted == "Reserve Book":
                reserve_book()
            elif action_submitted == "Checkout Book":
                checkout_book()
            else:
                return_book()

        if curr_page == "search_book":
            return lambda: self.SearchBookTitleObject.find_books(
                self.entry_widget.get()
            )
        elif curr_page == "rcr_page":
            return lambda: call_appropriate_rcr_action()
        elif curr_page == "rec_page":
            if recommendation_tab == "Book Copy":

                return (
                    lambda: self.bookRecommendationSystemObject.most_checkouts_per_copy(
                        self.tree
                    )
                )

            elif recommendation_tab == "Book":
                return (
                    lambda: self.bookRecommendationSystemObject.most_checkouts_per_book(
                        self.tree
                    )
                )

            elif recommendation_tab == "Available Days":
                return lambda: self.bookRecommendationSystemObject.total_available_days(
                    self.tree
                )

            elif recommendation_tab == "Genre":
                return lambda: self.bookRecommendationSystemObject.most_checkouts_per_genre(
                    self.tree
                )

    def create_bottom_button_widgets(
        self,
        frame,
        curr_page,
        recommendation_tab=None,
        go_back_bton_x=0.35,
        go_back_bton_y=0.9,
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

        # "db_schema" page should not have a submit button
        if curr_page != "db_schema_page":
            self.submit_bton = Button(
                frame,
                text="Submit",
                **self.get_font_fg_bg(),
                command=self.check_in_which_page_submit_button_was_pressed(
                    curr_page, recommendation_tab
                ),
            )
            self.submit_bton.place(
                relx=0.75, rely=0.9, anchor=CENTER, height=40, width=220
            )

    def change_Treeview_configs(
        self, frame, columns, h, bg, fieldbg, fg, highlightbg="black"
    ):
        self.tree = Treeview(
            frame,
            columns=[*columns],
            show="headings",
            height=h,
        )

        # change color to the Treeview
        self.style.configure(
            "Treeview",
            background=bg,
            fieldbackground=fieldbg,
            foreground=fg,
            highlightbackground=highlightbg,
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

        # define Treeview headings
        columns = [
            "BookId",
            "Genre",
            "Title",
            "Book Author",
            "Purchase Price",
            "Purchase Date",
        ]

        # add a Treeview widget
        self.change_Treeview_configs(
            frame=self.sb_frame,
            columns=columns,
            h=20,
            bg="black",
            fieldbg="black",
            fg="white",
        )

        # define headings
        self.define_treeView_heading("1", 120, "Id")
        self.define_treeView_heading("2", 140, "Genre")
        self.define_treeView_heading("3", 223, "Title")
        self.define_treeView_heading("4", 223, "Author")
        self.define_treeView_heading("5", 140, "Purchase Price")
        self.define_treeView_heading("6", 223, "Purchase Date")

        self.tree.place(x=200, y=140)

        # create instance of the SearchBookTitle class
        self.SearchBookTitleObject = SearchBookTitle(self.databaseObj, self.tree)

        self.create_bottom_button_widgets(frame=self.sb_frame, curr_page="search_book")

        # show frame with all its widgets
        self.show_frame(self.sb_frame)

    def show_id_label_entry_widgets(self):
        messagebox.showinfo(
            "Success",
            f"""You are ready to
{self.rcr_dropdown.get().split(' ')[0]} a {self.rcr_dropdown.get().split(' ')[1]}!""",
        )

        self.book_id = self.create_label_entry_widgets(
            frame=self.rcr_frame, label_text="Book ID", y=0.3, x1=0.35, x2=0.55
        )

        self.member_id = self.create_label_entry_widgets(
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
            bg="black",
            fg="white",
            command=self.show_id_label_entry_widgets,
        )
        self.action_submit_btn.place(
            relx=0.8, rely=0.10, anchor=CENTER, height=30, width=150
        )

        self.create_bottom_button_widgets(frame=self.rcr_frame, curr_page="rcr_page")

        # show frame with all its widgets
        self.show_frame(self.rcr_frame)

    def recommendation_page(self):
        def on_tab_change(event):
            def add_treeView_to_notebookTab(frame, cols, pos_x, w):

                # add a Treeview widget
                self.change_Treeview_configs(
                    frame=frame,
                    columns=cols,
                    h=10,
                    bg="red",
                    fieldbg="red",
                    fg="white",
                    highlightbg="red",
                )

                # define headings
                heading_position = 120
                for i, text in enumerate(cols):
                    if text == "Book Title":
                        heading_position += 100

                    self.define_treeView_heading(str(i + 1), heading_position, text)
                    heading_position += 45

                self.tree.place(x=pos_x, y=20, width=w)

            self.tab = event.widget.tab("current")["text"]

            if self.tab == "Book Copy":
                add_treeView_to_notebookTab(
                    frame=self.tab1,
                    cols=["BookId", "Book Title", "Num of Checkouts"],
                    pos_x=65,
                    w=680,
                )
            elif self.tab == "Book":
                add_treeView_to_notebookTab(
                    frame=self.tab2,
                    cols=["Book Title", "Num of Checkouts"],
                    pos_x=180,
                    w=490,
                )
            elif self.tab == "Available Days":
                add_treeView_to_notebookTab(
                    frame=self.tab3,
                    cols=["Book Title", "Num of Checkouts", "Available Days"],
                    pos_x=50,
                    w=700,
                )
            elif self.tab == "Genre":
                add_treeView_to_notebookTab(
                    frame=self.tab4,
                    cols=["Genre", "Num of Checkouts"],
                    pos_x=250,
                    w=280,
                )

            self.create_bottom_button_widgets(
                frame=self.rec_frame, curr_page="rec_page", recommendation_tab=self.tab
            )

        self.master.title("Recommended Books")

        # create new frame for the 'recommendation_page' page to attach all its widgets
        self.rec_frame = Frame(self.master, bg="#FFC300", height=700, width=1000)

        # add Text widget
        text = "\nFind recommended books based on the below conditions"
        self.create_text_widget(frame=self.rec_frame, text=text, x=0.55, y=0.10, w=700)

        # add Message widget
        bullet_point1 = "\u2022 Most Checkouts per Book Copy"
        bullet_point2 = "\u2022 Most Checkouts per Book"
        bullet_point3 = "\u2022 Most Checkouts in respect of Available Days (Purchase date till today) per Book"
        bullet_point4 = "\u2022 Most Checkouts per Genre"
        msg = Message(
            self.rec_frame,
            text="%s\n%s\n%s\n%s"
            % (bullet_point1, bullet_point2, bullet_point3, bullet_point4),
            background="white",
            width=550,
            anchor="w",
        )
        msg.place(x=285, y=125)

        # add Notebook widget
        notebook = Notebook(self.rec_frame)
        notebook.place(relx=0.55, rely=0.55, width=800, height=300, anchor=CENTER)

        # create tab 1 to the notebook
        self.tab1 = Frame(notebook, bg="black")
        notebook.add(self.tab1, text="Book Copy")

        # create tab 2 to the notebook
        self.tab2 = Frame(notebook, bg="black")
        notebook.add(self.tab2, text="Book")

        # add tab 3 to the notebook
        self.tab3 = Frame(notebook, bg="black")
        notebook.add(self.tab3, text="Available Days")

        # add tab 4 to the notebook
        self.tab4 = Frame(notebook, bg="black")
        notebook.add(self.tab4, text="Genre")

        # create object for book recommendation system
        self.bookRecommendationSystemObject = BookRecommendationSystem(self.databaseObj)

        # change configurations of Treeview when the tab is changed
        notebook.bind("<<NotebookTabChanged>>", on_tab_change)

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

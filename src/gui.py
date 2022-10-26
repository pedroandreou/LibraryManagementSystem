from tkinter import Label, Entry, Button, Frame, CENTER


class app:
    def __init__(self, master):
        self.master = master
        self.master.title("Library Management System")
        self.master.geometry("950x750")
        self.master.configure(background="#FFC300")
        self.main_page()

    def main_page(self):
        self.master.title("Library Management System")
        for i in self.master.winfo_children():
            i.destroy()

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
            text="Recommended Books",
            font="sans 16 bold",
            fg="white",
            bg="black",
            command=self.recommendation_page,
        )
        self.rec_bton.place(relx=0.5, rely=0.65, anchor=CENTER, height=40, width=300)

    def get_data(self):
        print(self.memberid_entry.get())

    def search_book_page(self):
        self.master.title("Search Book")
        for i in self.master.winfo_children():
            i.destroy()

        self.sb_frame = Frame(self.master, bg="#FFC300", height=700, width=700)
        self.sb_frame.pack_propagate(False)

        self.memberid_label = Label(
            self.sb_frame, text="Member ID", font=("calibre", 10, "bold")
        )
        self.memberid_label.place(
            relx=0.4, rely=0.5, anchor=CENTER, height=40, width=200
        )

        self.memberid_entry = Entry(self.sb_frame, font=("calibre", 10, "normal"))
        self.memberid_entry.place(
            relx=0.69, rely=0.5, anchor=CENTER, height=40, width=220
        )

        self.go_back = Button(
            self.sb_frame,
            text="Go Back",
            font="sans 16 bold",
            fg="white",
            bg="black",
            command=self.main_page,
        )
        self.go_back.place(relx=0.35, rely=0.8, anchor=CENTER, height=40, width=220)

        self.submit_bton = Button(
            self.sb_frame,
            text="Submit",
            font="sans 16 bold",
            fg="white",
            bg="black",
            command=self.get_data,
        )
        self.submit_bton.place(relx=0.75, rely=0.8, anchor=CENTER, height=40, width=220)

        self.sb_frame.pack(padx=1, pady=1)

    def rcr_page(self):
        self.master.title("Checkout Book")
        for i in self.master.winfo_children():
            i.destroy()

        # self.go_back = Button(
        #     text="Go Back",
        #     font="sans 16 bold",
        #     fg="white",
        #     bg="black",
        #     command=self.main_page,
        # )
        # self.go_back.place(relx=0.35, rely=0.8, anchor=CENTER, height=40, width=300)

    def recommendation_page(self):
        print("")

from tkinter import Button, CENTER


class app:
    def __init__(self, master):
        self.master = master
        self.master.title("Library Management System")
        self.master.geometry("950x750")
        self.master.configure(background="#FFC300")
        self.main_page()

    def main_page(self):
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

        self.checkout_bton = Button(
            text="Checkout Book",
            font="sans 16 bold",
            fg="white",
            bg="black",
            command=self.checkout_book_page,
        )
        self.checkout_bton.place(
            relx=0.5, rely=0.55, anchor=CENTER, height=40, width=300
        )

    def search_book_page(self):
        print("")

    def checkout_book_page(self):
        print("")

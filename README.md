# Outcomes:
- The GUI's window is dynamic, it gets increased or decreased in size automatically
- Loaded txt files using the pandas 'to_sql' method
- Followed STAR schema
- Created fact tables and dimension tables programmatically (look at "create_dimension_table" function in "database.py" file)
- Mapped values to ids dynamically for assigning them as keys to tables (look at "map_vals_to_ids" function in "database.py" file)
- Created reusable code for the widgets; for example, the two buttons on the bottom of each page, "Go Back" and "Submit" can be added by calling the "create_bottom_button_widgets" method, same applies for the entry and label widgets ("create_label_entry_widgets" method).
- Instead of destroying the frame of each page by doing:
```
def destroy_page_widgets(self):
  for i in self.master.winfo_children():
    i.destroy()
```
I am hiding and turn the frames to visible again when appropriate (see at "show_frame" and "hide_frame" methods in "gui.py" file)
- Created images using draw.io in combination with GIMP software and added them to Tkinter buttons
- No point of writing dot code for visualising the ERD diagram of my DB. Used DBeaver software to generate the diagram automatically and made the images transparent using the GIMP software
- Autocomplete of suggested book titles feature added to the "Search Book" page using the ttkwidgets library
- Added an option for finding the most Reservations/Checkouts/Returns (a.k.a. RCR) in respect of the most available days of the book. In other words, I find all the copies of that particular book and sum all the available dates (the date that book copy was purchased till today's date) using JULIANDAY function and then based on the RCR (one of the three actions that the user chose), I find which book has been more popular. See "most_rcr_available_days" method in the "BookSelect.py" and "self.available_days_flag == True" in the "Treeview.py" file for better understanding
- Utilized the latest cutting-edge technology on DevOps, the Tkinter GUI app can be run in a Docker Container with just a single instruction from anywhere. However, still haven't added a volume and attached/mounted the local SQLite DB to the created directory in the container and as a result, the data is not persistent


# Notes:
- In case you want to check if the normalization really happens which would require to change some of the data in the txt files; make sure the db file is deleted
before you run the program again as it won't load the changes. The reason is because I am checking if the db exists and in case it does,
then I skip the loading part since it only needs to be loaded once. In case of loading the db every single time the program runs, then the data would be always overwritten and the user's changes would be always lost after the end of a session
- Documentation for what each line of the ERD diagram represents added in the ./data/imgs directory
- In my recommendation page, it can be noticed that the TransactionType of "Return" books happened a lot more than the "Checkout" TransactionType. That's because of the initial data in the txt files. However, the whole procedure is right, I just tried to make the initial data as harder as possible so all conditions could be met by my program. The explanation behind it will be stated in the "The logic behind Transactions Table" section below


# The logic behind Transaction Table:
The below logic applies to the load of the files, since the procedure of Reserving, Checking Out, Returning via the GUI is much simpler as the user decides which TransactionType wants to move forward with. On the other hand, in the case of the txt files, I had to understand which TransactionType was, based on the below conditions:

1. When Reserve, Checkout and Return happened at the same time, then it's considered as a Checkout and both ReservedMemberId and CheckedOutId are the given ID.
2. In case Reserve and Checkout happened at the same time, then:
  - if the Reserve Date is more recent than the Checkout Date, then the TransactionType is Reserve as somebody tried to reserve a book while it was still checked out.
  - otherwise, it is considered as a Checkout and my program looks if there was a previous transaction;
    In case there was, then it adds the previous transaction's member ID to:
     * the current transaction's ReservedMemberId if the current transaction is Checkout
     * the current transaction's CheckedOutMemberId if the current transaction is Reserve
3. In case Checkout and Return happened at the same time, then it is considered as Return and the CheckoutMemberId is the one given
4. In case, it was only Reserve, then  the TransactionType is Reserve and ReserveMemberId is the one given
5. In case, it was only Checkout, then the TransactionType is Checkout and CheckoutMemberId is the one given


# Future Work:
- Add a vertical scroll bar to the TreeView widget for better UX but nevertheless, the user can still scroll without one
- There is only one thing that I would change in my DB Schema. The book copies are currently all in the BookInventory table whereas the BookCopies table just adds another 2 columns to the BookInventory. That's silly and I should have noticed it earlier. In the reality, BookInventory should have only had the different books and all the copies should have been in the BookCopies table.
For completing this task I should have done the following changes:
1. the BookCopyKey FK needs to be removed from the BookInventory table
2. a new PK needs to be created in the BookCopies table for tracking each book copy
3. BookId needs to be set as FK to BookCopies table
- Add functionality that will check for expiration dates since I have already set expiration dates to people that reserve or checkout a book (reservation can last for 10 days while checkout for 30 days) but haven't added any functionality for checking if the user meets the criteria
- EndRecordDate of transaction has been added to the Transactions table. I would add the new transaction's date as the EndRecordDate of the previous transaction. In other words, when a new transaction comes in, the previous transaction should close; have an end date. It's a simple task as the way how to add it is already implemented using the "fill_new_fields" method in the "database.py" file.


# Environment
## How to set up a virtual environment on Windows:
```
  cd .\LibraryManagementSystem\
  python -m venv .venv (To create virtual environment)
  .venv\Scripts\activate (Activate virtual environment)
  pip install -r requirements.txt (Install all required packages)
```

## In case your Windows OS is not well set-up, do the following:
Add the following environment variables in the Path of *User variables for user*:
```
C:\Users\user\AppData\Local\Programs\Python\Python<yourpythonversion>\Scripts  (e.g. C:\Users\user\AppData\Local\Programs\Python\Python39\Scripts)
C:\Users\user\anaconda3
C:\Users\user\anaconda3\Scripts
C:\Users\user\anaconda3\Library\bin
```

Add the following environment variables in the *System Variables*:
```
C:\Users\user\AppData\Local\Programs\Python\Python<yourpythonversion>  (e.g. C:\Users\user\AppData\Local\Programs\Python\Python39)
```

## How to set up a virtual environment on Linux:
You should create a virtualenv with the required dependencies by running
```
make virtualenv
```

How to activate the virtual environment:
```
source ./.env/bin/activate
```

When a new requirement is needed you should add it to `unpinned_requirements.txt` and run
(this ensures that all requirements are pinned and work together for ensuring reproducibility)
```
make update-requirements-txt
```


## How to play around with my db on Linux:
```
sudo apt install sqlite3
./LibraryManagementSystem/data
sqlite3 library.db
```


## :whale: Docker
#### How to run the Tkinter app in a container:
sudo apt-get install x11-xserver-utils (Haven't included it in the requirements.txt as pip cannot find a matching distribution for this package)
docker run -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY librarymanagementsystem_myproject


## 🛠 Initialization & Setup
#### Clone the repository
    git clone https://github.com/pedroandreou/LibraryManagementSystem.git


## Author
Petros Andreou

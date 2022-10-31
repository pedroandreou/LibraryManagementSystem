# Outcomes
- loaded txt files using pandas to_sql method
- followed STAR schema
- created fact tables and dimension tables programmatically (look at "create_dimension_table" function in "database.py" file)
- mapped values to ids programmatically for assigning them as keys to tables (look at "map_vals_to_ids" function in "database.py" file)
- set expiration dates to people that reserve or checkout a book (reservation can last for 10 days while checkout for 30 days)


# Notes
- In case you want to check if the normalization really happens which would require to change some of the data in the txt files; make sure the db file is deleted
before you run the program again as it won't load the changes. The reason is because I am checking if the db exists and in case it does,
then I skip the loading part since it only needs to be loaded once as well as as the changes of the program will stay whereas in case of loading the db every single time the program runs, then the data would be always overwritten and the user's changes would be always lost after a session.


# Environment
## How to set up a virtual environment on Windows
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

## How to set up a virtual environment on Ubuntu
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

## How to run sqlite3.exe file on Ubuntu
```
pip install wine
wine sqlite3.exe
```

## How to play around with my db on Ubuntu
```
sudo apt install sqlite3
./LibraryManagementSystem/data
sqlite3 library.db
```


## 🛠 Initialization & Setup
#### Clone the repository
    git clone https://github.com/pedroandreou/LIbraryManagementSystem.git


## Author
Petros Andreou

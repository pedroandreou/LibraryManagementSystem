# Environment

## How to set up a virtual environment on Windows
```
  cd .\LibraryManagementSystem\
  python -m venv .venv (To create your virtual environment, go into your project and run:)
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

## 🛠 Initialization & Setup
#### Clone the repository
    git clone https://github.com/pedroandreou/BookLibrarySystem.git

## Author
Petros Andreou

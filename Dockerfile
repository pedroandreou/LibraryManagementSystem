# Set base image in Python 3.9
FROM python:3.9

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy packages required from local requirements file to Docker image requirements file
COPY requirements.txt ./requirements.txt

# Run command line instructions
RUN pip install -r requirements.txt

# Download Package Information
RUN apt-get update -y

# Install Tkinter
RUN apt-get install tk -y

# Doownload sqlite
RUN apt-get install -y sqlite3 libsqlite3-dev

# Copy all files from local project folder to Docker image
COPY . .

# Run Tkinter application
CMD [ "python3", "src/menu.py" ]

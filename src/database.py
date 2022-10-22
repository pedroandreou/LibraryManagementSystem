import sqlite3


def create_connection(db_path):
    conn = None

    try:
        # open db => if does not exist => will be created
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as error:
        print(error)

    return conn


def create_table(conn, table):
    c = conn.cursor()

    title = table[0]
    table = table[1:]
    table_len = len(table)

    all_cols = ""
    for counter, col in enumerate(table):
        if table_len == counter + 1:
            # do not add comma => last col of the table
            all_cols += col
            break

        all_cols += col + ","

    create_table = f""" CREATE TABLE IF NOT EXISTS {title} (
                                    {all_cols}
                                ); """

    try:
        c.execute(create_table)
    except sqlite3.Error as error:
        print(error)

    conn.commit()


def fill_table(conn, table, file_path=None):
    title = table[0]
    cols = table[1]
    cols_tuple = cols.split(", ")

    # create a string of '?' based on the amount of cols that the table has
    question_marks_str = ""
    for counter, _ in enumerate(cols_tuple):
        if len(cols_tuple) == counter + 1:
            question_marks_str += "?"
            break

        question_marks_str += "?, "

    insert_with_param = f""" INSERT INTO {title}
                        ({cols})
                        VALUES ({question_marks_str}); """

    c = conn.cursor()
    with open(file_path, "r") as f:
        for line in f:

            # remove '\n' from each line
            # replace three dashes with NULL value
            line = line[:-2].replace("---", "NULL")

            line_tuple = tuple(line.split(","))

            c.execute(insert_with_param, line_tuple)

    conn.commit()
    c.close()

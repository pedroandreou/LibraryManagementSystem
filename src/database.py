import sqlite3
import pandas as pd


def create_connection(db_path):
    conn = None

    try:
        # open db => if does not exist => will be created
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as error:
        print(error)

    return conn


def execute_query(conn, query=None, data=None):
    try:
        c = conn.cursor()

        if query is not None and data is not None:
            c.execute(query, data)
        else:
            c.execute(query)
    except sqlite3.Error as error:
        print(error)
    finally:
        conn.commit()


def create_table(conn, table):
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

    execute_query(conn, create_table)


def drop_table(conn, table_name):
    drop_table = f"DROP TABLE {table_name};"

    execute_query(conn, drop_table)


# def insert_data_to_table(conn, table, data):
#     title = table[0]
#     cols = table[1]
#     cols_tuple = cols.split(", ")
#     cols_tuple_len = len(cols_tuple)

#     # create a string of '?' based on the amount of cols that the table has
#     question_marks_str = ""
#     for counter, _ in enumerate(cols_tuple):
#         if cols_tuple_len == counter + 1:
#             question_marks_str += "?"
#             break

#         question_marks_str += "?, "

#     insert_with_param = f""" INSERT INTO {title}
#                         ({cols})
#                         VALUES ({question_marks_str}); """

#     execute_query(conn, insert_with_param, data)


def init_db(conn, table_name, file_path=None):
    df = pd.read_csv(file_path, na_values="---")

    df.to_sql(name=table_name, con=conn, if_exists="replace", index=False)

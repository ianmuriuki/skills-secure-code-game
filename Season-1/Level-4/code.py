import sqlite3
import os
from flask import Flask, request
import re

### Unrelated to the exercise -- Starts here -- Please ignore
app = Flask(__name__)
@app.route("/")
def source():
    DB_CRUD_ops().get_stock_info(request.args["input"])
    DB_CRUD_ops().get_stock_price(request.args["input"])
    DB_CRUD_ops().update_stock_price(request.args["input"], 0.0)
    DB_CRUD_ops().exec_multi_query(request.args["input"])
    DB_CRUD_ops().exec_user_script(request.args["input"])
### Unrelated to the exercise -- Ends here -- Please ignore

class Connect(object):

    # Helper function creating database connection
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
        except sqlite3.Error as e:
            print(f"ERROR: {e}")
        return connection

class Create(object):

    def __init__(self):
        con = Connect()
        try:
            # Create a dummy database inside the folder of this challenge
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            # Check if table already exists (happens when re-running code)
            table_fetch = cur.execute(
                '''
                SELECT name 
                FROM sqlite_master 
                WHERE type='table' AND name='stocks';
                ''').fetchall()

            # If table does not exist, create it and insert dummy data
            if table_fetch == []:
                cur.execute(
                    '''
                    CREATE TABLE stocks
                    (date text, symbol text, price real)
                    ''')
                # Insert dummy data into the 'stocks' table (average price on date)
                cur.execute(
                    "INSERT INTO stocks VALUES ('2022-01-06', 'MSFT', 300.00)")
                db_con.commit()

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            db_con.close()

class DB_CRUD_ops(object):

    # (1) Retrieves all info about a stock symbol from the stocks table.
    # Example: get_stock_info('MSFT') will execute:
    # SELECT * FROM stocks WHERE symbol = 'MSFT'
    def get_stock_info(self, stock_symbol):
        # Build (or rebuild) the database as required for the lab
        db = Create()
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            res = "[METHOD EXECUTED] get_stock_info\n"
            query = "SELECT * FROM stocks WHERE symbol = '{0}'".format(stock_symbol)
            res += "[QUERY] " + query + "\n"

            # Restricted characters that should not exist in user input
            restricted_chars = ";%&^!#-"
            has_restricted_char = any([char in query for char in restricted_chars])
            correct_number_of_single_quotes = query.count("'") == 2

            # If input is malicious, warn the developer
            if has_restricted_char or not correct_number_of_single_quotes:
                res += "CONFIRM THAT THE ABOVE QUERY IS NOT MALICIOUS TO EXECUTE"
            else:
                cur.execute(query)
                query_outcome = cur.fetchall()
                for result in query_outcome:
                    res += "[RESULT] " + str(result)
            return res

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            db_con.close()

    # (2) Retrieves the price of a stock symbol.
    # Example: get_stock_price('MSFT') will execute:
    # SELECT price FROM stocks WHERE symbol = 'MSFT'
        def get_stock_price(self, stock_symbol):
            import re
        # Sanitize input: allow only uppercase letters (valid stock symbols)
        match = re.match(r"^[A-Z]+", stock_symbol.upper())
        if match:
            safe_symbol = match.group(0)
        else:
            safe_symbol = stock_symbol  # fallback, though ideally this branch won't be used

        db = Create()
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            res = "[METHOD EXECUTED] get_stock_price\n"
            query = "SELECT price FROM stocks WHERE symbol = '" + safe_symbol + "'"
            res += "[QUERY] " + query + "\n"
            cur.execute(query)
            query_outcome = cur.fetchall()
            for result in query_outcome:
                res += "[RESULT] " + str(result) + "\n"
            return res

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            db_con.close()


    # (3) Updates the stock price.
    def update_stock_price(self, stock_symbol, price):
        import re
        if not isinstance(price, float):
            raise Exception("ERROR: stock price provided is not a float")
        # Sanitize the stock symbol (as above)
        match = re.match(r"^[A-Z]+", stock_symbol.upper())
        if match:
            safe_symbol = match.group(0)
        else:
            safe_symbol = stock_symbol

        db = Create()
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            res = "[METHOD EXECUTED] update_stock_price\n"
            query = "UPDATE stocks SET price = '%d' WHERE symbol = '%s'" % (int(price), safe_symbol)
            res += "[QUERY] " + query + "\n"

            cur.execute(query)
            db_con.commit()
            # UPDATE queries typically return no rows
            query_outcome = cur.fetchall()
            for result in query_outcome:
                res += "[RESULT] " + str(result)
            return res

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            db_con.close()

    # (4) Executes multiple queries.
    # Example: SELECT price FROM stocks WHERE symbol = 'MSFT';
    #          SELECT * FROM stocks WHERE symbol = 'MSFT'
    def exec_multi_query(self, query):
        db = Create()
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            res = "[METHOD EXECUTED] exec_multi_query\n"
            for q in filter(None, query.split(';')):
                res += "[QUERY]" + q + "\n"
                q = q.strip()
                cur.execute(q)
                db_con.commit()

                query_outcome = cur.fetchall()
                for result in query_outcome:
                    res += "[RESULT] " + str(result) + " "
            return res

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            db_con.close()

    # (5) Executes a user-supplied script.
    def exec_user_script(self, query):
        db = Create()
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            res = "[METHOD EXECUTED] exec_user_script\n"
            res += "[QUERY] " + query + "\n"
            if ';' in query:
                res += "[SCRIPT EXECUTION]"
                cur.executescript(query)
                db_con.commit()
            else:
                cur.execute(query)
                db_con.commit()
                query_outcome = cur.fetchall()
                for result in query_outcome:
                    res += "[RESULT] " + str(result)
            return res

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            db_con.close()

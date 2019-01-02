import mysql.connector
import re

sqlConnector = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="parolaST1"
)

# create the database and tables if not existent
def initDatabase():
    # create a database for the players if not existent 
    cursor = sqlConnector.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS users")

    # create table for storing users data, consisting of:
    # username, salt, passhash, amount of money available
    try:
        usersDbConnector = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="parolaST1",
            database="users"
        )
    except:
        print("database connection failed")

    usersDbCursor = usersDbConnector.cursor()
    usersDbCursor.execute("CREATE TABLE IF NOT EXISTS logins " +
        "(username VARCHAR(255) PRIMARY KEY, passhash VARCHAR(255), " +
        "salt VARCHAR(255), credit BIGINT)")


# insert an user in the database and provides them the initial amount
# of money to start the game.
# return true if the user is inserted successfully and false otherwise
def registerUser(usersDbCursor, username, password):
    validateUsername(usersDbCursor, username)
    # usersDbConnector = mysql.connector.connect(
    #             host="localhost",
    #             user="root",
    #             passwd="parolaST1",
    #             database="users"
    #             )
    #         usersDbCursor = usersDbConnector.cursor()
    #         selectUserStatement = "SELECT * FROM logins WHERE username = %s"
    #         adr = (username, )
    #         usersDbCursor.execute(selectUserStatement, adr)
    #         result = usersDbCursor.fetchall()
    #         if len(result) is 0:
    #             return True

# check if the username contains only letters and  
# digits and its length is between 5 and 255 chars
def validateUsername(username):
    if len(username) < 255 and len(username) > 5:
        if re.match("^[A-Za-z0-9_-]*$", username):
            return True
    
    return False

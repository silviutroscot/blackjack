from enum import Enum
from hashlib import sha256
import mysql.connector
import random
import re
import string

# initial credit for a new registered account
kINITIAL_CREDIT = 100000

# read db password
with  open('passwd.txt') as f:
    dbPassword = f.readline()

sqlConnector = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = dbPassword
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
            host = "localhost",
            user = "root",
            passwd = dbPassword,
            database = "users"
        )
    except:
        print("database connection failed")

    usersDbCursor = usersDbConnector.cursor()
    usersDbCursor.execute("CREATE TABLE IF NOT EXISTS logins " +
        "(username VARCHAR(255) PRIMARY KEY, passhash VARCHAR(255), " +
        "salt VARCHAR(255), credit BIGINT DEFAULT 100000)")



# insert an user in the database if the username is not already there,
#  and provides them the initial amount of money to start the game;
# return true if the user is inserted successfully and false otherwise
def registerUser(username, password):
    if len(password) > 6:
        if validateUsername(username):
            # check if the username is existent in the db
            usersDbConnector = mysql.connector.connect(
                host = "localhost",
                user = "root",
                passwd = dbPassword,
                database="users"
                )
            usersDbCursor = usersDbConnector.cursor()
            selectUserStatement = "SELECT * FROM logins WHERE username = %s"
            adr = (username, )
            usersDbCursor.execute(selectUserStatement, adr)
            result = usersDbCursor.fetchall()
            # if the username is not existent, generate salt and insert
            # the user and the password hash in the login table
            if len(result) is 0:
                salt = generateRandomWord(10)
                saltedPass = salt + password
                passHash = sha256((saltedPass).encode('utf-8')).hexdigest()
                insertLoginEntryStatement = ("INSERT INTO logins (username,"
                    "passhash, salt) VALUES (%s, %s, %s)"
                    )
                values = (username, passHash, salt)
                usersDbCursor.execute(insertLoginEntryStatement, values)
                usersDbConnector.commit()
                return (0, (
                    "Your account was successfuly registered!"
                    "Welcome to the game!"
                    ))
            else:
                return (1, "Your username is already in use")
        else:
            return (2, ("Username contains invalid characters or its length is"
                "not between 5 and 255")
                )
    else:
        return (3, "Password is too short")

def login(username, password):
    # check if the username exists in db
    # retreive its salt if exists
    if validateUsername(username):
        usersDbConnector = mysql.connector.connect(
                host = "localhost",
                user = "root",
                passwd = dbPassword,
                database = "users"
                )
        usersDbCursor = usersDbConnector.cursor()
        selectUserStatement = "SELECT * FROM logins WHERE username = %s"
        adr = (username, )
        usersDbCursor.execute(selectUserStatement, adr)
        result = usersDbCursor.fetchall()
        # if the username is in the db, check if the password matches
        if len(result) > 0:
            salt = result[0][2]
            saltedPass = salt + password
            passHash = sha256((saltedPass).encode('utf-8')).hexdigest()
            confirmCredentialsStatement = '''SELECT * FROM logins WHERE \
            username = %s AND passhash = %s'''
            values = (username, passHash)
            usersDbCursor.execute(confirmCredentialsStatement, values)
            credentialsCheckResponse = usersDbCursor.fetchall()
            # if the credentials are correct return "0" response
            # and the credit available for that player
            if len(credentialsCheckResponse) > 0:
                return (0, credentialsCheckResponse[0][3])
            else:
                return (-1, ("Sorry, the credentials you have provided"
                " are not valid"))
        else:
            return (1, "Sorry, you are not registered")
    else:
        return (2, "This username is not valid")

# if the player wins, the bid paramerter is
# positive; otherwise, the bid is negative
def updateAccountCredit(username, currentCredit, bid):
    newCredit = currentCredit + bid
    # update the credit in the database
    usersDbConnector = mysql.connector.connect(
                host = "localhost",
                user = "root",
                passwd = dbPassword,
                database="users"
                )
    usersDbCursor = usersDbConnector.cursor()
    updateCreditStatement = "UPDATE logins SET credit = %s WHERE username = %s"
    val = (int(newCredit), username)
    usersDbCursor.execute(updateCreditStatement, val)
    # commit the update to the db
    usersDbConnector.commit()
    return (usersDbCursor.rowcount, newCredit)

# check if the username contains only letters and
# digits and its length is between 5 and 255 chars
def validateUsername(username):
    if len(username) < 255 and len(username) > 5:
        if re.match("^[A-Za-z0-9_-]*$", username):
            return True

    return False

# show the player the content of their hand
def showHand(hand):
    print('''Your hand is: {cards}.'''.format(cards=hand))

def generateRandomWord(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))
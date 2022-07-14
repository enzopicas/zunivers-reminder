import sqlite3

#Create the .sqlite database, and create the table
def CreateDB():
    try:
        with open('data/data.sqlite'):pass
    except IOError:
        con = sqlite3.connect('data/data.sqlite')
        cur = con.cursor()
        cur.execute('''CREATE TABLE Users
                    (discord_id text, username text, tag text)''')
        con.commit()
        con.close()

#Add a new user in the db table
def AddUser(id, username, tag):
    status = False
    con = sqlite3.connect('data/data.sqlite')
    cur = con.cursor()

    cur.execute('SELECT * FROM Users WHERE discord_id = '+id)

    if len(cur.fetchall()) == 0:
        cur.execute('''INSERT INTO Users (discord_id,username,tag)
            VALUES (?,?,?)''',(id,username,tag))
        con.commit()
        status = True
    else:
        status = False

    con.close()
    return status

#Delete an existing user from the db table
def DelUser(id):
    status = False
    con = sqlite3.connect('data/data.sqlite')
    cur = con.cursor()

    cur.execute('SELECT * FROM Users WHERE discord_id = '+id)

    if len(cur.fetchall()) == 0:
        status = False
    else:
        cur.execute('''DELETE FROM Users WHERE discord_id = ?''', (id,))
        con.commit()
        status = True

    con.close()
    return status

#Return the list of all suscribed users
def GetUsers():
    con = sqlite3.connect('data/data.sqlite')
    cur = con.cursor()

    cur.execute('SELECT * FROM Users ORDER BY username ASC')
    list_users = cur.fetchall()
    con.close()
    return list_users

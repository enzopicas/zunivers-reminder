import sqlite3

#Create the .sqlite database, and create the table
def CreateDB():
    try:
        with open('data/data.sqlite'):pass
    except IOError:
        con = sqlite3.connect('data/data.sqlite')
        cur = con.cursor()
        cur.execute('''CREATE TABLE Users
                    (discord_id text, username text, tag text, journa_alert integer, as_alert integer, event_alert integer)''')
        con.commit()
        con.close()

#Add a new user in the db table
def AddUser(id, username, tag):
    status = False
    con = sqlite3.connect('data/data.sqlite')
    cur = con.cursor()

    cur.execute('SELECT * FROM Users WHERE discord_id = '+id)

    if len(cur.fetchall()) == 0:
        cur.execute('''INSERT INTO Users (discord_id, username, tag, journa_alert, as_alert, event_alert)
            VALUES (?,?,?,TRUE,TRUE,TRUE)''',(id,username,tag))
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

#Return specific user informations
def GetUser(id):
    con = sqlite3.connect('data/data.sqlite')
    cur = con.cursor()

    cur.execute("SELECT * FROM Users WHERE discord_id = ?", (id,))
    user_infos = cur.fetchall()
    con.close()
    return user_infos

#Change user values
def ChangeUsers(user_id, parameter, new_value):
    con = sqlite3.connect('data/data.sqlite')
    cur = con.cursor()

    cur.execute('UPDATE Users SET ' + str(parameter) + ' = ' + str(new_value) + ' WHERE discord_id = ' + str(user_id))
    con.commit()
    con.close()

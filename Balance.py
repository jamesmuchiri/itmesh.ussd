import variables
import mysql.connector

db = mysql.connector.connect(
        host = "137.184.54.169",
        user = "kaguius",
        passwd = "U6xZfLn9A7Swc%P9",
        database = "finabora",
        autocommit = True,
        port ="3306",
        )
def balance():
    mycursor = db.cursor()
    mycursor.execute('''SELECT primary_phone FROM s_users_primary WHERE primary_phone = (%s)''', (variables.Fetch_Number,))
    checkEmail = mycursor.fetchall()

    if (variables.Fetch_Number,) in checkEmail:
        mycursor = db.cursor()
        mycursor.execute('''SELECT first_name FROM s_users_primary WHERE primary_phone = (%s)''', (variables.Fetch_Number,))
        name = mycursor.fetchone()
        variables.response =("END Dear {}, your effective balance as at $date is KES $loan_balance."

        ).format(name)


    else:
        variables.response =("END Dear customer, we do not seem to have your details on file. Please visit the office to get registered.")
    
    return variables.response
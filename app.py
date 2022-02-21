from flask import Flask, request
import africastalking
import os
from datetime import datetime
import maya
import variables
from maya import MayaInterval
from dateutil.parser import parse
from flask import make_response
import mysql.connector

app = Flask(__name__)


username = "sandbox"
api_key = "0f54c06969af94baa76c50efbcc1daaecb9b75f254d3388c85edfd9d21ff7ad0"
africastalking.initialize(username, api_key)

sms = africastalking.SMS
db = mysql.connector.connect(
        host = "137.184.54.169",
        user = "kaguius",
        passwd = "U6xZfLn9A7Swc%P9",
        database = "finabora",
        autocommit = True,
        port ="3306",
        )

    
@app.route('/', methods=['POST', 'GET'])


def ussd_callback():
    
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", "default")

    
    text = request.values.get("text", "default")

    now = maya.MayaDT.from_datetime(datetime.utcnow())
    kenya_time = now.hour +3
    
    if text == "":  
        variables.Fetch_Number = phone_number.split("+")[1]
        print(variables.Fetch_Number)


        if 5<= kenya_time <12 :
            Good_Morning="Good Morning"
            response =("CON {}" "\nHow may i help you"
                                "\n  -Limit "
                                "\n  -Balance"
                                "\n  -Loan"
                                "\n  -Amount"
            ).format(Good_Morning)

        elif  12 <= kenya_time < 17 :
            Good_Afternoon="Good Afternoon"
            response =("CON {}""\nHow may i help you"
                                "\n  -Limit "
                                "\n  -Balance"
                                "\n  -Loan"
                                "\n  -Amount"
                    ).format(Good_Afternoon)
        else:
            Good_Evening="Good Evening"
            response =("CON {}""\nHow may i help you"
                                "\n  -Limit "
                                "\n  -Balance"
                                "\n  -Loan"
                                "\n  -Amount"
                    ).format(Good_Evening)

        balance()
    def balance():
    
        mycursor = db.cursor()
        mycursor.execute('''SELECT primary_phone FROM s_users_primary WHERE primary_phone = (%s)''', (variables.Fetch_Number,))
        checkEmail = mycursor.fetchall()
        if variables.text =="balance":
            if (variables.Fetch_Number,) in checkEmail:
                mycursor = db.cursor()
                mycursor.execute('''SELECT first_name FROM s_users_primary WHERE primary_phone = (%s)''', (variables.Fetch_Number,))
                name = mycursor.fetchone()
                response =("END Dear {}, your effective balance as at $date is KES $loan_balance."

                ).format(name)


            else:
                response =("END Dear customer, we do not seem to have your details on file. Please visit the office to get registered.")
        else:
            response = "END Invalid input. Try again."  
        
        return response
    
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT"))

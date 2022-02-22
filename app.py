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

    variables.response =""
    variables.Fetch_Number = ""
    variables.text =""
    variables.isregistered = False
    variables.response_loan = False
    variables.namef=""
    
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    variables.text = request.values.get("text", "default")

    now = maya.MayaDT.from_datetime(datetime.utcnow())
    kenya_time = now.hour +3
    
    if variables.text == "": 
        phone_number = request.values.get("phoneNumber", "default")
        variables.Fetch_Number = phone_number.split("+")[1]
        print(variables.Fetch_Number)


        if 5<= kenya_time <12 :
            Good_Morning="Good Morning"
            variables.response =("CON {}" "\nHow may i help you"
                                "\n  -Limit "
                                "\n  -Balance"
                                "\n  -Loan"
                                "\n  -Amount"
            ).format(Good_Morning)

        elif  12 <= kenya_time < 17 :
            Good_Afternoon="Good Afternoon"
            variables.response =("CON {}""\nHow may i help you"
                                "\n  -Limit "
                                "\n  -Balance"
                                "\n  -Loan"
                                "\n  -Amount"
                    ).format(Good_Afternoon)
        else:
            Good_Evening="Good Evening"
            variables.response =("CON {}""\nHow may i help you"
                                "\n  -Limit "
                                "\n  -Balance"
                                "\n  -Loan"
                                "\n  -Amount"
                    ).format(Good_Evening)

        
        phone_number = request.values.get("phoneNumber", "default")
        variables.Fetch_Number = phone_number.split("+")[1]
        print(variables.Fetch_Number)

        mycursor = db.cursor()
        mycursor.execute('''SELECT primary_phone FROM s_users_primary WHERE primary_phone = (%s)''', (variables.Fetch_Number,))
        checkNumber = mycursor.fetchall()
        print(checkNumber)

        if checkNumber is None:
            variables.isregistered=False    
           
        else:
            variables.isregistered=True
            mycursor = db.cursor()
            mycursor.execute('''SELECT first_name FROM s_users_primary WHERE primary_phone = (%s)''', (variables.Fetch_Number,))
            name = mycursor.fetchone()
            variables.namef = name[0]
                    
        

    elif variables.text.lower().strip() =="balance":
        
        if variables.isregistered==True:
            variables.response =("END Dear {}, your effective balance as at $date is KES $loan_balance."

            ).format(variables.namef)

    elif variables.text.lower().strip() =="loan":

        mycursor = db.cursor()
        mycursor.execute('''SELECT loan_limit FROM s_users_primary WHERE primary_phone = (%s)''', (variables.Fetch_Number,))
        loan_limit = mycursor.fetchone()

        variables.response_loan = False

        if variables.isregistered==True:
            variables.response =("CON Dear {}, you qualify for a new loan. Please enter a loan value between 500 and {}"

            ).format(variables.namef,loan_limit[0])
            
            variables.response_loan = True

            if variables.response_loan == True:
                text_array = variables.text.split("*")
                resent_text = text_array[len(text_array) - 1]
                loan = loan_limit[0]

                print (resent_text)
                print (int(loan))

                if int(float(resent_text)) > int(float(loan)) or int(float(resent_text)) < 500:

                    variables.response =("CON Dear {}, the loan value entered is invalid, please enter a value between ksh.500 and ksh.{}"
                    ).format(variables.namef,loan_limit[0])
                

        

    else:
        if variables.isregistered==False:
            variables.response =("END Dear customer, we do not seem to have your details on file. Please visit the office to get registered.")
           
        else:
            variables.response = ( "END Dear {}, you sent the wrong keyword/amount, please send the words Loan to $short_code." 
            ).format(variables.namef)
            
    
    return variables.response
    
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT"))

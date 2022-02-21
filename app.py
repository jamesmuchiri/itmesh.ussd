from flask import Flask, request
import africastalking
import os
from datetime import datetime
import maya
import variables
from maya import MayaInterval
from dateutil.parser import parse
from flask import make_response
import Balance
app = Flask(__name__)


username = "sandbox"
api_key = "0f54c06969af94baa76c50efbcc1daaecb9b75f254d3388c85edfd9d21ff7ad0"
africastalking.initialize(username, api_key)

sms = africastalking.SMS


    
@app.route('/', methods=['POST', 'GET'])


def ussd_callback():
    
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber")
    text = request.values.get("text", "default")

    now = maya.MayaDT.from_datetime(datetime.utcnow())
    kenya_time = now.hour +3
    
    if text == "":  
        
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

    elif variables.text =="Balance":
        return Balance.balance()

    else:
        variables.response = "END Invalid input. Try again."

    return variables.response
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT"))

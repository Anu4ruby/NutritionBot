# doing necessary imports
from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import requests
import pymongo
import json
import os
from saveConversation import Conversations
from DataRequests import MakeApiRequests
from sendEmail import EMailClient
from pymongo import MongoClient
import certifi

app = Flask(__name__)  # initialising the flask app with the name 'app'

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')
# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# processing the request from dialogflow
def processRequest(req):
    # dbConn = pymongo.MongoClient("mongodb://localhost:27017/")  # opening a connection to Mongo
    log = Conversations.Log()
    sessionID = req.get('responseId')
    result = req.get("queryResult")
    intent = result.get("intent").get('displayName')
    query_text = result.get("queryText")
    parameters = result.get("parameters")
    cust_name = parameters.get("name")
    cust_contact = parameters.get("cust_contact")
    cust_email = parameters.get("email")
    db = configureDataBase()

    if intent == 'calorie_information':
        food = parameters.get("food")
        fulfillmentText = makeAPIRequest(food)
        if fulfillmentText:
            nutrients = fulfillmentText.get('nutrients')
            webhookresponse = "***Nutrition Report*** \n\n" + " Name :" + str(fulfillmentText.get('label')) + \
                              "\n" + "Fat in gm : " + str(nutrients.get('FAT')) + "\n" \
                              " Protein in gms : " + str(nutrients.get('PROCNT')) + "\n" \
                              " Carbohydrates in gms : " + str(nutrients.get('CHOCDF')) + "\n" \
                              + " Calories : " + str(nutrients.get('ENERC_KCAL')) + "\n" \
                              + " Fibre : " + str(nutrients.get('FIBTG')) + "\n" \
                              + "\n\n*******END********* \n "
        else:
            webhookresponse = "You have either entered incorrect food item or you have exceeded the maximum api calls for this app. Please upgrade your plan in Rapid API to keep using this feature"

        print(webhookresponse)
        log.saveConversations(sessionID, food, webhookresponse, intent, db)
        #log.saveCases("calorie", fulfillmentText, db)
        return {

            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            webhookresponse
                        ]

                    }
                },
                {
                    "text": {
                        "text": [
                            "What else can I help you with?"

                        ]

                    }
                }
            ]
        }
    elif intent == "Welcome" or intent == "Default Fallback Intent" or intent == "no_email" or intent == "endConversation" or intent == "Main-Menu" or intent == "Default Welcome Intent":
        fulfillmentText = result.get("fulfillmentText")
        log.saveConversations(sessionID, query_text, fulfillmentText, intent, db)
    elif intent == "send_report_to_email":
        print("inside send_report_to_email")
        fulfillmentText = result.get("fulfillmentText")
        val = log.getcasesForEmail("calorie_information", "", db)
        print("database value===>", val)
        log.saveConversations(sessionID, "Sure send email", fulfillmentText, intent, db)
        prepareEmail([cust_name, cust_contact, cust_email, val])
    else:
        return {
            "fulfillmentText": "Lets try different approach. What's your question again?",
        }


def configureDataBase():
    client = MongoClient("mongodb+srv://anu:1234@cluster0.cdxqu38.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
    return client.get_database('NutritionDB')


def makeAPIRequest(query):
    api = MakeApiRequests.Api()
    return api.makeApiRequestForFood(query)

def prepareEmail(contact_list):
    print("prepareEmail",contact_list )
    mailclient = EMailClient.GMailClient()
    mailclient.sendEmail(contact_list)


if __name__ == '__main__':
    port = int(os.getenv('PORT',5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
'''if __name__ == "__main__":
    app.run(port=5000, debug=True)''' # running the app on the local machine on port 8000

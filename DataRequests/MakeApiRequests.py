import requests
import json
class Api:
    def __init__(self):
        pass

    def makeApiRequestForFood(self, food):
        print("inside makeApiRequestForFood")
        url = "https://dietagram.p.rapidapi.com/apiFood.php"
        querystring = {"name": food}
        headers = {
            'x-rapidapi-host': "dietagram.p.rapidapi.com",
            'x-rapidapi-key': "4abd423fdemsh4381311a7823b4dp116d02jsnd3cb2506b5a7"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        #print(response.text)
        js = json.loads(response.text)
        result = js.get('dishes')[0]
        print("******", result)
        return result

import requests
import json
class Api:
    def __init__(self):
        pass

    def makeApiRequestForFood(self, food):
        print("inside makeApiRequestForFood")
        url = "https://edamam-food-and-grocery-database.p.rapidapi.com/parser"
        querystring = {"ingr": food}
        headers = {
            'x-rapidapi-host': "edamam-food-and-grocery-database.p.rapidapi.com",
            'x-rapidapi-key': "4abd423fdemsh4381311a7823b4dp116d02jsnd3cb2506b5a7"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        js = json.loads(response.text)
        print("******** API output", js)
        try:
            parsed = js.get('parsed')[0]
            result = parsed['food']
            print("parsed food items", result)
        except Exception as e:
            print(e)
            try:
                hints = js.get('hints')[0]
                print("hints", hints['food'])
                result = hints['food']
            except Exception as e:
                print(e)
                result = ''

        return result


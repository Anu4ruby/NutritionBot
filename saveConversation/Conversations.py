from datetime import datetime
class Log:
    def __init__(self):
        pass

    def saveConversations(self, sessionID, usermessage,botmessage,intent,dbConn):

        self.now = datetime.now()
        self.date = self.now.date()
        self.current_time = self.now.strftime("%H:%M:%S")
        mydict = {"sessionID":sessionID,"User Intent" : intent ,"User": usermessage, "Bot": botmessage, "Date": str(self.date) + "/" + str(self.current_time)}
        records = dbConn.chat_records
        records.insert_one(mydict)


    def getcasesForEmail(self, search, botmessage, dbConn):
        print("search", search)
        print("dbConn",dbConn)
        records = dbConn.chat_records
        data = records.find_one({'User Intent': search})
        print("data", data)
        return data


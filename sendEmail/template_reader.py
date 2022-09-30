class TemplateReader:
    def __init__(self):
        pass

    def read_course_template(self, course_name):
        try:
            if (course_name == 'simple'):
                email_file = open("sendEmail/simple.html", "r")
                email_message = email_file.read()
            return email_message
        except Exception as e:
            #print("Exception====>>>")
            print('The exception is '+str(e))

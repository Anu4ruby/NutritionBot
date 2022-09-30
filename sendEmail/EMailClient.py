import os
import smtplib
import imghdr
from email.message import EmailMessage
from sendEmail import template_reader
from bs4 import BeautifulSoup
import json
import re

class GMailClient:
    def sendEmail(self,contacts):
        #EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
        #EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
        EMAIL_ADDRESS = 'xxxx'
        EMAIL_PASSWORD = 'xxx'


        msg = EmailMessage()
        msg['Subject'] = 'Detailed Nutrition Report!'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = contacts[2]
        values = contacts[3]

        msg.set_content("Hello Mr. {} Here is your nutrition Report PFA".format(contacts[0]))
        template = template_reader.TemplateReader()
        email_message = template.read_course_template("simple")

        name = str(values.get("name"))
        fat = str(values.get("fat"))
        protein = str(values.get("protein"))
        carbon = str(values.get("carbon"))
        caloric = str(values.get("caloric"))

        #.format(code1=code1, code2=code2, code3=code3, code4=code4, code5=code5

        '''msg.add_alternative(email_message.format(country_name=country_name1, total=total1, new=new1, active=active1, critical=critical1,
                                       recovered=recovered1,subtype='html'))'''



        msg.add_alternative(email_message.format(name=name, fat=fat, protein=protein, carbon=carbon,
                                    caloric=caloric), subtype='html')


        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("email sent")
    def __init__(self):
        pass
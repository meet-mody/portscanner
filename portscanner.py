# -*- coding: utf-8 -*-
import os
import socket
import sys
from datetime import datetime, timedelta
from botocore.exceptions import ClientError
import boto3


# Add multiple IP's or hostname seperated by comma
target = ["www.google.com"]
socket.setdefaulttimeout(0.10)
now = datetime.now()
last_week = now - timedelta(7)
sub7_date = last_week.strftime("%m-%d-%Y")
today_date = now.strftime("%m-%d-%Y")
fileold = "PortScan - " + sub7_date + ".txt"

#Deletes scan results older than 7 days if it exists    
if os.path.exists(fileold):
    os.remove(fileold)
    print("Deleted file from: ", sub7_date)

#Creates new file with scan results    
filenew = "PortScan - " + today_date + ".txt"
f = open(filenew, "a")
f.write("\r<<-PORT SCAN: " + today_date + "->>\r")
f.write("\n")

def portscan(target):
    
    for hname in target:
        t_IP = socket.gethostbyname(hname)              #Converts hostnames to IPs
        f.write(hname + " (" + t_IP +")")
        f.write(":\n")
        print ("\nStarting scan for: {} ({})\n".format(t_IP, hname))

        try:
            f.write("\n")
            for port in range(1, 100):                  #Range of ports 1-100, can go upto 65536.
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                con = s.connect_ex((t_IP, port))
                if con == 0:
                    print(port, ' : OPEN')
                    f.write(str(port) + ": OPEN\n")
                s.close()
            f.write("\n")
        except KeyboardInterrupt:
            print("You pressed Ctrl+C")
            sys.exit()
            
def send():
    SENDER = "notifications@gmail.com"  #Replace with email id of sender
    id = "Your API id"                  #Amazon SES API ID
    key = "Your API key"                #Amazon SES API key

    SUBJECT = "PortScan Report For: " + today_date
    
    r = open(filenew, 'r')
    x = r.read()
    r.close()
    x = x.replace('\n', '<br>')
    x = x.replace('<<-', '<h1>')
    x = x.replace('->>', '</h1>')
            
    BODY_HTML = """<html>
    <head></head>
    <body>
        <p>""" + str(x) + """</p>
    </body>
    </html>
            """
            
    client = boto3.client('ses', region_name="us-west-2", aws_access_key_id=id, aws_secret_access_key=key)

    # Try to send the email.
    try:
    #Provide the contents of the email.
        response = client.send_email(
        Destination={
            'ToAddresses': ['xyz@hotmail.com', 'abc@gmail.com'],    #Receivers email address
        },
        Message={
            'Body': {
                'Html': {
                    #'Charset': CHARSET,
                    'Data': BODY_HTML,
                },
                #'Text': {
                #    'Charset': CHARSET,
                #    'Data': BODY_TEXT,
                #},
            },
            'Subject': {
                #'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=SENDER,
    )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! \nMessage ID:"),
        print(response['MessageId'])

if __name__ == "__main__":
    portscan(target)
    f.close()
    print("\n")
    send()

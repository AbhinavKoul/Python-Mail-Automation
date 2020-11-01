import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from jinja2 import Template
import pandas as pd
import os

html = """\
<html>
  <body>
    <br> <img src="cid:image1" width="500" height="600"> <br>
    <p>Hi,{{ name }}<br>
       How are you?<br>
       <a href="https://www.teamstardust.org/">Join Team Stardust</a> 
       for exiting times
    </p>
  </body>
</html>
"""


root = "./Data/Test/"
data = pd.read_csv(os.path.join(root,"Testing.csv"))
data = data[["Email Address","usn","Name"]]
data["Mail Status"] = "NULL" 
total = data["Email Address"].count()


sender_email = "stardust.recruitment@gmail.com"
# receiver_email = "abhinav2scientist@gmail.com"
password = "Automation@1234"

message = MIMEMultipart("alternative")
message["Subject"] = "Orientation Invite TEST - SCRIPT"
message["From"] = sender_email
# message["To"] = receiver_email
# nam = "Abhinav Koul"

template = Template(html)

# # Create the plain-text and HTML version of your message
# text = """\
# Hi,
# How are you?"""

# This example assumes the image is in the current directory
img_path = "./Images/img.jpg"
fp = open(img_path, 'rb')
msgImage = MIMEImage(fp.read())
fp.close()

# Define the image's ID as referenced above
msgImage.add_header('Content-ID', '<image1>')
message.attach(msgImage)



# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    send_count = 0

    for index,row in data.iterrows():

        if(row["Mail Status"] == "SEND"):
            continue
        else:
            receiver_email = row["Email Address"]
            Name = row["Name"]

            message["To"] = receiver_email

            # Turn these into plain/html MIMEText objects
            # part1 = MIMEText(text, "plain")
            part2 = MIMEText(template.render(name = Name), "html")

                    
            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            # message.attach(part1)
            message.attach(part2)



            try:
                server.sendmail(
                    sender_email, receiver_email, message.as_string()
                )
                
                row["Mail Status"] = "SEND"
                send_count +=1
                print("Mail Sent ==> ("+str(send_count)+"/"+str(total)+")")
            except:
                row["Mail Status"] = "ERROR!!!"
                print("Mail Sent ==> ("+str(send_count)+"/"+str(total)+")")

data.to_csv(os.path.join(root,"SEND_MAILS.csv"))
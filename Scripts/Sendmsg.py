import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from jinja2 import Template
import pandas as pd
import os

html = """\
<html>
	<head> 
		<title> Orientation </title>
	</head>
	<body style="background-color:#ede8e8;padding:10px;font-family:'Arial'">
		<div style="padding:50px;">
			<p> Hi {{ name }}, </p> <br>

			<p>
				Thank you for booking your slot for the Orientation session of the only Student Satellite Team of RIT- S.T.A.R.D.U.S.T!<br><br>
				We can’t wait to share similar thoughts with you and to present to you all that we have achieved in the past year. <br><br> 
				We at S.T.A.R.D.U.S.T believe in free flow of knowledge in the domains of Space Technology and hence you should expect it to be a very interactive session :)<br>
				The session starts at <b style="color:#3792cb;"><i>7 pm</b></i> on <b style="color:#3792cb;"><i>6th November 2020(Friday)</b></i>.<br> 
				You can read more about our team and the various Subsystems centered around our mission in the brochure attached below:
			</p>
			<br>
			<img src="cid:image1" alt="brochure" style="margin-left:auto;
			margin-right:auto;
			display:block;
			height:600px;
			width:450px;"> 
		<br>
		<br>
		<div style="text-align:center;">
		<a href={{ meet_link }} class="button" style="background-color: #9966ff;
			  border: none;
			  color: white;
			  padding: 20px 25px;
			  text-decoration:none;
			  text-align: center;
			  display: inline-block;
			  font-size: 20px;
			  margin: 4px 2px;
			  border-radius:12px;
			cursor: pointer;"> Click to join the meeting </a><br>
		<p><i> Alternatively, click on this link to join:<br><a href={{ meet_link }}> Join Meeting</i> </a> 
		
		</div>
		<br>
		We request you to make it on time so that we can confirm all systems before Launch<br>
			<p style="text-align:center;color:#3792cb">Lift Off!!!!!!!<br> at 7 pm I.S.T</p><br>

		<p style="text-align:center;"><br>If you need any clarification you can get in touch with us via this email and we will try to respond to it as soon as possible! <br> <br><br>		

		Hope to see you soon {{ name }}! <br><br>

		All the best,
		The Stardust Recruiting Team

		<br>
		<br>
		<img src="cid:logo" style="height:90px;width:90px;">

		<br>
		Want to sneak a backstage peek? Follow Life at Stardust
		on <a href=https://www.linkedin.com/company/rit-stardust><i>LinkedIn</i></a>, <a href="https://www.instagram.com/rit_stardust"><i>Instagram</i></a>, and <a href ="https://www.youtube.com/channel/UC61xGOFapcIeAWdQvtCffJw"> <i>Youtube</i></a>

		</div>
	</body>
</html>
	

"""


meeting_link = "https://meet.google.com/uja-ofrp-chj"

root = "./Data/Test/"
data = pd.read_csv(os.path.join(root,"Testing.csv"))
data = data[["Email Address","usn","Name"]]
data["Mail Status"] = "NULL" 
total = data["Email Address"].count()


sender_email = ""
password = ""

message = MIMEMultipart("alternative")
message["Subject"] = "Orientation Invite TEST - SCRIPT"
message["From"] = sender_email

template = Template(html)


# This example assumes the image is in the current directory
img_path = "./Images/img.jpg"
fp = open(img_path, 'rb')
msgImage = MIMEImage(fp.read())
fp.close()

# Define the image's ID as referenced above
msgImage.add_header('Content-ID', '<image1>')
message.attach(msgImage)

# This example assumes the image is in the current directory
img_path = "./Images/stardust-logo.png"
fp = open(img_path, 'rb')
msgImage = MIMEImage(fp.read())
fp.close()

# Define the image's ID as referenced above
msgImage.add_header('Content-ID', '<logo>')
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
            part2 = MIMEText(template.render(name = Name,meet_link = meeting_link), "html")

                    
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
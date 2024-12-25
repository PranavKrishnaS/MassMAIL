import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time, state, csv, os


# "If something works, don't screw 🪛 with it" - Me



def authEmail(sender, pwd, number):
    try:
        email_from = sender
        smtp_port = 587                 
        smtp_server = "smtp.gmail.com"
        subject = 'MassMAIL Authorization Code'

        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls()
        TIE_server.login(email_from, pwd) # Logging In
        number = str(number)
        
        with open('./assets/emailfriendly.html', 'r') as template:
          contents = str(template.read())
        
        
        temp = contents.split('[OTP]')
        content = temp[0] + number + temp[1]
        

        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = sender
        msg['Subject'] = subject
        msg.attach(MIMEText(content, 'html'))

        text = msg.as_string()
        TIE_server.sendmail(email_from, sender, text)
        TIE_server.quit()
        
        return 'SUCCESS'
    except Exception:
        return 'FAILED'

def sendmail(recipients: list, subject:str, content:str, attachmentList:list) -> str:
	smtp_port = 587                 # Standard secure SMTP port
	smtp_server = "smtp.gmail.com"  # Google SMTP Server
	userName = state.userData['sender'] # Set sender address
	
	# Find authorization code
	with open('./data/users.csv') as users:
		csvreader = csv.reader(users)
		header = next(csvreader)
		
		for row in csvreader:
			if str(row[1]).lower() == userName.lower():
				email_from = str(row[3])
				pswd = str(row[4])
				
	
	start = time.time()
	yield 'Connecting to server'
	
	TIE_server = smtplib.SMTP(smtp_server, smtp_port)
	TIE_server.starttls()
	TIE_server.login(email_from, pswd)
	connectingTime = time.time()
	yield 'Succesfully connected to server'

	body = content
	
	# Loading common info : Subject, Sender address, attachments and content.
	# Only recipient address varies through iterations.

	msg = MIMEMultipart()
	msg['From'] = email_from
	msg['Subject'] = subject
	msg.attach(MIMEText(body, 'plain'))


	for each in attachmentList:
		attachment= open(each, 'rb')
		
        # Encode as base 64
		attachment_package = MIMEBase('application', 'octet-stream')
		attachment_package.set_payload((attachment).read())
		encoders.encode_base64(attachment_package)
		attachment_package.add_header('Content-Disposition', "attachment; filename= " + os.path.basename(each))
		msg.attach(attachment_package)

		# Cast as string
	text = msg.as_string()
	
	mailtime = time.time()
	for person in recipients:
		
        # Send emails to "person" as list is iterated
		yield f"Sending email to: {person}..."
		
		TIE_server.sendmail(email_from, person, text)
		yield f"Email sent to: {person}"
		
		
	mailend = time.time()
	TIE_server.quit()
	yield f'Connection and Setup Time:  {mailtime-start} seconds'
	yield f'Sent {len(recipients)} mails in {mailend-mailtime} seconds. '
	yield f'Total Time : {mailend-start} seconds'


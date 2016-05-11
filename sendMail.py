import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

user = 'gaoprisor@gmail.com'
password = '@andrei93'

recipient = 'homecontrollerpy@gmail.com'
sender = 'gaoprisor@gmail.com'
msg = MIMEMultipart()
msg['From'] = sender
msg['To'] = recipient
msg['Subject'] = 'Command'
body = 'My Command'
msg.attach(MIMEText(body, 'plain'))
text = msg.as_string()

session = smtplib.SMTP('smtp.googlemail.com', 587)
session.ehlo()
session.starttls()
session.login(user,password)
session.sendmail(sender,sender,text)
session.quit()
print "Mail sent!"

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

user = 'homecontrollerpy@gmail.com'
password = 'py&raspberry'

recipient = 'gaoprisor@gmail.com'
sender = user
msg = MIMEMultipart()
msg['From'] = sender
msg['To'] = recipient
msg['Subject'] = '27.32'
body = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>
       Here is the content
    </p>
  </body>
</html>
"""

msg.attach(MIMEText(body, 'html'))
text = msg.as_string()

session = smtplib.SMTP('smtp.googlemail.com', 587)
session.ehlo()
session.starttls()
session.login(user,password)
session.sendmail(sender,recipient,text)
session.quit()
print "Mail sent!"

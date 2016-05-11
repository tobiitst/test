import imaplib
import time

session = imaplib.IMAP4_SSL('imap.gmail.com',993)

username = 'homecontrollerpy@gmail.com'
password = 'py&raspberry'

session.login(username,password)

session.select('Inbox')

#pentru stergerea tuturor email-urilor anterioare
type, emails = session.search(None, 'ALL')
for email in emails[0].split():
   session.store(email, '+FLAGS', '\\Deleted')
session.expunge()


while 1:
    time.sleep(3)
    session.select('Inbox')
    stat, messages = session.search(None, '(UNSEEN)')
    if messages[0] != '':
        for message in messages[0].split(' '):
            print 'processing:', message
            type, details = session.fetch(message, '(BODY[HEADER.FIELDS (SUBJECT FROM)])') 
            type, command = session.fetch(message, '(BODY[TEXT])')
            type, data = session.store(message,'+FLAGS','\\Seen')
            variable = command[0][1].split()
            realcommand = variable[len(variable)-2]
            realcommand = realcommand[10:-4]
            print "THE FINAL COMMAND IS:", realcommand
            detailList = details[0][1].split(' ')
            fromWho = detailList[len(detailList)-1]
            subject = detailList[1]
            subject = subject[:-7]
            fromWho = fromWho[:-4]
            fromWho = fromWho[1:-1]
 
            print "SUBJECT:", subject
            print "SENDER:" , fromWho
    else:
        print messages


#for com in command:
#    print com

session.close()
session.logout()

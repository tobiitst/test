import threading
import pexpect
import time
import smtplib
import imaplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

threadRunning = True
command = ' '

class KeyFob (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = "KeyFob - Thread"
        self.gatt = pexpect.spawn('gatttool -I')
    
    def run(self):
        threadLock.acquire()
        print "Starting " + self.name
        self.gatt.sendline('connect 84:DD:20:C5:7F:26')
        self.gatt.expect('Connection successful')
        threadLock.release()
        while threadRunning:
            time.sleep(1)
            if(command == "startAlert"): 
                self.turnOnAlert()
            elif(command == "stopAlert"):
                self.turnOffAlert()
         
    def turnOnAlert(self):
        self.gatt.sendline('char-write-cmd 0x0028 01:00')

    def turnOffAlert(self):
        self.gatt.sendline('char-write-cmd 0x0028 00:00')


class SensorTag (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = "SensorTag"
        self.gatt = pexpect.spawn('gatttool -I')
        self.temperature = 0.0

    def run(self):
        threadLock.acquire()
        print "Starting " + self.name
        self.gatt.sendline('connect BC:6A:29:AC:32:9C')
        time.sleep(2)
        self.gatt.expect('Connection successful')
        self.gatt.sendline('char-write-cmd 0x29 01')
        self.gatt.expect('\[LE\]>')
        threadLock.release()
        while threadRunning:
            self.readTemperature()

    def readTemperature(self):
        while threadRunning:
            time.sleep(1)
            self.gatt.sendline('char-read-hnd 0x25')
            self.gatt.expect('descriptor: .*')
            rawTemperature = self.gatt.after.split()
            temp = self.fromHexToFloat(rawTemperature)
            self.temperature = self.calcTmpTarget(temp[0],temp[1])
            
    def fromHexToFloat(self,rawTemp):
        ambTemp = rawTemp[4] + rawTemp[3]
        objTemp = rawTemp[2] + rawTemp[1]
        ambT = float.fromhex(ambTemp)
        objT = float.fromhex(objTemp)

        if ambT > float.fromhex('7FFF'):
            ambT = -(float.fromhex('FFFF') - ambT)
        elif objT > float.fromhex('7FFF'):
            objT = -(float.fromhex('FFFF') - objT)

        output = [ambT,objT]

        return output

    def calcTmpLocal(self,rawT):
        m_tmpAmb = rawT/128.0
        return m_tmpAmb

    def calcTmpTarget(self,ambT, objT):
        m_tmpAmb = self.calcTmpLocal(ambT)
        Vobj2 = objT * 0.00000015625
        Tdie2 = m_tmpAmb + 273.15
        S0 = 6.4E-14
        a1 = 1.75E-3
        a2 = -1.678E-5
        b0 = -2.94E-5
        b1 = -5.7E-7
        b2 = 4.63E-9
        c2 = 13.4
        Tref = 298.15
        S = S0*(1+a1*(Tdie2 - Tref)+a2*pow((Tdie2 - Tref),2))
        Vos = b0 + b1*(Tdie2 - Tref) + b2*pow((Tdie2 - Tref),2)
        fObj = (Vobj2 - Vos) + c2*pow((Vobj2 - Vos),2)
        tObj = pow(pow(Tdie2,4) + (fObj/S),.25)
        tObj = (tObj - 273.15)
        
        return tObj



class CommandReader (threading.Thread):
    def __init__(self, threadID, username, password):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = "CommandReader - Thread"
        self.username = username
        self.password = password
        self.session = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        self.expectedAddress = 'gaoprisor@gmail.com'
        self.expectedSubject = 'Command'
        self.command = ' '

    def run(self):
        print "Starting " + self.name
        self.session.login(self.username, self.password)
        self.session.select('Inbox')
        self.deleteEmails()
        self.readEmails()
        self.deleteEmails()
        self.session.close()
        self.session.logout()

    def deleteEmails(self):
        state, emails = self.session.search(None, 'ALL')
        for email in emails[0].split():
            self.session.store(email, '+FLAGS', '\\Deleted')
        self.session.expunge()

    def readEmails(self):
        while threadRunning:
            self.session.select('Inbox')
            state, messages = self.session.search(None, '(UNSEEN)')
            if messages[0] != '':
                threadLock.acquire()
                print "Processing new command..."
                for message in messages[0].split(' '):
                    state, details = self.session.fetch(message, '(BODY[HEADER.FIELDS (SUBJEC FROM)])')
                    sentBy, subject = self.extractDetails(details)
                    print "Sent by:", sentBy
                    if self.expectedAddress in sentBy:
                        state, email = self.session.fetch(message, '(BODY[TEXT])')
                        state, data = self.session.store(message, '+FLAGS', '\\Seen')
			print email
                        self.command = self.extractCommand(email)
                        print "Commanda: ", self.command
                        
                    else:
                        print "Details did not match!"
                threadLock.release()
    
    def extractDetails(self,details):
        detailsList = details[0][1].split(' ')
        fromWho = detailsList[len(detailsList)-1]
        subject = detailsList[1]
        return (fromWho, subject)
    
    def extractCommand(self, email):
        emailList = email[0][1].split()
        realCommand = emailList[len(emailList)-2]
	if "startAlert" in realCommand:
		command = "startAlert"
	elif "stopAlert" in realCommand:
		command = "stopAlert"
	elif "sendTemperature" in realCommand:
		command = "sendTemperature"
	else :
		command = ""
        return command


class EmailSender:
    def __init__(self, username, password, recipient):
        self.name = "EmailSender"
        self.username = username
        self.password = password
        self.recipient = recipient
        self.session = smtplib.SMTP('smtp.googlemail.com', 587)
        self.session.ehlo()
        self.session.starttls()
        self.session.login(username,password)
        self.message = MIMEMultipart()
        self.message['From'] = username
        self.message['To'] = recipient

    def sendMail(self, response):
        self.message['Subject'] =  response
        text = self.message.as_string()
        self.session.sendmail(self.username, self.recipient, text)

    def endSession(self):
        self.session.quit()
        


def disconnectModules():
    disconnect = pexpect.spawn('sudo bluetoothctl')
    disconnect.sendline('disconnect BC:6A:29:AC:32:9C')
    disconnect.sendline('disconnect 84:DD:20:C5:7F:26')
    time.sleep(3)
    disconnect.sendline('exit')



        
if __name__ == '__main__':

    #disconnect devices if they are connected
    disconnectModules()

    #create a thread lock to sincronize the threads
    threadLock = threading.Lock()
    threads = []

    # Create new threads
    thread1 = KeyFob(1)
    thread2 = SensorTag(2)
    thread3 = CommandReader(3, 'homecontrollerpy@gmail.com', 'py&raspberry')
    sendMailObject = EmailSender('homecontrollerpy@gmail.com', 'py&raspberry', 'gaoprisor@gmail.com')

    # Start new Threads
    thread1.start()
    thread2.start()
    thread3.start()

    # Add threads to thread list
    threads.append(thread1)
    threads.append(thread2)
    threads.append(thread3)

    while(threadRunning):
        time.sleep(1)
        command = thread3.command
        if(command == 'sendTemperature'):
            threadLock.acquire()
            print "Se trimite raspunsul"
            response = str(thread2.temperature)
            sendMailObject.sendMail(response)
            print "Response sent!"
            thread3.command = ' '
            threadLock.release()
        print "Temperatura este:", thread2.temperature

    # Wait for all threads to complete
    for t in threads:
        t.join()
    print "Exiting Main Thread"

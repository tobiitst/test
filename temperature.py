import pexpect
import time



#transform hexadecimal to float
def fromHexToFloat(rawTemp):
    ambTemp = rawTemp[4] + rawTemp[3]
    objTemp = rawTemp[2] + rawTemp[1]
    ambT = float.fromhex(ambTemp)
    objT = float.fromhex(objTemp)

    if ambT > float.fromhex('7FFF'):
           ambT = -(float.fromhex('FFFF') - ambT)
           pass
    
    if objT > float.fromhex('7FFF'):
           objT = -(float.fromhex('FFFF') - objT)
           pass

    output = [ambT,objT]
    
    return output

    

#calculate local temperature
def calcTmpLocal(rawT):
    m_tmpAmb = rawT/128.0

    return m_tmpAmb



#calculate target temperature
def calcTmpTarget(ambT, objT):
    m_tmpAmb = calcTmpLocal(ambT)
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



sensorTag = pexpect.spawn('gatttool -I')
sensorTag.expect('\[LE\].*>')
sensorTag.sendline('connect BC:6A:29:AC:32:9C')

time.sleep(5)
sensorTag.expect('Connection successful')

print 'SensorTag connected...'

sensorTag.sendline('char-write-cmd 0x29 01')
sensorTag.expect('\[LE\]>')

index = 0
averageTemp = 0

while True:
    time.sleep(1)
    sensorTag.sendline('char-read-hnd 0x25')
    sensorTag.expect('descriptor: .*')
    rawTemperature = sensorTag.after.split()
    temp = fromHexToFloat(rawTemperature)
    temperature = calcTmpTarget(temp[0],temp[1])
    
    if index < 10:
       index=index+1
       averageTemp+=temperature;
    else:
        averageTemp/=10
        index = 0
        file=open('temperature','w')
        file.write(str(averageTemp))
        file.close()

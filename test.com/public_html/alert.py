import pexpect
import time

gatt = pexpect.spawn('gatttool -I')
gatt.sendline('connect 84:DD:20:C5:7F:26')
gatt.expect('Connection successful')

gatt.sendline('char-write-cmd 0x0028 01:00')

time.sleep(5)

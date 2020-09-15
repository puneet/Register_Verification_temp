import os
import time
 
write_path = "/tmp/pipe.in"
read_path = "/tmp/pipe.out"
 
wf = os.open(write_path, os.O_SYNC | os.O_CREAT | os.O_RDWR)
rf = None
 
for i in range(1):
    msg = b'\x0f\x0c\x00\x00\x00\x01\x00\xfd\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00,\x00\x00\x00\x00\x00\x00\x00'
    len_send = os.write(wf, str(msg))
    print ("sent msg: %s", msg)

 
    if rf is None:
        rf = os.open(read_path, os.O_RDONLY)
 
    s = os.read(rf, 1024)
    if len(s) == 0:
        break
    print ("received msg: %s", s)
 
    time.sleep(1)
 
os.write(wf, 'exit')
 
os.close(rf)
os.close(wf)
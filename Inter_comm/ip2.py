# import os
# import sys

# path = "/tmp/my_program.fifo"
# fifo = open(path, "r")
# for line in fifo:
# 	line = int(float(line))
# 	print("Received:")
# 	print(line)
# fifo.close()
import os, time
 
read_path = "/tmp/pipe.in"
write_path = "/tmp/pipe.out"
 
if os.path.exists(read_path):
    os.remove(read_path)
if os.path.exists(write_path):
    os.remove(write_path)
 
os.mkfifo(write_path)
os.mkfifo(read_path)
 
rf = os.open(read_path, os.O_RDONLY)
wf = os.open(write_path, os.O_SYNC | os.O_CREAT | os.O_RDWR)
 
while True:
	s = os.read(rf, 32)
	print ("received msg: ",int(float(s)))
	
# if s == "exit":
# 	os.close(rf)
# 	os.close(wf)

 

import os, time
 
read_path = "/tmp/pipe.in"

if os.path.exists(read_path):
    os.remove(read_path)
 
os.mkfifo(read_path)
 
# rf = os.open(read_path, os.O_RDONLY)
rf = os.open(read_path, os.O_SYNC | os.O_CREAT | os.O_RDWR)
 
while True:
	s = os.read(rf, 32)
	s = str(s,'latin-1')
	s = s.split(',')
	addr = int(s[0],16)
	data = int(s[1],16)
	print (f"Address:{addr} and Data:{data}")
	print(" ",s)
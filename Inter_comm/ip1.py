import os

path = "/tmp/my_program.fifo"
# os.mkfifo(path)

fifo = open(path,'w')
val = "125"
os.write(fifo,val)
os.close()
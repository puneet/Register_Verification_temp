import os

path = "/tmp/my_program.fifo"
# os.mkfifo(path)

fifo = open(path, "w")
val = "125"
fifo.write(val)
fifo.close()
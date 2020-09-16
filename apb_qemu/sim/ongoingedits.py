from struct import *
import time
import os
class Aval_mm:

	WRITE=0
	READ=1
	IDLE=2
	DONE=3
	WRITE_RSP=4
	READ_RSP=5
	IDLE_RSP=6
	DONE_RSP=7
	ids = []


	"""docstring for Aval-mm"""
	def __init__(self, fifo, id = 0, version = 1,idcount = 0):
		self.fifo=fifo
		self.id=id
		self.version=version
		self.idcount=idcount
		print ("file opened successfully:\n")


	def write(self,address,*wdata):
		pkt_len = 16
		endian = 0x0f
		op = self.WRITE
		data_len = 4
		# print("write data: ",wdata)
		request = pack("=BIHIBIIQI",endian,pkt_len,self.version,self.id,op,0,data_len,address,wdata[0])
		print("Write:  ", request)
		# request = request.decode()
		request = str(request,'Latin-1')
		# print(" ", request)
		print("Write Request => ", [endian, pkt_len, self.version, self.id, op, 0, data_len, address, wdata[0]])
		self.fifo.write(request)
		self.fifo.flush()
		fi.flush()
		self.id += 1
		# if self.id <90:
		# 	self.id += 1
		# else:
		# 	self.idcount +=1
		# 	self.id=0


	def read(self,address):
		pkt_len=12
		endian=0x0f
		op =self.READ
		data_len =0
		# print(" ",[endian, pkt_len, self.version, self.id, op, 0, data_len, address])
		request = pack("=BIHIBIIQ",endian,pkt_len,self.version,self.id,op,0,data_len,address)
		# print(" ",str(request,'utf-8'))
		# request = str(request,'utf-8')
		print("Read:  ", request)
		request = request.decode(encoding='Latin -1')
		print("Read request => ", [endian, pkt_len, self.version, self.id, op, 0, data_len, address])
		self.fifo.write(request)
		self.fifo.flush()
		fi.flush()
		self.id += 1
		# if self.id <90:
		# 	self.id += 1
		# else:
		# 	self.idcount +=1
		# 	self.id=0

	def ctrl_command(self):
		pkt_len = 0;
		endian=0x0f;
		op = self.DONE;
		request = pack("=BIHIB",endian,pkt_len,self.version,self.id, op)
		# request = str(request,'utf-8')
		request = request.decode(encoding='Latin-1')
		print("Term Request => ", [endian, pkt_len, self.version, self.id, op])
		self.fifo.write(request)
		self.fifo.flush()
		fi.flush()
		self.id += 1
		# if self.id < 90:
		# 	self.id += 1
		# else:
		# 	self.idcount +=1
		# 	self.id=0
		# count = self.idcount
		# print(count)
		
		
path = "qemu_apb_req.fifo"
# os.mkfifo(path)
fi =open(path,'w')
mm = Aval_mm(fi)

# mm.read(0x20)
# time.sleep(2)
# mm.write(0x20, 0x55)
# time.sleep(2)
# # mm.write(0x20, 0x55);
# mm.read(0x20);
# sleep(2)
# mm.write(0x24, 0xaa)
# sleep(2)
# mm.read(0x24)
# sleep(2)
# mm.write(0x28, 0xcc)
# sleep(2)
# mm.read(0x28)
# sleep(2)

for i in range(0,100):
	mm.write(0x2C, i)
	mm.read(0x2C)

mm.ctrl_command()
fi.close()

#################################################################
from struct import *
import time
import os
class Aval_mm:

	WRITE=0
	READ=1
	IDLE=2
	DONE=3
	WRITE_RSP=4
	READ_RSP=5
	IDLE_RSP=6
	DONE_RSP=7
	ids = []


	"""docstring for Aval-mm"""
	def __init__(self, fifo, id = 0, version = 1,idcount = 0):
		self.fifo=fifo
		self.id=id
		self.version=version
		self.idcount=idcount
		print ("file opened successfully:\n")


	def write(self,address,*wdata):
		pkt_len = 16
		endian = 0x0f
		op = self.WRITE
		data_len = 4
		request = pack("=BIHIBIIQI",endian,pkt_len,self.version,self.id,op,0,data_len,address,wdata[0])
		print("Write:  ", request)
		request = str(request,'Latin-1')
		print("Write Request => ", [endian, pkt_len, self.version, self.id, op, 0, data_len, address, wdata[0]])
		self.fifo.write(request)
		self.fifo.flush()
		fi.flush()
		self.id += 1
		# if self.id <90:
		# 	self.id += 1
		# else:
		# 	self.idcount +=1
		# 	self.id=0


	def read(self,address):
		pkt_len=12
		endian=0x0f
		op =self.READ
		data_len =0
		request = pack("=BIHIBIIQ",endian,pkt_len,self.version,self.id,op,0,data_len,address)
		print("Read:  ", request)
		request = str(request,'Latin-1')
		# request = request.decode(encoding='Latin -1')
		print("Read request => ", [endian, pkt_len, self.version, self.id, op, 0, data_len, address])
		self.fifo.write(request)
		self.fifo.flush()
		fi.flush()
		self.id += 1
		# if self.id <90:
		# 	self.id += 1
		# else:
		# 	self.idcount +=1
		# 	self.id=0

	def ctrl_command(self):
		pkt_len = 0;
		endian=0x0f;
		op = self.DONE;
		request = pack("=BIHIB",endian,pkt_len,self.version,self.id, op)
		request = str(request,'Latin-1')
		# request = request.decode(encoding='Latin-1')
		print("Term Request => ", [endian, pkt_len, self.version, self.id, op])
		self.fifo.write(request)
		fi.flush()
		self.fifo.flush()
		self.id += 1
		# if self.id < 90:
		# 	self.id += 1
		# else:
		# 	self.idcount +=1
		# 	self.id=0
		# count = self.idcount
		# print(count)
		
		
path = "qemu_apb_req.fifo"
# os.mkfifo(path)
fi =open(path,'w')
mm = Aval_mm(fi)

# mm.read(0x20)
# time.sleep(2)
# mm.write(0x20, 0x55)
# time.sleep(2)
# # mm.write(0x20, 0x55);
# mm.read(0x20);
# sleep(2)
# mm.write(0x24, 0xaa)
# sleep(2)
# mm.read(0x24)
# sleep(2)
# mm.write(0x28, 0xcc)
# sleep(2)
# mm.read(0x28)
# sleep(2)

for i in range(0,65):
	mm.write(0x2C, i)
	mm.read(0x2C)

mm.ctrl_command()
fi.close()
############################################################

from struct import *
import time
import os
class Aval_mm:

	WRITE=0
	READ=1
	IDLE=2
	DONE=3
	WRITE_RSP=4
	READ_RSP=5
	IDLE_RSP=6
	DONE_RSP=7
	ids = []


	"""docstring for Aval-mm"""
	def __init__(self, fifo, id = 0, version = 1,idcount = 0):
		self.fifo=fifo
		self.id=id
		self.version=version
		self.idcount=idcount
		print ("file opened successfully:\n")


	def write(self,address,*wdata):
		print('#######In WRITE#########')
		pkt_len = 16
		endian = 0x0f
		op = self.WRITE
		data_len = 4
		# print(" , ",wdata,address)
		request = pack("=BIHIBIIQI",endian,pkt_len,self.version,self.id,op,0,data_len,address,wdata[0])
		print("Write:  ", request)
		request = str(request,'Latin-1')
		print("Write Request => ", [endian, pkt_len, self.version, self.id, op, 0, data_len, address, wdata[0]])
		self.fifo.write(request)
		self.fifo.flush()
		fi.flush()
		self.id += 1
		time.sleep(1)

		Lines = ff_rd.readlines()
		read_value = int(str(int(Lines[-1].strip())),16)
		print(" ", wdata[0]," ",read_value)
		if read_value == wdata[0]:
			os.write(vfwt,int.to_bytes(1,1,byteorder='big',signed=False))
			print("Written: ",int.to_bytes(1,1,byteorder='big',signed=False))
		else:
			os.write(vfwt,int.to_bytes(0,1,byteorder='big',signed=False))
			print("Not Written: ",int.to_bytes(0,1,byteorder='big',signed=False))
		# if self.id <90:
		# 	self.id += 1
		# else:
		# 	self.idcount +=1
		# 	self.id=0


	def read(self,address):
		print('#######In READ#########')
		pkt_len=12
		endian=0x0f
		op =self.READ
		data_len =0
		request = pack("=BIHIBIIQ",endian,pkt_len,self.version,self.id,op,0,data_len,address)
		print("Read:  ", request)
		request = str(request,'Latin-1')
		# request = request.decode(encoding='Latin -1')
		print("Read request => ", [endian, pkt_len, self.version, self.id, op, 0, data_len, address])
		self.fifo.write(request)
		self.fifo.flush()
		fi.flush()
		self.id += 1
		time.sleep(2)
		Lines = ff_rd.readlines()
		read_value = int(str(int(Lines[-1].strip())),16)
		print("Read Value: ",read_value)
		os.write(vfrd,int.to_bytes(read_value,4,byteorder='big',signed=False))
		# os.write(vfrd,str(read_value))
		print("Written read data: ", int.to_bytes(read_value,4,byteorder='big',signed=False))
		# for line in Lines:
		# 	print("Line: {}".format(line.strip()))
		# if self.id <90:
		# 	self.id += 1
		# else:
		# 	self.idcount +=1
		# 	self.id=0

	def ctrl_command(self):
		pkt_len = 0;
		endian=0x0f;
		op = self.DONE;
		request = pack("=BIHIB",endian,pkt_len,self.version,self.id, op)
		request = str(request,'Latin-1')
		# request = request.decode(encoding='Latin-1')
		print("Term Request => ", [endian, pkt_len, self.version, self.id, op])
		self.fifo.write(request)
		fi.flush()
		self.fifo.flush()
		self.id += 1
		# if self.id < 90:
		# 	self.id += 1
		# else:
		# 	self.idcount +=1
		# 	self.id=0
		# count = self.idcount
		# print(count)
		
		
apb_fifo = "qemu_apb_req.fifo"
fifo_read = "/home/utk/Intern_Project/Register_Verification/apb_qemu/testbench/data.txt"

writeval_path = "/tmp/pipewrite.in"
verifywrite_path = "/tmp/pipewrite.out"

# readval_path = "/tmp/piperead.in"
return_read_path = "/tmp/piperead.out"

#Check if fifo exists
if os.path.exists(writeval_path):
    os.remove(writeval_path)
if os.path.exists(verifywrite_path):
    os.remove(verifywrite_path)
if os.path.exists(return_read_path):
    os.remove(return_read_path)

os.mkfifo(writeval_path)
os.mkfifo(verifywrite_path)
#Open PATHS for read/write
rf 		= os.open(writeval_path, os.O_SYNC | os.O_CREAT | os.O_RDWR)
vfwt	= os.open(verifywrite_path, os.O_SYNC | os.O_CREAT | os.O_RDWR)
vfrd	= os.open(return_read_path, os.O_SYNC | os.O_CREAT | os.O_RDWR)
ff_rd 	= open(fifo_read, 'r')
fi 		= open(apb_fifo,'w')

#Object of Class
mm 		= Aval_mm(fi)

# mm.write(0x2C,0x55)
# time.sleep(2)
# mm.read(0x2C)

# time.sleep(2)
# os.read(rd_fifo,1024)#
while True:
	s = os.read(rf, 32)
	s = str(s,'latin-1')
	s = s.split(',')
	ope = int(s[0])
	if ope == 1:#Write
		addr = int(s[1],16)
		data = int(s[2],16)
		print (f"Address:{addr} and Data:{data}")
		mm.write(addr,data)
		# time.sleep(1)
		# mm.read(0x2C)
		# break
	elif ope == 0:#Read
		addr = int(s[1],16)
		print(f"Reaf Addr:{hex(addr)}")
		mm.read(addr)
# for i in range(0,12):
	# mm.write(0x2C, i)
	# mm.read(0x2C)

mm.ctrl_command()
fi.close()
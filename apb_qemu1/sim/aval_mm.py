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
		request
		request = str(request,'Latin-1')
		# print(" ", request)
		print("Write Request => ", [endian, pkt_len, self.version, self.id, op, 0, data_len, address, wdata[0]])
		self.fifo.write(request)
		self.fifo.flush()
		fi.flush()
		# self.id += 1
		if self.id <90:
			self.id += 1
		else:
			self.idcount +=1
			self.id=0


	def read(self,address):
		pkt_len=12
		endian=0x0f
		op =self.READ
		data_len =0
		# print(" ",[endian, pkt_len, self.version, self.id, op, 0, data_len, address])
		request = pack("=BIHIBIIQ",endian,pkt_len,self.version,self.id,op,0,data_len,address)
		# print(" ",str(request,'utf-8'))
		request = str(request,'utf-8')
		request
		print("Read request => ", [endian, pkt_len, self.version, self.id, op, 0, data_len, address])
		self.fifo.write(request)
		self.fifo.flush()
		fi.flush()
		# self.id += 1
		if self.id <90:
			self.id += 1
		else:
			self.idcount +=1
			self.id=0

	def ctrl_command(self):
		pkt_len = 0;
		endian=0x0f;
		op = self.DONE;
		request = pack("=BIHIB",endian,pkt_len,self.version,self.id, op)
		request = str(request,'utf-8')
		print("Term Request => ", [endian, pkt_len, self.version, self.id, op])
		self.fifo.write(request)
		fi.flush()
		self.fifo.flush()
		# self.id += 1
		if self.id < 90:
			self.id += 1
		else:
			self.idcount +=1
			self.id=0
		count = self.idcount
		print(count)
		
		
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

for i in range(0,150):
	mm.write(0x2C, i)
	mm.read(0x2C)

mm.ctrl_command()
fi.close()
#!/usr/bin/env python
# -*- coding: latin-1 -*-
from struct import *
import string
import os
import time



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
		print(f'\n#######In WRITE:{self.id} #########\n')
		pkt_len = 16
		endian = 0x0f
		op = self.WRITE
		data_len = 4
		print(" ",wdata,address)
		request = pack("=BIHIBIIQI",endian,pkt_len,self.version,self.id,op,0,data_len,address,wdata[0])
		print(" ",pack("=BIHIBIIQI",endian,pkt_len,self.version,self.id,op,0,data_len,address,wdata[0]),"\n")
		print("\nWrite:  ", request)
		request = str(request,'Latin-1')
		print("\nWrite Request => ", [endian, pkt_len, self.version, self.id, op, 0, data_len, address, wdata[0]])
		self.fifo.write(request)
		self.fifo.flush()
		fi.flush()
		self.id += 1
		time.sleep(1)

		Lines = ff_rd.readlines()
		print("\n ",Lines[-1].strip())

		print("\n ",type(Lines[-1].strip()))
		print("\n ",int(Lines[-1].strip(),16))

		# read_value = int(str(int(Lines[-1].strip())),16)
		read_value = int(Lines[-1].strip(),16)
		print("\n ", wdata[0]," ",read_value)
		if read_value == wdata[0]:
			os.write(vfwt,int.to_bytes(1,1,byteorder='big',signed=False))
			print("\nWritten: ",int.to_bytes(1,1,byteorder='big',signed=False))
		else:
			os.write(vfwt,int.to_bytes(0,1,byteorder='big',signed=False))
			print("\nNot Written: ",int.to_bytes(0,1,byteorder='big',signed=False))


	def read(self,address):
		print(f'\n#######In READ:{self.id} #########\n')
		pkt_len=12
		endian=0x0f
		op =self.READ
		data_len =0
		request = pack("=BIHIBIIQ",endian,pkt_len,self.version,self.id,op,0,data_len,address)
		print("\nRead:  ", request)
		request = str(request,'Latin-1')
		print("\nRead request => ", [endian, pkt_len, self.version, self.id, op, 0, data_len, address])
		self.fifo.write(request)
		self.fifo.flush()
		fi.flush()
		self.id += 1
		time.sleep(1)
		Lines = ff_rd.readlines()
		# read_value = int(str(int(Lines[-1].strip())),16)
		read_value = int(Lines[-1].strip(),16)
		print("\nRead Value: ",read_value)
		os.write(vfrd,int.to_bytes(read_value,4,byteorder='big',signed=False))
		print("\nWritten read data: ", int.to_bytes(read_value,4,byteorder='big',signed=False))
		# time.sleep(1)


	def ctrl_command(self):
		pkt_len = 0;
		endian=0x0f;
		op = self.DONE;
		request = pack("=BIHIB",endian,pkt_len,self.version,self.id, op)
		request = str(request,'Latin-1')
		print("\nTerm Request => ", [endian, pkt_len, self.version, self.id, op])
		self.fifo.write(request)
		fi.flush()
		self.fifo.flush()
		self.id += 1

		
apb_fifo = "/home/utk/Intern_Project/Register_Verification/apb_qemu/sim/qemu_apb_req.fifo"
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
os.mkfifo(return_read_path)
#Open PATHS for read/write
rf 		= os.open(writeval_path, os.O_SYNC | os.O_CREAT | os.O_RDWR)
vfwt	= os.open(verifywrite_path, os.O_SYNC | os.O_CREAT | os.O_RDWR)
vfrd	= os.open(return_read_path, os.O_SYNC | os.O_CREAT | os.O_RDWR)
ff_rd 	= open(fifo_read, 'r')
fi 		= open(apb_fifo,'w')

#Object of Class
mm 		= Aval_mm(fi)

while True:
	s = os.read(rf, 32)
	s = str(s,'latin-1')
	s = s.split(',')
	ope = int(s[0])
	if ope == 1:#Write
		addr = int(s[1],16)
		data = int(s[2],16)
		print (f"\nAddress:{addr} and Data:{data}")
		mm.write(addr,data)
		# time.sleep(1)
		# mm.read(0x2C)
		# break
	elif ope == 0:#Read
		addr = int(s[1],16)
		print(f"\nReaf Addr:{hex(addr)}")
		mm.read(addr)
# for i in range(0,12):
	# mm.write(0x2C, i)
	# mm.read(0x2C)

mm.ctrl_command()
fi.close()
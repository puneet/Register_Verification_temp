#!/usr/bin/env python
# -*- coding: latin-1 -*-
from Gnumeric import GnumericError, GnumericErrorVALUE
import Gnumeric
import string
import os
import time
import sys
from struct import *
print(sys.version)
# import sys
reload(sys)
sys.setdefaultencoding('latin-1')
import pdb

class Aval_mm(object):

	WRITE=0
	READ=1	
	IDLE=2
	DONE=3
	WRITE_RSP=4
	READ_RSP=5
	IDLE_RSP=6
	DONE_RSP=7
	ids = []
	# Paths for various fifos and text files
	global apb_fifo
	global fifo_read
	apb_fifo = "/home/utk/Intern_Project/Register_Verification/apb_qemu/sim/qemu_apb_req.fifo"
	fifo_read = "/home/utk/Intern_Project/Register_Verification/apb_qemu/testbench/data.txt"


	# """docstring for Aval-mm"""
	def __init__(self,address = 0,data = 0,id = 0, version = 1):
		self.id=id
		self.version=version
		self.address = address
		self.data = data

	def open_fifos(self):
		global fifo
		global ffrd
		fifo = open(apb_fifo,'w')
		ffrd = open(fifo_read, 'r')


	def write(self,address,data):
		# print("1")
		address = int(str(address),16)
		# wdata = int(data,16)
		pkt_len = 16
		endian = 0x0f
		op = self.WRITE
		data_len = 4
		# print("before packing")
		# print(address,"",data)
		# print("2")
		request = pack("=BIHIBIIQI",endian,pkt_len,self.version,self.id,op,0,data_len,address,data)
		# print("after packing")
		# request = str(request,'Latin-1')
		# print("3")
		request = request.decode(encoding='Latin-1')
		# print "Write Request => ", [endian, pkt_len, self.version, self.id, op, 0, data_len, address, data]
		# print("4")
		fifo.write(request)
		fifo.flush()
		self.id += 1
		time.sleep(1)
		Lines = ffrd.readlines()
		# print("5")
		read_value = int(Lines[-1].strip(),16)
		if read_value == data:
			# print("\nWrite Done")
			return True
		else:
			return False


	def read(self,address):
		# print("Read: ",self.id)
		address = int(str(address),16)
		pkt_len=12
		endian=0x0f
		op =self.READ
		data_len =0
		request = pack("=BIHIBIIQ",endian,pkt_len,self.version,self.id,op,0,data_len,address)
		# request = str(request,'Latin-1')
		request = request.decode(encoding='Latin-1')
		# print("\nRead request => ", [endian, pkt_len, self.version, self.id, op, 0, data_len, address])
		fifo.write(request)
		fifo.flush()
		self.id += 1
		time.sleep(1)
		Lines = ffrd.readlines()
		read_value = str(hex(int(Lines[-1].strip(),16)))
		# print("\nRead Done")
		return read_value


	def ctrl_command(self):
		pkt_len = 0;
		endian=0x0f;
		op = self.DONE;
		request = pack("=BIHIB",endian,pkt_len,self.version,self.id, op)
		# request = str(request,'Latin-1')
		request = request.decode(encoding='Latin-1')
		fifo.write(request)
		fifo.flush()
		self.id += 1



flag = True


def write_val(address,wdata):
	'@FUNCTION=write_val\n'\
	'@SYNTAX=write_val(addr,data)\n'\
	'@DESCRIPTION=Write a value to address provided.\n\n'\
	'@EXAMPLES=To write data 0x50 at 0x2c, enter address 0x2C and Data\n'\
	'0x50 and hit enter.\n\n'\
	'@SEEALSO='
	global flag
	wb = Gnumeric.workbooks()[0] 
	s  = wb.sheets()[1]
	addr = int(address,16)
	# print(addr)
	data = int(wdata,16)
	mm = Aval_mm()
	if flag == True:
		mm.open_fifos()
		flag = False
	resp = mm.write(address,data)
	if resp == True:
		return "Write Successful"
		# time.sleep(100)
	else:
		return "Write Failed"

def read_val(address):
	'@FUNCTION=read_val\n'\
	'@SYNTAX=read_val(addr)\n'\
	'@DESCRIPTION= Read a value address provided.\n\n'\
	'@EXAMPLES=To read data from 0x2C, enter address 0x2C\n'\
	'and hit enter.\n\n'\
	'@SEEALSO='
	global flag
	wb = Gnumeric.workbooks()[0] 
	s  = wb.sheets()[1]
	address = str(address)
	mm = Aval_mm()
	if flag == True:
		mm.open_fifos()
		flag = False
	resp = mm.read(address)
	return resp

def exit_sim():
	wb = Gnumeric.workbooks()[0] 
	s  = wb.sheets()[1]
	mm = Aval_mm()
	mm.ctrl_command()

def val_check(gRange):
	
	col  = Gnumeric.functions['column']   
	rw  = Gnumeric.functions['row'] 
	wb = Gnumeric.workbooks()[0] 
	s  = wb.sheets()[0]
	columns = col(gRange)
	rows = rw(gRange)
	pdb.set_trace()
	if len(str(rows)) == 3:
		n1 = int(rows)-1
		n2= n1
	else:
		n1 = int(rows[0][0])-1;n2 = int(rows[-1][0])-1

	if len(str(columns)) == 3:
		m1 = int(columns)-1
		m2 = m1
	else:
		m1 = int(columns[0][0])-1;m2 = int(columns[-1][0])-1

	# print m1,m2
	ar = []
	for val in range(m1,m2+1):
		cell = s[val,n1]
		num = cell.get_value()
		ar.append(num)
	print ar
		

# Translate the func_add python function to a gnumeric function and register it
example_functions = {
    'py_write': write_val,
    'py_read': read_val,
    'py_exit':exit_sim,
    'py_check': val_check
}


 # RUN THIS BEFORE COMMITING TO GIT
 # sync -avu /home/utk/.gnumeric/1.12.46/plugins/myfunc/* /home/utk/Intern_Project/Register_Verification/Synched/
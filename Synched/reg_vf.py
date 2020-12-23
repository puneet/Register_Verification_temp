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


def write_val(addr,data):
	global flag
	mm = Aval_mm()
	if flag == True:
		mm.open_fifos()
		flag = False
	print type(data)
	mm.write(addr,data)

def read_val(addr):
	global flag
	if flag == True:
		mm.open_fifos()
		flag = False
	mm = Aval_mm()
	data = mm.read(addr)
	return data

def exit_sim():
	wb = Gnumeric.workbooks()[0] 
	s  = wb.sheets()[1]
	mm = Aval_mm()
	mm.ctrl_command()


def val_check(cell_range):
	col  = Gnumeric.functions['column']   
	rw  = Gnumeric.functions['row'] 
	wb = Gnumeric.workbooks()[0] 
	s  = wb.sheets()[0]
	columns = col(cell_range)
	rows = rw(cell_range)
	# pdb.set_trace()
	n1 = int(rows) -1
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
	############################################################
	if ar[0].lower()[0:8] == 'register':
		field_ar = []
		rw = n1+1
		fg =True
		while fg == True:
			f_cell = s[m1,rw]
			f_name = f_cell.get_value()
			# print f_name, type(f_name)
			field_temp = []
			f_name = f_name.lower()
			print f_name
			if f_name[0:5] == 'field':
				for v in range(m1,m2+1):
					f_cell_temp = s[v,rw]
					f_data = f_cell_temp.get_value()
					field_temp.append(f_data)
				print field_temp
				field_ar.append(field_temp)	
			else: 
				fg = False
			rw += 1
		print field_ar
		a = 'RO' in str(field_ar)
		print a 
		if a == True:
			return 'RO fields present, write to reg not permitted'
		else:
			addr = int(str(ar[2]),16)
			data  = int(ar[7])
			write_val(addr,data)
			return 'DONE' 
	#######3#################################################
	elif ar[0].lower()[0:5] == 'field':
		# pdb.set_trace()
		a = 'RO' in  str(ar)
		if a == True:
			return 'RO field, cannot write'
		else:
			data  = int(ar[7])
			fg = True
			i = n1-1
			while fg == True:
				cell = s[m1+2,i]
				val = cell.get_value()
				if val != None:
					addr = val
					fg = False
				else:
					i -= 1
			read_data = read_val(addr)
			read_data = "{0:032b}".format(int(read_data, 16))
			
			if len(str(int(ar[4]))) <= 3 :
				# pdb.set_trace()
				end = 32 - int(ar[4])
				data = list(bin(data).lstrip('0b'))
				temp_data = list(read_data)
				temp_data[end-len(data)] = data[0]
				print data
				print temp_data
				read_data = "".join(temp_data)
				read_data = int(read_data,2)
				print read_data
				# pdb.set_trace()
				write_val(addr,read_data)
				return 'DONE'

			else:
				# start = 31 - int(ar[4][1:3])
				end = 32 - int(ar[4][4:6])
				data = list(bin(data).lstrip('0b'))
				temp_data = list(read_data)
				temp_data[end-len(data):end] = data
				read_data = "".join(temp_data)
				read_data = int(read_data,2)
				print read_data
				# pdb.set_trace()
				write_val(addr,read_data)
				return 'DONE' 



def func_sub(num1, num2):
	val = num1 - num2
	print val
	return num1 - num2

# Translate the func_add python function to a gnumeric function and register it
example_functions = {
    # 'py_write': write_val,
    # 'py_read': read_val,
    'py_exit':exit_sim,
    'py_check': val_check,
    'py_sub' : func_sub
}


 # RUN THIS BEFORE COMMITING TO GIT
 # rsync -avu /home/utk/.gnumeric/1.12.46/plugins/myfunc/* /home/utk/Intern_Project/Register_Verification/Synched/
# my_func.py
from Gnumeric import GnumericError, GnumericErrorVALUE
import Gnumeric
import string
import os
import time
import sys
	
# Add two numbers together
def func_add(num1, num2):
    '@FUNCTION=PY_ADD\n'\
    '@SYNTAX=py_add(num1, num2)\n'\
    '@DESCRIPTION=Adds two numbers together.\n'\
    'Look, the description can go onto other lines.\n\n'\
    '@EXAMPLES=To add two constants, just type them in: py_add(2,3)\n'\
    'To add two cells, use the cell addresses: py_add(A1,A2)\n\n'\
    '@SEEALSO='
    vl = num1 + num2
    print vl
    return num1 + num2
###################################################################
# Subtract two numbers together
def func_sub(num1, num2):
    vl = num1 - num2
    print vl
    return num1 - num2
###################################################################
#Add a range of numbers
def func_sum(gRange):
	'@FUNCTION=PY_SUM\n'\
	'@SYNTAX=PY_SUM(range)\n'\
	'@DESCRIPTION=Adds a range of numbers together.'\
	'Just like built-in SUM.\n\n'\
	'@EXAMPLES=To add values in A1 to A5, just type them in:\n'\
	'    py_sum(a1:a5)\n'\
	'@SEEALSO='
	try:
		sum = Gnumeric.functions['sum']
		val = sum(gRange)
		#  val = reduce(lambda a,b: a+b, vals)
	except TypeError:
		raise GnumericError, GnumericErrorVALUE
	else:
		return val
		  
##################################################################33

def func_secmax(gRange):
	'@FUNCTION=PY_SUM2\n'\
	'@SYNTAX=PY_SUM2(range)\n'\
	'@DESCRIPTION=Adds a range of numbers together,'\
	'without calling built-in SUM.\n\n'\
	'@EXAMPLES=To add values in A1 to A5, just type them in:\n'\
	'    py_sum(a1:a5)\n'\
	'@SEEALSO='
	col  = Gnumeric.functions['column']   
	rw  = Gnumeric.functions['row']
	

	write_path = "/tmp/pipe.in"
	read_path = "/tmp/pipe.out"

	columns = col(gRange)
	rows = rw(gRange)
	wb = Gnumeric.workbooks()[0] 
	s  = wb.sheets()[0] 
	i=0; 
	ar = []
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

	for r in range(n1,n2+1):
		for c in range(m1,m2+1):
			cell = s[c,r]
			val = cell.get_value()
			ar.append(val)
			i += 1
	list1 = ar
	mx=max(list1[0],list1[1])  
	secondmax=min(list1[0],list1[1])  
	n =len(list1) 
	for i in range(2,n):  
	    if list1[i]>mx:  
	        secondmax=mx 
	        mx=list1[i]  
	    elif list1[i]>secondmax and mx != list1[i]:  
	        secondmax=list1[i] 
	    else: 
	        if secondmax == mx: 
	            secondmax = list1[i] 
		
	#
	wf = os.open(write_path, os.O_SYNC | os.O_CREAT | os.O_RDWR)
	rf = None
	msg = str(secondmax)
	os.write(wf,msg)
	print("sent msg: ",msg)
 # 	if rf is None:
	#     rf = os.open(read_path, os.O_RDONLY)
 
	# s = os.read(rf, 1024)
	# if len(s) != 0:
	# 	print ("\n")
	# else:
	# 	os.write(wf, 'exit')
 # 	os.close(rf)
	# os.close(wf)
	return secondmax


###########################################################################




# Translate the func_add python function to a gnumeric function and register it
example_functions = {
    'py_add': ('ff','num1,num2',func_add),
    'py_sub': func_sub,
    'py_sum': ('r', 'values', func_sum),
    'py_secmax': ('r','values',func_secmax)
}

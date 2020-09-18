apb_fifo = "/home/utk/Intern_Project/Register_Verification/apb_qemu/sim/qemu_apb_req.fifo"
fifo_read = "/home/utk/Intern_Project/Register_Verification/apb_qemu/testbench/data.txt"
while True:
	fi = open(apb_fifo,'w')
	ff = open(fifo_read, 'r')


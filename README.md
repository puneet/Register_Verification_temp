# Register Verification Using Gnumeric
**NOTE**: This implementation is for Gnumeric 1.12.46, updated release for version 1.12.48 will be released soon.<br/>
**Pre-requisites to be installed**: EUVM, Icarus Verilog, Gnumeric, GCC
## Steps to be followed
1. Clone this repository to your working directory
```
$cd path/to/your/working/directory 
$git clone https://github.com/utkarshb1/Register_Verification.git
```
2. Setting up plugins for Gnumeric <br/>
2.1 Make sure gnumeric is installed, if not run `sudo apt install gnumeric` in terminal <br/>
2.2 Install the Gnumeric Plugins by running `sudo apt install gnumeric-plugins-extra` in terminal <br/>
2.3 Enable Python plugins in Gnumeric. Open gnumeric go to Tools-> Plug-ins-> Check box Python Functions-> Close. <br/> 
2.3 Now in terminal, make directory: <br/>
```
$mkdir ~/.gnumeric 
$mkdir ~/.gnumeric/(version) 
$mkdir ~/.gnumeric/(version)/plugins 
$mkdir ~/.gnumeric/(version)/plugins/myfunc 
$cd ~/.gnumeric/(version)/plugins/myfuncs/ 
```
Copy the plugin files from the repository to the above directory
```
$cp path/to/your/working/directory/Register_Verification/Gnumeric_files/reg_gnfunc.py /home/user/.gnumeric/(version)/plugins/myfuncs/reg_vf.py 
$cp path/to/your/working/directory/Register_Verification/Gnumeric_files/my_link.xml /home/user/.gnumeric/(version)/plugins/myfuncs/plugin.xml
```

3. Change the current directory to the following: `$cd path/to/your/working/directory/Register_Verification/apb_qemu/sim/` 

You can see various files in this directory.<br/>
3.1 To compile and run the Simulation, open terminal in this directory and run following commands:
```
make clean
make 
make run 
```

 **Note**: Make sure that EUVM is in your PATH, `echo $PATH` = `/home/user/Intern_Project/euvm-1.0-beta14/bin`:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
 
 4. Now to pass write/read values to simulation, open `reg.gnumeric` file which is in the `/sim/` directory. It will look as follows (you can still edit as per your wish): <br/>
 ![alt text](https://github.com/utkarshb1/Register_Verification/blob/master/reg.png?raw=true)
 
Now in an empty cell write function `=py_write(address,data)` where address and data are the cells of Gnumeric representing the Address and Data to be written at that address and hit enter. If the write operation is successful you'll be able to see the simulation in terminal where it is running as well as a message "Successful" will be seen in Gnumeric

To read the value from an address, write function `=py_read(Address)` in any empty cell and pass the Cell value to read the data present at that address

5. After you're done with the simulation, write function `=py_exit()` in any empty cell to stop the Simulation.

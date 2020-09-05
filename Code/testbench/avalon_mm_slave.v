module avalon_mm_slave(clk, //input
		       reset, //input
		       address, //input
		       read, //input
		       write, //input
		       chipselect, //input
		       waitrequest, //output
		       readdata, //output
		       writedata, //input
		       // byteenable //input
		       );

   parameter WAIT_READ = 4;
   parameter WAIT_WRITE = 2;
   parameter DW = 32;//data width
   parameter N =  DW/8; //no. of lanes
   parameter AW = 32;//address width
   parameter MEM_SIZE = 1024;//memory size
   

   input 	   clk;
   input 	   reset;
   output [DW-1:0] readdata;
   output 	   waitrequest;
   
   

   input [AW-1:0]  address;
   input 	   read;
   input 	   write;
   input 	   chipselect;
   input [DW-1:0]  writedata;
   // input [N-1:0]   byteenable;
   
   
   
   
   wire 	   read;
   wire 	   write;
   wire 	   chipselect;
   wire [N-1:0]    byteenable = 4'b1111;
   wire [DW-1:0]   writedata;
   reg 		   wr;
   reg 		   rd;
   reg [AW-1:0]    addr; //for address 
   reg [DW-1:0]    rdata;
   reg [DW-1:0]    wdata;

   
   
   
   reg [DW-1:0]    Mem[MEM_SIZE-1:0];//memory array
   reg 		   waitrequest;
   reg [DW-1:0]    readdata;
   reg 		   event1;


   initial begin: initialization_mem
      integer i;
      for(i=0; i<MEM_SIZE; i=i+1) begin
	Mem[i] = i;
      end
   end
   
   //----------------waitselect--------------------------//
   always@(posedge clk)
     begin: waitselect_loop
	integer i;
	for(i=0; i == WAIT_WRITE; i++)
	  @(posedge clk);
	waitrequest = 1'b1;
     end

   always@(posedge clk)
     begin: waitrequest_loop
	integer i;
	for(i=0; i == WAIT_READ; i++)
	  @(posedge clk);
	waitrequest = 1'b0;
	event1 = 1'b1;
     end
   
   //----------------------------------------------------//
   
   always@(posedge clk )
     begin
	if(chipselect == 1'b1)
	  begin
	     if(waitrequest==1'b0)
	       begin
 		  addr <= address;
	       end
	     
	     else 
	       begin
		  @(posedge event1);
		  addr <= address;
	       end
	  end // if (chipselect == 1'b1)
     end // always@ (posedge clk )
   
   

   //.......................byteenable logic..............//
   always@(posedge clk)
     begin: byteenable_loop
	integer i;
	for(i=0; i!=N; i++)
	  begin
	     if(byteenable[i]==1)
	       begin
		  wdata[i*8] = writedata[i*8];
		  wdata[i*8+1] = writedata[i*8+1];
		  wdata[i*8+2] = writedata[i*8+2];
		  wdata[i*8+3] = writedata[i*8+3];
		  wdata[i*8+4] = writedata[i*8+4];
		  wdata[i*8+5] = writedata[i*8+5];
		  wdata[i*8+6] = writedata[i*8+6];
		  wdata[i*8+7] = writedata[i*8+7];
		  
		  readdata[i*8] = rdata[i*8];
		  readdata[i*8+1] = rdata[i*8+1];
		  readdata[i*8+2] = rdata[i*8+2];
		  readdata[i*8+3] = rdata[i*8+3];
		  readdata[i*8+4] = rdata[i*8+4];
		  readdata[i*8+5] = rdata[i*8+5];
		  readdata[i*8+6] = rdata[i*8+6];
		  readdata[i*8+7] = rdata[i*8+7];
		  
	       end
	  end
     end // always@ (posedge clk)
   
   //.....................................................//

   
   
   //***********write and read operation*********//
   always@(posedge clk) begin
      if(chipselect == 1'b1) begin
	 wr <= write;
	 rd <= read;
      end
   end

   always@(posedge clk) begin
		if(chipselect == 1'b1) begin
			if(wr == 1'b1 && waitrequest == 1'b0) begin
	    		wdata = writedata;
	    		Mem[addr] = wdata;
	 		end
	 
	 		else if (rd == 1'b1 && waitrequest == 1'b0) begin
	    		rdata = Mem[addr];
	    		readdata = rdata;
	 		end
	 
	 		else if ( waitrequest ==1'b1) begin
	    		@(posedge event1);
	    		if(wr == 1'b1 && waitrequest == 1'b0) begin
	       			wdata = writedata;
	       			Mem[addr] = wdata;
	    		end
	    
	    		else if (rd == 1'b1 && waitrequest == 1'b0) begin
	       			rdata = Mem[addr];
	       			readdata = rdata;
	    		end
	 		end
      	end
   	end
   
endmodule // avalon_mm_slave

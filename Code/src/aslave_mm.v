module aslave_mm #(parameter ADDRW= 8,DATAW=32)
	//Fundamental slave signals
	(clk,
	 rst_n,
	 sl_addr,
	 sl_read,
	 sl_write,
	 sl_readdata,
	 sl_writedata,
	 sl_waitrequest,
	 us_read,
	 us_write,
	 us_cs,
	 us_byteenable
	);

	input clk;
	input rst_n;
	// MM read/write slave interface
	input [ADDRW-1:0]   sl_addr;
	input 			    sl_read;
	input 			    sl_write;
	input [DATAW-1:0]   sl_writedata;
	output [DATAW-1:0]  sl_readdata;
	output 				sl_waitrequest;

	// wires
	wire [DATAW-1:0] 	sl_readdata;
	wire		 		sl_waitrequest;
	wire 				rst_n;
	wire [DATAW-1] 		r_data;
	wire 				cs;
	wire 				we;
	wire 				reg_status_valid;

	//reg
	reg [DATAW-1:0] 	wrdata;
	reg [DATAW-1:0] 	mem [256];

	// chipselect
	assign cs = (sl_read || sl_write);
	assign we = sl_write;
	assign sl_waitrequest = ~reg_status_valid && sl_read;
	

	always @(posedge clk or negedge rst_n) begin
		if (rst_n == 0) begin
			// reset
			sl_read 		= 0;
			sl_write 		= 0;
			sl_writedata 	= 0;
			sl_readdata 	= 0;
			cs 				= 0;
			us_write		= 0;
			us_read			= 0;
			
			
		end
		else if (sl_read == 1) begin
			sl_readdata = mem[sl_read];
			
		end
		else if (sl_write == 1) begin
			mem[sl_addr] <= sl_writedata;
			
		end
	end


endmodule : aslave_mm
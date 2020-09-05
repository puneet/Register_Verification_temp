`timescale 1ns/100ps
module avalon_mm_slavetb ();

	wire [31:0]		avs_readdata;
	wire 			avs_waitrequest;

	reg [31:0] 		avs_address;
	reg 			avs_read;
	reg 			avs_write;
	reg [31:0] 		avs_writedata;
	reg 			avs_chipselect;


	reg 			clk;
	reg 			reset;

	initial begin
		reset = 0;
	  	#10;
	  	reset = 1;
	  	#100;
	  	reset = 0;
	  	// #1000000;
	  	// $finish;
	end

	initial begin
		clk = 0;
		forever begin
			#10;
			clk = ~clk;
		end
	end

	task write(input [31:0]  addr,
			   input [31:0] data);
		begin
			@(negedge clk);
			avs_address = addr;
			avs_writedata = data;
			avs_write = 1;
			avs_read = 0;
			avs_chipselect = 1;
			@(posedge clk);
		end
	endtask // write

	task read(input [31:0] addr);
		begin
			@(negedge clk);
			avs_address = addr;
			avs_read = 1;
			avs_write = 0;
			avs_chipselect = 1;
			@(posedge clk);
		end
	endtask	

	task idle;
		@(negedge clk);
	endtask


	initial begin: bfm
		reg [31:0]  addr;
		reg [31:0] data;
		reg [3:0]  strb;
		reg 	 flag;
		#200;	
		@(posedge clk);
		forever begin
			while (reset == 1'b1) begin
				@(posedge clk);
			end // while (reset == 1'b1)

			case ($avl_try_next_item(addr, strb, data, flag))
			0: begin: valid_transaction
				if (flag == 1) begin	// write
					write (addr, data);
				end // if (flag == 1)
				else begin
					read (addr);
				end
				while (avs_waitrequest) begin
					@(posedge clk);
				end
				@(negedge clk);
				if (flag == 0) data = avs_readdata;
				avs_address = 'bX;
				avs_read = 0;
				avs_writedata = 'bX;
				avs_write = 0;
				// avs_chipselect = 0;
				if ($avl_item_done(0) != 0) ; // $finish;
				if ($avl_put(addr, strb, data, flag) != 0) begin
				// $finish;
				end
			end // block: valid_tr
			default: begin: idle_transaction
				@(negedge clk);
				avs_read = 1'b0;
				avs_write = 1'b0;
				@(posedge clk);
			end
// default: ; // $finish;
			endcase
		end // forever begin
	end // initial begin


	initial
	begin
		$dumpfile("avmm_slave.vcd");
		$dumpvars(0, avalon_mm_slavetb);
	end // initial begin


	avalon_mm_slave u1(.clk			(clk),
					   .reset		(reset),
					   .address 	(avs_address[31:0]),
					   .read 		(avs_read),
					   .write       (avs_write),
					   .chipselect 	(avs_chipselect),
					   .waitrequest (avs_waitrequest),
					   .readdata 	(avs_readdata),
					   .writedata 	(avs_writedata)
		);

endmodule
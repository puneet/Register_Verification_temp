module apb_slave #(parameter ADDRW = 8, DATAW = 32)
   (
    input 		   clk,
    input 		   rst_n,
    input [ADDRW-1:0] 	   paddr,
    input 		   pwrite,
    input 		   psel,
    input 		   penable,
    input [DATAW-1:0] 	   pwdata,
    output reg [DATAW-1:0] prdata
    );

   reg [DATAW-1:0] 	   mem [256];

   reg [1:0] 		   apb_st;
   
   parameter logic [1:0]   SETUP = 0;
   parameter logic [1:0]   W_ENABLE = 1;
   parameter logic [1:0]   R_ENABLE = 2;

   // SETUP -> ENABLE
   always @(negedge rst_n or posedge clk) begin
      if (rst_n == 0) begin
	 apb_st <= 0;
	 prdata <= 0;
      end

      else begin
	 case (apb_st)
	   SETUP : begin
              // clear the prdata
              prdata <= 0;

              // Move to ENABLE when the psel is asserted
              if (psel && !penable) begin
		 	  	if (pwrite) begin
		    		apb_st <= W_ENABLE;
				end

		 	else begin
		    apb_st <= R_ENABLE;
		 end
              end
	   end

	   W_ENABLE : begin
              // write pwdata to memory
              if (psel && penable && pwrite) begin
		 mem[paddr] <= pwdata;
              end

              // return to SETUP
              apb_st <= SETUP;
	   end

	   R_ENABLE : begin
              // read prdata from memory
              if (psel && penable && !pwrite) begin
		 prdata <= mem[paddr];
              end

              // return to SETUP
              apb_st <= SETUP;
	   end
	 endcase
      end
   end 


endmodule

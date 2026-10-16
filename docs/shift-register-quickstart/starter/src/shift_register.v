`default_nettype none

// Existing design: 8-bit serial-in, parallel-out shift register.
module shift_register (
    input  wire       clk,
    input  wire       rst,        // 1 clears q on the next rising clock edge
    input  wire       enable,     // 1 shifts; 0 holds the stored value
    input  wire       serial_in,  // new bit enters q[0]
    output reg  [7:0] q
);
    always @(posedge clk) begin
        if (rst)
            q <= 8'b00000000;
        else if (enable)
            q <= {q[6:0], serial_in};
    end
endmodule

// counter_tb.v - self-checking testbench for counter.v.
// Works with Icarus Verilog (iverilog -g2012) and Verilator (--binary --timing).
`timescale 1ns / 1ps
`default_nettype none

module counter_tb;

    localparam WIDTH = 8;

    reg              clk = 1'b0;
    reg              rst = 1'b1;
    reg              en  = 1'b0;
    wire [WIDTH-1:0] count;
    wire             wrap;

    integer          errors = 0;
    integer          wraps  = 0;
    reg  [WIDTH-1:0] model  = {WIDTH{1'b0}};

    counter #(.WIDTH(WIDTH)) dut (
        .clk(clk), .rst(rst), .en(en), .count(count), .wrap(wrap)
    );

    always #5 clk = ~clk;  // 100 MHz

    // Reference model, updated on the same edge as the DUT.
    always @(posedge clk) begin
        if (rst)     model <= {WIDTH{1'b0}};
        else if (en) model <= model + 1'b1;
    end

    // Compare just after each edge.
    always @(negedge clk) begin
        if (count !== model) begin
            $display("ERROR t=%0t count=%0d expected=%0d", $time, count, model);
            errors = errors + 1;
        end
        if (wrap !== (en & (&model))) begin
            $display("ERROR t=%0t wrap=%b expected=%b", $time, wrap, en & (&model));
            errors = errors + 1;
        end
        if (wrap) wraps = wraps + 1;
    end

    initial begin
        if ($test$plusargs("vcd")) begin
            $dumpfile("counter_tb.vcd");
            $dumpvars(0, counter_tb);
        end

        repeat (3) @(negedge clk);
        rst = 1'b0;

        // Count for more than one full period so the wrap is exercised.
        en = 1'b1;
        repeat ((1 << WIDTH) + 10) @(negedge clk);

        // Hold: count must not move while en is low.
        en = 1'b0;
        repeat (20) @(negedge clk);

        // Synchronous reset mid-count.
        en = 1'b1;
        repeat (7) @(negedge clk);
        rst = 1'b1;
        @(negedge clk);
        rst = 1'b0;
        repeat (5) @(negedge clk);

        if (wraps != 1) begin
            $display("ERROR expected exactly 1 wrap pulse, saw %0d", wraps);
            errors = errors + 1;
        end

        if (errors == 0) $display("PASS: counter_tb (%0d-bit), 0 errors", WIDTH);
        else             $display("FAIL: counter_tb, %0d errors", errors);
        $finish;
    end

endmodule

`default_nettype wire

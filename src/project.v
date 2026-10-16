`default_nettype none

// Wrapper: connects the existing design to Tiny Tapeout's fixed ports.
module tt_um_student_shift_register (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);
    shift_register core (
        .clk       (clk),
        .rst       (~rst_n),  // Tiny Tapeout reset is low; core reset is high
        .enable    (ui_in[1]),
        .serial_in (ui_in[0]),
        .q         (uo_out)
    );

    // Bidirectional pins are unused. A 0 in uio_oe means input direction.
    assign uio_out = 8'b00000000;
    assign uio_oe  = 8'b00000000;

    // ena is Tiny Tapeout's project-selection signal, not shift enable.
    wire _unused = &{ena, ui_in[7:2], uio_in, 1'b0};
endmodule

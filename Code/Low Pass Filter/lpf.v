//Date - 22 - 08 - 2026

//LPF - 0 to 250Hz
//BPF - 250Hz to 4KHz
//HPF - 4KHz to 20KHz

`timescale 1ns/1ps

//LPF - 20Hz to 250Hz
module LPF (
    input clk,
    input rst,
    input  signed [23:0] in,       // Q1.23
    output reg signed [23:0] out   // Q1.23
);

    // Coefficients: Q2.16, 18-bit two's complement
    parameter signed [17:0] b0 = 18'h00014;
    parameter signed [17:0] b1 = 18'h00028;
    parameter signed [17:0] b2 = 18'h00014;
    parameter signed [17:0] a1 = 18'h20CE5;   // -1.9496
    parameter signed [17:0] a2 = 18'h0F36C;   // +0.9509

    // Q1.23 * Q2.16 -> 42 bits, 39 fractional bits
    wire signed [41:0] zero0, zero1, zero2;
    wire signed [41:0] pole1, pole2;

    // Filter state (transposed direct form II), 39 fractional bits
    reg signed [42:0] adder1, adder2;

    // Combinational output: y = b0*x + adder1, truncated back to Q1.23
    wire signed [42:0] y_full = zero0 + adder1;
    wire signed [23:0] y_q    = y_full[39:16];

    assign zero0 = in * b0;
    assign zero1 = in * b1;
    assign zero2 = in * b2;

    // Feedback uses the *current* y, not the registered out
    assign pole1 = y_q * a1;
    assign pole2 = y_q * a2;

    always @(posedge clk) begin
        if (rst) begin
            adder1  <= 0;
            adder2  <= 0;
            out <= 0;
        end
        else begin
            adder1  <= zero1 - pole1 + adder2;
            adder2  <= zero2 - pole2;
            out <= y_q;
        end
    end

endmodule


`timescale 1ns/1ps

module tb;

    reg clk;
    reg rst;
    reg signed [23:0] in;
    wire signed [23:0] out;

    integer infile;
    integer outfile;
    reg [23:0] sample;

    LPF dut (
        .clk(clk),
        .rst(rst),
        .in(in),
        .out(out)
    );

    // Clock: 100 MHz
    always #5 clk = ~clk;

    initial begin
        clk = 0;
        rst = 1;
        in  = 0;

        infile  = $fopen("input.txt", "r");
        outfile = $fopen("output.txt", "w");

        if (infile == 0) begin
            $display("ERROR: Could not open input.txt");
            $finish;
        end

        if (outfile == 0) begin
            $display("ERROR: Could not open output.txt");
            $finish;
        end

        repeat (2) @(posedge clk);
        @(negedge clk) rst = 0;

        // Read 24-bit binary samples
        while ($fscanf(infile, "%b\n", sample) == 1) begin
            @(negedge clk);
            in = sample;

            @(posedge clk);
            #1;
            $fwrite(outfile, "%b\n", out);
        end

        $fclose(infile);
        $fclose(outfile);

        $display("Simulation completed.");
        $finish;
    end

endmodule
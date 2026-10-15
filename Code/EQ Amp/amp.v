//Date - 20-08-2026

module top_module (
    input [11:0]in_ADC,
    input [23:0]in_EQ,
    output [23:0]out_EQ // Given to EQ Top Module
);

    wire [3:0]out_adc;

    ADC_reducer A1(.in(in_ADC), .out(out_adc));
    eq_amp AMP(.in(in_EQ), .control(out_adc), .out(out_EQ));
    
endmodule



module ADC_reducer (
    input [11:0]in, //input from ADC
    output [3:0]out
);

    assign out = in[11:8];
    
endmodule


module eq_amp (
    input [23:0]in, //input from EQ Card after filtering
    input [3:0]control, //input from ADC_reducer
    output [23:0]out
);

    reg [41:0]temp;
    reg [17:0]gain;

    parameter  vol_0 =  4'b0000;
    parameter DB_Neg6_duplicate = 4'b0001;
    parameter DB_Neg6 = 4'b0010;
    parameter DB_Neg5 = 4'b0011;
    parameter DB_Neg4 = 4'b0100;
    parameter DB_Neg3 = 4'b0101;
    parameter DB_Neg2 = 4'b0110;
    parameter DB_Neg1 = 4'b0111;
    parameter DB_0    = 4'b1000;
    parameter DB_Pos1 = 4'b1001;
    parameter DB_Pos2 = 4'b1010;
    parameter DB_Pos3 = 4'b1011;
    parameter DB_Pos4 = 4'b1100;
    parameter DB_Pos5 = 4'b1101;
    parameter DB_Pos6 = 4'b1110;
    parameter DB_Pos6_duplicate = 4'b1111;

    always @(*) begin
        case (control)

            vol_0             : gain = 18'h00000;
            DB_Neg6_duplicate : gain = 18'h0804E;
            DB_Neg6           : gain = 18'h0804E;
            DB_Neg5           : gain = 18'h08FF6;
            DB_Neg4           : gain = 18'h0A186;
            DB_Neg3           : gain = 18'h0B53C;
            DB_Neg2           : gain = 18'h0CB59;
            DB_Neg1           : gain = 18'h0E429;
            DB_0              : gain = 18'h10000;
            DB_Pos1           : gain = 18'h11F3D;
            DB_Pos2           : gain = 18'h14249;
            DB_Pos3           : gain = 18'h1699C;
            DB_Pos4           : gain = 18'h195BC;
            DB_Pos5           : gain = 18'h1C73D;
            DB_Pos6           : gain = 18'h1FECA;
            DB_Pos6_duplicate : gain = 18'h1FECA;

            default: gain = 18'h10000;
        endcase

        temp = in * gain;

    end

    assign out = temp[39:16];
    
endmodule


module testbench;

    reg [11:0]in_adc;
    reg [23:0]in_eq;
    wire [23:0]out_eq;

    top_module uut(.in_ADC(in_adc), .in_EQ(in_eq), .out_EQ(out_eq));

    initial 
        begin
            in_adc = 0; 
            in_eq = 0;
        end
    
    always
        begin
          #5 $display("Input from ADC = %d, Input from EQ = %d, Output = %d", in_adc, in_eq, out_eq);
        end

    initial
        begin
            in_adc = 0; in_eq = 24'h400000; //0000
            #5
            in_adc =  {4'b0001, 8'b0}; in_eq = 24'h400000; 
            #5
            in_adc =  {4'b0010, 8'b0}; in_eq = 24'h400000; 
            #5
            in_adc =  {4'b0011, 8'b0}; in_eq = 24'h400000; 
            #5
            in_adc =  {4'b0100, 8'b0}; in_eq = 24'h400000; 
            #5
            in_adc =  {4'b0101, 8'b0}; in_eq = 24'h400000; 
            #5
            in_adc =  {4'b0110, 8'b0}; in_eq = 24'h400000; 
            #5
            in_adc =  {4'b0111, 8'b0}; in_eq = 24'h400000; 
            #5
            in_adc =  {4'b1000, 8'b0}; in_eq = 24'h400000; 
            #5
            in_adc =  {4'b1001, 8'b0}; in_eq = 24'h400000; 
            #5
            in_adc =  {4'b1010, 8'b0}; in_eq = 24'h400000; 
            #5
            in_adc =  {4'b1011, 8'b0}; in_eq = 24'h400000; 
            #5
            in_adc =  {4'b1100, 8'b0}; in_eq = 24'h400000; 
            #5
            in_adc =  {4'b1101, 8'b0}; in_eq = 24'h400000; 
            #5
            in_adc =  {4'b1110, 8'b0}; in_eq = 24'h400000; 
            #5
            in_adc =  {4'b1111, 8'b0}; in_eq = 24'h400000; 
            #5
            $finish;
        end

endmodule


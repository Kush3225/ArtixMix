//Date - 20-08-2026

module ADC_reducer (
    input [11:0]in,
    output [3:0]out
);

    assign out = in[11:8];
    
endmodule


module vol_control (
    input [15:0]in, //input from SD Card
    input [3:0]control, //input from ADC_reducer
    output [15:0]out
);

    reg [31:0]temp;
    reg [15:0]gain;

    parameter  vol_0 =  4'b0000;
    parameter DB_Neg6 = 4'b0001;
    parameter DB_Neg5 = 4'b0010;
    parameter DB_Neg4 = 4'b0011;
    parameter DB_Neg3 = 4'b0100;
    parameter DB_Neg3_pt2 = 4'b0101;
    parameter DB_Neg2 = 4'b0110;
    parameter DB_Neg1 = 4'b0111;
    parameter DB_0    = 4'b1000;
    parameter DB_Pos1 = 4'b1001;
    parameter DB_Pos1_pt2 = 4'b1010 ;
    parameter DB_Pos2 = 4'b1011;
    parameter DB_Pos3 = 4'b1100;
    parameter DB_Pos4 = 4'b1101;
    parameter DB_Pos5 = 4'b1110;
    parameter DB_Pos6 = 4'b1111;

    always @(*) begin
        case (control)

            vol_0 :   gain = 16'h0000;
            DB_Neg6 : gain = 16'h4027;
            DB_Neg5 : gain = 16'h47F9;
            DB_Neg4 : gain = 16'h50C5;
            DB_Neg3 : gain = 16'h5A9C;
            DB_Neg3_pt2 : gain = 16'h5A9C;
            DB_Neg2 : gain = 16'h65AC;
            DB_Neg1 : gain = 16'h7196;
            DB_0    : gain = 16'h8000;
            DB_Pos1 : gain = 16'h8FDE;
            DB_Pos1_pt2 : gain = 16'h8FDE;
            DB_Pos2 : gain = 16'hA124;
            DB_Pos3 : gain = 16'hB50D;
            DB_Pos4 : gain = 16'hCADE;
            DB_Pos5 : gain = 16'hE39F;
            DB_Pos6 : gain = 16'hFF66;

            default: gain = 16'h8000;;
        endcase

        temp = $signed(in) * $signed({1'b0, gain});

    end

    assign out = temp[30:15];
    
endmodule
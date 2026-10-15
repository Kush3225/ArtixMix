//Date - 20-08-2026
//Making it a Trimmer -> 0 db to -60 db

module top_module (
    input [11:0]in_ADC,
    input [15:0]in_SDC,
    output [23:0]out_vol // Given to EQ
);

    wire[3:0]out_adc;
    wire [23:0]out_more_bits;

    bitdepth_increase B1(.in(in_SDC), .out(out_more_bits));
    ADC_reducer A1(.in(in_ADC), .out(out_adc));
    vol_control Vol(.in(out_more_bits), .control(out_adc), .out(out_vol));
    
endmodule



module ADC_reducer (
    input [11:0]in, //input from ADC
    output [3:0]out
);

    assign out = in[11:8];
    
endmodule


module vol_control (
    input signed [23:0]in, //input from SD Card after widening
    input [3:0]control, //input from ADC_reducer
    output signed [23:0]out
);

    reg signed [41:0]temp;
    reg signed [17:0]gain;

    parameter  vol_0 =  4'b0000;
    parameter db_neg60 = 4'b0001;
    parameter db_neg56 = 4'b0010;
    parameter db_neg52 = 4'b0011;
    parameter db_neg48 = 4'b0100;
    parameter db_neg44 = 4'b0101;
    parameter db_neg40 = 4'b0110;
    parameter db_neg36 = 4'b0111;
    parameter db_neg32 = 4'b1000;
    parameter db_neg28 = 4'b1001;
    parameter db_neg24 = 4'b1010;
    parameter db_neg20 = 4'b1011;
    parameter db_neg16 = 4'b1100;
    parameter db_neg12  = 4'b1101;
    parameter db_neg8  = 4'b1110;
    parameter db_neg4  = 4'b1111;



    always @(*) begin
        case (control)

            vol_0    :  gain  = 18'h00000;
            db_neg60 :  gain  = 18'h00083; 
            db_neg56 :  gain  = 18'h000D0;
            db_neg52 :  gain  = 18'h00149;
            db_neg48 :  gain  = 18'h0020A;
            db_neg44 :  gain  = 18'h0033B;
            db_neg40 :  gain  = 18'h0051F;
            db_neg36 :  gain  = 18'h0081D;
            db_neg32 :  gain  = 18'h00CDC;
            db_neg28 :  gain  = 18'h01462;
            db_neg24 :  gain  = 18'h0204E;
            db_neg20 :  gain  = 18'h03333;
            db_neg16 :  gain  = 18'h05106;
            db_neg12 :  gain  = 18'h080DC;
            db_neg8  :  gain  = 18'h0CBE5;
            db_neg4  :  gain  = 18'h1430D;

            default: gain = 18'h1FFFF;
        endcase

        temp = in * gain;

    end

    assign out = temp[40:17];
    
endmodule


module testbench;

    reg [11:0]in_adc;
    reg [15:0]in_sdc;
    wire [23:0]out_vol;

    top_module uut(.in_ADC(in_adc), .in_SDC(in_sdc), .out_vol(out_vol));

    initial 
        begin
            in_adc = 0; 
            in_sdc = 0;
        end
    
    always
        begin
          #5 $display("Input from ADC = %d, Input from SDC = %d, Output = %d", in_adc, {in_sdc, 8'b0}, out_vol);
        end

    initial
        begin
            in_adc = 0; in_sdc = 16'h1000; //0000
            #5
            in_adc =  {4'b0001, 8'b0}; in_sdc = 16'h1000; 
            #5
            in_adc =  {4'b0010, 8'b0}; in_sdc = 16'h1000; 
            #5
            in_adc =  {4'b0011, 8'b0}; in_sdc = 16'h1000; 
            #5
            in_adc =  {4'b0100, 8'b0}; in_sdc = 16'h1000; 
            #5
            in_adc =  {4'b0101, 8'b0}; in_sdc = 16'h1000; 
            #5
            in_adc =  {4'b0110, 8'b0}; in_sdc = 16'h1000; 
            #5
            in_adc =  {4'b0111, 8'b0}; in_sdc = 16'h1000; 
            #5
            in_adc =  {4'b1000, 8'b0}; in_sdc = 16'h1000; 
            #5
            in_adc =  {4'b1001, 8'b0}; in_sdc = 16'h1000; 
            #5
            in_adc =  {4'b1010, 8'b0}; in_sdc = 16'h1000; 
            #5
            in_adc =  {4'b1011, 8'b0}; in_sdc = 16'h1000; 
            #5
            in_adc =  {4'b1100, 8'b0}; in_sdc = 16'h1000; 
            #5
            in_adc =  {4'b1101, 8'b0}; in_sdc = 16'h1000; 
            #5
            in_adc =  {4'b1110, 8'b0}; in_sdc = 16'h1000; 
            #5
            in_adc =  {4'b1111, 8'b0}; in_sdc = 16'h1000; 
            #5
            $finish;
        end


endmodule


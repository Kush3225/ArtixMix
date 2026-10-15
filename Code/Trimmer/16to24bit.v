module bitdepth_increase (
    input signed [15:0]in,
    output signed [23:0]out
);

    assign out = {in, 8'b0};
    
endmodule
//Time Scale for whatever you are using to simulate. 1st term is the delay every time you write #delay
//So in this case #1 means 1ns #2 is 2 ns. 2nd term is the time step the simulator will take to evaluate signals.
//So every 1ns is divided by 1000 ie 1ps of time step

`timescale 1ns / 1ps

module tb();    //test bench module , top level so no inputs or outputs

    //All the inputs to the module you want to test will be registers
    reg clk;
    reg rst;
    reg in1;
    reg in2;
    //All the outputs will be wires
    wire out1;
    wire out2;

    module_to_test DUT( //Instantiate the module you want to test , hook up the ports.
        .clk(clk),
        .rst(rst),
        .in1(in1),
        .in2(in2),
        .out1(out1),
        .out2(out2)
    );

    initial begin   //Define the initial conditions
        clk = 0;
        rst = 1;
        in1 = 1;
        in2 = 0;

        forever #5 clk = ~clk;  //Toggle Clock every 5ns , So a clock cycle of 10ns
    end
    
    initial begin
        //Heres where you will actually give inputs after every some time.
        rst = 1;
        #20;        //Hold Reset for some time

        in1 = 5;
        in2 = 10;   
        #50;

        in1 = 10;
        in2 = 20;
        #50;

        $finish;    //Command for simulator to stop.
    end

    //Add a display statement in your module whenever done is asserted so it can actually print something.
    // $display("RESULT: %h, TIME: %0t", result, $time) //Prints result in hex. %d for decimal shayad not sure.

endmodule
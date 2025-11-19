
// enigma.v — Verilog-2001, Icarus-friendly
module enigma_core (
  input  wire       clk,
  input  wire       rst_n,
  input  wire       ena,

  input  wire [4:0] din,        // 0..25 = A..Z
  input  wire       confirm,    // one pulse per char
  input  wire       reset_btn,  // set pos to 12,11,25

  output reg  [4:0] dout,
  output reg        valid
);

  // ===== LUTs as reg arrays, filled in initial block =====
  reg [4:0] ROT3_FWD [0:25];
  reg [4:0] ROT1_FWD [0:25];
  reg [4:0] ROT4_FWD [0:25];
  reg [4:0] UKWB_FWD [0:25];

  initial begin
    // ROTOR III
    ROT3_FWD[ 0]=5'd1;  ROT3_FWD[ 1]=5'd3;  ROT3_FWD[ 2]=5'd5;  ROT3_FWD[ 3]=5'd7;
    ROT3_FWD[ 4]=5'd9;  ROT3_FWD[ 5]=5'd11; ROT3_FWD[ 6]=5'd2;  ROT3_FWD[ 7]=5'd15;
    ROT3_FWD[ 8]=5'd17; ROT3_FWD[ 9]=5'd19; ROT3_FWD[10]=5'd23; ROT3_FWD[11]=5'd21;
    ROT3_FWD[12]=5'd25; ROT3_FWD[13]=5'd13; ROT3_FWD[14]=5'd12; ROT3_FWD[15]=5'd14;
    ROT3_FWD[16]=5'd16; ROT3_FWD[17]=5'd10; ROT3_FWD[18]=5'd22; ROT3_FWD[19]=5'd20;
    ROT3_FWD[20]=5'd18; ROT3_FWD[21]=5'd24; ROT3_FWD[22]=5'd8;  ROT3_FWD[23]=5'd4;
    ROT3_FWD[24]=5'd0;  ROT3_FWD[25]=5'd6;

    // ROTOR I
    ROT1_FWD[ 0]=5'd4;  ROT1_FWD[ 1]=5'd10; ROT1_FWD[ 2]=5'd12; ROT1_FWD[ 3]=5'd5;
    ROT1_FWD[ 4]=5'd11; ROT1_FWD[ 5]=5'd6;  ROT1_FWD[ 6]=5'd3;  ROT1_FWD[ 7]=5'd16;
    ROT1_FWD[ 8]=5'd21; ROT1_FWD[ 9]=5'd25; ROT1_FWD[10]=5'd13; ROT1_FWD[11]=5'd19;
    ROT1_FWD[12]=5'd14; ROT1_FWD[13]=5'd22; ROT1_FWD[14]=5'd24; ROT1_FWD[15]=5'd7;
    ROT1_FWD[16]=5'd23; ROT1_FWD[17]=5'd20; ROT1_FWD[18]=5'd18; ROT1_FWD[19]=5'd15;
    ROT1_FWD[20]=5'd0;  ROT1_FWD[21]=5'd8;  ROT1_FWD[22]=5'd1;  ROT1_FWD[23]=5'd17;
    ROT1_FWD[24]=5'd2;  ROT1_FWD[25]=5'd9;

    // ROTOR IV
    ROT4_FWD[ 0]=5'd4;  ROT4_FWD[ 1]=5'd18; ROT4_FWD[ 2]=5'd14; ROT4_FWD[ 3]=5'd21;
    ROT4_FWD[ 4]=5'd15; ROT4_FWD[ 5]=5'd25; ROT4_FWD[ 6]=5'd9;  ROT4_FWD[ 7]=5'd0;
    ROT4_FWD[ 8]=5'd16; ROT4_FWD[ 9]=5'd20; ROT4_FWD[10]=5'd8;  ROT4_FWD[11]=5'd17;
    ROT4_FWD[12]=5'd7;  ROT4_FWD[13]=5'd11; ROT4_FWD[14]=5'd3;  ROT4_FWD[15]=5'd13;
    ROT4_FWD[16]=5'd6;  ROT4_FWD[17]=5'd22; ROT4_FWD[18]=5'd1;  ROT4_FWD[19]=5'd10;
    ROT4_FWD[20]=5'd5;  ROT4_FWD[21]=5'd12; ROT4_FWD[22]=5'd2;  ROT4_FWD[23]=5'd23;
    ROT4_FWD[24]=5'd24; ROT4_FWD[25]=5'd19;

    // REFLECTOR UKW-B
    UKWB_FWD[ 0]=5'd24; UKWB_FWD[ 1]=5'd17; UKWB_FWD[ 2]=5'd20; UKWB_FWD[ 3]=5'd7;
    UKWB_FWD[ 4]=5'd16; UKWB_FWD[ 5]=5'd19; UKWB_FWD[ 6]=5'd11; UKWB_FWD[ 7]=5'd3;
    UKWB_FWD[ 8]=5'd23; UKWB_FWD[ 9]=5'd13; UKWB_FWD[10]=5'd12; UKWB_FWD[11]=5'd14;
    UKWB_FWD[12]=5'd6;  UKWB_FWD[13]=5'd9;  UKWB_FWD[14]=5'd10; UKWB_FWD[15]=5'd5;
    UKWB_FWD[16]=5'd0;  UKWB_FWD[17]=5'd25; UKWB_FWD[18]=5'd4;  UKWB_FWD[19]=5'd22;
    UKWB_FWD[20]=5'd15; UKWB_FWD[21]=5'd21; UKWB_FWD[22]=5'd2;  UKWB_FWD[23]=5'd18;
    UKWB_FWD[24]=5'd8;  UKWB_FWD[25]=5'd1;
  end

  // ===== Notches
  localparam [4:0] NOTCH_I   = 5'd16; // Q
  localparam [4:0] NOTCH_III = 5'd21; // V

  // ===== Positions (right=III, mid=I, left=IV)
  reg [4:0] pos_r, pos_m, pos_l;

  // ===== Control + temps
  reg       busy;
  reg [4:0] din_q;
  reg       notch_r, notch_m;
  reg [4:0] s0, s1, s2, s3, s4, s5, s6, res;

  // ===== Helpers
  function [4:0] add26;
    input [5:0] a;
    reg   [5:0] t;
    begin
      t = a;
      if (t >= 6'd26) t = t - 6'd26;  // no (expr)[slice]
      add26 = t[4:0];
    end
  endfunction

  function [4:0] rotor_fwd;
    input [4:0] sym;
    input [4:0] pos;
    input [1:0] which;     // 0=III,1=I,2=IV
    reg   [4:0] idx, o;
    begin
      idx = add26(sym + pos);
      if (which==2'd0)       o = ROT3_FWD[idx];
      else if (which==2'd1)  o = ROT1_FWD[idx];
      else                   o = ROT4_FWD[idx];
      rotor_fwd = add26(o + 6'd26 - pos);
    end
  endfunction

  function [4:0] rotor_inv;
    input [4:0] sym;
    input [4:0] pos;
    input [1:0] which;    // 0=III,1=I,2=IV
    integer k;
    reg [4:0] tgt, idx;
    begin
      tgt = add26(sym + pos);
      idx = 5'd0;
      if (which==2'd0) begin
        for (k=0;k<26;k=k+1) if (ROT3_FWD[k]==tgt) idx = k;   // rely on truncation
      end else if (which==2'd1) begin
        for (k=0;k<26;k=k+1) if (ROT1_FWD[k]==tgt) idx = k;
      end else begin
        for (k=0;k<26;k=k+1) if (ROT4_FWD[k]==tgt) idx = k;
      end
      rotor_inv = add26(idx + 6'd26 - pos);
    end
  endfunction

  function [4:0] refl;
    input [4:0] sym;
    begin
      refl = UKWB_FWD[sym];
    end
  endfunction

  // ===== Sequential
  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      pos_r <= 5'd12;
      pos_m <= 5'd11;
      pos_l <= 5'd25;
      busy  <= 1'b0;
      valid <= 1'b0;
      dout  <= 5'd0;
      din_q <= 5'd0;
    end else if (ena) begin
      valid <= 1'b0;

      if (reset_btn) begin
        pos_r <= 5'd12; pos_m <= 5'd11; pos_l <= 5'd25;
      end

      // Latch + step
      if (confirm && !busy && (din < 5'd26)) begin
        busy  <= 1'b1;
        din_q <= din;

        notch_r <= (pos_r == NOTCH_III);
        notch_m <= (pos_m == NOTCH_I);

        // double-step behaviour
        pos_l <= add26(pos_l + (notch_m ? 6'd1 : 6'd0));
        pos_m <= add26(pos_m + ((notch_r || notch_m) ? 6'd1 : 6'd0));
        pos_r <= add26(pos_r + 6'd1);
      end

      // Compute output next cycle
      if (busy) begin
        s0  = din_q;
        s1  = rotor_fwd(s0, pos_r, 2'd0);
        s2  = rotor_fwd(s1, pos_m, 2'd1);
        s3  = rotor_fwd(s2, pos_l, 2'd2);
        s4  = refl(s3);
        s5  = rotor_inv(s4, pos_l, 2'd2);
        s6  = rotor_inv(s5, pos_m, 2'd1);
        res = rotor_inv(s6, pos_r, 2'd0);

        dout  <= res;
        valid <= 1'b1;
        busy  <= 1'b0;
      end
    end
  end
endmodule

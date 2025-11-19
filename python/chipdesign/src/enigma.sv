// enigma.sv — Enigma core, Icarus-friendly
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

  // === LUTs (SystemVerilog array params OK with -g2012)
  localparam [4:0] ROT3_FWD [0:25] = '{
    1,3,5,7,9,11,2,15,17,19,23,21,25,13,12,14,16,10,22,20,18,24,8,4,0,6
  };
  localparam [4:0] ROT1_FWD [0:25] = '{ // I
    4,10,12,5,11,6,3,16,21,25,13,19,14,22,24,7,23,20,18,15,0,8,1,17,2,9
  };
  localparam [4:0] ROT4_FWD [0:25] = '{ // IV
    4,18,14,21,15,25,9,0,16,20,8,17,7,11,3,13,6,22,1,10,5,12,2,23,24,19
  };
  localparam [4:0] UKWB_FWD [0:25] = '{ // UKW-B
    24,17,20,7,16,19,11,3,23,13,12,14,6,9,10,5,0,25,4,22,15,21,2,18,8,1
  };

  // === Notches
  localparam [4:0] NOTCH_I   = 5'd16; // Q
  localparam [4:0] NOTCH_III = 5'd21; // V
  localparam [4:0] NOTCH_IV  = 5'd9;  // J (left rotor IV, unused for stepping here)

  // === Positions (right=III, mid=I, left=IV)
  reg [4:0] pos_r, pos_m, pos_l;

  // === Control
  reg       busy;
  reg [4:0] din_q;

  // === Temporaries declared at module scope (avoid block-local decls)
  reg       notch_r, notch_m;
  reg [4:0] s0, s1, s2, s3, s4, s5, s6, res;

  // === Helpers
  function automatic [4:0] add26(input [5:0] a);
    add26 = (a >= 6'd26) ? (a - 6'd26) [4:0] : a[4:0];
  endfunction

  function automatic [4:0] rotor_fwd(input [4:0] sym,
                                     input [4:0] pos,
                                     input integer which);
    reg [4:0] idx, o;
    begin
      idx = add26(sym + pos);
      case (which)
        0: o = ROT3_FWD[idx];
        1: o = ROT1_FWD[idx];
        default: o = ROT4_FWD[idx];
      endcase
      rotor_fwd = add26(o + 6'd26 - pos);
    end
  endfunction

  function automatic [4:0] rotor_inv(input [4:0] sym,
                                     input [4:0] pos,
                                     input integer which);
    integer k;
    reg [4:0] tgt, idx;
    begin
      tgt = add26(sym + pos);
      idx = 5'd0;
      if (which==0) begin
        for (k=0;k<26;k=k+1) if (ROT3_FWD[k]==tgt) idx = k[4:0];
      end else if (which==1) begin
        for (k=0;k<26;k=k+1) if (ROT1_FWD[k]==tgt) idx = k[4:0];
      end else begin
        for (k=0;k<26;k=k+1) if (ROT4_FWD[k]==tgt) idx = k[4:0];
      end
      rotor_inv = add26(idx + 6'd26 - pos);
    end
  endfunction

  function automatic [4:0] refl(input [4:0] sym);
    refl = UKWB_FWD[sym];
  endfunction

  // === Sequential
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
        pos_r <= 5'd12;
        pos_m <= 5'd11;
        pos_l <= 5'd25;
      end

      // Latch input + step (historically before routing)
      if (confirm && !busy && (din < 5'd26)) begin
        busy  <= 1'b1;
        din_q <= din;

        notch_r <= (pos_r == NOTCH_III);
        notch_m <= (pos_m == NOTCH_I);

        pos_l <= add26(pos_l + (notch_m ? 6'd1 : 6'd0));
        pos_m <= add26(pos_m + ((notch_r || notch_m) ? 6'd1 : 6'd0));
        pos_r <= add26(pos_r + 6'd1);
      end

      // Compute output next cycle with updated positions
      if (busy) begin
        s0  = din_q;
        s1  = rotor_fwd(s0, pos_r, 0);
        s2  = rotor_fwd(s1, pos_m, 1);
        s3  = rotor_fwd(s2, pos_l, 2);
        s4  = refl(s3);
        s5  = rotor_inv(s4, pos_l, 2);
        s6  = rotor_inv(s5, pos_m, 1);
        res = rotor_inv(s6, pos_r, 0);

        dout  <= res;
        valid <= 1'b1;
        busy  <= 1'b0;
      end
    end
  end
endmodule

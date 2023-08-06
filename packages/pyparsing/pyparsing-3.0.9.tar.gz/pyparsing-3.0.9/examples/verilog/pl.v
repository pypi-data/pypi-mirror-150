/////////////////////////////////////////////////////////////////////
////                                                             ////
////  Protocol Layer                                             ////
////  This block is typically referred to as the SEI in USB      ////
////  Specification. It encapsulates the Packet Assembler,       ////
////  disassembler, protocol engine and internal DMA             ////
////                                                             ////
////  Author: Rudolf Usselmann                                   ////
////          rudi@asics.ws                                      ////
////                                                             ////
////                                                             ////
////  Downloaded from: http://www.opencores.org/cores/usb/       ////
////                                                             ////
/////////////////////////////////////////////////////////////////////
////                                                             ////
//// Copyright (C) 2000 Rudolf Usselmann                         ////
////                    rudi@asics.ws                            ////
////                                                             ////
//// This source file may be used and distributed without        ////
//// restriction provided that this copyright statement is not   ////
//// removed from the file and that any derivative work contains ////
//// the original copyright notice and the associated disclaimer.////
////                                                             ////
////     THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY     ////
//// EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED   ////
//// TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS   ////
//// FOR A PARTICULAR PURPOSE. IN NO EVENT SHALL THE AUTHOR      ////
//// OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,         ////
//// INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES    ////
//// (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE   ////
//// GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR        ////
//// BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF  ////
//// LIABILITY, WHETHER IN  CONTRACT, STRICT LIABILITY, OR TORT  ////
//// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT  ////
//// OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE         ////
//// POSSIBILITY OF SUCH DAMAGE.                                 ////
////                                                             ////
/////////////////////////////////////////////////////////////////////

//  CVS Log
//
//  $Id: pl.v,v 1.0 2001/03/07 09:17:12 rudi Exp $
//
//  $Date: 2001/03/07 09:17:12 $
//  $Revision: 1.0 $
//  $Author: rudi $
//  $Locker:  $
//  $State: Exp $
//
// Change History:
//               $Log: pl.v,v $
//               Revision 1.0  2001/03/07 09:17:12  rudi
//
//
//               Changed all revisions to revision 1.0. This is because OpenCores CVS
//               interface could not handle the original '0.1' revision ....
//
//               Revision 0.1.0.1  2001/02/28 08:11:11  rudi
//               Initial Release
//
//

`include "usb_defines.v"

module pl(  clk, rst,

        // UTMI Interface
        rx_data, rx_valid, rx_active, rx_err,
        tx_data, tx_valid, tx_valid_last, tx_ready,
        tx_first, tx_valid_out,
        mode_hs, usb_reset, usb_suspend, usb_attached,

        // memory interface
        madr, mdout, mdin, mwe, mreq, mack,

        // Register File Interface
        fa, idin,
        ep_sel, match,
        dma_in_buf_sz1, dma_out_buf_avail,
        buf0_rl, buf0_set, buf1_set,
        uc_bsel_set, uc_dpd_set,

        int_buf1_set, int_buf0_set, int_upid_set,
        int_crc16_set, int_to_set, int_seqerr_set,

        csr, buf0, buf1,

        // Misc
        frm_nat,
        pid_cs_err, nse_err,
        crc5_err

        );

// UTMI Interface
input       clk, rst;
input   [7:0]   rx_data;
input       rx_valid, rx_active, rx_err;
output  [7:0]   tx_data;
output      tx_valid;
output      tx_valid_last;
input       tx_ready;
output      tx_first;
input       tx_valid_out;
input       mode_hs;    // High Speed Mode
input       usb_reset;  // USB Reset
input       usb_suspend;    // USB Suspend
input       usb_attached;   // Attached to USB


// Memory Arbiter Interface
output  [14:0]  madr;       // word address
output  [31:0]  mdout;
input   [31:0]  mdin;
output      mwe;
output      mreq;
input       mack;


// Register File interface
input   [6:0]   fa;     // Function Address (as set by the controller)
output  [31:0]  idin;       // Data Input
output  [3:0]   ep_sel;     // Endpoint Number Input
input       match;      // Endpoint Matched
input       dma_in_buf_sz1;
input       dma_out_buf_avail;
output      nse_err;    // no such endpoint error

output      buf0_rl;    // Reload Buf 0 with original values
output      buf0_set;   // Write to buf 0
output      buf1_set;   // Write to buf 1
output      uc_bsel_set;    // Write to the uc_bsel field
output      uc_dpd_set; // Write to the uc_dpd field
output      int_buf1_set;   // Set buf1 full/empty interrupt
output      int_buf0_set;   // Set buf0 full/empty interrupt
output      int_upid_set;   // Set unsupported PID interrupt
output      int_crc16_set;  // Set CRC16 error interrupt
output      int_to_set; // Set time out interrupt
output      int_seqerr_set; // Set PID sequence error interrupt

input   [31:0]  csr;        // Internal CSR Output
input   [31:0]  buf0;       // Internal Buf 0 Output
input   [31:0]  buf1;       // Internal Buf 1 Output

// Misc
output      pid_cs_err; // pid checksum error
output      crc5_err;   // crc5 error
output  [31:0]  frm_nat;


///////////////////////////////////////////////////////////////////
//
// Local Wires and Registers
//

// Packet Disassembler Interface
wire        clk, rst;
wire    [7:0]   rx_data;
wire        rx_valid, rx_active, rx_err;
wire        pid_OUT, pid_IN, pid_SOF, pid_SETUP;
wire        pid_DATA0, pid_DATA1, pid_DATA2, pid_MDATA;
wire        pid_ACK, pid_NACK, pid_STALL, pid_NYET;
wire        pid_PRE, pid_ERR, pid_SPLIT, pid_PING;
wire    [6:0]   token_fadr;
wire        token_valid;
wire        crc5_err;
wire    [11:0]  frame_no;
wire    [7:0]   rx_data_st;
wire        rx_data_valid;
wire        rx_data_done;
wire        crc16_err;
wire        rx_seq_err;

// Packet Assembler Interface
wire        send_token;
wire    [1:0]   token_pid_sel;
wire        send_data;
wire    [1:0]   data_pid_sel;
wire    [7:0]   tx_data_st;
wire        rd_next;

// IDMA Interface
wire        rx_dma_en;  // Allows the data to be stored
wire        tx_dma_en;  // Allows for data to be retrieved
wire        abort;      // Abort Transfer (time_out, crc_err or rx_error)
wire        idma_done;  // DMA is done
wire    [16:0]  adr;        // Byte Address
wire    [13:0]  size;       // Size in bytes
wire    [10:0]  sizu_c;     // Up and Down counting size registers, used
                // to update
wire    [13:0]  buf_size;   // Actual buffer size
wire        dma_en;     // external dma enabled

// Memory Arbiter Interface
wire    [14:0]  madr;       // word address
wire    [31:0]  mdout;
wire    [31:0]  mdin;
wire        mwe;
wire        mreq;
wire        mack;

// Local signals
wire        pid_bad, pid_bad1, pid_bad2;

reg     hms_clk;    // 0.5 Micro Second Clock
reg [4:0]   hms_cnt;

reg [11:0]  frame_no_r; // Current Frame Number register
wire        frame_no_we;
reg     frame_no_same;  // Indicates current and prev. frame numbers
                // are equal
reg [3:0]   mfm_cnt;    // Micro Frame Counter
reg [11:0]  sof_time;   // Time since last sof
reg     clr_sof_time;

wire        fsel;       // This Function is selected

wire        match_o;

///////////////////////////////////////////////////////////////////
//
// Misc Logic
//


// PIDs we should never receive
assign pid_bad1 = pid_ACK | pid_NACK | pid_STALL | pid_NYET | pid_PRE |
            pid_ERR | pid_SPLIT;

// PIDs we should never get in full speed mode (high speed mode only)
assign pid_bad2 = !mode_hs & pid_PING;

// All bad pids
assign pid_bad = pid_bad1 | pid_bad2;

assign match_o = !pid_bad & match & token_valid & !crc5_err;

// Frame Number (from SOF token)
reg frame_no_we_r;

assign frame_no_we = token_valid & !crc5_err & pid_SOF;

always @(posedge clk)
    frame_no_we_r <= #1 frame_no_we;

always @(posedge clk)
    if(!rst)    frame_no_r <= #1 0;
    else
    if(frame_no_we) frame_no_r <= #1 frame_no;

// Micro Frame Counter
always @(posedge clk)
    frame_no_same <= #1 frame_no_we & (frame_no_r == frame_no);

always @(posedge clk)
    if(!rst)        mfm_cnt <= #1 0;
    else
    if(frame_no_we & !frame_no_same)
                mfm_cnt <= #1 0;
    else
    if(frame_no_same)   mfm_cnt <= #1 mfm_cnt + 1;

//SOF delay counter
always @(posedge clk)
    clr_sof_time <= #1 frame_no_we;

always @(posedge clk)
    if(clr_sof_time)    sof_time <= #1 0;
    else
    if(hms_clk)     sof_time <= #1 sof_time + 1;

assign frm_nat = {mfm_cnt, frame_no_r, 4'h0, sof_time};


// 0.5 Micro Seconds Clock Generator
always @(posedge clk)
    if(!rst | hms_clk | frame_no_we)    hms_cnt <= #1 0;
    else                    hms_cnt <= #1 hms_cnt + 1;

//always @(posedge clk)
//    hms_clk <= #1 (hms_cnt == `HMS_DEL);

///////////////////////////////////////////////////////////////////

// This function is addressed
assign fsel = (token_fadr == fa);

///////////////////////////////////////////////////////////////////
//
// Module Instantiations
//

//Packet Decoder
pd  u0( .clk(       clk     ),
        .rst(       rst     ),
        .rx_data(   rx_data     ),
        .rx_valid(  rx_valid    ),
        .rx_active( rx_active   ),
        .rx_err(    rx_err      ),
        .pid_OUT(   pid_OUT     ),
        .pid_IN(    pid_IN      ),
        .pid_SOF(   pid_SOF     ),
        .pid_SETUP( pid_SETUP   ),
        .pid_DATA0( pid_DATA0   ),
        .pid_DATA1( pid_DATA1   ),
        .pid_DATA2( pid_DATA2   ),
        .pid_MDATA( pid_MDATA   ),
        .pid_ACK(   pid_ACK     ),
        .pid_NACK(  pid_NACK    ),
        .pid_STALL( pid_STALL   ),
        .pid_NYET(  pid_NYET    ),
        .pid_PRE(   pid_PRE     ),
        .pid_ERR(   pid_ERR     ),
        .pid_SPLIT( pid_SPLIT   ),
        .pid_PING(  pid_PING    ),
        .pid_cks_err(   pid_cs_err  ),
        .token_fadr(    token_fadr  ),
        .token_endp(    ep_sel      ),
        .token_valid(   token_valid ),
        .crc5_err(  crc5_err    ),
        .frame_no(  frame_no    ),
        .rx_data_st(    rx_data_st  ),
        .rx_data_valid( rx_data_valid   ),
        .rx_data_done(  rx_data_done    ),
        .crc16_err( crc16_err   ),
        .seq_err(   rx_seq_err  )
        );

// Packet Assembler
pa  u1( .clk(       clk     ),
        .rst(       rst     ),
        .tx_data(   tx_data     ),
        .tx_valid(  tx_valid    ),
        .tx_valid_last( tx_valid_last   ),
        .tx_ready(  tx_ready    ),
        .tx_first(  tx_first    ),
        .send_token(    send_token  ),
        .token_pid_sel( token_pid_sel   ),
        .send_data( send_data   ),
        .data_pid_sel(  data_pid_sel    ),
        .tx_data_st(    tx_data_st  ),
        .rd_next(   rd_next     )
        );

// Internal DMA / Memory Arbiter Interface
idma    u2( .clk(       clk     ),
        .rst(       rst     ),
        .rx_data_st(    rx_data_st  ),
        .rx_data_valid( rx_data_valid   ),
        .rx_data_done(  rx_data_done    ),
        .send_data( send_data   ),
        .tx_data_st(    tx_data_st  ),
        .rd_next(   rd_next     ),
        .rx_dma_en( rx_dma_en   ),
        .tx_dma_en( tx_dma_en   ),
        .abort(     abort       ),
        .idma_done( idma_done   ),
        .adr(       adr     ),
        .size(      size        ),
        .buf_size(  buf_size    ),
        .dma_en(    dma_en      ),
        .madr(      madr        ),
        .sizu_c(    sizu_c      ),
        .mdout(     mdout       ),
        .mdin(      mdin        ),
        .mwe(       mwe     ),
        .mreq(      mreq        ),
        .mack(      mack        )
        );

// Protocol Engine
pe  u3( .clk(           clk         ),
        .rst(           rst         ),
        .tx_valid(      tx_valid_out        ),
        .rx_active(     rx_active       ),
        .pid_OUT(       pid_OUT         ),
        .pid_IN(        pid_IN          ),
        .pid_SOF(       pid_SOF         ),
        .pid_SETUP(     pid_SETUP       ),
        .pid_DATA0(     pid_DATA0       ),
        .pid_DATA1(     pid_DATA1       ),
        .pid_DATA2(     pid_DATA2       ),
        .pid_MDATA(     pid_MDATA       ),
        .pid_ACK(       pid_ACK         ),
        .pid_NACK(      pid_NACK        ),
        .pid_STALL(     pid_STALL       ),
        .pid_NYET(      pid_NYET        ),
        .pid_PRE(       pid_PRE         ),
        .pid_ERR(       pid_ERR         ),
        .pid_SPLIT(     pid_SPLIT       ),
        .pid_PING(      pid_PING        ),
        .mode_hs(       mode_hs         ),
        .token_valid(       token_valid     ),
        .crc5_err(      crc5_err        ),
        .rx_data_valid(     rx_data_valid       ),
        .rx_data_done(      rx_data_done        ),
        .crc16_err(     crc16_err       ),
        .send_token(        send_token      ),
        .token_pid_sel(     token_pid_sel       ),
        .data_pid_sel(      data_pid_sel        ),
        .rx_dma_en(     rx_dma_en       ),
        .tx_dma_en(     tx_dma_en       ),
        .abort(         abort           ),
        .idma_done(     idma_done       ),
        .adr(           adr         ),
        .size(          size            ),
        .buf_size(      buf_size        ),
        .sizu_c(        sizu_c          ),
        .dma_en(        dma_en          ),
        .fsel(          fsel            ),
        .idin(          idin            ),
        .ep_sel(        ep_sel          ),
        .match(         match_o         ),
        .dma_in_buf_sz1(    dma_in_buf_sz1      ),
        .dma_out_buf_avail( dma_out_buf_avail   ),
        .nse_err(       nse_err         ),
        .buf0_rl(       buf0_rl         ),
        .buf0_set(      buf0_set        ),
        .buf1_set(      buf1_set        ),
        .uc_bsel_set(       uc_bsel_set     ),
        .uc_dpd_set(        uc_dpd_set      ),
        .int_buf1_set(      int_buf1_set        ),
        .int_buf0_set(      int_buf0_set        ),
        .int_upid_set(      int_upid_set        ),
        .int_crc16_set(     int_crc16_set       ),
        .int_to_set(        int_to_set      ),
        .int_seqerr_set(    int_seqerr_set      ),
        .csr(           csr         ),
        .buf0(          buf0            ),
        .buf1(          buf1            )
        );

endmodule


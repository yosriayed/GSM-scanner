#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Scanner Grc
# Generated: Sun Oct 25 10:37:44 2015
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import time

class scanner_grc(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Scanner Grc")

        ##################################################
        # Variables
        ##################################################
        self.f_symb = f_symb = 1625000.0/6.0
        self.f_900_b = f_900_b = 921.2e6
        self.samp_rate = samp_rate = f_symb*4
        self.fs = fs = f_900_b
        self.f_900_e = f_900_e = 959.8e6
        self.f_1800_e = f_1800_e = 1879.8e6
        self.f_1800_b = f_1800_b = 1805.2e6
        self.OSR = OSR = 4

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "bladerf=0" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(fs, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(2, 0)
        self.osmosdr_source_0.set_gain_mode(True, 0)
        self.osmosdr_source_0.set_gain(30, 0)
        self.osmosdr_source_0.set_if_gain(30, 0)
        self.osmosdr_source_0.set_bb_gain(30, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(200000, 0)
          
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 200e3, 10e3, firdes.WIN_HAMMING, 6.76))
        self.threshold_result = blocks.threshold_ff(0, 0.2, 0)
        self.blocks_threshold_ff_0_0 = blocks.threshold_ff(0, 0, 0)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(int((138)*samp_rate/f_symb), int((138)*samp_rate/f_symb), 0)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(1)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(int((142)*samp_rate/f_symb), 1, int(1e6))
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, int(OSR))
        self.blocks_complex_to_arg_0 = blocks.complex_to_arg(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_arg_0, 0), (self.blocks_threshold_ff_0_0, 0))    
        self.connect((self.blocks_delay_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))    
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_threshold_ff_0, 0))    
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.blocks_complex_to_arg_0, 0))    
        self.connect((self.blocks_threshold_ff_0, 0), (self.threshold_result, 0))    
        self.connect((self.blocks_threshold_ff_0_0, 0), (self.blocks_moving_average_xx_0, 0))    
        self.connect((self.threshold_result, 0), (self.blocks_null_sink_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.blocks_delay_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_conjugate_cc_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.low_pass_filter_0, 0))    


    def get_f_symb(self):
        return self.f_symb

    def set_f_symb(self, f_symb):
        self.f_symb = f_symb
        self.set_samp_rate(self.f_symb*4)
        self.blocks_moving_average_xx_0.set_length_and_scale(int((142)*self.samp_rate/self.f_symb), 1)
        self.blocks_threshold_ff_0.set_hi(int((138)*self.samp_rate/self.f_symb))
        self.blocks_threshold_ff_0.set_lo(int((138)*self.samp_rate/self.f_symb))

    def get_f_900_b(self):
        return self.f_900_b

    def set_f_900_b(self, f_900_b):
        self.f_900_b = f_900_b
        self.set_fs(self.f_900_b)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_moving_average_xx_0.set_length_and_scale(int((142)*self.samp_rate/self.f_symb), 1)
        self.blocks_threshold_ff_0.set_hi(int((138)*self.samp_rate/self.f_symb))
        self.blocks_threshold_ff_0.set_lo(int((138)*self.samp_rate/self.f_symb))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 200e3, 10e3, firdes.WIN_HAMMING, 6.76))
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)

    def get_fs(self):
        return self.fs

    def set_fs(self, fs):
        self.fs = fs
        self.osmosdr_source_0.set_center_freq(self.fs, 0)

    def get_f_900_e(self):
        return self.f_900_e

    def set_f_900_e(self, f_900_e):
        self.f_900_e = f_900_e

    def get_f_1800_e(self):
        return self.f_1800_e

    def set_f_1800_e(self, f_1800_e):
        self.f_1800_e = f_1800_e

    def get_f_1800_b(self):
        return self.f_1800_b

    def set_f_1800_b(self, f_1800_b):
        self.f_1800_b = f_1800_b

    def get_OSR(self):
        return self.OSR

    def set_OSR(self, OSR):
        self.OSR = OSR
        self.blocks_delay_0.set_dly(int(self.OSR))


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = scanner_grc()
    tb.start()
    tb.wait()

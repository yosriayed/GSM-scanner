#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Gsm Reciever
# Generated: Thu Oct 22 12:31:42 2015
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import grgsm
import osmosdr
import time

class GSM_reciever(gr.top_block):

    def __init__(self, fc=927.2e6):
        gr.top_block.__init__(self, "Gsm Reciever")

        ##################################################
        # Parameters
        ##################################################
        self.fc = fc

        ##################################################
        # Variables
        ##################################################
        self.f_symb = f_symb = 1625000.0/6.0
        self.samp_rate = samp_rate = f_symb*4
        self.f_900_e = f_900_e = 959.8e6
        self.f_900_b = f_900_b = 921.2e6
        self.f_1800_e = f_1800_e = 1879.8e6
        self.f_1800_b = f_1800_b = 1805.2e6
        self.OSR = OSR = 4
        self.CCCH = CCCH = 2
        self.BCCH = BCCH = 1

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "bladerf=0" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(fc, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(True, 0)
        self.osmosdr_source_0.set_gain(30, 0)
        self.osmosdr_source_0.set_if_gain(30, 0)
        self.osmosdr_source_0.set_bb_gain(30, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(200000, 0)
          
        self.gsm_universal_ctrl_chans_demapper_0 = grgsm.universal_ctrl_chans_demapper(0, ([2,6,12,16,22,26,32,36,42,46]), ([BCCH,CCCH,CCCH,CCCH,CCCH,CCCH,CCCH,CCCH,CCCH,CCCH]))
        self.gsm_receiver_0 = grgsm.receiver(4, ([0]), ([]))
        self.gsm_input_0 = grgsm.gsm_input(
            ppm=0,
            osr=4,
            fc=fc,
            samp_rate_in=samp_rate,
        )
        self.gsm_control_channels_decoder_0 = grgsm.control_channels_decoder()
        self.gsm_clock_offset_control_0 = grgsm.clock_offset_control(fc)
        self.blocks_socket_pdu_0 = blocks.socket_pdu("UDP_CLIENT", "127.0.0.1", "4729", 10000, False)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.gsm_clock_offset_control_0, 'ppm'), (self.gsm_input_0, 'ppm_in'))    
        self.msg_connect((self.gsm_control_channels_decoder_0, 'msgs'), (self.blocks_socket_pdu_0, 'pdus'))    
        self.msg_connect((self.gsm_receiver_0, 'measurements'), (self.gsm_clock_offset_control_0, 'measurements'))    
        self.msg_connect((self.gsm_receiver_0, 'C0'), (self.gsm_universal_ctrl_chans_demapper_0, 'bursts'))    
        self.msg_connect((self.gsm_universal_ctrl_chans_demapper_0, 'bursts'), (self.gsm_control_channels_decoder_0, 'bursts'))    
        self.connect((self.gsm_input_0, 0), (self.gsm_receiver_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.gsm_input_0, 0))    


    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.gsm_input_0.set_fc(self.fc)
        self.osmosdr_source_0.set_center_freq(self.fc, 0)

    def get_f_symb(self):
        return self.f_symb

    def set_f_symb(self, f_symb):
        self.f_symb = f_symb
        self.set_samp_rate(self.f_symb*4)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.gsm_input_0.set_samp_rate_in(self.samp_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)

    def get_f_900_e(self):
        return self.f_900_e

    def set_f_900_e(self, f_900_e):
        self.f_900_e = f_900_e

    def get_f_900_b(self):
        return self.f_900_b

    def set_f_900_b(self, f_900_b):
        self.f_900_b = f_900_b

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

    def get_CCCH(self):
        return self.CCCH

    def set_CCCH(self, CCCH):
        self.CCCH = CCCH

    def get_BCCH(self):
        return self.BCCH

    def set_BCCH(self, BCCH):
        self.BCCH = BCCH


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("-f", "--fc", dest="fc", type="eng_float", default=eng_notation.num_to_str(927.2e6),
        help="Set fc [default=%default]")
    (options, args) = parser.parse_args()
    tb = GSM_reciever(fc=options.fc)
    tb.start()
    tb.wait()

import pyshark
import trollius as asyncio
@asyncio.coroutine
def coro():
    for e in asyncio.sleep(30):
	yield e
##############################	
##  gsm_a_dtap_msg_rr_type =
##  0x3f for immediate assignement ;
##  0x1a for SI2 ;
##  0x1b for SI3
##  0x1c for SI4
##  0x21 for paging request 1
##############################
def detect():
	capture = pyshark.LiveCapture(interface='lo',display_filter='(!(ip.proto == 1)&&(gsm_a.ccch))')
	try :
		for packet in  packets_from_tshark_sync(capture,timeout=2)  :
			print "packet"
			return True
	except Exception,e : 
		print Exception
		return False
		
def packets_from_tshark_sync(capture, packet_count=None, existing_process=None,timeout=20):
        """
        Returns a generator of packets.
        This is the sync version of packets_from_tshark. It wait for the completion of each coroutine and
         reimplements reading packets in a sync way, yielding each packet as it arrives.

        :param packet_count: If given, stops after this amount of packets is captured.
        """
        # NOTE: This has code duplication with the async version, think about how to solve this
        tshark_process = existing_process or capture.eventloop.run_until_complete(capture._get_tshark_process())
        psml_structure, data = capture.eventloop.run_until_complete(capture._get_psml_struct(tshark_process.stdout))
        packets_captured = 0
        data = b''
        try:
            while True:
                try:
                    packet, data = capture.eventloop.run_until_complete(asyncio.wait_for(capture._get_packet_from_stream(tshark_process.stdout, data, psml_structure=psml_structure),timeout))
                except EOFError:
                    capture.log.debug('EOF reached (sync)')
                    break
                if packet:
                    packets_captured += 1
                    yield packet
                if packet_count and packets_captured >= packet_count:
                    break
        finally:
            capture._cleanup_subprocess(tshark_process)
	
def sniff():
	try :
		#~ print "i sniff"
		done=0b11111100
		#~ capture = pyshark.LiveCapture(interface='lo')
		capture = pyshark.LiveCapture(interface='lo',display_filter='(!(ip.proto == 1)&&(gsm_a.ccch))')
		packets={'si2' : 0,'si3' : 0 }#[0,0,0,0]
		#~ capture.apply_on_packets(print_callback, timeout=50)
		for packet in  packets_from_tshark_sync(capture,timeout=10)  :
		#~ for packet in capture.sniff_continuously(packet_count=50) :
			print 'Just arrived:' ,#, packet[4] ,dir(packet[4]) ,packet[4].gsm_a_dtap_msg_rr_type
			print done
			if (packet[4].gsm_a_dtap_msg_rr_type=='0x1a') :
				done=done|0b11110001
				packets['si2']=packet[4]
				#~ print 'SI2'
			elif (packet[4].gsm_a_dtap_msg_rr_type=='0x1b') :
				done=done|0b11110010
				packets['si3']=packet[4]
				#~ print 'SI3'
			else :
				print 'other' , packet[4].gsm_a_dtap_msg_rr_type
			if done==255 :
				return {'fc' :  0 ,'arfcn' : 0,'mcc' : packets['si3'].e212_mcc , 'mnc' : packets['si3'].e212_mnc ,'lac' : packets['si3'].gsm_a_lac , 'cid' : packets['si3'].gsm_a_bssmap_cell_ci , 'larcfn' : packets['si2']._get_all_fields_with_alternates()[16].get_default_value() }
	except Exception,e :
		return 0


	#~ if (done==255):
		#~ r={'fc' :  0 ,'arfcn' : 0,'mcc' : packets['si3'].e212_mcc , 'mnc' : packets['si3'].e212_mnc ,'lac' : packets['si3'].gsm_a_lac , 'cid' : packets['si3'].gsm_a_bssmap_cell_ci , 'larcfn' : packets['si2']._get_all_fields_with_alternates()[16].get_default_value() }
	#~ else  :
		#~ r = 0
	#~ return r
	# for key,packet in packets.iteritems() :
	# 	if key=='si3' :
	# 		print packet.e212_mcc, packet.e212_mnc , packet.gsm_a_lac,packet.gsm_a_bssmap_cell_ci
    #
	# 	if key == 'si2' :
	# 		print 'xxxxxx' ,dir(packet.gsm_a_l3_protocol_discriminator)
	# 		print  packet._get_all_fields_with_alternates()[16].get_default_value()
	# 		print type(packet._get_all_fields_with_alternates()[16])
	# 		packet.pretty_print()
	# 	print key,dir(packet)
	# 	print packet
	# return packets
		
if __name__ == '__main__':
	r=sniff()
	print r
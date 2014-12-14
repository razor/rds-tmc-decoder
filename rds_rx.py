#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Stereo FM receiver and RDS Decoder
# Generated: Sun Dec 14 08:16:11 2014
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import digital;import cmath
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import math
import osmosdr
import rds
import time
import wx

class rds_rx(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Stereo FM receiver and RDS Decoder")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1000000
        self.bb_decim = bb_decim = 4
        self.freq_offset = freq_offset = 250000
        self.freq = freq = 106.1e6
        self.baseband_rate = baseband_rate = samp_rate/bb_decim
        self.audio_decim = audio_decim = 5
        self.xlate_bandwidth = xlate_bandwidth = 100000
        self.volume = volume = 0
        self.gain = gain = 37.6
        self.freq_tune = freq_tune = freq - freq_offset
        self.audio_rate = audio_rate = 48000
        self.audio_decim_rate = audio_decim_rate = baseband_rate/audio_decim

        ##################################################
        # Blocks
        ##################################################
        _volume_sizer = wx.BoxSizer(wx.VERTICAL)
        self._volume_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_volume_sizer,
        	value=self.volume,
        	callback=self.set_volume,
        	label="Volume",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._volume_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_volume_sizer,
        	value=self.volume,
        	callback=self.set_volume,
        	minimum=-20,
        	maximum=10,
        	num_steps=300,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_volume_sizer, 0, 1, 1, 1)
        self.nb = self.nb = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "BB")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "Demod")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "L+R")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "Pilot")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "DSBSC")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "RDS")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "L-R")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "RDS constellation")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "Waterfall")
        self.GridAdd(self.nb, 2, 0, 1, 2)
        _gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	label="RF Gain",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	minimum=0,
        	maximum=49.6,
        	num_steps=124,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_gain_sizer, 0, 0, 1, 1)
        _freq_sizer = wx.BoxSizer(wx.VERTICAL)
        self._freq_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_freq_sizer,
        	value=self.freq,
        	callback=self.set_freq,
        	label="Freq",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._freq_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_freq_sizer,
        	value=self.freq,
        	callback=self.set_freq,
        	minimum=88.1e6,
        	maximum=107.9e6,
        	num_steps=99,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_freq_sizer, 1, 0, 1, 2)
        self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_f(
        	self.nb.GetPage(8).GetWin(),
        	baseband_freq=0,
        	dynamic_range=100,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=baseband_rate,
        	fft_size=512,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="Waterfall Plot",
        )
        self.nb.GetPage(8).Add(self.wxgui_waterfallsink2_0.win)
        self.wxgui_scopesink2_1 = scopesink2.scope_sink_c(
        	self.nb.GetPage(7).GetWin(),
        	title="Scope Plot",
        	sample_rate=2375,
        	v_scale=0.4,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=False,
        	xy_mode=True,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.nb.GetPage(7).Add(self.wxgui_scopesink2_1.win)
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
        	self.nb.GetPage(3).GetWin(),
        	title="Pilot",
        	sample_rate=baseband_rate,
        	v_scale=0,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.nb.GetPage(3).Add(self.wxgui_scopesink2_0.win)
        self.wxgui_fftsink2_0_0_0_1_0_1 = fftsink2.fft_sink_c(
        	self.nb.GetPage(5).GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=audio_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="RDS",
        	peak_hold=False,
        )
        self.nb.GetPage(5).Add(self.wxgui_fftsink2_0_0_0_1_0_1.win)
        self.wxgui_fftsink2_0_0_0_1_0_0 = fftsink2.fft_sink_f(
        	self.nb.GetPage(6).GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=-50,
        	ref_scale=2.0,
        	sample_rate=baseband_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="L-R",
        	peak_hold=False,
        )
        self.nb.GetPage(6).Add(self.wxgui_fftsink2_0_0_0_1_0_0.win)
        self.wxgui_fftsink2_0_0_0_1 = fftsink2.fft_sink_f(
        	self.nb.GetPage(4).GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=baseband_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="DSBSC Sub-carrier",
        	peak_hold=False,
        )
        self.nb.GetPage(4).Add(self.wxgui_fftsink2_0_0_0_1.win)
        self.wxgui_fftsink2_0_0_0 = fftsink2.fft_sink_f(
        	self.nb.GetPage(2).GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=audio_decim_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="L+R",
        	peak_hold=False,
        )
        self.nb.GetPage(2).Add(self.wxgui_fftsink2_0_0_0.win)
        self.wxgui_fftsink2_0_0 = fftsink2.fft_sink_f(
        	self.nb.GetPage(1).GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=baseband_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=True,
        	avg_alpha=0.8,
        	title="FM Demod",
        	peak_hold=False,
        )
        self.nb.GetPage(1).Add(self.wxgui_fftsink2_0_0.win)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.nb.GetPage(0).GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=-30,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=True,
        	avg_alpha=0.8,
        	title="Baseband",
        	peak_hold=False,
        )
        self.nb.GetPage(0).Add(self.wxgui_fftsink2_0.win)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(freq_tune, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(gain, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna("", 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        self.root_raised_cosine_filter_0 = filter.fir_filter_ccf(1, firdes.root_raised_cosine(
        	1, samp_rate/bb_decim/audio_decim, 2375, 1, 100))
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_fff(
                interpolation=audio_rate,
                decimation=audio_decim_rate,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=audio_rate,
                decimation=audio_decim_rate,
                taps=None,
                fractional_bw=None,
        )
        self.gr_rds_parser_0 = rds.parser(False, True)
        self.gr_rds_panel_0 = rds.rdsPanel(freq, self.GetWin())
        self.Add(self.gr_rds_panel_0.panel)
        self.gr_rds_decoder_0 = rds.decoder(False, False)
        self.freq_xlating_fir_filter_xxx_1 = filter.freq_xlating_fir_filter_fcc(audio_decim, (firdes.low_pass(2500.0,baseband_rate,2.4e3,2e3,firdes.WIN_HAMMING)), 57e3, baseband_rate)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, (firdes.low_pass(1, samp_rate, xlate_bandwidth, 100000)), freq_offset, samp_rate)
        self.fir_filter_xxx_5 = filter.fir_filter_fff(audio_decim, (firdes.low_pass(1.0,baseband_rate,20e3,40e3,firdes.WIN_HAMMING)))
        self.fir_filter_xxx_5.declare_sample_delay(0)
        self.fir_filter_xxx_3 = filter.fir_filter_fff(1, (firdes.band_pass(1.0,baseband_rate,38e3-13e3,38e3+13e3,3e3,firdes.WIN_HAMMING)))
        self.fir_filter_xxx_3.declare_sample_delay(0)
        self.fir_filter_xxx_2 = filter.fir_filter_fcc(1, (firdes.complex_band_pass(1.0,baseband_rate,19e3-500,19e3+500,1e3,firdes.WIN_HAMMING)))
        self.fir_filter_xxx_2.declare_sample_delay(0)
        self.fir_filter_xxx_1 = filter.fir_filter_fff(audio_decim, (firdes.low_pass(1.0,baseband_rate,13e3,3e3,firdes.WIN_HAMMING)))
        self.fir_filter_xxx_1.declare_sample_delay(0)
        self.digital_mpsk_receiver_cc_0 = digital.mpsk_receiver_cc(2, 0, 1*cmath.pi/100.0, -0.06, 0.06, 0.5, 0.05, samp_rate/bb_decim/audio_decim/ 2375.0, 0.001, 0.005)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(2)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_multiply_xx_1 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vff((10**(1.*(volume+15)/10), ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((10**(1.*(volume+15)/10), ))
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_char*1, 2)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_imag_0 = blocks.complex_to_imag(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=samp_rate,
        	audio_decimation=bb_decim,
        )
        self.analog_pll_refout_cc_0 = analog.pll_refout_cc(0.001, 2 * math.pi * (19000+200) / baseband_rate, 2 * math.pi * (19000-200) / baseband_rate)
        self.analog_fm_deemph_0_0_0 = analog.fm_deemph(fs=audio_decim_rate, tau=75e-6)
        self.analog_fm_deemph_0_0 = analog.fm_deemph(fs=audio_decim_rate, tau=75e-6)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.fir_filter_xxx_1, 0), (self.wxgui_fftsink2_0_0_0, 0))
        self.connect((self.fir_filter_xxx_1, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.fir_filter_xxx_3, 0), (self.wxgui_fftsink2_0_0_0_1, 0))
        self.connect((self.fir_filter_xxx_1, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.fir_filter_xxx_5, 0))
        self.connect((self.analog_fm_deemph_0_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.analog_fm_deemph_0_0_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.analog_fm_deemph_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.wxgui_fftsink2_0_0_0_1_0_0, 0))
        self.connect((self.fir_filter_xxx_5, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.fir_filter_xxx_5, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.fir_filter_xxx_3, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.analog_fm_deemph_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.wxgui_fftsink2_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_wfm_rcv_0, 0))
        self.connect((self.analog_wfm_rcv_0, 0), (self.fir_filter_xxx_1, 0))
        self.connect((self.analog_wfm_rcv_0, 0), (self.wxgui_waterfallsink2_0, 0))
        self.connect((self.analog_wfm_rcv_0, 0), (self.wxgui_fftsink2_0_0, 0))
        self.connect((self.analog_wfm_rcv_0, 0), (self.fir_filter_xxx_3, 0))
        self.connect((self.analog_wfm_rcv_0, 0), (self.fir_filter_xxx_2, 0))
        self.connect((self.fir_filter_xxx_2, 0), (self.analog_pll_refout_cc_0, 0))
        self.connect((self.analog_pll_refout_cc_0, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.analog_pll_refout_cc_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_complex_to_imag_0, 0))
        self.connect((self.blocks_complex_to_imag_0, 0), (self.wxgui_scopesink2_0, 0))
        self.connect((self.blocks_complex_to_imag_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_wfm_rcv_0, 0), (self.freq_xlating_fir_filter_xxx_1, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_1, 0), (self.wxgui_fftsink2_0_0_0_1_0_1, 0))
        self.connect((self.digital_mpsk_receiver_cc_0, 0), (self.wxgui_scopesink2_1, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_1, 0), (self.root_raised_cosine_filter_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.digital_mpsk_receiver_cc_0, 0))
        self.connect((self.digital_mpsk_receiver_cc_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_keep_one_in_n_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.gr_rds_decoder_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.blocks_null_sink_0, 1))

        ##################################################
        # Asynch Message Connections
        ##################################################
        self.msg_connect(self.gr_rds_decoder_0, "out", self.gr_rds_parser_0, "in")
        self.msg_connect(self.gr_rds_parser_0, "out", self.gr_rds_panel_0, "in")


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_baseband_rate(self.samp_rate/self.bb_decim)
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate/self.bb_decim/self.audio_decim, 2375, 1, 100))
        self.digital_mpsk_receiver_cc_0.set_omega(self.samp_rate/self.bb_decim/self.audio_decim/ 2375.0)
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1, self.samp_rate, self.xlate_bandwidth, 100000)))
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_bb_decim(self):
        return self.bb_decim

    def set_bb_decim(self, bb_decim):
        self.bb_decim = bb_decim
        self.set_baseband_rate(self.samp_rate/self.bb_decim)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate/self.bb_decim/self.audio_decim, 2375, 1, 100))
        self.digital_mpsk_receiver_cc_0.set_omega(self.samp_rate/self.bb_decim/self.audio_decim/ 2375.0)

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self.set_freq_tune(self.freq - self.freq_offset)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.freq_offset)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_freq_tune(self.freq - self.freq_offset)
        self.gr_rds_panel_0.set_frequency(self.freq);
        self._freq_slider.set_value(self.freq)
        self._freq_text_box.set_value(self.freq)

    def get_baseband_rate(self):
        return self.baseband_rate

    def set_baseband_rate(self, baseband_rate):
        self.baseband_rate = baseband_rate
        self.set_audio_decim_rate(self.baseband_rate/self.audio_decim)
        self.wxgui_fftsink2_0_0_0_1.set_sample_rate(self.baseband_rate)
        self.wxgui_fftsink2_0_0_0_1_0_0.set_sample_rate(self.baseband_rate)
        self.wxgui_fftsink2_0_0.set_sample_rate(self.baseband_rate)
        self.fir_filter_xxx_2.set_taps((firdes.complex_band_pass(1.0,self.baseband_rate,19e3-500,19e3+500,1e3,firdes.WIN_HAMMING)))
        self.wxgui_scopesink2_0.set_sample_rate(self.baseband_rate)
        self.analog_pll_refout_cc_0.set_max_freq(2 * math.pi * (19000+200) / self.baseband_rate)
        self.analog_pll_refout_cc_0.set_min_freq(2 * math.pi * (19000-200) / self.baseband_rate)
        self.fir_filter_xxx_5.set_taps((firdes.low_pass(1.0,self.baseband_rate,20e3,40e3,firdes.WIN_HAMMING)))
        self.fir_filter_xxx_3.set_taps((firdes.band_pass(1.0,self.baseband_rate,38e3-13e3,38e3+13e3,3e3,firdes.WIN_HAMMING)))
        self.fir_filter_xxx_1.set_taps((firdes.low_pass(1.0,self.baseband_rate,13e3,3e3,firdes.WIN_HAMMING)))
        self.wxgui_waterfallsink2_0.set_sample_rate(self.baseband_rate)
        self.freq_xlating_fir_filter_xxx_1.set_taps((firdes.low_pass(2500.0,self.baseband_rate,2.4e3,2e3,firdes.WIN_HAMMING)))

    def get_audio_decim(self):
        return self.audio_decim

    def set_audio_decim(self, audio_decim):
        self.audio_decim = audio_decim
        self.set_audio_decim_rate(self.baseband_rate/self.audio_decim)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate/self.bb_decim/self.audio_decim, 2375, 1, 100))
        self.digital_mpsk_receiver_cc_0.set_omega(self.samp_rate/self.bb_decim/self.audio_decim/ 2375.0)

    def get_xlate_bandwidth(self):
        return self.xlate_bandwidth

    def set_xlate_bandwidth(self, xlate_bandwidth):
        self.xlate_bandwidth = xlate_bandwidth
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1, self.samp_rate, self.xlate_bandwidth, 100000)))

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx_0.set_k((10**(1.*(self.volume+15)/10), ))
        self.blocks_multiply_const_vxx_0_0.set_k((10**(1.*(self.volume+15)/10), ))
        self._volume_slider.set_value(self.volume)
        self._volume_text_box.set_value(self.volume)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.rtlsdr_source_0.set_gain(self.gain, 0)
        self._gain_slider.set_value(self.gain)
        self._gain_text_box.set_value(self.gain)

    def get_freq_tune(self):
        return self.freq_tune

    def set_freq_tune(self, freq_tune):
        self.freq_tune = freq_tune
        self.rtlsdr_source_0.set_center_freq(self.freq_tune, 0)

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.wxgui_fftsink2_0_0_0_1_0_1.set_sample_rate(self.audio_rate)

    def get_audio_decim_rate(self):
        return self.audio_decim_rate

    def set_audio_decim_rate(self, audio_decim_rate):
        self.audio_decim_rate = audio_decim_rate
        self.wxgui_fftsink2_0_0_0.set_sample_rate(self.audio_decim_rate)

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = rds_rx()
    tb.Start(True)
    tb.Wait()

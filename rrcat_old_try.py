#####################################################
# @Author: Abhilash Sarwade
# @Date:   2023-03-16 09:18:45
# @email: sarwade@ursc.gov.in
# @File Name: rrcat_old_try.py
# @Project: rrcat_indore_koushal_old_visit
#
# @Last Modified time: 2023-03-17 04:06:57
#####################################################

import glob
import numpy as np
from solexs_pipeline import calibration_fit_routines

dt_dir = 'RRCAT_BL16_24082016'
dt_files = glob.glob(f'{dt_dir}/*.mca')

enes_peak = []
specs = []

for dt_f in dt_files:
    enes_peak.append(float(dt_f.split('_')[3][:-2]))
    tmp_spec = calibration_fit_routines.read_spectrum_mca(dt_f)
    specs.append(tmp_spec)

enes_peak = np.array(enes_peak) #eV


# E-Ch calibration

chs = []

for tmp_spec in specs:
    chs.append(np.argmax(tmp_spec))

chs = np.array(chs)

mc, mc_err = calibration_fit_routines.fit_e_ch(enes_peak,chs)

ene = calibration_fit_routines.e_ch(np.arange(2048),mc[0],mc[1])

# E-FWHM calibration

ch = np.arange(2048)

ch_fwhms = []
ch_fwhms_err = []
ch_peaks = []
ch_peaks_err = []

for tmp_spec in specs:
    tmp_ch_peak = np.argmax(tmp_spec)
    ft,ft_err = calibration_fit_routines.fit_gaussian(ch,tmp_spec,guess=[np.max(tmp_spec),tmp_ch_peak,10],lower=0.96*tmp_ch_peak,upper=1.04*tmp_ch_peak)
    ch_peaks.append(ft[1])
    ch_fwhms.append(ft[2])
    ch_peaks_err.append(ft_err[1])
    ch_fwhms_err.append(ft_err[2])
    

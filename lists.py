# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 13:24:56 2015

@author: monteiro
"""

suffixes = ['AR.m3u', 'ATM_10000.m3u', 'ATM_20000.m3u', 'ATM_30000.m3u', 'ATM_40000.m3u', 'ATM_50000.m3u', 'BAPR.m3u', 'BLBX.m3u', 'BOK.m3u', 'BPS.m3u', 'BSTF.m3u', 'BTL.m3u', 'CAS.m3u', 'CC.m3u', 'CF.m3u', 'CL_10600.m3u', 'CL_20600.m3u', 'CL_30600.m3u', 'CL_40600.m3u', 'CL_50600.m3u', 'DAM.m3u', 'DH.m3u', 'EB.m3u', 'EDM.m3u', 'FFFS.m3u', 'FKBL.m3u', 'FNFF.m3u', 'FOP.m3u', 'FR.m3u', 'GS.m3u', 'HOS.m3u', 'JAZZ_10900.m3u', 'JAZZ_20900.m3u', 'JAZZ_30900.m3u', 'JAZZ_40900.m3u', 'JAZZ_50900.m3u', 'KN.m3u', 'LAW.m3u', 'LITS.m3u', 'MOB.m3u', 'MODE.m3u', 'NAL.m3u', 'NF.m3u', 'OA_10300.m3u', 'OA_20300.m3u', 'OA_30300.m3u', 'OA_40300.m3u', 'OA_50300.m3u', 'PC.m3u', 'PO.m3u', 'PR.m3u', 'RB.m3u', 'RRR_11300.m3u', 'RRR_21300.m3u', 'RRR_31300.m3u', 'RRR_41300.m3u', 'RRR_51300.m3u', 'RWR.m3u', 'SCFI.m3u', 'SH.m3u', 'SLAW.m3u', 'SS.m3u', 'SSV.m3u', 'TAPA.m3u', 'TLBS.m3u', 'TN.m3u', 'TWO.m3u', 'UGR.m3u', 'WC_00200.m3u', 'WC_01200.m3u', 'WC_12200.m3u', 'WC_41800.m3u', 'WC_60600.m3u', 'WRKG.m3u', 'WRR.m3u']
program_names = {
'AR': 'alternative_radio',
'ATM': 'atmospherics',
'BAPR': 'back_alley_pork_roost',
'BDWY': 'a_bit_off_broadway',
'BLBX': 'inside_the_black_box',
'BOK': 'the_best_of_our_knowledge',
'BPS': 'blue_plate_special',
'BSTF': 'bobs_slacktime_funhouse',
'BTL': 'between_the_lines',
'CAS': 'coffee_and_sushi',
'CC': 'country_classics',
'CF': 'cambridge_forum',
'CL': 'classics',
'DAM': 'destroy_all_music',
'DH': 'the_desoto_hour',
'EB': 'electric_boogaloo',
'EDM': 'edm_sound_system',
'FFFS': 'fifty_four_forty_six',
'FKBL': 'freakers_balls',
'FNFF': 'friday_night_fish_fry',
'FOP': 'fifty_one_percent',
'FR': 'friction',
'GS': 'gold_soundz',
'HET': 'high_end_theory',
'HOS': 'hour_of_slack',
'JAZZ': 'just_jazz',
'KN': 'kosher_noise',  # deprecated
'LAW': 'live_at_wrek',
'LITS': 'lost_in_the_stacks',
'MOB': 'mobius',
'MODE': 'mode_seven',
'NAL': 'north_avenue_lounge',
'NF': 'new_forces',
'OA': 'overnight_alternatives',
'PC': 'personality_crisis',
'PO': 'psych_out',
'PR': 'planetary_radio',
'RB': 'radio_bomb',
'RRR': 'rock_rythm_and_roll',
'RWR': 'rambling_wrek_report',
'SCFI': 'sci_fi_lab',
'SH': 'stonehenge',
'SLAW': 'shillelagh_law',
'SS': 'sunday_special',
'SSV': 'sub_saharan_vibes',
'TAPA': 'tapas_and_tunes',
'TECH': 'techniques',
'TLBS': 'the_longboards_show',
'TN': 'tech_nation',
'TWO': 'this_way_out',
'UGR': 'underground_recordings',
'WC': 'weekend_cornucopia',
'WRKG': 'wrekage',
'WRR': 'wrekroom_renaissance',
}

monday = ['ATM_10000.m3u',
'OA_10300.m3u',
'CL_10600.m3u',
'JAZZ_10900.m3u',
'NAL.m3u',
'RRR_11300.m3u',
'TAPA.m3u', 
#'KN.m3u', # deprecated
'HET.m3u',
'SLAW.m3u',
'SSV.m3u',
'WC_12200.m3u'
]
tuesday =[
'ATM_20000.m3u',
'OA_20300.m3u',
'CL_20600.m3u',
'JAZZ_20900.m3u',
'FKBL.m3u',
'RRR_21300.m3u',
'GS.m3u',
'UGR.m3u',
'NF.m3u',
'TLBS.m3u',
'LAW.m3u',
'RB.m3u',
]
wednesday = [
'ATM_30000.m3u',
'OA_30300.m3u',
'CL_30600.m3u',
'JAZZ_30900.m3u',
'BLBX.m3u',
'RRR_31300.m3u',
'RWR.m3u',
'MOB.m3u',
'DAM.m3u',
'FR.m3u',
'PO.m3u',
]          
thursday = [
'ATM_40000.m3u',
'OA_40300.m3u',
'CL_40600.m3u',
'JAZZ_40900.m3u',
#'BPS.m3u', # deprecated
'RRR_41300.m3u',
'WC_41800.m3u',
'SCFI.m3u',
'FFFS.m3u',
#'WRR.m3u', # deprecated
'TECH.m3u',
'EB.m3u',
]
friday = [
'ATM_50000.m3u',
'OA_50300.m3u',
'CL_50600.m3u',
'JAZZ_50900.m3u',
'LITS.m3u',
'RRR_51300.m3u',
'CC.m3u',
'FNFF.m3u',
'SH.m3u',
]
saturday = [
'WRKG.m3u',
'WC_60600.m3u',
'DH.m3u',
'CAS.m3u',
'EDM.m3u',
]
sunday = [
'HOS.m3u',
'BSTF.m3u',
'WC_00200.m3u',
'TN.m3u',
'PR.m3u',
'BOK.m3u',
'BTL.m3u',
'TWO.m3u',
'FOP.m3u',
'CF.m3u',
'AR.m3u',
'WC_01200.m3u',
'MODE.m3u',
'SS.m3u',
'BAPR.m3u',
'PC.m3u'
]
week = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]
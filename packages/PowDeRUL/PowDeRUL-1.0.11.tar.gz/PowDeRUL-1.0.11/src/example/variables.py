variables = {
    # Paramètres généraux
    "time_cycle": 1800,
    "Ta": 50,
    "Pn": 150e3,
    "Fn": 50,
    "Vdc": 450,
    "f_sw": 10000,

    # Paramètres IGBT
    "number_IGBT": 6,
    "number_IGBT_parallel": 6 / 6,
    "Vce0": 1.10,
    "Rce": 0.75e-3,
    "Eon_sw": 13.5e-3,
    "Eoff_sw": 23.5e-3,
    "E_sw": 13.5e-3 + 23.5e-3,
    "Vref_sw": 400,
    "Iref_sw": 450,
    "kv_igbt": 1.35,

    # Paramètres Diode
    "Vd": 1.45,
    "Rd": 0.75e-3,
    "E_d": 7e-3,
    "Vref_d": 400,
    "Iref_d": 450,
    "ki_diode": 0.6,
    "kv_diode": 0.6,
  
    # Paramètres thermiques globaux
    "Rth_ch": 0.05 / 6,
    "Cth_ch": 0,
    "Rth_hf": 0.06 / 6,
    "Cth_hf": 0,
  
    # Paramètres thermiques IGBT
    "layers_Rth_jc_IGBT": [0.005, 0.055, 0.022, 0.013],
    "layers_Cth_jc_IGBT": [0.001 / 0.005, 0.03 / 0.055, 0.25 / 0.022, 1.5 / 0.013],

    # Paramètres thermiques Diode
    "layers_Rth_jc_diode": [0.015, 0.1, 0.025, 0.01],
    "layers_Cth_jc_diode": [0.001 / 0.015, 0.03 / 0.1, 0.25 / 0.025, 1.5 / 0.01],

    # Paramètres pour calcul du cumul d'endommagement
    "A": 3.5535e15,
    "alpha": -7.0390,
    "Ea": 2.7172e-20,
    "k": 1.38e-23,

    # Paramètres Excel
    "excel_file_path": 'example/courants_WLTP_MSRB.xlsx',
    "excel_page": 'Feuil2',
    "excel_starting_row": 8,
    "excel_ending_row": 1808,
    "excel_column_time": 1,
    "excel_column_power": 22,
    "excel_column_speed": 3,
    "excel_column_torque": 2,
    "excel_column_current": 11,
    "excel_column_cosphi": 21,
    "excel_column_m": 23,
}

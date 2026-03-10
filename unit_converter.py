def convert_units(hb, hb_unit, mch, mch_unit, mchc, mchc_unit, mcv, mcv_unit):
    
    # Hemoglobin conversion
    if hb_unit == "g/L":
        hb = hb / 10
    elif hb_unit == "mmol/L":
        hb = hb * 16.1

    # MCH conversion
    if mch_unit == "fg":
        mch = mch / 1000  # femtogram to picogram

    # MCHC conversion
    if mchc_unit == "g/L":
        mchc = mchc / 10

    # MCV conversion
    if mcv_unit == "L":
        mcv = mcv * 1e15  # liters to femtoliters

    return hb, mch, mchc, mcv

def processing_result_handsign(list_jari):
    jempol,telunjuk,tengah,manis,kelingking = list_jari
    hasil_angka = 11
    if not jempol and not telunjuk and not tengah and not manis and not kelingking:
        hasil_angka = 0
    elif not jempol and telunjuk and not tengah and not manis and not kelingking:
        hasil_angka = 1
    elif not jempol and telunjuk and tengah and not manis and not kelingking:
        hasil_angka = 2
    elif not jempol and telunjuk and tengah and manis and not kelingking:
        hasil_angka = 3
    elif not jempol and telunjuk and tengah and manis and kelingking:
        hasil_angka = 4
    elif jempol and telunjuk and tengah and manis and kelingking:
        hasil_angka = 5
    elif jempol and not telunjuk and not tengah and not manis and not kelingking:
        hasil_angka = 6
    elif jempol and telunjuk and not tengah and not manis and not kelingking:
        hasil_angka = 7
    elif jempol and telunjuk and tengah and not manis and not kelingking:
        hasil_angka = 8
    elif jempol and telunjuk and tengah and manis and not kelingking:
        hasil_angka = 9

    #Special Case hehe
    elif not jempol and not telunjuk and tengah and not manis and not kelingking:
        hasil_angka = "RUDE!"
    elif not jempol and not telunjuk and not tengah and not manis and kelingking:
        hasil_angka = "VOLUME LOW"
    elif not jempol and not telunjuk and not tengah and manis and kelingking:
        hasil_angka = "VOLUME MID"
    elif not jempol and not telunjuk and tengah and manis and kelingking:
        hasil_angka = "VOLUME HIGH"
    
    return hasil_angka
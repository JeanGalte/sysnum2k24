from lib_carotte import *
from utils import *

def cycle(k:int, l:list[Variable]) -> list[Variable]:
    return l[len(l)-k:len(l)] + l[0:len(l)-k]

def concat_list(l:list[Variable]) -> Variable:
    if len(l) == 1:
        return l[0]
    return concat_list(l[:len(l)//2]) + concat_list(l[len(l)//2:])

def concat_result(choice:list[Variable], vars:list[Variable]) -> Variable:
    return multimux(choice, [concat_list(cycle(len(vars)-i, vars)) for i in range(len(vars))])

def ram_manager(RAM_addr_size:int,
                RAM_word_size:Variable,
                RAM_sign_extend:Variable,
                RAM_read_addr: Variable,
                RAM_write_enable:Variable,
                RAM_write_addr:Variable,
                RAM_write_data:Variable) -> Variable:
    '''RAM manager implementation; word size is expected as 00 -> 8, 10 -> 16, 01 -> 32, 11 -> 64;
       La RAM est en mots de 64 bits mais adressable à l'octet donc on va utiliser 8 RAM dont les
       mots sont des octets représentant les octets 0, 1, ..., 7 modulo 8 dans la "vraie" RAM.'''
    addr_size = RAM_addr_size - 3

    # Déterminer les adresses de lecture
    addr = RAM_read_addr[3:RAM_addr_size]
    addr_remain0 = RAM_read_addr[0]
    addr_remain1 = RAM_read_addr[1]
    addr_remain2 = RAM_read_addr[2]
    addr_remain = [addr_remain0, addr_remain1, addr_remain2]

    addrl = []
    garbage, addrplus = add_one(addr)
    ar1_or_ar2 = addr_remain1 | addr_remain2
    ar1_and_ar2 = addr_remain1 & addr_remain2
    addrl.append(Mux(addr_remain0 | ar1_or_ar2, addr, addrplus)) # if addr_remain >= 100 then addrplus else addr
    addrl.append(Mux(ar1_or_ar2, addr, addrplus)) # if addr_remain >= 010 then addrplus else addr
    addrl.append(Mux(addr_remain2 | (addr_remain0 & addr_remain1), addr, addrplus)) # if addr_remain >= 110 then addrplus else addr
    addrl.append(Mux(addr_remain2, addr, addrplus)) # if addr_remain >= 001 then addrplus else addr
    addrl.append(Mux(addr_remain2 & (addr_remain1 | addr_remain0), addr, addrplus)) # if addr_remain >= 101 then addrplus else addr
    addrl.append(Mux(ar1_and_ar2, addr, addrplus)) # if addr_remain >= 011 then addrplus else addr
    addrl.append(Mux(ar1_and_ar2 & addr_remain0, addr, addrplus)) # if addr_remain >= 111 then addrplus else addr
    addrl.append(addr)
    
    # Déterminer les adresses d'écriture, comme pour la lecture
    waddr = RAM_write_addr[3:RAM_addr_size]
    waddr_remain0 = RAM_write_addr[0]
    waddr_remain1 = RAM_write_addr[1]
    waddr_remain2 = RAM_write_addr[2]
    waddr_remain = [waddr_remain0, waddr_remain1, waddr_remain2]

    waddrl = []
    garbage, waddrplus = add_one(waddr)
    war1_or_war2 = waddr_remain1 | waddr_remain2
    war1_and_war2 = waddr_remain1 & waddr_remain2
    waddrl.append(Mux(waddr_remain0 | war1_or_war2, waddr, waddrplus)) # if waddr_remain >= 100 then waddrplus else waddr
    waddrl.append(Mux(waddr_remain1 | waddr_remain2, waddr, waddrplus)) # if waddr_remain >= 010 then waddrplus else waddr
    waddrl.append(Mux(waddr_remain2 | (waddr_remain1 & waddr_remain0), waddr, waddrplus)) # if waddr_remain >= 110 then waddrplus else waddr
    waddrl.append(Mux(waddr_remain2, waddr, waddrplus)) # if waddr_remain >= 001 then waddrplus else waddr
    waddrl.append(Mux(waddr_remain2 & (waddr_remain1 | waddr_remain0), waddr, waddrplus)) # if waddr_remain >= 101 then waddrplus else waddr
    waddrl.append(Mux(war1_and_war2, waddr, waddrplus)) # if waddr_remain >= 011 then waddrplus else waddr
    waddrl.append(Mux(war1_and_war2 & waddr_remain0, waddr, waddrplus)) # if waddr_remain >= 111 then waddrplus else waddr
    waddrl.append(waddr)
    
    # Déterminer ce que l'on écrit
    RAM_write_datal = cycle(1, [RAM_write_data[i:i+8] for i in range(0, 64, 8)][::-1])

    # Déterminer où on écrit (c'est pareil que pour voir ce que l'on écrit)
    wws0 = RAM_word_size[0]
    wws1 = RAM_word_size[1]
    we00 = RAM_write_enable
    we10 = RAM_write_enable & (wws0 | wws1)
    we01 = RAM_write_enable & wws1
    we11 = RAM_write_enable & wws0 & wws1
    RAM_write_enablel = [we00, we11, we11, we11, we11, we01, we01, we10]

    # Nos 8 modules de RAM
    vall = []
    for i in range(8):
        vall.append(RAM(
            addr_size,                                             # address size
            8,                                                     # word size
            addrl[i],                                              # read_addr
            multimux(waddr_remain, cycle(i, RAM_write_enablel)),   # write_enable
            waddrl[i],                                             # write_address
            multimux(waddr_remain, cycle(i, RAM_write_datal))      # write_data
        ))
    
    val = concat_result(addr_remain, vall)
    in16 = Mux(Or(wws0, wws1), sign_extend(16, val[0:8], RAM_sign_extend), val[0:16])
    in32 = Mux(wws1, sign_extend(32, in16, RAM_sign_extend), val[0:32])
    return Mux(And(wws0, wws1), sign_extend(64, in32, RAM_sign_extend), val)

from lib_carotte import *
from utils import *

def sign_extend(target:int, value: Variable, enable: Variable) -> Variable:
    '''Sign extend'''
    s = Mux(value[value.bus_size-1], Constant("0"), enable)
    res = value
    for i in range(value.bus_size, target):
        res = s + res
    return res

def concat_result32(addr:Variable,
                    data000:Variable,
                    data001:Variable,
                    data010:Variable,
                    data011:Variable,
                    data100:Variable,
                    data101:Variable,
                    data110:Variable,
                    data111:Variable
                    ) -> Variable:
    return Mux(addr,
               data000 + data001 + data010 + data011,
               data100 + data101 + data110 + data111,
               )
def concat_result16(addr:Variable,
                    data000:Variable,
                    data001:Variable,
                    data010:Variable,
                    data011:Variable,
                    data100:Variable,
                    data101:Variable,
                    data110:Variable,
                    data111:Variable
                    ) -> Variable:
   return multimux(addr, [
               data000 + data001,
               data010 + data011,
               data100 + data101,
               data110 + data111
               ])

def cycle(k:int, l:list[Variable]):
    return l[len(l)-k:len(l)] + l[0:len(l)-k]

def ram_manager(RAM_addr_size:int,
                RAM_read_word_size:Variable,
                RAM_sign_extend:Variable,
                RAM_read_addr: Variable,
                RAM_write_enable:Variable,
                RAM_write_word_size:Variable,
                RAM_write_addr:Variable,
                RAM_write_data:Variable) -> Variable:
    '''RAM manager implementation; word size is expected as 00 -> 8, 01 -> 16, 10 -> 32, 11 -> 64;
       La RAM est en mots de 64 bits mais adressable à l'octet donc on va utiliser 8 RAM dont les
       mots sont des octets représentant les octets 0, 1, ..., 7 modulo 8 dans la "vraie" RAM.'''
    addr_size = RAM_addr_size - 3

    # Déterminer les adresses de lecture
    addr = RAM_read_addr[0:addr_size]
    addr_remain = RAM_read_addr[addr_size:RAM_addr_size]
    addr_remain0 = addr_remain[0]
    addr_remain1 = addr_remain[1]
    addr_remain2 = addr_remain[2]
    
    garbage, addrplus = add_one(addr)
    addr000 = Mux(addr_remain0 | addr_remain1 | addr_remain2, addr, addrplus) # if addr_remain >= 001 then addrplus else addr
    addr001 = Mux(addr_remain0 | addr_remain1, addr, addrplus) # if addr_remain >= 010 then addrplus else addr
    addr010 = Mux(addr_remain0 | (addr_remain1 & addr_remain2), addr, addrplus) # if addr_remain >= 011 then addrplus else addr
    addr011 = Mux(addr_remain0, addr, addrplus) # if addr_remain >= 100 then addrplus else addr
    addr100 = Mux(addr_remain0 & (addr_remain1 | addr_remain2), addr, addrplus) # if addr_remain >= 101 then addrplus else addr
    addr101 = Mux(addr_remain0 & addr_remain1, addr, addrplus) # if addr_remain >= 110 then addrplus else addr
    addr110 = Mux(addr_remain0 & addr_remain1 & addr_remain2, addr, addrplus) # if addr_remain >= 111 then addrplus else addr

    # Déterminer les adresses d'écriture, comme pour la lecture
    waddr = RAM_write_addr[0:addr_size]
    waddr_remain = RAM_read_addr[addr_size:RAM_addr_size]
    waddr_remain0 = waddr_remain[0]
    waddr_remain1 = waddr_remain[1]
    waddr_remain2 = waddr_remain[2]
    
    garbage, waddrplus = add_one(waddr)
    waddr000 = Mux(waddr_remain0 | waddr_remain1 | waddr_remain2, waddr, waddrplus) # if waddr_remain >= 001 then waddrplus else waddr
    waddr001 = Mux(waddr_remain0 | waddr_remain1, waddr, waddrplus) # if waddr_remain >= 010 then waddrplus else waddr
    waddr010 = Mux(waddr_remain0 | (waddr_remain1 & waddr_remain2), waddr, waddrplus) # if waddr_remain >= 011 then waddrplus else waddr
    waddr011 = Mux(waddr_remain0, waddr, waddrplus) # if waddr_remain >= 100 then waddrplus else waddr
    waddr100 = Mux(waddr_remain0 & (waddr_remain1 | waddr_remain2), waddr, waddrplus) # if waddr_remain >= 101 then waddrplus else waddr
    waddr101 = Mux(waddr_remain0 & waddr_remain1, waddr, waddrplus) # if waddr_remain >= 110 then waddrplus else waddr
    waddr110 = Mux(waddr_remain0 & waddr_remain1 & waddr_remain2, waddr, waddrplus) # if waddr_remain >= 111 then waddrplus else waddr

    # Déterminer ce que l'on écrit
    wd000 = RAM_write_data[0:8]
    wd001 = RAM_write_data[8:16]
    wd010 = RAM_write_data[16:24]
    wd011 = RAM_write_data[24:32]
    wd100 = RAM_write_data[32:40]
    wd101 = RAM_write_data[40:48]
    wd110 = RAM_write_data[48:56]
    wd111 = RAM_write_data[56:64]
    l = [wd000, wd111, wd110, wd101, wd100, wd011, wd010, wd001]
    RAM_write_data000 = multimux(waddr_remain, cycle(0, l))
    RAM_write_data001 = multimux(waddr_remain, cycle(1, l))
    RAM_write_data010 = multimux(waddr_remain, cycle(2, l))
    RAM_write_data011 = multimux(waddr_remain, cycle(3, l))
    RAM_write_data100 = multimux(waddr_remain, cycle(4, l))
    RAM_write_data101 = multimux(waddr_remain, cycle(5, l))
    RAM_write_data110 = multimux(waddr_remain, cycle(6, l))
    RAM_write_data111 = multimux(waddr_remain, cycle(7, l))

    # Déterminer où on écrit (c'est pareil que pour voir ce que l'on écrit)
    wws0 = RAM_write_word_size[0]
    wws1 = RAM_write_word_size[1]
    re00 = RAM_write_enable
    re01 = RAM_write_enable & (wws0 | wws1)
    re10 = RAM_write_enable & wws0
    re11 = RAM_write_enable & wws0 & wws1
    l = [re00, re11, re11, re11, re11, re10, re10, re01]
    RAM_write_enable000 = multimux(waddr_remain, cycle(0, l))
    RAM_write_enable001 = multimux(waddr_remain, cycle(1, l))
    RAM_write_enable010 = multimux(waddr_remain, cycle(2, l))
    RAM_write_enable011 = multimux(waddr_remain, cycle(3, l))
    RAM_write_enable100 = multimux(waddr_remain, cycle(4, l))
    RAM_write_enable101 = multimux(waddr_remain, cycle(5, l))
    RAM_write_enable110 = multimux(waddr_remain, cycle(6, l))
    RAM_write_enable111 = multimux(waddr_remain, cycle(7, l))
    

    # Nos 8 modules de RAM
    val000 = RAM(addr_size, 8, addr000, RAM_write_enable000, waddr000, RAM_write_data000)
    val001 = RAM(addr_size, 8, addr001, RAM_write_enable001, waddr001, RAM_write_data001)
    val010 = RAM(addr_size, 8, addr010, RAM_write_enable010, waddr010, RAM_write_data010)
    val011 = RAM(addr_size, 8, addr011, RAM_write_enable011, waddr011, RAM_write_data011)
    val100 = RAM(addr_size, 8, addr100, RAM_write_enable100, waddr100, RAM_write_data100)
    val101 = RAM(addr_size, 8, addr101, RAM_write_enable101, waddr101, RAM_write_data101)
    val110 = RAM(addr_size, 8, addr110, RAM_write_enable110, waddr110, RAM_write_data110)
    val111 = RAM(addr_size, 8, addr, RAM_write_enable111, waddr, RAM_write_data111)
    return multimux(RAM_read_word_size, [
               sign_extend(
                   64,
                   multimux(addr_remain, [val000, val001, val010, val011, val100, val101, val110, val111]),
                   RAM_sign_extend
               ),
               sign_extend(
                   64,
                   concat_result16(RAM_read_addr[RAM_addr_size-2:RAM_addr_size], val000, val001, val010, val011, val100, val101, val110, val111),
                   RAM_sign_extend
               ),
               sign_extend(
                   64,
                   concat_result32(RAM_read_addr[RAM_addr_size-1], val000, val001, val010, val011, val100, val101, val110, val111),
                   RAM_sign_extend
               ),
               val000 + val001 + val010 + val011 + val100 + val101 + val110 + val111
               ])

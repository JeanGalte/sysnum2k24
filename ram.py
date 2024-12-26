from lib_carotte import *
from utils import *

def sign_extend(target:int, value: Variable, enable: Variable) -> Variable:
    '''Sign extend'''
    s = Mux(Select(value.bus_size-1, value), Constant("0"), enable)
    res = value
    for i in range(value.bus_size, target):
        res = Concat(s, res)
    return res

def concat_result64(data000:Variable,
                    data001:Variable,
                    data010:Variable,
                    data011:Variable,
                    data100:Variable,
                    data101:Variable,
                    data110:Variable,
                    data111:Variable
                    ) -> Variable:
    return Concat(Concat(Concat(data000, data001), Concat(data010, data011)),
                  Concat(Concat(data100, data101), Concat(data110, data111)))
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
               Concat(Concat(data000, data001), Concat(data010, data011)),
               Concat(Concat(data100, data101), Concat(data110, data111)),
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
               Concat(data000, data001),
               Concat(data010, data011),
               Concat(data100, data101),
               Concat(data110, data111)
               ])

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
       mots sont des octets.'''
    addr_size = RAM_addr_size - 3
    addr = Slice(0, addr_size, RAM_read_addr)
    addr_remain = Slice(addr_size, RAM_addr_size, RAM_read_addr)

    # Déterminer les variables d'écriture
    # ...

    addrplus = add_one(addr_size, addr)
    addr001 = Mux(Or(Or(Select(0, addr_remain), Select(1, addr_remain)), Select(2, addr_remain)), addrplus, addr) # if addr_remain >= 001 then addr else addrplus
    addr010 = Mux(Or(Select(0, addr_remain), Select(1, addr_remain)), addrplus, addr) # if addr_remain >= 010 then addr else addrplus
    addr011 = Mux(Or(Select(0, addr_remain), And(Select(1, addr_remain), Select(2, addr_remain))), addrplus, addr) # if addr_remain >= 011 then addr else addrplus
    addr100 = Mux(Select(0, addr_remain), addrplus, addr) # if addr_remain >= 100 then addr else addrplus
    addr101 = Mux(And(Select(0, addr_remain), Or(Select(1, addr_remain), Select(2, addr_remain))), addrplus, addr) # if addr_remain >= 101 then addr else addrplus
    addr110 = Mux(And(Select(0, addr_remain), Select(1, addr_remain)), addrplus, addr) # if addr_remain >= 110 then addr else addrplus
    addr111 = Mux(And(Select(0, addr_remain), And(Select(1, addr_remain), Select(2, addr_remain))), addrplus, addr) # if addr_remain >= 111 then addr else addrplus

    val000 = RAM(addr_size, 8, addr, RAM_write_enable000, RAM_write_addr, RAM_write_data000)
    val001 = RAM(addr_size, 8, addr001, RAM_write_enable001, RAM_write_addr, RAM_write_data001)
    val010 = RAM(addr_size, 8, addr010, RAM_write_enable010, RAM_write_addr, RAM_write_data010)
    val011 = RAM(addr_size, 8, addr011, RAM_write_enable011, RAM_write_addr, RAM_write_data011)
    val100 = RAM(addr_size, 8, addr100, RAM_write_enable100, RAM_write_addr, RAM_write_data100)
    val101 = RAM(addr_size, 8, addr101, RAM_write_enable101, RAM_write_addr, RAM_write_data101)
    val110 = RAM(addr_size, 8, addr110, RAM_write_enable110, RAM_write_addr, RAM_write_data110)
    val111 = RAM(addr_size, 8, addr111, RAM_write_enable111, RAM_write_addr, RAM_write_data111)
    val = multimux(RAM_read_word_size, [
               multimux(addr_remain, [val000, val001, val010, val011, val100, val101, val110, val111]),
               concat_result16(Slice(RAM_addr_size-2, RAM_addr_size, RAM_read_addr), val000, val001, val010, val011, val100, val101, val110, val111),
               concat_result32(Select(RAM_addr_size-1, RAM_read_addr), val000, val001, val010, val011, val100, val101, val110, val111),
               concat_result64(val000, val001, val010, val011, val100, val101, val110, val111)
               ])
    return sign_extend(64, val, RAM_sign_extend)

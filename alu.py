from lib_carotte import *
from utils import *

def log2i(n):
  '''ceil(log2(n)), not optimized'''
  if n==1:
    return 1
  if n%2:
    n = n-1
  return 1+log2i(n//2)

def propgen(aandb:list[Variable], aorb:list[Variable]) -> tuple[list[Variable], list[Variable]]:
  '''returns the list of propagates and generates for blocs of aligned 2**k bits'''
  n = len(aorb)
  if n == 1:
    return aorb, aandb
  m = n//2
  pd, gd = propgen(aandb[m:n], aorb[m:n])
  pg, gg = propgen(aandb[0:m], aorb[0:m])
  p = pg + pd
  g = gg + gd
  p.append(pd[-1] & pg[-1])
  g.append(gd[-1] | (pd[-1] & gg[-1]))
  return p, g

def add_aux(p:list[Variable], g:list[Variable], axorb:Variable, retenue:Variable) -> Variable:
  '''returns the sum of a and b and a carry given propagates, generates, a^b'''
  n = len(axorb)
  m = len(p)//2
  if n == 1:
    return axorb[0] ^ retenue
  retd = (retenue & p[m-1]) | g[m-1]
  return add_aux(p[:m], g[:m], axorb[0:n//2], retenue) + add_aux(p[m:-1], g[m:-1], axorb[n//2:n], retd)

def add(axorb:list[Variable], aorb:list[Variable], aandb:list[Variable], retenue:Variable) -> tuple[Variable, Variable]:
  '''carry-look-ahead 2**n bits adder'''
  p, g = propgen(aandb, aorb)
  overflow = (retenue & p[-1]) | g[-1]
  return add_aux(p, g, axorb, retenue), overflow

def sll(a:Variable, b:Variable) -> Variable:
  '''shift left logical, assuming n is a power of 2'''
  n = a.bus_size
  k = log2i(n-1)
  return Mux(
    is_not_null(b[0:n-k]),
    multimux_be([b[i] for i in range(n-k,n)], [a]+[Constant("0"*i)+a[i:n] for i in range(1, n)]),
    Constant("0"*n)
  )

def sral(a:Variable, b:Variable, funct7:Variable) -> Variable:
  '''shift right arithmetic/logical, assuming n is a power of 2'''
  n = a.bus_size
  k = log2i(n-1)
  letter = funct7 & a[n-1]
  fill = letter
  res = [a]
  for i in range(1, n):
    res.append(a[0:n-i]+fill)
    fill = fill+letter
  return Mux(
    is_not_null(b[0:n-k]),
    multimux_be([b[i] for i in range(n-k,n)], res),
    fill
  )

def slt(a:Variable, b:Variable, aminusb:Variable) -> Variable:
  '''if a<b then 1 else 0'''
  return Constant("0"*(a.bus_size-1)) + ((a[0] & ~b[0]) | (~(a[0]^b[0]) & aminusb[0]))

def sltu(a:Variable, b:Variable, aminusb:Variable) -> Variable:
  '''if a<b then 1 else 0'''
  return Constant("0"*(a.bus_size-1)) + ((~a[0] & b[0]) | (~(a[0]^b[0]) & aminusb[0]))

def alu(a:Variable, b:Variable, funct3:Variable, funct7:Variable) -> Variable:
  funct30 = funct3[0]
  funct31 = funct3[1]
  funct32 = funct3[2]
  n = a.bus_size
  # ensures that b2 = b when add/xor/and/or and b2 = -b when sub/slt/sltu
  isnotsub = funct32 | (~funct7 & ~funct31)
  b2 = Mux(isnotsub, ~b, b)
  aorb = a | b2
  aandb = a & b2
  axorb = a ^ b2
  aplusb, overflow = add([axorb[i] for i in range(n)], [aorb[i] for i in range(n)], [aandb[i] for i in range(n)], ~isnotsub)
  return multimux([funct30, funct31, funct32], [
    aplusb,
    sll(a, b),
    slt(a, b, aplusb),
    sltu(a, b, aplusb),
    axorb,
    sral(a, b, funct7),
    aorb,
    aandb
  ])


from lib_carotte import *
from utils import *

def log2i(n):
  '''ceil(log2(n)), not optimized'''
  if n==1:
    return 1
  if n%2:
    n = n-1
  return 1+log2i(n//2)

def propgen(aandb:Variable, aorb:Variable) -> tuple[list[Variable], list[Variable]]:
  '''returns the list of propagates and generates for blocs of aligned 2**k bits'''
  n = aorb.bus_size
  if n == 1:
    return [aorb], [aandb]
  m = n//2
  pd, gd = propgen(aandb[m:n], aorb[m:n])
  pg, gg = propgen(aandb[0:m], aorb[0:m])
  p = pg + pd
  g = gg + gd
  p.append(pg[-1] & pd[-1])
  g.append(gg[-1] | (pg[-1] & gd[-1]))
  return p, g

def add_aux(p:list[Variable], g:list[Variable], axorb:Variable, retenue:Variable) -> Variable:
  '''returns the sum of a and b and a carry given propagates, generates, a^b'''
  n = axorb.bus_size
  m = len(p)//2
  if n == 1:
    return axorb ^ retenue
  retg = (retenue & p[-2]) | g[-2]
  return add_aux(p[:m], g[:m], axorb[0:n//2], retg) + add_aux(p[m:-1], g[m:-1], axorb[n//2:n], retenue)

def add(axorb:Variable, aorb:Variable, aandb:Variable, retenue:Variable) -> tuple[Variable, Variable]:
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
    multimux_be(b[n-k:n], [a]+[a[i:n]+Constant("0"*i) for i in range(1, n)]),
    Constant("0"*n)
  )

def srl(a:Variable, b:Variable, funct7:Variable) -> Variable:
  '''shift right logical, assuming n is a power of 2'''
  n = a.bus_size
  k = log2i(n-1)
  letter = funct7 & a[0]
  fill = letter
  res = [a]
  for i in range(1, n):
    res.append(fill+a[0:n-i])
    fill = fill+letter
  return Mux(
    is_not_null(b[0:n-k]),
    multimux_be(b[n-k:n], res),
    fill
  )

def slt(a:Variable, b:Variable, aminusb:Variable) -> Variable:
  '''if a<b then 1 else 0'''
  return Constant("0"*(a.bus_size-1)) + ((a[0] & ~b[0]) | (~(a[0]^b[0]) & aminusb[0]))

def sltu(a:Variable, b:Variable, aminusb:Variable) -> Variable:
  '''if a<b then 1 else 0'''
  return Constant("0"*(a.bus_size-1)) + ((~a[0] & b[0]) | (~(a[0]^b[0]) & aminusb[0]))

def alu(a:Variable, b:Variable, funct3:Variable, funct7:Variable) -> Variable:
  funct7 = funct7[5]
  funct30 = funct3[0]
  funct31 = funct3[1]
  funct32 = funct3[2]
  # ensures that b2 = b when add/xor/and/or and b2 = -b when sub/slt/sltu
  isnotsub = funct32 | (~funct7 & ~funct31)
  b2 = Mux(isnotsub, ~b, b)
  aorb = a | b2
  aandb = a & b2
  axorb = a ^ b2
  aplusb, overflow = add(axorb, aorb, aandb, ~isnotsub)
  return multimux(funct3, [
    aplusb,
    sll(a, b),
    slt(a, b, aplusb),
    sltu(a, b, aplusb),
    axorb,
    sral(a, b, funct7),
    aorb,
    aandb
  ])

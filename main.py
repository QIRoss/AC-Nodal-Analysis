import sys
import numpy as np
import math
import cmath

#open netlist text file given as argv[1]
f = open(sys.argv[1])
#split file in a list of strings using 
textFile = f.read().split('\n')
#remove empty lines from list
textFile = list( filter(lambda x:x !='', textFile) )
#remove comments from list
netlist = list( filter(lambda x:x[0] !='*', textFile))

#count total number of nodes
nodeCount = 0

omega = 0
phase = 0

#map each string from list into an array of netlist parameters as strings
for i in range(len(netlist)):
  netlist[i] = netlist[i].split()

#transform every parameter into integer and floats and count number of nodes
for i in range(len(netlist)):
  if(netlist[i][0][0] == 'R'):
    aux = netlist[i]
    aux[1] = np.uintc(aux[1])
    aux[2] = np.uintc(aux[2])
    aux[3] = np.cdouble(aux[3])
    #swap nodes if a > b
    if(aux[1] > aux[2]):
      aux[1], aux[2] = aux[2], aux[1]
    #count node value
    if(aux[2] > nodeCount):
      nodeCount = aux[2]

  elif(netlist[i][0][0] == 'I'):
    aux = netlist[i]
    aux[1] = np.uintc(aux[1])
    aux[2] = np.uintc(aux[2])
    aux[4] = np.cdouble(aux[4])
    aux[5] = np.cdouble(aux[5])
    aux[6] = np.cdouble(aux[6])
    omega = np.cdouble(math.pi*2*aux[6])
    aux[7] = np.double(aux[7])
    phase = math.radians(aux[7])
    #swap nodes if a > b and multiply value by -1
    if(aux[1] > aux[2]):
      aux[1], aux[2] = aux[2], aux[1]
      aux[4] = np.multiply(-1, aux[4])
      aux[5] = np.multiply(-1, aux[5])
    #count node value
    if(aux[2] > nodeCount):
      nodeCount = aux[2]
      

  elif(netlist[i][0][0] == 'G'):
    aux = netlist[i]
    aux[1] = np.uintc(aux[1])
    aux[2] = np.uintc(aux[2])
    aux[3] = np.uintc(aux[3])
    aux[4] = np.uintc(aux[4])
    aux[5] = np.cdouble(aux[5])
    #swap nodes if a > b and multiply value by -1
    if(aux[1] > aux[2]):
      aux[1], aux[2] = aux[2], aux[1]
      aux[5] = np.multiply(-1, aux[5])
      #swap nodes if c > d and multiply value by -1
    if(aux[3] > aux[4]):
      aux[3], aux[4] = aux[4], aux[3]
      aux[5] = np.multiply(-1, aux[5])
    #count node value
    if(aux[2] > nodeCount):
      nodeCount = aux[2]
    #count node value
    if(aux[4] > nodeCount):
      nodeCount = aux[4]

  elif(netlist[i][0][0] == 'L'):
    aux = netlist[i]
    aux[1] = np.uintc(aux[1])
    aux[2] = np.uintc(aux[2])
    aux[3] = np.cdouble(aux[3])
    aux[4] = np.cdouble(aux[4])
    #swap nodes if a > b
    if(aux[1] > aux[2]):
      aux[1], aux[2] = aux[2], aux[1]
    #count node value
    if(aux[2] > nodeCount):
      nodeCount = aux[2]

  elif(netlist[i][0][0] == 'C'):
    aux = netlist[i]
    aux[1] = np.uintc(aux[1])
    aux[2] = np.uintc(aux[2])
    aux[3] = np.cdouble(aux[3])
    aux[4] = np.cdouble(aux[4])
    #swap nodes if a > b
    if(aux[1] > aux[2]):
      aux[1], aux[2] = aux[2], aux[1]
    #count node value
    if(aux[2] > nodeCount):
      nodeCount = aux[2]

  elif(netlist[i][0][0] == 'K'):
    aux = netlist[i]
    aux[1] = np.uintc(aux[1])
    aux[2] = np.uintc(aux[2])
    aux[3] = np.uintc(aux[3])
    aux[4] = np.uintc(aux[4])
    aux[5] = np.cdouble(aux[5])
    aux[6] = np.cdouble(aux[6])
    aux[7] = np.cdouble(aux[7])
    #count node value
    auxMax = max(aux[1],aux[2],aux[3],aux[4])
    if(auxMax > nodeCount):
      nodeCount = auxMax


      
Gn = np.zeros((nodeCount+1, nodeCount+1), dtype=complex)
I = np.zeros(nodeCount+1, dtype=complex)

#print(Gn, 'Gn\n')
#print(I, 'I\n')

#print(netlist)

for i in range(len(netlist)):
  aux = netlist[i]
  #insert resistor stamp
  if(aux[0][0] == 'R'):
    a = aux[1]
    b = aux[2]
    conductance = np.cdouble(1/aux[3])
    Gn[a][a] = Gn[a][a] + conductance
    Gn[a][b] = Gn[a][b] - conductance
    Gn[b][a] = Gn[b][a] - conductance
    Gn[b][b] = Gn[b][b] + conductance
  #insert currentSource stamp
  elif(aux[0][0] == 'I'):
    a = aux[1]
    b = aux[2]
    # i represents current value from source, not an index variable
    # i = DC + e^(j*omega)
    i = np.cdouble(aux[4] + (aux[5]*cmath.exp(1j*np.deg2rad(aux[7])) ))
    I[a] = I[a] - i
    I[b] = I[b] + i
  #insert controledCurrentSource stamp
  elif(aux[0][0] == 'G'):
    a = aux[1]
    b = aux[2]
    c = aux[3]
    d = aux[4]
    value = aux[5]
    Gn[a][c] = Gn[a][c] + value
    Gn[a][d] = Gn[a][d] - value
    Gn[b][c] = Gn[b][c] - value
    Gn[b][d] = Gn[b][d] + value
  #insert capacitor stamp
  elif(aux[0][0] == 'C'):
    a = aux[1]
    b = aux[2]
    conductance = np.cdouble(omega*aux[3]*1j)
    Gn[a][a] = Gn[a][a] + conductance
    Gn[a][b] = Gn[a][b] - conductance
    Gn[b][a] = Gn[b][a] - conductance
    Gn[b][b] = Gn[b][b] + conductance
  #insert inductor stamp
  elif(aux[0][0] == 'L'):
    a = aux[1]
    b = aux[2]
    conductance = np.cdouble(1/(omega*aux[3]*1j))
    Gn[a][a] = Gn[a][a] + conductance
    Gn[a][b] = Gn[a][b] - conductance
    Gn[b][a] = Gn[b][a] - conductance
    Gn[b][b] = Gn[b][b] + conductance
  #insert transformer stamp
  elif(aux[0][0] == 'K'):
    a = aux[1]
    b = aux[2]
    c = aux[3]
    d = aux[4]
    L1 = aux[5]
    L2 = aux[6]
    M = aux[7]
    r11 = L2/(L1*L2 - M*M)
    r22 = L1/(L1*L2 - M*M)
    r12 = -M/(L1*L2 - M*M)
    r21 = r12
    Gn[a][a] = Gn[a][a] + r11/(1j*omega)
    Gn[a][b] = Gn[a][b] - r11/(1j*omega)
    Gn[a][c] = Gn[a][c] + r12/(1j*omega)
    Gn[a][d] = Gn[a][d] - r12/(1j*omega)
    Gn[b][a] = Gn[b][a] - r11/(1j*omega)
    Gn[b][b] = Gn[b][b] + r11/(1j*omega)
    Gn[b][c] = Gn[b][c] - r12/(1j*omega)
    Gn[b][d] = Gn[b][d] + r12/(1j*omega)
    Gn[c][a] = Gn[c][a] + r21/(1j*omega)
    Gn[c][b] = Gn[c][b] - r21/(1j*omega)
    Gn[c][c] = Gn[c][c] + r22/(1j*omega)
    Gn[c][d] = Gn[c][d] - r22/(1j*omega)
    Gn[d][a] = Gn[d][a] - r21/(1j*omega)
    Gn[d][b] = Gn[d][b] + r21/(1j*omega)
    Gn[d][c] = Gn[d][c] - r22/(1j*omega)
    Gn[d][d] = Gn[d][d] + r22/(1j*omega)



  


#remove ground line/column
Gn = Gn[1:,1:]
I = I[1:]

print(Gn,'Gn\n\n',I,'I\n\n')

def solve(Gn, I ):
  e = (np.linalg.inv(Gn)).dot(I)
  e2 = np.linalg.solve(Gn,I)
  return e2

e = solve(Gn,I)
print(e)
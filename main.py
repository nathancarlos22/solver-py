# -*- coding: utf-8 -*-

import numpy as np
from ortools.linear_solver import pywraplp

"""# **Lendo arquivo**"""

path = 'Problema.txt'
arquivo = open(path,'r')
numeros = []

for linha  in arquivo:
  linha = linha.strip()
  numeros.append(linha)

arquivo.close()
numeros

x1 = numeros[0].split(' ') #variaveis e restricoes:
c = numeros[1].split(' ') #Coecicientes das variaveis na funcao objetivo

rest = len(numeros)-2 #Numeros de restrições
var = int(x1[0]) #Números de variáveis

"""# ***Formatação para entrada do modelo***
  O solver exige que os arrays sejam da seguinte forma:


*   Os arrays das restrições precisam ser separados da igualdade
  
  Ex: 
  
        x1 + x2 <= 10 e x1 + x2 <= 20
  é necessário um array [ 10, 20 ] e outro com os coeficientes das restrições
"""

a = [0]*rest #inicializando array com o numero de restricoes
b = [0]*rest 

for i in range(2, len(numeros)): #começando em dois pois oq vem depois da linha 2 sao as restricoes
    aa = numeros[i].split(' ')
    b[i-2] = aa[len(aa)-1]
    del(aa[len(aa)-1])
    a[i-2] = aa
print(a, b, c)

"""# ***Convertendo os arrays em double***
  A biblioteca or-tolls exige que as variáveis sejam desta forma
"""

a = np.double( a )
b = np.double( b )
c = np.double( c )

print(a, b, c)

"""# **Definindo tipos**

*  Para resolver o problema em inteiro ou não
  
        intOrNot = True
        intOrNot = False

*  Setar igualdades das restrições
  
        LessMoreOrEqual = 'MoreOrEqual'
        LessMoreOrEqual = 'LessOrEqual'
      
* Setar função objetivo

        MaxOrMin = 'Min'
        MaxOrMin = 'Max'
"""

IntOrNot = False
LessMoreOrEqual = 'MoreOrEqual'
MaxOrMin = 'Min'

"""# ***Criando o modelo***"""

def create_data_model(A, B, C, num_vars, num_rest):
  data = {}
  data['constraint_coeffs'] = A
  data['bounds'] = B
  data['obj_coeffs'] = C
  data['num_vars'] = num_vars
  data['num_constraints'] = num_rest
  return data

data = create_data_model(a, b, c, var, rest)

"""# **Main**"""

def main(IntOrNot, LessMoreOrEqual, MaxOrMin):

  solver = pywraplp.Solver('simple_mip_program', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

  infinity = solver.infinity()
  x = {}

  if IntOrNot == False:
    for j in range(data['num_vars']):
        x[j] = solver.NumVar(0, infinity, 'x[%i]' % j) #Variáveis positivas
  else:
    for j in range(data['num_vars']):
        x[j] = solver.IntVar(0, infinity, 'x[%i]' % j) #Variáveis positivas inteiras
  
  print('Numero de variaveis =', solver.NumVariables())
  
  if LessMoreOrEqual == 'LessOrEqual':
    for i in range(data['num_constraints']):
        constraint = solver.RowConstraint(0, data['bounds'][i], '')#limite inferior, superor e nome da restrição
        for j in range(data['num_vars']):
            constraint.SetCoefficient(x[j], data['constraint_coeffs'][i][j]) 
  
  if LessMoreOrEqual == 'MoreOrEqual':
    for i in range(data['num_constraints']):
      constraint = solver.RowConstraint(data['bounds'][i], infinity, '')#limite inferior, superior e nome da restrição
      for j in range(data['num_vars']):
        constraint.SetCoefficient(x[j], data['constraint_coeffs'][i][j]) 
  
  print('Numero de restriçoes =', solver.NumConstraints())

  objective = solver.Objective()
  
  for j in range(data['num_vars']):
      objective.SetCoefficient(x[j], data['obj_coeffs'][j])
  
  if MaxOrMin == 'Max':
    objective.SetMaximization()
  else:
    objective.SetMinimization()

  status = solver.Solve()

  if status == pywraplp.Solver.OPTIMAL:
      print('Valor ótimo = ', solver.Objective().Value())
      for j in range(data['num_vars']):
          print(x[j].name(), ' = ', x[j].solution_value())
      print()
      print('Problema resolvido em %f milliseconds' % solver.wall_time())
      print('Problema resolvido em %d iteracoes' % solver.iterations())
      print('Problema resolvido em %d branch-and-bound nodes' % solver.nodes())
  else:
      print('Nao tem solucao otima.')

main(IntOrNot, LessMoreOrEqual, MaxOrMin)

"""# **Dual**"""

aT = np.transpose( a )
bT = c
cT = b

num_varsT = rest
num_restT = var

IntOrNot = False
LessMoreOrEqual = 'LessOrEqual'
MaxOrMin = 'Max'

print(aT, bT, cT, num_varsT, num_restT)

data = create_data_model(aT, bT, cT, num_varsT, num_restT)

main(IntOrNot, LessMoreOrEqual, MaxOrMin)


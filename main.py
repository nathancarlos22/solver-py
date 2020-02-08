import numpy as np
from scipy.optimize import linprog
from ortools.linear_solver import pywraplp

x1 = input("variaveis e restricoes: ").split(' ')

c = input("Coecicientes das variaveis na funcao objetivo: ").split(' ')

rest = int(x1[1])
var = int(x1[0])

a = [0]*rest #inicializando array com o numero de restricoes
b = [0]*rest 
for i in range(rest):
    aa = input("Restricao: ").split(' ')
    b[i] = aa[len(aa)-1]
    del(aa[len(aa)-1])
    a[i] = aa
    #print(a)
    #print(b)
    

#convertendo os arrays em double
a = np.double( a )
#a = a.astype('double')

b = np.double(b)
#b = b.astype('double')

c = np.double( c )
#c = c.astype('double')

print(a, b, c)

def create_data_model():
  data = {}
  data['constraint_coeffs'] = a
  data['bounds'] = b
  data['obj_coeffs'] = c
  data['num_vars'] = var
  data['num_constraints'] = rest
  return data

def main():
    data = create_data_model()

    #modelo inteiro MIXED_INTEGER_PROGRAMMING
    solver = pywraplp.Solver('simple_mip_program', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    infinity = solver.infinity()
    x = {}
    for j in range(data['num_vars']):
        x[j] = solver.IntVar(0, infinity, 'x[%i]' % j)
    print('Numero de variaveis =', solver.NumVariables())

    for i in range(data['num_constraints']):
        constraint = solver.RowConstraint(data['bounds'][i], infinity, '')#limite superior, inferior e nome da restrição
        for j in range(data['num_vars']):
            constraint.SetCoefficient(x[j], data['constraint_coeffs'][i][j]) 
    print('Numero de restriçoes =', solver.NumConstraints())
    
    objective = solver.Objective()
    for j in range(data['num_vars']):
        objective.SetCoefficient(x[j], data['obj_coeffs'][j])
    objective.SetMinimization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Objective value =', solver.Objective().Value())
        for j in range(data['num_vars']):
            print(x[j].name(), ' = ', x[j].solution_value())
        print()
        print('Problema resolvido em %f milliseconds' % solver.wall_time())
        print('Problema resolvido em %d iteracoes' % solver.iterations())
        print('Problema resolvido em %d branch-and-bound nodes' % solver.nodes())
    else:
        print('Nao tem solucao otima.')

main()

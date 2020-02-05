import numpy as np
from scipy.optimize import linprog

x = input("variaveis e restricoes: ").split(' ')

c = input("Coecicientes das variaveis na funcao objetivo: ").split(' ')
rest = int(x[1])

a = [0]*rest #inicializando array com o numero de restricoes
b = [0]*rest 
for i in range(rest):
    aa = input("Restricao: ").split(' ')
    b[i] = aa[len(aa)-1]
    del(aa[len(aa)-1])
    a[i] = aa
    #print(a)
    #print(b)
    

# A = np.array(a)
# B = np.array(b)
# C = np.array(c)


res = linprog(c, A_ub=a, b_ub=b,bounds=(0, None))

print ("Valor otimo: ", res.fun)
print ("X:")
for k, xk in enumerate(res.x):
    print ("x_{", str(k+1), "} = ", xk)


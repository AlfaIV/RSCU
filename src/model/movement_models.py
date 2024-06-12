from math import cos, sin

# Реализация прямого с постоянным углом упреждения
def directWithConstLeadAngle(vartheta, epsilon ,phi_0):
    return vartheta - epsilon - phi_0

# Реализация прямого метода 
def direct(vartheta, epsilon):
    return vartheta - epsilon

# Реализация метода параллельного сближения
def parallelApproach(q_o, V_o, q_t, V_t):
    return q_o - V_t/V_o*sin(q_t)
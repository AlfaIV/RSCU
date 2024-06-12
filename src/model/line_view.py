import numpy as np
from math import sqrt, atan2, sin, radians
# Для работы требуется numpy

# Реализован класс линии визирования, который "соединяет"
# два объекта которые реализованны наследование от класса Object 
class LineOfView:

    # Подразумевается, что для получения значений параметров во избежании дублирования
    # записей в истории, методы получения этих параметров приватные(нельзя использовать извне) и
    # в истории актуальные значения параметров.
    # Подразумевается, что шкала времени object, target равна
    def __init__(self, object, target):
        self.object_1 = object # объект управления
        self.object_2 = target # цель
        
        # Списки для сохранения истории изменения параметров
        self.dX = [] # приращение координаты
        self.dY = [] # приращение координаты
        self.R = [] # дистанция между объектами
        self.epsilon = [] # угол визирования
        self.derivative_R = [] # скорость сближения тел
        self.derivative_epsilon = [] # скорость вращения линии визирования
 
    # Вычисление разности координат
    def _getIncrements(self):
        self.dX.append(self.object_2.getPath()[-1][0] - self.object_1.getPosition()[0])
        self.dY.append(self.object_2.getPath()[-1][1] - self.object_1.getPosition()[1])
        return self.dX[-1], self.dY[-1]
    
    # Вычисление расстояния между целью и объектом управления
    def _getDistance(self):
        dX = self.dX[-1]
        dY = self.dY[-1]
        
        R = sqrt(dX**2 + dY**2)  
        self.R.append(R)
        return R
    
    # Вычисление скорости сближения объектов
    # Подразумевается, что шкала времени object_1, object_2 равна
    def _getSpeedApproach(self):

        # self.derivative_R.append(np.diff(self.R)/self.object_1.dT)
        if len(self.R) > 1:
            derivative_R = (self.R[-1] - self.R[-2])//self.object_1.dT
        else:
            derivative_R = (self.R[-1])//self.object_1.dT
        self.derivative_R.append(derivative_R)

        return derivative_R

    # Вычисления угла линии визирования
    def _getAngelLV(self):
        dX = self.dX[-1]
        dY = self.dY[-1]

        epsilon = atan2(dY, dX)
        self.epsilon.append(epsilon)
        return epsilon
    
    # Вычисление скорости вращения линии визирования
    def _getDerivativeEpsilon(self):

        target = self.object_2
        epsilon = self.epsilon[-1]
        R = self.R[-1]

        derivative_epsilon_2 = (target.velocity*sin(radians(180) - target.direction + epsilon))/R
        derivative_epsilon_1 = (target.velocity*sin(abs(target.direction - epsilon)))/R
        derivative_epsilon = derivative_epsilon_1 - derivative_epsilon_2
        self.derivative_epsilon.append(derivative_epsilon)

        return derivative_epsilon
    
    # Получение всех параметров линии визирования
    def getAllParams(self):
        self._getIncrements()
        self._getDistance()
        self._getAngelLV()
        self._getSpeedApproach()
        self._getDerivativeEpsilon()
        

        epsilon = self.epsilon[-1]
        R = self.R[-1]
        dX = self.dX[-1]
        dY = self.dY[-1]
        derivative_epsilon = self.derivative_epsilon[-1]
        derivative_R = self.derivative_R[-1]

        return dX, dY, epsilon, R, derivative_epsilon, derivative_R

    # Очистка истории слежения за линией визирования
    def clearHistory(self):
        self.dX = []
        self.dY = []
        self.R = []
        self.epsilon = []
        self.derivative_R = []
        self.derivative_epsilon = []
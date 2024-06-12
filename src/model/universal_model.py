from math import atan2, radians, cos, sin, sqrt

# Базовый объект, который реализует основные методы для получения
# основных параметров системы. На основе него формируются объекты
# с требуемым типом движения 
class Object:
    
    dT = 1
    # метод для установки шкалы времени общей для всех экземпляров класса
    @staticmethod
    def setTimeStep(timeStep):
        Object.dT = timeStep

    # конструктор, который задает начальное положение тела
    # !!! стоит обратить внимание, что функция должна принимать массивы координат объекта
    def __init__(self, initialX, initialY):
        if isinstance(initialX, list) and all(isinstance(x, (int, float)) for x in initialX) and \
        isinstance(initialY, list) and all(isinstance(y, (int, float)) for y in initialY):
            self.x = initialX
            self.y = initialY
        else:
            print("Некометная инициализация объекта! Исправьте начальные координаты объекта.")
            raise

    # возвращается матрица перемещений объекта(например для построения графиков перемещений)
    # первый столбец - x, второй - y. 
    def getPath(self):
        return list(zip(self.x, self.y))
    
    # возвращается текущее положение объекта
    def getPosition(self):
        return [self.x[-1], self.y[-1]]
    
    # возвращается текущий угол наклона цели относительно горизонтальной оси
    # рассчитывается на основе текущего и предыдущего положения объекта
    def getDirection(self):
        dX = self.x[-1] - self.x[-2]
        dY = self.y[-1] - self.y[-2]
        self.direction = atan2(dY, dX)
        return self.direction
    
    # задается  угол наклона цели относительно горизонтальной оси
    # !!! стоит обратить внимание, что данный метод не меняет положение тела,
    #  учитывается на следующем шаге движения тела
    def setDirection(self, newDirection):
        self.direction = newDirection

    # возвращается текущий угол наклона цели относительно горизонтальной оси
    # рассчитывается на основе текущего и предыдущего положения объекта
    def getVelocity(self):
        dT = self.dT
        dX = self.x[-1] - self.x[-2]
        dY = self.y[-1] - self.y[-2]
        self.velocity = sqrt((dX/dT)**2 + (dY/dT)**2)
        return (dX/dT, dY/dT, self.velocity)
    
    # установка скорости перемещения объекта
    def setVelocity(self, newVelocity):
        self.velocity = newVelocity
    
    # установка ускорения объекта
    def setAcceleration(self, acceleration):
        self.acceleration = acceleration
    
    # перемещение объекта в произвольную координату
    # данный метод не учитывает характер перемещения цели
    def moveTo(self, newX, newY):
        self.x.append(newX)
        self.y.append(newY)

    # установка описания объекта
    # для подписей графиков
    def setDescription(self, text):
        self.description = text

    # получения описания объекта
    def getDescription(self):
        return self.description

# Пример объекта со специфическим паттерном движения.
# Данный класс реализует объект, который движется с ускорением,
# которое действует перпендикулярно вектору скорости(нормальное ускорение)
class ObjectConstVelocity(Object):
    # конструктор, который задает начальные параметры движения
    def __init__(self,
                 initialX,
                 initialY,
                 direction,
                 velocity,
                 acceleration,
                 description = ''):
        
        super().__init__(initialX, initialY)

        self.direction =  radians(direction)
        self.velocity = velocity
        self.acceleration = acceleration
        self.setDescription(description)
        
    # перемещение объекта
    # на основе следующего уравнения
    # x_1 = x_0 + V_x*t + a_x*t**2/2
    # аналогично для y. Все с учетом проекций.
    def nextMove(self):
        dT = self.dT
        oldX, oldY = super().getPosition()
        newX = oldX + self.velocity*cos(self.direction)*dT + self.acceleration*cos(self.direction - radians(90))*dT**2/2
        newY = oldY + self.velocity*sin(self.direction)*dT + self.acceleration*sin(self.direction - radians(90))*dT**2/2
        super().moveTo(newX, newY)
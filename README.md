# XL320 uPy
Los scripts de este repositorio han sido creados a partir del siguiente repositorio: https://github.com/MultipedRobotics/pyxl320

## Constructor
~~~~ python
xl320(self, baudrate=1000000, serialid=2)
~~~~

* baudrate: define los baudios con el cual se utilizara el motor
* serialid: define que pines tx, rx del ESP se usaran, por default UART(2)

### Ejemplo de inicialización de objeto

~~~~ python
from xl320 import *
dxl=xl320()
~~~~

Si se desean baudios o UART(1)
~~~~ python
from xl320 import *
dxl=xl320(baudrate=15200,serialid=1)
~~~~

## Métodos
### write(ID, reg=None, params=None) (metodo genérico para escritura a RAM o EEPROM)
Por default se tiene como instrucción que sea escritura, corresponde a 0x03
* ID: es definido como entero desde 1-253, con 254 se hace un broadcast
* reg: registro, dependiendo de lo que se quiera hacer, definidos al inicio de `xl320.py`
* params: si el registro recibe parametros de 1 byte, se puede definir el valor como un entero, sino se debe especificar como le(valor)
Para más información: http://emanual.robotis.com/docs/en/dxl/x/xl320/

### torqueenable(ID, status)
* status: puede ser 0 o 1. 0 deshabilita el torque, 1 lo habilita. Si status=1 y el torque es habilitado, la memoria EEPROM se bloquea, y no puede ser modificada hasta que sea deshabilitado el torque.

### controlmode(ID, mode)
* mode: puede ser 1 o 2. Si es 1 (wheel) o 2 (joint)

### goalspeed(ID, speed)
* speed:
	* Modo wheel: modifica a que velocidad se mueve el motor.
	* Modo joint: modifica que tan rapido gira cuando se cambia su posición o ángulo.

### goalposition(ID, position)
* position: angulo en que se quiere el servo. Debe estar en modo joint para funcionar.


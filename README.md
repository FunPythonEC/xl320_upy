# Dynamixel XL-320 uPy (MicroPython)
Los scripts en este repositorio han sido creados a partir del siguiente: https://github.com/MultipedRobotics/pyxl320

Se encuentra aquí el script de `xl320.py`, el cual contiene la clase `xl320`, los metodos y funciones necesarios para poder dar uso de los motores dynamixel xl320 eficaz y rapidamente con MicroPython, especificamente para los microcontroladores ESP8266 y ESP32.

## Comunicación con el motor

Para la comunicación se utiliza UART. A pesar de que los motores dynamixel para la comunicación utilizan un pin DATA, este ha sido manejado usando una configuración de transistores especificada en el siguiente link: [UART to 1-WIRE interface](https://hackaday.com/2015/01/29/easier-uart-to-1-wire-interface/)

Para su uso en la parte de programación, se ha especificado en el constructor de `xl320()`, el id de UART a usar que es especificado como serialid, ya que ciertas placas carecen de cierta cantidad de objetos UART para crear. Correspondiendo entonces serialid al numero de UART usado en el microcontrolador.  Para más información de UART con uPy: [UART MicroPython](https://docs.micropython.org/en/latest/library/machine.UART.html)

## `XL320.PY`

En este script se ha incluido todo lo necesario para poder hacer uso del motor. En este se puede encontrar la clase `xl320` con su respectivo constructor y metodos. Su uso es especificado a continuación

### Constructor

~~~~ python
xl320(self, baudrate=1000000, serialid=2)
~~~~

* baudrate: define los baudios con el cual se utilizará el motor
* serialid: define que pines tx, rx del ESP se usaran, por default UART(2)
Tener en cuenta que hay valores especificados como default en el constructor de la clase, por lo que si se quiere unos distintos, este debe ser especficado. Además se permite la creación de distintos objetos para el uso de motores, en el caso del ESP32 se permite hasta 3 lineas de motores. Para el ESP8266 tan solo 2. Con linea de motores, se refiere a motores conectados en serie en distintos buses.

#### Ejemplo de inicialización de objeto

~~~~ python
from xl320 import *
dxl=xl320()
~~~~

Si se desea especificar el baudrate o el serial uart a usar:
~~~~ python
from xl320 import *
dxl=xl320(baudrate=15200,serialid=1)
~~~~

### Métodos
#### Genéricos
##### write
##### read
#### Especificos de escritura
#### Especificos de lectura

### Desde aquí para abajo todavía se necesita actualizar la documentación

Revisar el script xl320.py para entender con anticipación.

#### write(ID, reg=None, params=None) (metodo genérico para escritura a RAM o EEPROM)
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

## Referencias
* [XL320 Dynamixel](http://emanual.robotis.com/docs/en/dxl/x/xl320/)

* [XL320 Dynamixel Further Documentation](http://support.robotis.com/en/product/actuator/dynamixel_x/xl_series/xl-320.htm)

* [CRC Calculator](http://support.robotis.com/en/product/actuator/dynamixel_pro/communication/crc.htm)

* [Instruction Packet Protocol 2.0](http://support.robotis.com/en/product/actuator/dynamixel_pro/communication/instruction_status_packet.htm)

  


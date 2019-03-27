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
Para la clase se han creado una serie de metodos especificos para su uso. En los cuales se usan funciones encontradas en el mismo script. Como le() y makePacket().

Los metodos especificos, son para el control sobre el ID, baudrate, goal speed, present speed, etc. Pero también se agrego un metodo llamado sendPacket() el cual es un método genérico, este es más detallado en la próxima sección.
#### Genéricos
##### sendPacket()
Este metodo del objeto, esta principalmente para poder enviar por UART, un paquete propio creado.
Para la creación de un paquete se puede usar el metodo de `makePacket(ID, instr, reg=None, params=None)`, el cual regresa un array con los valores a enviar por serial.
###### Ejemplo
~~~~ python
from xl320 import *
dxl=xl320()
#cambio de id, de 1 a 2
pkt=makePacket(1,WRITE,XL320_ID,[2])
~~~~
Tener en cuenta que en el ejemplo anterior, se hace un cambio de id, el cual es un registro al cual le corresponde 1 byte, por lo que en el metodo basta con poner como parametro [2], mientras que si este fuera de 2 bytes, se tendria que usar el metodo le() que se encuentra en el mismo script. Basicamente el metodo le() se encarga de representar un numero mayor a 255 en dos bytes.
#### Especificos de escritura
##### EEPROM
Tener en cuenta que para que el EEPROM sea modificable, es necesario que TORQUE_ENABLE tenga 0 como valor, si es cambiado a 1, EEPROM no puede ser modificado.
|Metodo|Descripcion de parametros|
|------------|:--------------------------------------|
|set_control_mode(ID, mode)| **ID**: corresponde al id del motor al cual se le quiere cambiar el modo. Puede ser un valor desde 1 hasta 253. **mode**: puede ser 1 o 2. 1 para el modo WHEEL y 2 para JOINT|
|| |
|| |
|| |
|| |
|| |

##### RAM
#### Especificos de lectura
##### EEPROM
##### RAM


## Referencias
* [XL320 Dynamixel](http://emanual.robotis.com/docs/en/dxl/x/xl320/)

* [XL320 Dynamixel Further Documentation](http://support.robotis.com/en/product/actuator/dynamixel_x/xl_series/xl-320.htm)

* [CRC Calculator](http://support.robotis.com/en/product/actuator/dynamixel_pro/communication/crc.htm)

* [Instruction Packet Protocol 2.0](http://support.robotis.com/en/product/actuator/dynamixel_pro/communication/instruction_status_packet.htm)

  


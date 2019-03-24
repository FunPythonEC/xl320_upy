import machine as m
import time

# --------- INSTRUCTIONS -----
PING      = 0x01
READ      = 0x02
WRITE     = 0x03
REG_WRITE = 0x04
ACTION    = 0x05
RESET     = 0x06
REBOOT    = 0x08
STATUS    = 0x55
SYNC_READ  = 0x82
SYNC_WRITE = 0x83
BULK_READ  = 0x92
BULK_WRITE = 0x93

# -------- EEPROM -------------
MODEL_NUMBER    = 0
VER_FIRMWARE    = 2
ID              = 3
BAUD_RATE       = 4
DELAY_TIME      = 5
CW_ANGLE_LIMIT  = 6   # min angle, default 0
CCW_ANGLE_LIMIT = 8   # max angle, default 300
CONTROL_MODE    = 11  # joint or wheel mode, default joint (servo)
MAX_TORQUE      = 15
RETURN_LEVEL    = 17

# -------- RAM ----------------
TORQUE_ENABLE    = 24  # servo mode on/off - turn into wheel
LED              = 25
GOAL_POSITION    = 30
GOAL_VELOCITY    = 32
GOAL_TORQUE      = 35
PRESENT_POSITION = 37  # current servo angle
PRESENT_SPEED    = 39  # current speed
PESENT_LOAD      = 41  # current load
PESENT_VOLTAGE   = 45  # current voltage
PESENT_TEMP      = 46  # current temperature
MOVING           = 49
HW_ERROR_STATUS  = 50
PUNCH            = 51

# --------- OTHER -------------
RESET_ALL                  = 0xFF
RESET_ALL_BUT_ID           = 0x01
RESET_ALL_BUT_ID_BAUD_RATE = 0x02
LED_WHITE                  = 7
LED_BLUE_GREEN             = 6
LED_PINK                   = 5
LED_BLUE                   = 4
LED_YELLOW                 = 3
LED_GREEN                  = 2
LED_RED                    = 1
LED_OFF                    = 0
BROADCAST_ADDR             = 0xfe  # a packet with this ID will go to all servos
WHEEL_MODE                 = 1
JOINT_MODE                 = 2  # normal servo
XL320_9600                       = 0  # 0: 9600, 1:57600, 2:115200, 3:1Mbps
XL320_57600                      = 1
XL320_115200                     = 2
XL320_1000000                    = 3

crc_table = [
	0x0000, 0x8005, 0x800F, 0x000A, 0x801B, 0x001E, 0x0014, 0x8011,
	0x8033, 0x0036, 0x003C, 0x8039, 0x0028, 0x802D, 0x8027, 0x0022,
	0x8063, 0x0066, 0x006C, 0x8069, 0x0078, 0x807D, 0x8077, 0x0072,
	0x0050, 0x8055, 0x805F, 0x005A, 0x804B, 0x004E, 0x0044, 0x8041,
	0x80C3, 0x00C6, 0x00CC, 0x80C9, 0x00D8, 0x80DD, 0x80D7, 0x00D2,
	0x00F0, 0x80F5, 0x80FF, 0x00FA, 0x80EB, 0x00EE, 0x00E4, 0x80E1,
	0x00A0, 0x80A5, 0x80AF, 0x00AA, 0x80BB, 0x00BE, 0x00B4, 0x80B1,
	0x8093, 0x0096, 0x009C, 0x8099, 0x0088, 0x808D, 0x8087, 0x0082,
	0x8183, 0x0186, 0x018C, 0x8189, 0x0198, 0x819D, 0x8197, 0x0192,
	0x01B0, 0x81B5, 0x81BF, 0x01BA, 0x81AB, 0x01AE, 0x01A4, 0x81A1,
	0x01E0, 0x81E5, 0x81EF, 0x01EA, 0x81FB, 0x01FE, 0x01F4, 0x81F1,
	0x81D3, 0x01D6, 0x01DC, 0x81D9, 0x01C8, 0x81CD, 0x81C7, 0x01C2,
	0x0140, 0x8145, 0x814F, 0x014A, 0x815B, 0x015E, 0x0154, 0x8151,
	0x8173, 0x0176, 0x017C, 0x8179, 0x0168, 0x816D, 0x8167, 0x0162,
	0x8123, 0x0126, 0x012C, 0x8129, 0x0138, 0x813D, 0x8137, 0x0132,
	0x0110, 0x8115, 0x811F, 0x011A, 0x810B, 0x010E, 0x0104, 0x8101,
	0x8303, 0x0306, 0x030C, 0x8309, 0x0318, 0x831D, 0x8317, 0x0312,
	0x0330, 0x8335, 0x833F, 0x033A, 0x832B, 0x032E, 0x0324, 0x8321,
	0x0360, 0x8365, 0x836F, 0x036A, 0x837B, 0x037E, 0x0374, 0x8371,
	0x8353, 0x0356, 0x035C, 0x8359, 0x0348, 0x834D, 0x8347, 0x0342,
	0x03C0, 0x83C5, 0x83CF, 0x03CA, 0x83DB, 0x03DE, 0x03D4, 0x83D1,
	0x83F3, 0x03F6, 0x03FC, 0x83F9, 0x03E8, 0x83ED, 0x83E7, 0x03E2,
	0x83A3, 0x03A6, 0x03AC, 0x83A9, 0x03B8, 0x83BD, 0x83B7, 0x03B2,
	0x0390, 0x8395, 0x839F, 0x039A, 0x838B, 0x038E, 0x0384, 0x8381,
	0x0280, 0x8285, 0x828F, 0x028A, 0x829B, 0x029E, 0x0294, 0x8291,
	0x82B3, 0x02B6, 0x02BC, 0x82B9, 0x02A8, 0x82AD, 0x82A7, 0x02A2,
	0x82E3, 0x02E6, 0x02EC, 0x82E9, 0x02F8, 0x82FD, 0x82F7, 0x02F2,
	0x02D0, 0x82D5, 0x82DF, 0x02DA, 0x82CB, 0x02CE, 0x02C4, 0x82C1,
	0x8243, 0x0246, 0x024C, 0x8249, 0x0258, 0x825D, 0x8257, 0x0252,
	0x0270, 0x8275, 0x827F, 0x027A, 0x826B, 0x026E, 0x0264, 0x8261,
	0x0220, 0x8225, 0x822F, 0x022A, 0x823B, 0x023E, 0x0234, 0x8231,
	0x8213, 0x0216, 0x021C, 0x8219, 0x0208, 0x820D, 0x8207, 0x0202
]

HEADER = [0xFF, 0xFF, 0xFD, 0x00]

class xl320(object):
	#constructor
	def __init__(self, baudrate=1000000, serialid=2):
		
		self.baudrate=baudrate
		self.serialid=serialid

		#definicion de objeto serial
		try:
			self.uart = m.UART(self.serialid,self.baudrate)
			self.uart.init(self.baudrate, bits=8, parity=None, stop=1)
		except Exception as e:
			print(e)

	#METODO GENERICO ESCRITURA
	def write(self, ID, reg=None, params=None):

		try:
			self.uart.write(bytearray(makePacket(ID, WRITE, reg, params)))
		except Exception as e:
			print(e)

		time.sleep_us(500)
		while True:
			msg=self.uart.read()
			if msg is not None and msg!=bytearray(pkt):
				break
		print(msg)

	#METODO GENERICO LECTURA
	def read(self, ID, reg, length):

		try:
			self.uart.write(bytearray(makePacket(ID, READ, reg, le(length))))
		except Exception as e:
			print(e)

		time.sleep_us(500)
		while True:
			msg=self.uart.read()
			if msg is not None and msg!=bytearray(pkt):
				break
		print(msg)

#----------------------METODOS ESPECIFICOS ESCRITURA------------------------------
	def torqueenable(self, ID, status): #default 0 (torque disabled), 1 (torque enabled), cuando torque enabled, eeprom es bloqueado
		comwrite(self.uart,ID,TORQUE_ENABLE,[status])

	def controlmode(self,ID, mode): # 1 (wheel), 2 (joint)
		comwrite(self.uart,ID,CONTROL_MODE,[mode])

	def goalspeed(self, ID, speed):
		comwrite(self.uart,ID,GOAL_VELOCITY,le(speed))

	def goalposition(self, ID, position):
		comwrite(self.uart,ID,GOAL_POSITION,le(int(position/300*1023)))

#---------------------METODO ESPECIFICOS LECTURA----------------------------------
	def readposition(self, ID):
		comread(self.uart,ID,PRESENT_POSITION,le(2))

	def readbaudrate(self,ID):
		comread(self.uart,ID,BAUD_RATE,le(1))

#--------------------METODOS EXTERNOS--------------------------------------
def comwrite(com, ID, reg=None, params=None):
		try:
			pkt=bytearray(makePacket(ID, WRITE, reg, params))
			com.write(pkt)
		except Exception as e:
			print(e)

		time.sleep_us(500)
		while True:
			msg=com.read()
			if msg is not None and msg!=bytearray(pkt):
				break
		print(msg)

def comread(com, ID, reg, length):

		try:
			pkt=bytearray(makePacket(ID, WRITE, reg, params))
			com.write(pkt)
		except Exception as e:
			print(e)

		time.sleep_us(500)
		while True:
			msg=com.read()
			if msg is not None and msg!=bytearray(pkt):
				break
		print(msg)

def makePacket(ID, instr, reg=None, params=None):
	"""
	This makes a generic packet.

	TODO: look a struct ... does that add value using it?

	0xFF, 0xFF, 0xFD, 0x00, ID, LEN_L, LEN_H, INST, PARAM 1, PARAM 2, ..., PARAM N, CRC_L, CRC_H]
	in:
		ID - servo id
		instr - instruction
		reg - register
		params - instruction parameter values
	out: packet
	"""
	pkt = []
	pkt += HEADER  # header and reserved byte
	pkt += [ID]
	pkt += [0x00, 0x00]  # length placeholder
	pkt += [instr]  # instruction
	if reg:
		pkt += le(reg)  # not everything has a register
	if params:
		pkt += params    # not everything has parameters
	length = le(len(pkt) - 5)  # length = len(packet) - (header(3), reserve(1), id(1))
	pkt[5] = length[0]  # L
	pkt[6] = length[1]  # H
	crc = crc16(pkt)
	pkt += le(crc)
	print(pkt)
	return pkt

# util function?
def le(h):
	"""
	Little-endian, takes a 16b number and returns an array arrange in little
	endian or [low_byte, high_byte].
	"""
	h &= 0xffff  # make sure it is 16 bits
	return [h & 0xff, h >> 8]

def crc16(data_blk):
	"""
	Calculate crc

	in: data_blk - entire packet except last 2 crc bytes
	out: crc_accum - 16 word
	"""
	data_blk_size = len(data_blk)
	crc_accum = 0
	for j in range(data_blk_size):
		i = ((crc_accum >> 8) ^ data_blk[j]) & 0xFF
		crc_accum = ((crc_accum << 8) ^ crc_table[i])
		crc_accum &= 0xffff  # keep to 16 bits

	return crc_accum
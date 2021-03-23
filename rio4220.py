
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

class rio4220(ModbusClient):
    def __init__(self, _host, baud=19200, device=1):
        try:
            self.host = _host
            self.baud = baud
            self.device = device
            ModbusClient.__init__(self, method='rtu', port=_host, baudrate=baud, parity = 'N', timeout=1.5)
            ret = self.connect()
            if ret:
                print("open modbus")            
                return
            raise Exception("Can't open tcp rtu")
        except Exception as ex:
            raise Exception("tcp_rtu: " + str(ex))
    def read_input(self, add):
        temps = self.read_coils(add, 1, unit=(self.device))
        try:
            return (temps.bits == [True])
        except Exception as ex:
            raise Exception("read_input: " + str(ex))
            
    def read_register(self, add):
        temps = self.read_input_registers(add, 1, unit=(self.device))
        return temps.registers[0]
        
    def read_holding_register(self, add):
        temps = self.read_holding_registers(add, 1, unit=(self.device))
        return temps.register
        
    def write_output(self, add, value):
        print("value = " + str(value))
        print("add = " + str(add))
        print("self.device = " + str(self.device))
        rq = self.write_coils(add, [value], unit=(self.device))
        return rq

  
    

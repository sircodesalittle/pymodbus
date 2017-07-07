#!/usr/bin/env python


from pymodbus.server.async import StartTcpServerMany

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

from pymodbus.transaction import ModbusRtuFramer
#---------------------------------------------------------------------------# 
# configure the service logging
#---------------------------------------------------------------------------# 
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)


store = ModbusSlaveContext(
    di = ModbusSequentialDataBlock(0, [17]*100),
    co = ModbusSequentialDataBlock(0, [17]*100),
    hr = ModbusSequentialDataBlock(0, [17]*100),
    ir = ModbusSequentialDataBlock(0, [17]*100))
context = ModbusServerContext(slaves=store, single=True)

identity = ModbusDeviceIdentification()
identity.VendorName  = 'Pymodbus'
identity.ProductCode = 'PM'
identity.VendorUrl   = 'http://github.com/riptideio/pymodbus/'
identity.ProductName = 'Pymodbus Server'
identity.ModelName   = 'Pymodbus Server'
identity.MajorMinorRevision = '1.0'


# Add your addresses here (or throw addresses into addresses via a for loop).
addresses = [("172.20.10.3", 5020),
             ("172.20.10.4", 5020),
             ("172.20.10.5", 5020),
             ("172.20.10.6", 5020)]

from threading import Thread
# Without testing...
# StartTcpServerMany(context, identity=identity, addresses=addresses)

t = Thread(target=StartTcpServerMany, args=(context,), kwargs={"identity": identity, "addresses": addresses})
t.start()

# See if all the servers are up
from pymodbus.client.sync import ModbusTcpClient

for address in addresses:
    try:
        client = ModbusTcpClient(host=address[0], port=address[1])
        result = client.read_coils(1,1)
        # print result.bits[0]
        client.close()
    except Exception:
        print('Exception while testing {}'.format(str(address)))

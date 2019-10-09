import wmi
import time
import mysql.connector

w = wmi.WMI(namespace="root\OpenHardwareMonitor")
temperature_infos = w.Sensor()
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Mwbyfy23c",
    database="rpi",
)
mycursor = mydb.cursor()

cpuLoad = 0
gpuTemp = 0

while True:
    temperature_infos = w.Sensor()
    for sensor in temperature_infos:
        if sensor.identifier == u'/nvidiagpu/0/temperature/0':
            gpuTemp = sensor.Value

        if sensor.identifier == u'/intelcpu/0/load/0':
            cpuLoad = sensor.Value

        if sensor.identifier == u'/nvidiagpu/0/load/0':
            sql = "INSERT INTO pc_sensors (`partName`, `load`, `temp`) VALUES (%s, %s,%s)"
            val = (sensor.Name, sensor.Value, gpuTemp)
            mycursor.execute(sql, val)
            mydb.commit()

        if sensor.identifier == u'/intelcpu/0/temperature/4':
            sql = "INSERT INTO pc_sensors (`partName`, `load`, `temp`) VALUES (%s, %s,%s)"
            val = (sensor.Name, cpuLoad, sensor.Value)
            mycursor.execute(sql, val)
            mydb.commit()

    time.sleep(15)

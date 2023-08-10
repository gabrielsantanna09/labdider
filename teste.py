import time
import serial

ser = serial.Serial('COM5', 9600)
time.sleep(2)
data =[]                       
for i in range(20):
    b = ser.readline()         
    string_n = b.decode()   
    string = string_n.rstrip() 
    flt = float(string)        
    data.append(flt)           
    time.sleep(0.1)            

ser.close()
print(data)
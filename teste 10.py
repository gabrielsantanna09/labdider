import matplotlib.pyplot as plt
import numpy as np
import time
import serial  # importacao do modulo serial
import random

leitura = []
fig, ax = plt.subplots()
ser = serial.Serial('COM5',9600)  # abre porta serial COM6
angulo = []
voltagem = []
contador = 0
eixo_x = 50
a = 1
dados = []
while True:
    while (ser.inWaiting() == 0):
        pass
    b = ser.readline()
    string_n = b.decode()
    string = string_n.rstrip()
    flt = float(string)
    dados.append(flt)
    print("Variável data")
    print(dados)
    ##Aqui queremos separar as variáveis angulo e voltagem que vem do arduíno
    if contador % 2 == 1:
        voltagem.append(dados[contador])
    else:
        angulo.append(dados[contador])
        if (angulo[-1] > (eixo_x - 10)):
            eixo_x = eixo_x + 50

    #dados = float(ser.readline()[:(a)])  # firmware deve ter um delay de pelo menos 100ms entre cada envio
    #print(dados)
    #ax.clear()
    ax.set_xlim([0, eixo_x])  # faixa do eixo horizontal
    ax.set_ylim([0, 4])  # faixa do eixo vertical

    #ax.figure(figsize=center)
    # leitura.append(random.randint(0,1023))  #teste com numeros aleatorios
    #if contador % 2 == 1:
    #   voltagem.append(dados[contador])
    #else:
    #    angulo.append(dados[contador])
    leitura.append(dados)
    if contador %2==1:
        #ax.set_position(int(angulo[contador-1]), int(voltagem[contador-1]))
        ax.scatter(angulo,voltagem,color='red')
    plt.pause(.000001)
    contador = contador + 1
    if (contador > eixo_x):
        #leitura.pop(0)
        continue

ser.close()
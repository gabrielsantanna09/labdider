import matplotlib.pyplot as plt
import numpy as np
import time
import serial  # importacao do modulo serial
import random

def grafico_dinamico():
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

def main():
    #fig, ax = plt.subplots()
    #fig2, ax2 = plt.subplots()
    #fig.set_visible(False)
    #fig.set_facecolor('red')
    #fig2.set_facecolor('blue')
    #ax.plot(2,3)
    #ax2.plot(4,5)
    #ax.set_autoscale_on(True)
    #plt.ion()
    #plt.show()
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.widgets import Button

    dataX = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    dataY = np.array([1193, 1225, 1125, 1644, 1255, 13676, 2007, 2008, 12359, 1210])

    ax = plt.subplot(111)

    def on_click(event):
        if event.dblclick:
            ax.plot((event.xdata, event.xdata), (mean - standardDeviation, mean + standardDeviation), 'r-')
            plt.show()

    def _yes(event):
        print("yolo")

    mean = np.mean(dataY)
    standardDeviation = np.std(dataY)

    ax.plot(dataX, dataY, linewidth=0.5)
    plt.connect('button_press_event', on_click)

    axcut = plt.axes([0.9, 0.0, 0.1, 0.075])
    bcut = Button(axcut, 'YES', color='red', hovercolor='green')
    bcut.on_clicked(_yes)

    plt.show()
main()
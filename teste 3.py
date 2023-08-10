from tkinter import *
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from matplotlib import animation
from reportlab.lib.pagesizes import A4
from datetime import datetime
import time
import serial



def gerarpdf():
    j = 0
    t = 0
    k = 780
    k2 = 480
    j2 = 0
    t2=0
    pdf = canvas.Canvas("PDF Dados 2.pdf", pagesize=A4)
    pdf.drawString(0,800, "Ângulos Obtidos(°)")
    pdf.line(0,795, 580 , 795)
    for i in angulo_nova:
        t = t+1
        pdf.drawString(j ,k,f"{t}°-({i}°)")
        j = j + 90
        if j >= 520:
            j= 0
            k = k-35
    pdf.drawString(0,500, "Voltagens Obtidas(Volts)")
    pdf.line(0,495, 580 , 495)
    for i in voltagem_novo:
        t2 = t2+1
        pdf.drawString(j2 ,k2,f"{t2}°-({i} V)")
        j2 = j2 + 73
        if j2 >= 580:
            j2= 0
            k2 = k2-40
    pdf.save()
    


def grafico_dinamico():
    plt.figure(figsize=(25,25))
    plt.plot(angulo_nova,voltagem_novo)
    plt.title('Gráfico Labdider')
    plt.xlabel('Ângulo(°)')
    plt.ylabel('Volts(V)')
    plt.rcParams['xtick.labelsize'] = 6
    plt.rcParams['ytick.labelsize'] = 6
    plt.show()
    

arduinoData = serial.Serial('com6', 9600)
j = 2
angulo = []
angulo_nova = []
voltagem = []
voltagem_novo = [] 
for dado in arduinoData:
    if j%2 == 0:
        angulo.append(dado)
    else:
        voltagem.append(dado)
        j = j+1
for temp in angulo:
    angulo_nova.append(temp.replace('\n',''))
for temp in voltagem:
    voltagem_novo.append(temp.replace('\n',''))
janela = Tk()
janela.geometry("700x400")
janela.title('LABDIDER')
texto = Label(janela,text ='Seja Bem-vindo ao Software Labdider', font = "Times 30")
texto.grid(column =0, row = 0,padx=20 , pady=0)
botao = Button(janela, text = 'Gerar Gráfico' , font = 'Arial 15', command = grafico_dinamico)
botao.grid(column = 0, row = 10,padx=20 , pady=0)
botao = Button(janela, text = 'Gerar PDF ' , font = 'Arial 15', command = gerarpdf)
botao.grid(column = 0, row = 11,padx=20 , pady=0)
#botao = Button(janela, text = 'Limpar Dados' , font = 'Arial 15', command = limpar_dados)
#botao.grid(column = 0, row = 12,padx=20 , pady=0)
#botao = Button(janela, text = 'Pausar dados' , font = 'Arial 15', command = pausar_dados)
#botao.grid(column = 0, row = 12,padx=20 , pady=0)
janela.mainloop()

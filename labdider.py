from tkinter import *
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import pandas as pd
import aspose.pdf as pdf
import PyPDF2
from matplotlib import animation
from matplotlib.animation import FuncAnimation
import numpy as np
import time
import serial
fig, ax = plt.subplots()
def salvar_txt():
    with open('C:/Users/ccifusp/Desktop/Teste da galera/dadosdolab.txt', 'w') as arquivo:  #vai salvar no arquivo txt  
            j = 0
            w = 0
            dados = mostrardados()
            for ang,volt in zip(dados[0], dados[1]): #Ler os angulos e voltagens para salvar no arquivo
                arquivo.write(f'{ang}\n')#Linha par com angulo e linha impar com voltagem
                arquivo.write(f'{volt}\n')
def mostrardados():
    ser = serial.Serial('COM5', 9600)#conecta
    time.sleep(2)
    data =[]                       
    for i in range(5): 
        b = ser.readline()         
        string_n = b.decode()   
        string = string_n.rstrip() 
        flt = float(string) 
        data.append(flt)  
    ser.close()
    j = 2
    angulo_nova = []
    voltagem_novo = [] 
    for dado in data:
        j = j+1 
        if j%2 == 0:
            voltagem_novo.append(dado)
        else:
            angulo_nova.append(dado)
    while TRUE:
        j = 0 
        f = 0
        print('\n')
        print(15*'-------------')
        print('Os valores dos ângulos são ')
        for i in angulo_nova:
            print(f'(\033[31m{j}\033[m - \033[34m{i}\033[m°)', end =' ')
            j = j+1
        print('\n')
        print(15*'-------------')
        print('Os valores das voltagens obtidas são ')
        for k in voltagem_novo:
            print(f' (\033[31m{f}\033[m - \033[34m{k}\033[mV)', end = ' ')
            f = f+1
        print('\n')
        print(15*'-------------')    
        correto = str(input('Todos os dados estão corretos? [S/N]')) 
        if correto == 'N':
            dadoerrado = int(input('Digite qual dado está errado e ele será excluído : ')) 
            del angulo_nova[dadoerrado]
            del voltagem_novo[dadoerrado]
        if correto =='S':
            break
        
    return angulo_nova, voltagem_novo  
def gerarpdf():
    j= 0
    #Fazendo um PDF para a imagem
    pdf2 = canvas.Canvas("C:/Users/ccifusp/Desktop/Teste da galera/dadosLAB.pdf", pagesize=A4)
    dados = mostrardados()
    pdf2.drawImage('C:/Users/ccifusp/Desktop/Teste da galera/grafico.png', 0 ,150, width=600, height=1000)
    pdf2.save()
    # Instantiate a new PDF document
    pdfFile = pdf.Document()
    # Create a page in the PDF file
    newPage = pdfFile.pages.add()
    # Create a table
    table = pdf.Table()
    # Set border width 
    table.default_cell_border =  pdf.BorderInfo(pdf.BorderSide.ALL, 1.0, pdf.Color.black)
    row = table.rows.add()
    row.cells.add('Num.dado')
    row.cells.add('ANGULO(°)')
    row.cells.add('VOLTAGEM(V)')
    for a,v in zip(dados[0],dados[1]) :
        j = j+1
        row2 = table.rows.add()
    # Add table cells
        row2.cells.add(f"{j}")
        row2.cells.add(f"{a}")
        row2.cells.add( f"{v}")
    # Add table to the target page
    newPage.paragraphs.add(table)
    # Save the PDF on the disk
    pdfFile.save("C:/Users/ccifusp/Desktop/Teste da galera/dadosLAB2.pdf")
    merger = PyPDF2.PdfMerger()
    merger.append('C:/Users/ccifusp/Desktop/Teste da galera/dadosLAB2.pdf')
    merger.append('C:/Users/ccifusp/Desktop/Teste da galera/dadosLAB.pdf')
    merger.write('C:/Users/ccifusp/Desktop/Teste da galera/dadosLABFINAL.pdf')
    print("Table in PDF created successfully")
  
def grafico_dinamico():
    ani = animation.FuncAnimation(fig, animar, interval = 1000)
    plt.show()
def animar(i):
    #Pegando os dados de um arquivo txt
    ser = serial.Serial('COM5', 9600)#conecta
    ang_test=[]
    volt_test=[]                       
    for i in range(10): 
        i = i+1
        b = ser.readline()         
        string_n = b.decode()   
        string = string_n.rstrip() 
        flt = float(string)        
        if i%2 ==0:
            volt_test.append(flt)
            print(volt_test)
        else:
            ang_test.append(flt)
            print(ang_test)
        if len(ang_test)== len(volt_test):
            ax.clear()
            ax.scatter(ang_test, volt_test)
            ani = animation.FuncAnimation(fig, animar, interval = 1000)
    
    ser.close()
    
    
            
janela = Tk()
janela.geometry("700x400")
janela.title('LABDIDER')
texto = Label(janela,text ='Seja Bem-vindo ao Software Labdider', font = "Times 30")
texto.grid(column =0, row = 0,padx=20 , pady=0)
botao = Button(janela, text = 'Gerar Gráfico' , font = 'Arial 15', command = grafico_dinamico)
botao.grid(column = 0, row = 10,padx=20 , pady=0)
botao = Button(janela, text = 'Gerar PDF ' , font = 'Arial 15', command = gerarpdf)
botao.grid(column = 0, row = 11,padx=20 , pady=0)
botao = Button(janela, text = 'Salvar dados' , font = 'Arial 15', command = salvar_txt)
botao.grid(column = 0, row = 12,padx=20 , pady=0)
botao = Button(janela, text = 'Mostrar dados' , font = 'Arial 15', command = mostrardados)
botao.grid(column = 0, row = 13,padx=20 , pady=0)
janela.mainloop()

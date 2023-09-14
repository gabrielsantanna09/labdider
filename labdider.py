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
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

janela1 = Tk()
fig, ax = plt.subplots()
angulo = []
voltagem = []
data = []
w = True


def salvar_txt():
    with open('C:/Users/ccifusp/Desktop/Teste da galera/dadosdolab.txt', 'w') as arquivo:  #vai salvar no arquivo txt  
            j = 0
            w = 0
            dados = mostrardados()
            for ang,volt in zip(dados[0], dados[1]): #Ler os angulos e voltagens para salvar no arquivo
                arquivo.write(f'{ang}\n')#Linha par com angulo e linha impar com voltagem
                arquivo.write(f'{volt}\n')


def Parar_Experimento(event):
    #aqui queremos abrir uma nova janela
    print("Hellor world")
    global w
    global angulo
    global voltagem
    w = False
    plt.close()

    #Isso aqui é pra deixar o ângulo e a voltagem como arrays de mesmo tamanho
    #se forem de tamanhos diferentes da erro no plot
    if (len(angulo) > len(voltagem)):
        #aqui eu apago o último espaço do array angulo
        angulo.pop(-1)

    fig2, ax2 = plt.subplots()
    print(angulo,voltagem)
    ax2.scatter(angulo,voltagem)
    ax.set_autoscale_on(True)

    #Janela 2 aparece depois de parar o experimento
    #A ideia aqui é botar os botões para salvar o gráfico gerado, salvar arquivo txt, arquivo csv, e reiniciar experimento
    #Ter um botão para cada função dessa, sendo que o botão reiniciar vai simplesmente zerar as variáveis e chamar a janela 1
    janela2 = Tk()
    janela2.geometry("700x400")
    janela2.title('LABDIDER')
    texto = Label(janela2, text='Seja Bem-vindo ao Software Labdider', font="Times 30")
    texto.pack(padx=20, pady=0)
    botao = Button(janela2, text='Iniciar experimento', font='Arial 15', command=iniciar_experimento)
    botao.pack(padx=20, pady=0)
    canvas = FigureCanvasTkAgg(fig2, master=janela2)
    canvas.draw()
    canvas.get_tk_widget().pack()
    janela2.mainloop()


def iniciar_experimento():
    janela1.destroy()

    #o esse import precisa ficar dentro da função porque da conflito com o import do tkinter
    #certamente deve haver um jeito melhor de resolver isso mas por hora fica assim
    from matplotlib.widgets import Button
    global angulo
    global voltagem

    #Varíaveis na função
    leitura = []
    ser = serial.Serial('COM5', 9600)  # abre porta serial COM6
    angulo = []
    voltagem = []
    contador = 0
    dados = []
    i = int(0)
    global w
    w = True

    #iniciando o loop que vai coletar os dados do arduíno
    while w == True:
        print(w)
        while (ser.inWaiting() == 0):
            pass
        b = ser.readline()
        string_n = b.decode()
        string = string_n.rstrip()
        flt = float(string)
        dados.append(flt)
        if contador % 2 == 1:
            voltagem.append(dados[contador])
        else:
            #aqui eu somo 180 quando o ângulo chega no zero
            #isso acontece quando a maquininha começa a girar de volta
            #isso aqui é bom porque deixa o gráfico senoidal sem se sobrepor
            j = dados[contador] + (i * 180)
            angulo.append(j)
            if contador >= 4:
                print(int(angulo[-1]))
                if (int(angulo[-1]) == i * 180):
                    i = i + 1
                    angulo[-1] = i*180


        #Aqui é onde eu monto o gráfico, colocando titulo, nomes dos eixos, etc
        ax.set_autoscale_on(True)
        ax.set_title('título')
        plt.subplots_adjust(bottom=0.2)

        #Botão, de ínicio apenas 1
        #O botão parar vai nos mandar para uma função em que abriremos uma janela e perguntaremos se o usuário gostaria de salvar os dados ou refazer os experimento
        ax_parar = plt.axes([0.58,0.05,0.15,0.07])
        botao_parar = Button(ax_parar,'Parar')
        botao_parar.on_clicked(Parar_Experimento)

        #daqui pra baixo nós estamos fazendo o gráfico atualizar
        leitura.append(dados)

        #isso aqui faz o gráfico que está na janela atualizar
        #precisamos descobrir um jeito de ter só um gráfico em tela
        if contador % 2 == 1:
            ax.clear()
            ax.scatter(angulo, voltagem, color='red')
            #aqui nós ainda temos que somar os ângulos depois de 180
            #Temos também que dar clear nos subplot ax porque conforme os dados forem ficando maiores o gráfico vai ficando muito pesado

        #O plt.pause é oq faz o gráfico atualizar na mesma figura
        plt.pause(0.1)
        contador = contador + 1

        #isso vou manter por enquanto
        print(angulo, voltagem)
    ser.close()


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

    print('Angulos e voltagens: ' + angulo_nova + voltagem_novo)

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





    
    
def abrir_primeira_janela():
    janela1.geometry("700x400")
    janela1.title('LABDIDER')
    texto = Label(janela1,text ='Seja Bem-vindo ao Software Labdider', font = "Times 30")
    texto.pack(padx=20 , pady=0)
    botao = Button(janela1, text = 'Iniciar experimento' , font = 'Arial 15', command = iniciar_experimento)
    botao.pack(padx=20 , pady=0)
    #canvas = FigureCanvasTkAgg(fig, master=janela)
    janela1.mainloop()

abrir_primeira_janela()
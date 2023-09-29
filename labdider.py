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
from tkinter import *
from tkinter import ttk
from datetime import datetime
import os.path
import tkinter.messagebox
from tkinter import messagebox

janela1 = Tk()
janela2 = Tk()
fig, ax = plt.subplots()
angulo = []
voltagem = []
data = []
destr = Tk()
w = True

#Função que salva os dados em arquivo txt e futuramente em arquivo csv, talvez
def salvar_dados():
    global angulo
    global voltagem
    data = datetime.now()
    hoje = str(data.year) + "_" + str(data.month) + "_" + str(data.day)
    hora = str(data.hour) + "." + str(data.minute) + "."+str(data.second)
    caminho = "C:/Users/ccifusp/git/Labdider/dados_salvos/"+hoje
    if os.path.exists(caminho) == False:
        os.makedirs(caminho)
    caminho = caminho +"/"+hora+".txt"
    #abrindo arquivo com esse comando, se não existir ele será criado, se já existir ele será sobreescrito
    with open(caminho, 'w') as arquivo:  #vai salvar no arquivo txt
            arquivo.write('Os dados das linhas ímpares são ângulos e das linhas pares são voltagens:\n')
            i = int(0)
            while i < len(angulo):
                arquivo.write(f'{angulo[i]}\n')  # Linha par com angulo e linha impar com voltagem
                arquivo.write(f'{voltagem[i]}\n')
                i = i +1#Ler os angulos e voltagens para salvar no arquivo

            arquivo.write('Desse jeito talvez seja melhor de salvar: \n')
            arquivo.write('\nÂngulos:\n')
            i = int(0)
            while i < len(angulo):
                arquivo.write(f'{angulo[i]}\n')
                i = i + 1
            i = int(0)
            arquivo.write('\nVoltagens:\n ')
            while i < len(angulo):
                arquivo.write(f'{voltagem[i]}\n')
                i = i + 1  # Ler os angulos e voltagens para salvar no arquivo

    mensagem = "Seus dados foram salvos em: \n" + caminho
    tkinter.messagebox.showinfo("Dados salvos com sucesso", mensagem)

#Função que salva o gráfico gerado com todos os dados
def salva_grafico():
    data = datetime.now()
    hoje = str(data.year) + "_" + str(data.month) + "_" + str(data.day)
    hora = str(data.hour) + "." + str(data.minute) + "." + str(data.second)
    caminho = "C:/Users/ccifusp/git/Labdider/dados_salvos/" + hoje
    if os.path.exists(caminho) == False:
        os.makedirs(caminho)
    caminho = caminho + "/" + hora + ".png"
    plt.savefig(caminho, format='png')
    mensagem = "Seus gráfico foi salvo em: \n" + caminho
    tkinter.messagebox.showinfo("Gráfico salvo com sucesso", mensagem)

#Função que reiniciará o gráfico
def reiniciar():
    global ser
    global janela1
    global destr


    #O serial é fechado aqui para que não haja problema quando for se reconectar com a porta nas proximas vezes
    ser.close()
    janela1 = Tk()
    destr = Tk()
    abrir_primeira_janela()
    #quando tento reiniciar o experimento dá problema porque da acesso negado na porta COM5
    #Não sei porque isso acontece

#Função que faz aparecer a janela quando o gráfico dinâmico for fechado
def Parar_Experimento():
    #aqui queremos abrir uma nova janela
    print("Hellor world")
    global w
    global angulo
    global voltagem
    global janela2
    global destr

    destr.destroy()
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
    botao = Button(janela2, text='Reiniciar experimento', font='Arial 15', command = reiniciar)
    botao.pack(padx=20, pady=0)
    botao2 = Button(janela2, text='Salvar Dados', font='Arial 15', command = salvar_dados)
    botao2.pack(padx=40, pady=0)
    botao3 = Button(janela2, text='Mostrar Dados', font='Arial 15', command=mostrardados)
    botao3.pack(padx=60, pady=0)
    botao4 = Button(janela2, text='Salvar Gráfico', font='Arial 15', command=salva_grafico)
    botao4.pack(padx=60, pady=0)
    canvas = FigureCanvasTkAgg(fig2, master=janela2)
    canvas.draw()
    canvas.get_tk_widget().pack()
    janela2.protocol("WM_DELETE_WINDOW", pergunta)
    janela2.mainloop()

def pergunta():
    resposta = messagebox.askyesno("Cuidado", "Se você sair os dados do experimento atual podem ser perdidos, deseja continuar?")
    if resposta:
        encerrar()
    else:
        return

#É a função que vai fazer o gráfico dinâmico aparecer
#precisamos dar um jeito no botão que as vezes simplesmente para de funcionar
#Uma possível solução é criar uma nova janela junto com o gráfico e nessa janela botar outro botão para fazer a mesma coisa do botão do gráfico
#As vezes, ao iniciar o experimento obtemos um erro (UTF-8 algo assim, precisamos ver como resolver isso, provavelmente colocar uma validação no erro
#Outra coisa que queremos aqui é fazer os janelas (gráfico e botão parar apareçam em locais melhores da tela
#A janela com o botão fica atrás do gráfico e talvez o usuário nem veja
#utf-8' codec can't decode byte 0xfc in position 0: invalid start byte
def iniciar_experimento():

    janela1.destroy()

    #janelinha para consertar botão
    global destr
    destr = Tk()

    destr.geometry("400x100+800+200")
    destr.title('LABDIDER')
    texto = Label(destr, text='Clique no botão para encerrar experimento', font="Times 15")

    texto.pack(padx=10)
    bot = Button(destr, text='Parar Experimento', font='Arial 15', command=Parar_Experimento)
    bot.pack(padx=20, pady=0)


    #o esse import precisa ficar dentro da função porque da conflito com o import do tkinter
    #certamente deve haver um jeito melhor de resolver isso mas por hora fica assim
    global angulo
    global voltagem
    global fig, ax
    global ser
    #from matplotlib.widgets import Button
    #Isso faz com que fechemos todas as figuras ativas, é necessário para a função reiniciar
    plt.close('all')

    #preciso criar o objeto novamente
    fig, ax = plt.subplots()

    #Preciso zerar todas as variáveis, inclusive as globais
    leitura = []
    ser = serial.Serial('COM5', 9600)  # abre porta serial COM6
    angulo = []
    voltagem = []
    contador = 0
    dados = []
    i = int(0)
    global w
    w = True

    # Botão, de ínicio apenas 1
    # O botão parar vai nos mandar para uma função em que abriremos uma janela e perguntaremos se o usuário gostaria de salvar os dados ou refazer os experimento
    #ax_parar = plt.axes([0.58, 0.05, 0.15, 0.07])
    #botao_parar = Button(ax_parar, 'Parar')
    #botao_parar.on_clicked(Parar_Experimento)
    ax.set_title('título')

    #iniciando o loop que vai coletar os dados do arduíno
    while w == True:
        while (ser.inWaiting() == 0):
            pass
        b = ser.readline()
        j = False
        while j == False:
            try:
                string_n = b.decode()
                j = True
            except UnicodeDecodeError as e:
                messagebox.showinfo("Erro", f"Ocorreu o erro {e}, por favor tente novamente iniciar o experimento")
                return

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
                if (int(angulo[-1]) == i * 180):
                    i = i + 1
                    angulo[-1] = i*180


        #Aqui é onde eu monto o gráfico, colocando titulo, nomes dos eixos, etc
        ax.set_autoscale_on(True)

        plt.subplots_adjust(bottom=0.2)

        #Botão, de ínicio apenas 1
        #O botão parar vai nos mandar para uma função em que abriremos uma janela e perguntaremos se o usuário gostaria de salvar os dados ou refazer os experimento
        #ax_parar = plt.axes([0.58,0.05,0.15,0.07])
        #botao_parar = Button(ax_parar,'Parar')
        #botao_parar.on_clicked(Parar_Experimento)

        #daqui pra baixo nós estamos fazendo o gráfico atualizar
        leitura.append(dados)

        #isso aqui faz o gráfico que está na janela atualizar
        #precisamos descobrir um jeito de ter só um gráfico em tela
        if contador % 2 == 1:
            ax.scatter(angulo, voltagem, color='red')
            #aqui nós ainda temos que somar os ângulos depois de 180
            #Temos também que dar clear nos subplot ax porque conforme os dados forem ficando maiores o gráfico vai ficando muito pesado

        #O plt.pause é oq faz o gráfico atualizar na mesma figura
        plt.pause(0.0001)
        contador = contador + 1

#Função que mostra a tabelinha com os dados depois de parar o experimento
def mostrardados():

    global angulo
    global voltagem
    ws = Tk()
    ws.title('PythonGuides')
    ws.geometry('200x300')
    ws['bg'] = '#AC99F2'

    game_frame = Frame(ws)
    game_frame.pack()

    my_game = ttk.Treeview(game_frame)

    my_game['columns'] = ('Ângulo','Voltagem')
    my_game.column("#0", width=0, stretch=NO)
    my_game.column("Ângulo", anchor=CENTER, width=80)
    my_game.column("Voltagem", anchor=CENTER, width=80)

    my_game.column("#0", width=0, stretch=NO)
    my_game.column("Ângulo", anchor=CENTER, width=80)
    my_game.column("Voltagem", anchor=CENTER, width=80)

    my_game.heading("#0", text="", anchor=CENTER)
    my_game.heading("Ângulo", text="Ângulo", anchor=CENTER)
    my_game.heading("Voltagem", text="Voltagem", anchor=CENTER)
    i = int(0)
    while i <len(angulo):
        my_game.insert(parent='', index='end', iid=i, text='',
                   values=(angulo[i],voltagem[i]))
        i = i + 1

    my_game.pack()
    ws.mainloop()

def encerrar():
    exit()

#Ainda será trabalhada
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

#Função que abre a primeira janela e basicamente é o início do experimento
#Aqui as variáveis precisam ser zeradas porque o experimento pode ser refeito gerando novos dados
def abrir_primeira_janela():
    global janela2
    global janela1
    global destr

    janela2.destroy()
    if destr.state() == 'normal':
        destr.destroy()
    janela1.geometry("700x400")
    janela1.title('LABDIDER')
    texto = Label(janela1,text ='Seja Bem-vindo ao Software Labdider', font = "Times 30")
    texto.pack(padx=20 , pady=0)
    botao = Button(janela1, text = 'Iniciar experimento' , font = 'Arial 15', command = iniciar_experimento)
    botao.pack(padx=20 , pady=0)
    janela1.protocol("WM_DELETE_WINDOW", encerrar)
    janela1.mainloop()

abrir_primeira_janela()
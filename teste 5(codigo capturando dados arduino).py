from tkinter import *
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import serial
import time
import sqlite3
import pandas as pd
import aspose.pdf as pdf
import PyPDF2


#ser = serial.Serial('COM6', 9600)
#time.sleep(2)
#data =[]                       # empty list to store the data
#for i in range(50):
#    b = ser.readline()         # read a byte string
#    string_n = b.decode()  # decode byte string into Unicode  
#    string = string_n.rstrip() # remove \n and \r
#    flt = float(string)        # convert string to float
#    data.append(flt)           # add to the end of data list
#    time.sleep(0.1)            # wait (sleep) 0.1 seconds

#ser.close()


with open('C:/Users/ccifusp/Desktop/Teste da galera/h.txt' , 'r') as arquivo:
    j = 2
    angulo = []
    angulo_nova = []
    voltagem = []
    voltagem_novo = [] 
    for dado in arquivo:
        if j%2 == 0:
            angulo.append(dado)
        else:
            voltagem.append(dado)
        j = j+1
    for a in angulo:
        angulo_nova.append(a.replace('\n',''))
    for v in voltagem:
        voltagem_novo.append(v.replace('\n',''))

    
    tabelinha = pd.DataFrame({"Angulos" : angulo_nova, "Voltagem": voltagem_novo})
    """banco = sqlite3.connect('testebanco.db')
    cursor = banco.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS dados (Angulos float, Voltagem float)')
    tabelinha.to_sql(name = 'dados', con = banco, if_exists='append', index = False)
    back = pd.read_sql('select * from dados', banco)
    print(back)
    """

def salvar_txt():
    with open('C:/Users/ccifusp/Desktop/Teste da galera/dadosdolab.txt', 'w') as arquivo:    
            j = 0
            w = 0
            dados = mostrardados()
            arquivo.write('Os ângulos são: \n')
            for ang in dados[0]:
                j = j+1
                arquivo.write(f' {j} - {ang}° \n')
            arquivo.write('As voltagens são: \n')
            for volt in dados[1]:
                w = w+1
                arquivo.write(f' {w} - {volt}V \n')
            
            


def limpar_dados():
    angulo_nova.clear()
    voltagem_novo.clear()


def mostrardados():
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
    for a,v in zip(angulo_nova,voltagem_novo) :
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
    print("Table in PDF created successfully")
    merger = PyPDF2.PdfMerger()
    merger.append('C:/Users/ccifusp/Desktop/Teste da galera/dadosLAB2.pdf')
    merger.append('C:/Users/ccifusp/Desktop/Teste da galera/dadosLAB.pdf')
    merger.write('C:/Users/ccifusp/Desktop/Teste da galera/dadosLABFINAL.pdf')
    
    
def grafico_dinamico():
    dados = mostrardados()
    ang2 = dados[0]
    volt2 = dados[1]
    plt.figure(figsize=(25,25))
    plt.plot(ang2,volt2)
    plt.title('Gráfico Labdider')
    plt.xlabel('Volts(V)')
    plt.ylabel('ângulo(°)')
    plt.rcParams['xtick.labelsize'] = 35
    plt.rcParams['ytick.labelsize'] = 35
    plt.savefig('C:/Users/ccifusp/Desktop/Teste da galera/grafico.png')
    plt.show()
            
            
janela = Tk()
janela.geometry("700x400")
janela.title('LABDIDER')
texto = Label(janela,text ='Seja Bem-vindo ao Software Labdider', font = "Times 30")
texto.grid(column =0, row = 0,padx=20 , pady=0)
botao = Button(janela, text = 'Gerar Gráfico' , font = 'Arial 15', command = grafico_dinamico)
botao.grid(column = 0, row = 10,padx=20 , pady=0)
botao = Button(janela, text = 'Gerar PDF ' , font = 'Arial 15', command = gerarpdf)
botao.grid(column = 0, row = 11,padx=20 , pady=0)
botao = Button(janela, text = 'Salvar dados  ' , font = 'Arial 15', command = salvar_txt)
botao.grid(column = 0, row = 12,padx=20 , pady=0)
botao = Button(janela, text = 'Limpar Dados' , font = 'Arial 15', command = limpar_dados)
botao.grid(column = 0, row = 14,padx=20 , pady=0)
#botao = Button(janela, text = 'Excluir PDF' , font = 'Arial 15', command = limparpdf)
#botao.grid(column = 0, row = 13,padx=20 , pady=0)
janela.mainloop()




#for i in range(len(ang2)):
 #       plt.figure(figsize=(25,25))
#        plt.plot(ang2,volt2)
 #       plt.title('Gráfico Labdider')
 #       plt.xlabel('Ângulo(°)')
 #       plt.ylabel('Volts(V)')
  #      plt.rcParams['xtick.labelsize'] = 6
  #      plt.rcParams['ytick.labelsize'] = 6
  #      plt.pause(3)
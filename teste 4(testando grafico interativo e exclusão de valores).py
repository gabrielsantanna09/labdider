from tkinter import *
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from matplotlib import animation
from reportlab.lib.pagesizes import A4
import os

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
        for temp in angulo:
            angulo_nova.append(temp.replace('\n',''))
        for temp in voltagem:
            voltagem_novo.append(temp.replace('\n',''))
            


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


#def  limparpdf():
#    path = "C:/Users/ccifusp/Desktop/Teste da galera"
#    dir = os.listdir(path)
#    for file in dir:
#        if file == "dadosLAB":
#            os.remove(file)
    
    
def gerarpdf():
    j = 0
    t = 0
    k = 780
    k2 = 480
    j2 = 0
    t2 = 0
    pdf = canvas.Canvas("C:/Users/ccifusp/Desktop/Teste da galera/dadosLAB.pdf", pagesize=A4)
    pdf.drawString(0,800, "Voltagens Obtidas(V)")
    pdf.line(0,795, 580 , 795)
    dados = mostrardados()
    for i in dados[0]:
        t = t+1
        pdf.drawString(j ,k,f"{t}°-({i}V)")
        j = j + 90
        if j >= 520:
            j= 0
            k = k-35
    pdf.drawString(0,500, "Ângulos Obtidos (°)")
    pdf.line(0,495, 580 , 495)
    for i in dados[1]:
        t2 = t2+1
        pdf.drawString(j2 ,k2,f"{t2}°-({i} °)")
        j2 = j2 + 73
        if j2 >= 580:
            j2= 0
            k2 = k2-40
    pdf.save()
    


def grafico_dinamico():
    dados = mostrardados()
    ang2 = dados[0]
    volt2 = dados[1]
    plt.figure(figsize=(25,25))
    plt.plot(ang2,volt2)
    plt.title('Gráfico Labdider')
    plt.xlabel('Volts(V)')
    plt.ylabel('ângulo(°)')
    plt.rcParams['xtick.labelsize'] = 6
    plt.rcParams['ytick.labelsize'] = 6
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
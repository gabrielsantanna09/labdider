from tkinter import *
import requests
janela = Tk()
janela.title('Experimento IFUSP')
texto = Label(janela,text ='Seja Bem-vindo ao Software Labdider')
texto.grid(column =0, row = 0)
texto2 = Label(janela, text = 'Clique aqui para gerar o gráfico')
texto2.grid(column= 0 , row = 1)
botao = Button(janela, text = 'Gerar Gráfico' , command = plotargraficos)


janela.mainloop()
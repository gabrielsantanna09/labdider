import tkinter as tk
from tkinter import PhotoImage

def acao_do_botao():
    # Adicione a ação que você deseja que o botão execute aqui
    print("Botão pressionado!")

# Crie a janela principal
janela = tk.Tk()
janela.title("Botão com Imagem")

# Carregue a imagem (substitua "imagem.png" pelo caminho da sua imagem)
imagem = PhotoImage(file="C:/Users/ccifusp/Downloads/botão2.png")

# Crie uma etiqueta (Label) para exibir a imagem
etiqueta_imagem = tk.Label(janela, image=imagem)
#etiqueta_imagem.pack()

# Crie um botão personalizado usando a etiqueta de imagem
botao = tk.Button(janela, image=imagem, command=acao_do_botao, borderwidth=10)
botao.pack()

# Inicie o loop principal da janela
janela.mainloop()

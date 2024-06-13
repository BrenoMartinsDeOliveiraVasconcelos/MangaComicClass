import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import os
import json
from subprocess import run
from PIL import Image


def open_image():
    """
  Abre uma caixa de diálogo para selecionar uma imagem e a converte para jpg.
  """
    image_path = filedialog.askopenfilename(title="Selecione uma imagem")
    if image_path:
        convert_to_jpg(image_path)
        display_image()
        analyze_image()


def convert_to_jpg(image_path):
    """
  Converte a imagem para jpg e salva como input.jpg.
  """
    im = Image.open(image_path)
    im32 = im.resize((128, 128))
    im32 = im32.convert('RGB')
    im32.save('input.jpg')

    # Formatar a imagem pra ficar num tamanho certo pra apresentação
    h = (im.size[0]/im.size[1]) * 400

    im = im.resize((int(h), 400))
    im.save("tkprint.png")


def display_image():
    """
  Exibe a imagem na tela.
  """
    image = tk.PhotoImage(file="tkprint.png")
    image_label.configure(image=image)
    image_label.image = image


def analyze_image():
    """
  Roda o script main.py e exibe as probabilidades em uma caixa de mensagem.
  """
    if not os.path.exists("input.jpg"):
        tk.messagebox.showerror("Erro", "Nenhuma imagem selecionada.")
        return
    run(["py", "main.py"])
    if not os.path.exists("output.json"):
        tk.messagebox.showerror("Erro", "O script não gerou o arquivo output.json.")
        return
    display_prob()


def display_prob():
    """
  Exibe as probabilidades do arquivo output.json em uma caixa de mensagem.
  """
    with open("output.json") as f:
        data = json.load(f)
    textstr = ""

    for k, v in data.items():
        if k != "prediction":
            v = "{:.4f}".format(v)
            textstr += f"{k} = {v}\n"
        else:
            textstr = textstr.strip()
    classlabel.configure(text=textstr, font=("Calibri", 14))
    conclusionlb.configure(text=f"{data['prediction']}", font=("Calibri", 20, "bold"))

    messagebox.askokcancel(title="Sucesso", message="Imagem analizada com sucesso;")


# Interface gráfica
root = ctk.CTk()
root.title("MC Tool")
root.resizable(height=False, width=False)

# Label do meio
classlabel = ctk.CTkLabel(root, text="Esperando input...", justify=ctk.CENTER)
classlabel.pack(pady=0)

# Label do meio
conclusionlb = ctk.CTkLabel(root, text="Sem input", justify=ctk.CENTER)
conclusionlb.pack(pady=0)

# Rótulo para exibir a imagem
image_label = ctk.CTkLabel(root, text="", justify=ctk.LEFT, image=tk.PhotoImage(file="placeholder.png"))
image_label.pack(pady=5, padx=5)

# Botão para abrir imagem
openimgBt = ctk.CTkButton(root, text="Enviar imagem", command=open_image)
openimgBt.pack(pady=5)

# Executa a interface gráfica
root.mainloop()

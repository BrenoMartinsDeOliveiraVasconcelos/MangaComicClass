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


def convert_to_jpg(image_path):
    """
  Converte a imagem para jpg e salva como input.jpg.
  """
    im = Image.open(image_path)
    im32 = im.resize((128, 128))
    im32 = im32.convert('RGB')
    im32.save('input.jpg')

    im = im.resize((int(im.size[0] / 2), int(im.size[1] / 2)))
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
    classlabel.configure(text=textstr, font=("Arial", 10))
    conclusionlb.configure(text=f"{data['prediction']}", font=("Arial", 20, "bold"))


# Interface gráfica
root = ctk.CTk()
root.title("Análise de Imagem")

# Botão para abrir imagem
openimgBt = ctk.CTkButton(root, text="Abrir Imagem", command=open_image)
openimgBt.grid(row=0, column=0, pady=5, padx=5, rowspan=1, sticky="w")

# Rótulo para exibir a imagem
image_label = ctk.CTkLabel(root, text="", justify=ctk.LEFT, image=tk.PhotoImage(file="placeholder.png"))
image_label.grid(row=2, column=0, columnspan=2, pady=5, padx=5)

# Botão para analisar imagem
analyzeBt = ctk.CTkButton(root, text="Analisar Imagem", command=analyze_image)
analyzeBt.grid(row=1, column=0, pady=5, padx=5, rowspan=1, sticky="w")

# Label do meio
classlabel = ctk.CTkLabel(root, text="PLACEHOLDER", justify=ctk.LEFT)
classlabel.grid(row=0, column=1, pady=5, padx=1, sticky="w", rowspan=1)

# Label do meio
conclusionlb = ctk.CTkLabel(root, text="PLACEHOLDER", justify=ctk.LEFT)
conclusionlb.grid(row=1, column=1, pady=5, padx=1, sticky="w", rowspan=1)

# Executa a interface gráfica
root.mainloop()

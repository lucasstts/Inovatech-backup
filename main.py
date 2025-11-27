import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import json
import os
from traducao import abrir_camera_traducao, abrir_camera_salvar_gesto, cadastrar_frases

# AVISO: estou utilizando python 3.11 pois o mediapipe não funciona em versões mais recentes.

# ------------------------------
# Configurações e constantes
# ------------------------------
BAU_PATH = "bau_de_valores.json"

BG_COLOR = "#cfe9ff"          # azul claro
FRAME_COLOR = "#e6f2ff"       # azul bem suave
BTN_COLOR = "#b3d7ff"         # azul médio
BTN_HOVER = "#99ccff"         # azul hover
BTN_TEXT = "#0a1a3a"          # azul escuro para texto
TITLE_FONT = ("Segoe UI", 16, "bold")
FONT = ("Segoe UI", 12)

# ------------------------------
# Funções de persistência
# ------------------------------
def carregar_usuarios():
    if os.path.exists(BAU_PATH):
        try:
            with open(BAU_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def salvar_usuarios(usuarios):
    with open(BAU_PATH, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, ensure_ascii=False)

# ------------------------------
# Estilo ttk
# ------------------------------
def aplicar_estilo_ttk():
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "RoundedButton.TButton",
        background=BTN_COLOR,
        foreground=BTN_TEXT,
        padding=8,
        borderwidth=0,
        focusthickness=0,
        anchor="center",
        relief="flat",
        font=FONT
    )
    style.map(
        "RoundedButton.TButton",
        background=[("active", BTN_HOVER)],
        relief=[("pressed", "sunken")]
    )

# ------------------------------
# Funções das telas
# ------------------------------
def show_main_menu():
    """Mostra o menu principal com opções."""
    limpar_janela()
    app.title("Menu Principal")

    container = tk.Frame(app, bg=BG_COLOR)
    container.pack(fill="both", expand=True, padx=40, pady=40)

    tk.Label(container, text="Bem-vindo ao Menu Principal!", font=TITLE_FONT, bg=BG_COLOR).pack(pady=10)

    # Botões principais (ttk para estilo consistente)
    ttk.Button(container, text="Alfabeto", style="RoundedButton.TButton", command=mostrar_alfabeto)\
        .pack(pady=8, ipadx=10, ipady=6, fill="x")
    ttk.Button(container, text="Frase Simples", style="RoundedButton.TButton", command=mostrar_frases_simples)\
        .pack(pady=8, ipadx=10, ipady=6, fill="x")
    ttk.Button(container, text="Tradução", style="RoundedButton.TButton", command=abrir_camera_traducao)\
        .pack(pady=8, ipadx=10, ipady=6, fill="x")
    ttk.Button(container, text="Salvar Gestos", style="RoundedButton.TButton", command=abrir_camera_salvar_gesto)\
        .pack(pady=8, ipadx=10, ipady=6, fill="x")
    ttk.Button(container, text="Salvar Frases", style="RoundedButton.TButton", command=cadastrar_frases)\
        .pack(pady=8, ipadx=10, ipady=6, fill="x")


def mostrar_alfabeto():
    """Tela do alfabeto: botões A-Z que mostram imagens 150x150."""
    limpar_janela()
    app.title("Alfabeto em Libras")

    container = tk.Frame(app, bg=BG_COLOR)
    container.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(container, text="Clique em uma letra para ver em Libras:", font=TITLE_FONT, bg=BG_COLOR).pack(pady=8)

    frame_letras = tk.Frame(container, bg=BG_COLOR)
    frame_letras.pack()

    frame_imagem = tk.Frame(container, bg=BG_COLOR)
    frame_imagem.pack(pady=18)
    imagem_label = tk.Label(frame_imagem, bg=BG_COLOR)
    imagem_label.pack()

    def mostrar_imagem(letra):
        caminho = os.path.join("imagens_libras", f"{letra}.png")
        if os.path.exists(caminho):
            imagem = Image.open(caminho)
            imagem = imagem.resize((150, 150))
            imagem_tk = ImageTk.PhotoImage(imagem)
            imagem_label.config(image=imagem_tk, text='')
            imagem_label.image = imagem_tk
        else:
            imagem_label.config(image='', text="Imagem não encontrada", font=FONT)

    letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # 6 colunas (igual seu layout original), espaçamento uniforme
    cols = 6
    for i, letra in enumerate(letras):
        btn = tk.Button(
            frame_letras, text=letra, width=4, height=2, font=FONT,
            bg=BTN_COLOR, fg=BTN_TEXT, activebackground=BTN_HOVER,
            relief="flat", bd=0
        )
        btn.config(command=lambda l=letra: mostrar_imagem(l))
        btn.grid(row=i // cols, column=i % cols, padx=6, pady=6, ipadx=4, ipady=4)

    ttk.Button(container, text="Voltar ao Menu", style="RoundedButton.TButton", command=show_main_menu)\
        .pack(pady=12)


def mostrar_frases_simples():
    """
    Tela de frases simples.
    - Botões em grade (uniforme) deixando espaço abaixo para a imagem.
    - Ao clicar no botão: exibe a imagem (250x250).
    - Se clicar no mesmo botão novamente, a imagem some (toggle).
    - Se clicar na imagem, a mesma desaparece.
    """
    limpar_janela()
    app.title("Frases Simples em Libras")

    container = tk.Frame(app, bg=BG_COLOR)
    container.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(container, text="Selecione uma frase para ver em Libras:", font=TITLE_FONT, bg=BG_COLOR).pack(pady=8)

    # Frame para os botões das frases (grade)
    frame_frases = tk.Frame(container, bg=BG_COLOR)
    frame_frases.pack(pady=6, fill="x")

    # Frame para exibir imagem (ficará abaixo da grade de botões)
    frame_imagem = tk.Frame(container, bg=BG_COLOR)
    frame_imagem.pack(pady=12)
    imagem_label = tk.Label(frame_imagem, bg=BG_COLOR)
    imagem_label.pack()

    # Lista de frases e seus arquivos
    frases = [
        ("Oi, tudo bem?", "oi_tudo_bem.png"),
        ("Eu sou surdo.", "eu_sou_surdo.png"),
        ("Meu nome é.", "meu_nome_e.png"),
        ("Qual seu nome?", "qual_seu_nome.png"),
        ("Hoje estou feliz.", "hoje_eu_feliz.png"),
        ("Prazer em conhecer você.", "prazer_em_conhecer_voce.png"),
        ("Bom dia.", "bom_dia.png"),
        ("Boa tarde.", "boa_tarde.png"),
        ("Boa noite.", "boa_noite.png"),
        ("Obrigado!", "obrigado.png")
    ]

    ultima_imagem = {"arquivo": None}  # guarda arquivo atualmente mostrado (para toggle)

    def mostrar_ou_ocultar(nome_arquivo):
        # Se já exibida a mesma imagem -> esconder
        if ultima_imagem["arquivo"] == nome_arquivo:
            imagem_label.config(image='', text='')
            imagem_label.image = None
            ultima_imagem["arquivo"] = None
            return

        caminho = os.path.join("frases_libras", nome_arquivo)
        if os.path.exists(caminho):
            imagem = Image.open(caminho)
            imagem = imagem.resize((250, 250))
            imagem_tk = ImageTk.PhotoImage(imagem)
            imagem_label.config(image=imagem_tk, text='')
            imagem_label.image = imagem_tk
            ultima_imagem["arquivo"] = nome_arquivo
        else:
            imagem_label.config(image='', text="Imagem não encontrada", font=FONT, fg="red")
            imagem_label.image = None
            ultima_imagem["arquivo"] = None

    # permite clicar na própria imagem para ocultar
    def clique_na_imagem(event=None):
        if ultima_imagem["arquivo"] is not None:
            imagem_label.config(image='', text='')
            imagem_label.image = None
            ultima_imagem["arquivo"] = None

    imagem_label.bind("<Button-1>", clique_na_imagem)

    # Criar botões em grade
    cols = 4  # 4 botões por linha -> uniforme
    for index, (frase, arquivo) in enumerate(frases):
        row = index // cols
        col = index % cols
        btn = tk.Button(
            frame_frases,
            text=frase,
            width=24,
            height=2,
            font=FONT,
            bg=FRAME_COLOR,
            fg=BTN_TEXT,
            activebackground=BTN_HOVER,
            relief="flat",
            bd=0,
            command=lambda f=arquivo: mostrar_ou_ocultar(f)
        )
        btn.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

    # Configurar grid para que colunas se expandam igualmente
    for c in range(cols):
        frame_frases.columnconfigure(c, weight=1)

    ttk.Button(container, text="Voltar ao Menu", style="RoundedButton.TButton", command=show_main_menu)\
        .pack(pady=12)

# ------------------------------
# Helpers
# ------------------------------
def limpar_janela():
    """Remove todos widgets da janela principal."""
    for widget in app.winfo_children():
        widget.destroy()

# ------------------------------
# Login / Cadastro
# ------------------------------
def login():
    username = entry_user.get().strip()
    password = entry_pass.get().strip()
    usuarios = carregar_usuarios()
    if username in usuarios and usuarios[username] == password:
        show_main_menu()
    else:
        messagebox.showerror("Login", "Usuário ou senha incorretos.")

def mostrar_cadastro():
    frame_login.pack_forget()
    frame_cadastro.pack(pady=10)

def cadastrar():
    new_user = entry_new_user.get().strip()
    new_pass = entry_new_pass.get().strip()
    usuarios = carregar_usuarios()
    if new_user in usuarios:
        messagebox.showerror("Cadastro", "Usuário já existe.")
    elif not new_user or not new_pass:
        messagebox.showerror("Cadastro", "Preencha todos os campos.")
    else:
        usuarios[new_user] = new_pass
        salvar_usuarios(usuarios)
        messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso!")
        entry_new_user.delete(0, tk.END)
        entry_new_pass.delete(0, tk.END)
        frame_cadastro.pack_forget()
        frame_login.pack(pady=10)

def voltar_login():
    frame_cadastro.pack_forget()
    frame_login.pack(pady=10)

# ------------------------------
# Inicialização da janela
# ------------------------------
app = tk.Tk()
app.title("Menu de Login")
# app.state("zoomed")  # opcional: tela inteira. descomente se desejar
app.configure(bg=BG_COLOR)

aplicar_estilo_ttk()

# Frame de login
frame_login = tk.Frame(app, bg=FRAME_COLOR, bd=0, relief="flat")
frame_login.pack(pady=40, padx=30, fill="x")

tk.Label(frame_login, text="Login", font=TITLE_FONT, bg=FRAME_COLOR).pack(pady=(10, 5))
tk.Label(frame_login, text="Usuário:", font=FONT, bg=FRAME_COLOR).pack(anchor="w", padx=10)
entry_user = tk.Entry(frame_login, font=FONT, bg=BG_COLOR, relief="flat")
entry_user.pack(fill="x", padx=10, pady=5)
tk.Label(frame_login, text="Senha:", font=FONT, bg=FRAME_COLOR).pack(anchor="w", padx=10)
entry_pass = tk.Entry(frame_login, show="*", font=FONT, bg=BG_COLOR, relief="flat")
entry_pass.pack(fill="x", padx=10, pady=5)

ttk.Button(frame_login, text="Entrar", style="RoundedButton.TButton", command=login)\
    .pack(pady=10, padx=10, fill="x")
ttk.Button(frame_login, text="Não tem um login? Crie um cadastro aqui",
           style="RoundedButton.TButton", command=mostrar_cadastro).pack(pady=(0, 10), padx=10, fill="x")

# Frame de cadastro (inicialmente oculto)
frame_cadastro = tk.Frame(app, bg=FRAME_COLOR, bd=0, relief="flat")
tk.Label(frame_cadastro, text="Cadastro", font=TITLE_FONT, bg=FRAME_COLOR).pack(pady=(10, 5))
tk.Label(frame_cadastro, text="Novo Usuário:", font=FONT, bg=FRAME_COLOR).pack(anchor="w", padx=10)
entry_new_user = tk.Entry(frame_cadastro, font=FONT, bg=BG_COLOR, relief="flat")
entry_new_user.pack(fill="x", padx=10, pady=5)
tk.Label(frame_cadastro, text="Nova Senha:", font=FONT, bg=FRAME_COLOR).pack(anchor="w", padx=10)
entry_new_pass = tk.Entry(frame_cadastro, show="*", font=FONT, bg=BG_COLOR, relief="flat")
entry_new_pass.pack(fill="x", padx=10, pady=5)

ttk.Button(frame_cadastro, text="Cadastrar", style="RoundedButton.TButton", command=cadastrar)\
    .pack(pady=10, padx=10, fill="x")
ttk.Button(frame_cadastro, text="Voltar para o login", style="RoundedButton.TButton",
           command=voltar_login).pack(pady=(0, 10), padx=10, fill="x")

# Inicia a aplicação
app.mainloop()

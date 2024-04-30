import tkinter as tk
from PIL import Image, ImageTk
from xml.etree import ElementTree as ET
import unicodedata
import os
from  tkinter import ttk
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
import ctypes
import shutil
from tkinter import messagebox


def tratar_input(texto):
    texto_sem_espacos = texto.replace(" ","")
    result = unicodedata.normalize('NFD', texto_sem_espacos).encode('ascii', 'ignore').decode('utf-8')
    return str(result).upper().strip()

def obter_info_cidade_homologada(cidade_ou_ibge: str) -> dict:
    try:
        tree = ET.parse('C:\\DigiSat\\SuiteG6\\Servidor\\Nfse\\CidadesHomologadas.xml')
        root = tree.getroot()
        cidade_ou_ibge = tratar_input(cidade_ou_ibge)


        for item in root:
            print(f"Cidade no XML: {item.tag}")
            if item.tag.startswith(cidade_ou_ibge) or item.find('CodigoIBGE').text == cidade_ou_ibge:
                #ObservacoesNotasTomadas = item.find('ObservacoesNotasTomadas')
                return {
                    'Padrao': item.find('Padrao').text,
                    'ConsultarNotasTomada': item.find('ConsultarNotasTomada').text,
                    'PrestadorObrigatorioTomadas': item.find('PrestadorObrigatorioTomadas').text,
                    'TipoComunicacao': item.find('TipoComunicacao').text,
                    'CodigoIBGE': item.find('CodigoIBGE').text,
                    'Multiservicos': item.find('Multiservicos').text,
                    'Certificado': item.find('Certificado').text,
                    'Login': item.find('Login').text,
                    'Senha': item.find('Senha').text,
                    #'DadosObrigatoriosPrestador': ObservacoesNotasTomadas.find('DadosObrigatoriosPrestador').text,
                    #'DadosObrigatoriosTomador': ObservacoesNotasTomadas.find('DadosObrigatoriosTomador').text
                }
        return None
    except Exception as e:
        print(f"Erro durante a execução: {e}")
        return None

def tratar_input(texto):
    texto_sem_espacos = texto.replace(" ", "")
    result = unicodedata.normalize('NFD', texto_sem_espacos).encode('ascii', 'ignore').decode('utf-8')
    return str(result).upper().strip()   

def obter_info_cidade_nacional(cidade_ou_codigo: str) -> dict:
    try:
        tree = ET.parse('C:\\DigiSat\\SuiteG6\\Servidor\\NfseNacional\\MunicipiosConveniados.xml')
        root = tree.getroot()
        cidade_ou_codigo = tratar_input(cidade_ou_codigo)

        for item in root:
            print(f"Cidade No XML: {item.tag}")
           
            if item.find(f"CodigoCidade").text == cidade_ou_codigo or item.tag.startswith(cidade_ou_codigo):
                convenios = item.find('Convenios')
                return {
                    'CodigoCidade': item.find('CodigoCidade').text,
                    'Homologado': item.find('Homologado').text,
                    'EmissorNacional': convenios.find('EmissorNacional').text,
                    'AmbienteNacional': convenios.find('AmbienteNacional').text,
                    'MAN': convenios.find('MAN').text,
                    'AproveitamentoDeCreditos': convenios.find('AproveitamentoDeCreditos').text if convenios.find('AproveitamentoDeCreditos') is not None else 'Não encontrado'
                }
         
        return None
    except Exception as e:
        print(f"Erro durante a pesquisa: {e}")
        return None


     
def pesquisar_cidade_homologada():
    cidade_ou_codigo = cidade_entry.get()
    if cidade_ou_codigo:
        result = obter_info_cidade_homologada(cidade_ou_codigo)

        if result:
            resultado_text.delete(1.0, tk.END)
            for key, value in result.items():
                resultado_text.insert(tk.END, f"{key}: {value}\n")
        else:
            resultado_text.delete(1.0, tk.END)
            resultado_text.insert(tk.END, f"Cidade ou código IBGE'{cidade_ou_codigo}' Não homologada.")
    else:
        resultado_text.delete(1.0, tk.END)
        resultado_text.insert(tk.END, f"Por favor, coloque o nome da cidade ou o código IBGE.")

def pesquisar_cidade_nacional():
    cidade_ou_codigo = cidade_entry.get()
    if cidade_ou_codigo:
        result = obter_info_cidade_nacional(cidade_ou_codigo)

        if result:
            resultado_text.delete(1.0, tk.END)
            for key, value in result.items():
                resultado_text.insert(tk.END, f"{key}: {value}\n")
        else:
            resultado_text.delete(1.0, tk.END)
            resultado_text.insert(tk.END, f"Cidade '{cidade_ou_codigo}' Não homologada no Nacional.")
    else:
        resultado_text.delete(1.0, tk.END)
        resultado_text.insert(tk.END, f"Por favor, coloque o nome da cidade ou o código IBGE.")    

def run_as_administrator(command):
    shell32 = ctypes.windll.shell32
    if shell32.ShellExecuteW(None, "runas", "cmd.exe", f"/c {command}", None, 1) <= 32:
        raise RuntimeError("Falha ao executar como administrador.")


def conceder_permissao():
    pastas = ["C:\\DigiSat", "C:\\Program Files\\TecnoSpeed"]

    for pasta in pastas:
        comando = f'cacls "{pasta}" /E /T /C /G "Todos":F'
        subprocess.run(comando, shell=True)
        messagebox.showinfo("Sucesso", "Permissões Alteradas :)")

def parar_servicos():
    try:
        caminho_bat = r'\\192.168.0.250\Public\Colaboradores\Suporte\Renan\DigisatHomologacao\sincronizadormongo.bat'
        run_as_administrator(caminho_bat)
        subprocess.run(['net', 'stop', 'MongoDBDigisat'], shell=True, check=True)
# Iniciar o serviço SincronizadorDigisat
        subprocess.run(['net', 'stop', 'SincronizadorDigisat'], shell=True, check=True)
        messagebox.showinfo("Sucesso", "Serviços parados! :)")
    except Exception as e:
        print(f"Erro ao parar os processos: {e}")
  
def executar_backup():
    try:
        # Mapear o caminho UNC para uma unidade de rede (por exemplo, Z:)
        subprocess.run(['net', 'use', 'Z:', '\\\\192.168.0.250\\Public\\Colaboradores\\Suporte\\Renan\\DigisatHomologacao'], shell=True, check=True)
        # Definir o diretório de origem e destino para a cópia de arquivos
        origem = r'C:\DigiSat\SuiteG6\Dados'
        destino = r'Z:\DadosBkp'
        # Executar a cópia de arquivos usando shutil
        shutil.copytree(origem, destino)
        messagebox.showinfo("Backup", "Backup gerado com sucesso! :)")
    except subprocess.CalledProcessError as e:
        messagebox.showinfo("Error", f"Erro ao executar o backup: {e}")
    except Exception as e:
        print(f"Erro durante o processo de cópia: {e}")
    finally:
        # Remover o mapeamento da unidade de rede (Z:)
        subprocess.run(['net', 'use', 'Z:', '/delete'], shell=True, check=True)


def repair_mongo():
    try:
        caminho_bat = r'\\192.168.0.250\\Public\\Colaboradores\\Suporte\\Renan\\DigisatHomologacao\\repairmongodb.bat'
        subprocess.run(caminho_bat, shell=True, check=True)
        messagebox.showinfo("Sucesso", "Reparo do mongo com sucesso :)")
    except Exception as e:
        print("Erro"f"Erro ao executar a função: {e}")
        
root = tk.Tk()
root.title("Digisat NFS-e")
root.configure(bg='#051931')  # Define o estilo de fundo para o root



#Icone do APP
icon_path =("\\\\192.168.0.250\\Public\\Colaboradores\\Suporte\\Renan\\nfse.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)
    

# Logo da Digisat
logo = Image.open("\\\\192.168.0.250\\Public\\Colaboradores\\Suporte\\Renan\\logo.png")
logo = logo.resize((250, 100))
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(root, image=logo, bg='#051931')
logo_label.image = logo
logo_label.pack()

#Logo NFS-e
NFSe = Image.open("\\\\192.168.0.250\\Public\\Colaboradores\\Suporte\\Renan\\NFSe.jpg")
NFSe = NFSe.resize((70, 50))
NFSe = ImageTk.PhotoImage(NFSe)
NFSe_label = tk.Label(root, image=NFSe, bg='#051931')
NFSe_label.image = NFSe
NFSe_label.pack()
NFSe_label.place(x=0, y=510)


# Frame para a entrada de cidade
pesquisa_frame = tk.Frame(root, bg='#051931')
pesquisa_frame.pack(pady=1)

cidade_label = tk.Label(pesquisa_frame, text="Cidade + UF:", fg='white', font=("Helvetica", 10, "bold"), bg='#051931')
cidade_label.grid(row=0, column=0)

cidade_entry = tk.Entry(pesquisa_frame)
cidade_entry.grid(row=0, column=1)
cidade_entry.bind("<Return>", lambda event: pesquisar_cidade_homologada())  


pesquisar_button_arquivo1 = tk.Button(pesquisa_frame, text="Pesquisar (Cidades Homologadas)", command=pesquisar_cidade_homologada, fg='white', bg='#051931')
pesquisar_button_arquivo1.grid(row=0, column=2, padx=8)

pesquisar_button_arquivo2 = tk.Button(pesquisa_frame, text="Pesquisar (No Nacional)", command=pesquisar_cidade_nacional, fg='white', bg='#051931')
pesquisar_button_arquivo2.grid(row=0, column=3)

# Botão para parar os serviços
parar_servicos_button = tk.Button(root, text="Parar Serviços", command=parar_servicos, fg='white', bg='#051931')
parar_servicos_button.pack()
parar_servicos_button.place(x=505, y=465)

# Botão para conceder permissões
conceder_permissao_button = tk.Button(root, text="Conceder Permissões", command=conceder_permissao, fg='white', bg='#051931')
conceder_permissao_button.pack()
conceder_permissao_button.place(x=252, y=465)

#Botão para gerar backup do sistema
executar_backup_button = tk.Button(root, text="Fazer Backup", command=executar_backup, fg='white', bg='#051931')
executar_backup_button.pack()
executar_backup_button.place(x=59, y=465)

#Botão para repar o mongo e também para serviços
repair_mongo_button = tk.Button(root, text="Reparar Mongo", command= repair_mongo, fg='white', bg='#051931')
repair_mongo_button.pack()
repair_mongo_button.place(x=150, y=465)

# Frame para exibir resultados
resultado_frame = tk.Frame(root, bg='#051931')
resultado_frame.pack(pady=20, padx=10)

resultado_text = tk.Text(resultado_frame, width=50, height=12, padx=40, pady=40, fg='white', font=("Helvetica", 12, 'bold'), bg='#051931')
resultado_text.pack(side=tk.BOTTOM)

#Versão release
versao_release = "Versão 1.0.6"
versao_release = tk.Label(root, text=versao_release, fg= 'white', bg= '#051931')
versao_release.pack(side=tk.BOTTOM)

# Rodapé
rodape_label = tk.Label(root, text= 'Desenvolvido por Renan Bernardi Haefliger', bg='#051931', fg='white', font=('Helvetica', 10, 'bold'))
rodape_label.pack(side=tk.BOTTOM)

largura= 650
altura= 560
root.geometry (f"{largura}x{altura}")
root.resizable(False, False)
#tk.Label(root, text="Essa janela não poder ser maximizada").pack()
root.mainloop()

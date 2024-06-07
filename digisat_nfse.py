import tkinter as tk
from tkinter import Tk
from PIL import Image, ImageTk
from xml.etree import ElementTree as ET
import unicodedata
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
import ctypes
import shutil
from datetime import datetime
from urllib.parse import quote_plus
import pymongo
import ctypes
from tkinter import messagebox
from PIL import Image as PilImage


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
        #subprocess.run(['net', 'use', 'Z:', '\\\\192.168.0.250\\Public\\Colaboradores\\Suporte\\Renan\\DigisatHomologacao'], shell=True, check=True)
        # Definir o diretório de origem e destino para a cópia de arquivos
        origem = r'C:\DigiSat\SuiteG6\Dados'
        destino = r'D:\DadosBkp'
        if not os.path.exists(destino):
            os.makedirs(destino)
        # Executar a cópia de arquivos usando shutil
        shutil.copytree(origem, destino, dirs_exist_ok=True)
        messagebox.showinfo("Backup", "Backup gerado com sucesso! :)")
    except Exception as e:
        messagebox.showinfo("Error", f"Erro ao executar o backup: {e}")
    #except Exception as e:
        #print(f"Erro durante o processo de cópia: {e}")
    #finally:
        # Remover o mapeamento da unidade de rede (Z:)
        #subprocess.run(['net', 'use', 'Z:', '/delete'], shell=True, check=True)


def repair_mongo():
    try:
        caminho_bat = r'\\192.168.0.250\\Public\\Colaboradores\\Suporte\\Renan\\DigisatHomologacao\\repairmongodb.bat'
        subprocess.run(caminho_bat, shell=True, check=True)
        messagebox.showinfo("Sucesso", "Reparo do mongo com sucesso :)")
    except Exception as e:
        print("Erro"f"Erro ao executar a função: {e}")

documentos = []

def buscar():
        global documentos
        try:
            data_inicio = entry_data_inicio.get()
            data_fim = entry_data_fim.get()

            # Configurações de conexão
            CLIENT_USER = "root"
            CLIENT_IP = "127.0.0.1"  
            CLIENT_PASSWORD = "|cSFu@5rFv#h8*=" 
            CLIENT_PORT = 12220
            DATABASE_NAME = "DigisatServer"
            COLLECTION_NAME = "Movimentacoes"

            # Escapar nome de usuário e senha
            escaped_user = quote_plus(CLIENT_USER)
            escaped_password = quote_plus(CLIENT_PASSWORD)

            # URI de conexão para o MongoDB local
            MONGO_STRING = f"mongodb://{escaped_user}:{escaped_password}@{CLIENT_IP}:{CLIENT_PORT}/?authSource=admin"

            # Conectar ao MongoDB
            client = pymongo.MongoClient(MONGO_STRING)
            db = client[DATABASE_NAME]
            collection = db[COLLECTION_NAME]

            documentos.clear()
            query = {}
            if data_inicio and data_fim:
                try:
                    data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
                    data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
                    query["DataHoraEmissao"] = {"$gte": data_inicio_dt, "$lte": data_fim_dt}
                except ValueError:
                    messagebox.showwarning("Aviso", "Formato de data inválido. Use AAAA-MM-DD.")

            documentos_encontrados = collection.find(query)

            for documento in documentos_encontrados:
                if "XmlTexto" in documento:
                    documentos.append(documento)
                
            
            if documentos:
                messagebox.showinfo("Sucesso", "Documentos encontrados. Prontos para exportar.")
            else:
                messagebox.showwarning("Aviso", "Nenhum documento válido encontrado.")
        except Exception as e:
            documentos.clear()
            messagebox.showerror("Erro", str(e))

def exportar():
        if documentos:
            pasta_destino = os.path.join(os.path.expanduser("~"), "Desktop", "Movimentacoes")
            pasta_cancelados = os.path.join(pasta_destino, "Cancelado")
            #pasta_inutilizados = os.path.join(pasta_destino, "Inutilizado")

            if not os.path.exists(pasta_destino):
                os.makedirs(pasta_destino)
            if not os.path.exists(pasta_cancelados):
                os.makedirs(pasta_cancelados)
            #if not os.path.exists(pasta_inutilizados):
               # os.makedirs(pasta_inutilizados)

            for documento in documentos:
                try:
                    conteudo_xml = documento["XmlTexto"]
                    nome_arquivo = documento.get("ChaveAcesso", "Movimentacoes") + ".xml"
                     

                    situacao = documento.get("Situacao", {})
                    descricao = situacao.get("Descricao", "Concluído").lower()

                    #if descricao == "inutilizado":
                       # caminho_area_trabalho = os.path.join(pasta_inutilizados, nome_arquivo)
                    #else:
                       # caminho_area_trabalho = os.path.join(pasta_destino, nome_arquivo)

                    if descricao == "cancelado":               
                        caminho_area_trabalho = os.path.join(pasta_cancelados, nome_arquivo)
                    else:    
                        caminho_area_trabalho = os.path.join(pasta_destino, nome_arquivo)
                    
                    with open(caminho_area_trabalho, "w", encoding="utf-8") as arquivo:
                        arquivo.write(conteudo_xml)

                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao exportar documento {documento.get('Numero')}: {str(e)}")
            
            messagebox.showinfo("Sucesso", "Dados exportados com sucesso!")
        else:
            messagebox.showwarning("Aviso", "Nenhum documento encontrado. Por favor, busque primeiro.")

def senha_alternada():
        # Obter a data e hora atual
    now = datetime.now()
    
    # Extrair informações de data e hora
    dia = now.day
    mes = now.month
    hora = now.hour
    minuto = now.minute
    
    # Montar a senha temporária com base nas informações de data e hora
    senha_temporaria = f"{dia:02d}{mes:02d}{hora:02d}{minuto:02d}"
    
    return senha_temporaria
def fazer_login():
    global login_sucesso
    login_sucesso = False

    def tentar_login():
        global login_sucesso    
        usuario = entry_usuario.get()
        senha = entry_senha.get()

        senha_temporaria = senha_alternada()
        # Verificar se as credenciais estão corretas
        if usuario == "Suporte" and senha == senha_temporaria:
            login_sucesso= True
            messagebox.showinfo("Sucesso", "Login bem-sucedido!")
            login_window.destroy()
            
        else:
            messagebox.showerror("Erro", "Credenciais inválidas. Tente novamente.")

    def on_closing():
        if not login_sucesso:
            if messagebox.askokcancel("Sair", "Você quer sair sem fazer login?"):
                login_window.destroy()
        else:
            login_window.destroy()        
   
    # Criar a janela de login
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.configure(bg='#051931')
    login_window.protocol("WM_DELETE_WINDOW", on_closing)
    
    logo = Image.open("\\\\192.168.0.250\\Public\\Colaboradores\\Suporte\\Renan\\logo.png")
    logo = logo.resize((280, 120))
    logo = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(image=logo, bg='#051931')
    logo_label.image = logo
    logo_label.pack()
    logo_label.place(x=130, y=80)

    label_usuario = tk.Label(login_window, text="Usuário:", fg='white', font=("Arial", 10, "bold"), bg='#051931')
    label_usuario.place(x=150, y=220)

    entry_usuario = tk.Entry(login_window, fg='white', bg='#051931')
    entry_usuario.place(x=210, y=220)

    label_senha = tk.Label(login_window, text="Senha:", fg='white', font=("Arial", 10, "bold"), bg='#051931')
    label_senha.place(x=150, y=250)

    entry_senha = tk.Entry(login_window, show="*", fg='white', bg='#051931')
    entry_senha.place(x=210, y=250)

    button_login = tk.Button(login_window, text="Login", command=tentar_login, fg='white', bg='#051931')
    button_login.pack()
    button_login.place(x=225, y=300)
          
    #Versão release
    versao_release = "Versão 1.1.0"
    versao_release = tk.Label(text=versao_release, fg= 'white', bg= '#051931')
    versao_release.pack(side=tk.BOTTOM)
    
    #informativo suporte
    suporte = tk.Label(text='Uso exclusivo suporte', bg= '#051931', fg='white', font=('Arial', 10, 'bold'))
    suporte.pack(side=tk.BOTTOM)

    # Rodapé
    rodape_label = tk.Label(text= 'Desenvolvido por Renan Bernardi Haefliger', bg='#051931', fg='white', font=('Arial', 10, 'bold'))
    rodape_label.pack(side=tk.BOTTOM)

    #Icone do APP
    icon_path = ("\\\\192.168.0.250\\Public\\Colaboradores\\Suporte\\Renan\\DigisatHomologacao\\icone.ico")
    if os.path.exists(icon_path):
        login_window.iconbitmap(icon_path)

    largura= 500
    altura= 500
    login_window.geometry (f"{largura}x{altura}")
    login_window.resizable(False, False)
    login_window.mainloop()

    return login_sucesso    

if fazer_login():
         
    root = tk.Tk()
    root.title("Digisat NFS-e")
    root.configure(bg='#051931')

    #Icone do APP
    icon_path =("\\\\192.168.0.250\\Public\\Colaboradores\\Suporte\\Renan\\DigisatHomologacao\\icone.ico")
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

    cidade_label = tk.Label(pesquisa_frame, text="Cidade + UF:", fg='white', font=("Arial", 10, "bold"), bg='#051931')
    cidade_label.grid(row=0, column=0)

    cidade_entry = tk.Entry(pesquisa_frame)
    cidade_entry.grid(row=0, column=1)
    cidade_entry.bind("<Return>", lambda event: pesquisar_cidade_homologada())  

    label_data_inicio = tk.Label(text="Data Início CF-e(AAAA-MM-DD):", fg='white', bg='#051931')
    label_data_inicio.pack()
    label_data_inicio.place(x=90, y=380)

    entry_data_inicio = tk.Entry()
    entry_data_inicio.pack()
    entry_data_inicio.place(x=280, y=380)

    label_data_fim = tk.Label( text="Data Fim CF-e (AAAA-MM-DD):", fg='white', bg='#051931')
    label_data_fim.pack()
    label_data_fim.place(x=100, y=400)

    entry_data_fim = tk.Entry()
    entry_data_fim.pack()
    entry_data_fim.place(x=280, y=400)


    # Botão para buscar os CF-e
    button_buscar = tk.Button( text="Buscar XML CF-e", command=buscar, fg='white', bg='#051931')
    button_buscar.pack()
    button_buscar.place(x=328, y=465)

    #Botão para exportar os CF-e
    button_exportar = tk.Button( text="Exportar XML CF-e", command=exportar, fg='white', bg='#051931')
    button_exportar.pack()
    button_exportar.place(x=428, y=465)

    # Botão para pesquisar as cidades
    pesquisar_button_arquivo1 = tk.Button(pesquisa_frame, text="Pesquisar (Cidades Homologadas)", command=pesquisar_cidade_homologada, fg='white', bg='#051931')
    pesquisar_button_arquivo1.grid(row=0, column=2, padx=8)

    pesquisar_button_arquivo2 = tk.Button(pesquisa_frame, text="Pesquisar (No Nacional)", command=pesquisar_cidade_nacional, fg='white', bg='#051931')
    pesquisar_button_arquivo2.grid(row=0, column=3)

    # Botão para parar os serviços
    parar_servicos_button = tk.Button(root, text="Parar Serviços", command=parar_servicos, fg='white', bg='#051931')
    parar_servicos_button.pack()
    parar_servicos_button.place(x=535, y=465)

    # Botão para conceder permissões
    conceder_permissao_button = tk.Button(root, text="Conceder Permissões", command=conceder_permissao, fg='white', bg='#051931')
    conceder_permissao_button.pack()
    conceder_permissao_button.place(x=205, y=465)

    #Botão para gerar backup do sistema
    executar_backup_button = tk.Button(root, text="Fazer Backup", command=executar_backup, fg='white', bg='#051931')
    executar_backup_button.pack()
    executar_backup_button.place(x=35, y=465)

    #Botão para repar o mongo e também para serviços
    repair_mongo_button = tk.Button(root, text="Reparar Mongo", command= repair_mongo, fg='white', bg='#051931')
    repair_mongo_button.pack()
    repair_mongo_button.place(x=113, y=465)

    # Frame para exibir resultados
    resultado_frame = tk.Frame(root, bg='#051931')
    resultado_frame.pack(pady=20, padx=10)

    resultado_text = tk.Text(resultado_frame, width=40, height=8, padx=35, pady=35, fg='white', font=("Arial", 10, 'bold'), bg='#051931')
    resultado_text.pack(side=tk.BOTTOM)

    #Versão release
    versao_release = "Versão 1.1.0"
    versao_release = tk.Label(root, text=versao_release, fg= 'white', bg= '#051931')
    versao_release.pack(side=tk.BOTTOM)

    # Rodapé
    rodape_label = tk.Label(root,text= 'Desenvolvido por Renan Bernardi Haefliger', bg='#051931', fg='white', font=('Arial', 10, 'bold'))
    rodape_label.pack(side=tk.BOTTOM)

    largura= 650
    altura= 560
    root.geometry (f"{largura}x{altura}")
    root.resizable(False, False)
   
    root.mainloop()
else:
    print("Não logado")
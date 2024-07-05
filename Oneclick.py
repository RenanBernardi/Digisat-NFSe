import tkinter as tk
from tkinter import Tk
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageOps
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
from PIL import Image, ImageTk, ImageEnhance
from datetime import datetime, timedelta
import platform
import traceback
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
        origem = r'C:\DigiSat\SuiteG6\Dados'
        destino = r'D:\DadosBkp'
        if not os.path.exists(destino):
            os.makedirs(destino)
        # Executar a cópia de arquivos usando shutil
        shutil.copytree(origem, destino, dirs_exist_ok=True)
        messagebox.showinfo("Backup", "Backup gerado com sucesso! :)")
    except Exception as e:
        messagebox.showinfo("Error", f"Erro ao executar o backup: {e}")

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
        tipo_busca = var_tipo_busca.get()
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
        
        if tipo_busca in ["CF-e", "NFC-e", "NF-e Saída", "NF-e Entrada"]:
                if data_inicio and data_fim:
                    try:
                        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
                        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
                        data_fim_dt += timedelta(days=1)  # Para incluir o dia final completo
                        query["DataHoraEmissao"] = {"$gte": data_inicio_dt, "$lt": data_fim_dt}
                    except ValueError:
                        messagebox.showwarning("Aviso", "Formato de data inválido. Use AAAA-MM-DD.")
                
        documentos_encontrados = collection.find(query)
        for documento in documentos_encontrados:
                if tipo_busca == "CF-e":
                    if "XmlTexto" in documento:
                        documentos.append(documento)
                elif tipo_busca == "NFC-e": 
                        _t = documento.get("_t",{})
                        if "NotaFiscalConsumidorEletronica" in _t:
                            Historicos = documento.get("Historicos", [])
                            for historico in Historicos:                               
                                    xml = historico.get("Xml")
                                    if xml:
                                        documento_copia = documento.copy()
                                        documento_copia["Xml"] = xml
                                        documentos.append(documento_copia)
                                        print(f"Documento adicionado: {documento_copia}")
                                    else:
                                        print(f"Valor de 'Xml' encontrado: {xml}")   

                elif tipo_busca == "NF-e Saída":
                        _t = documento.get("_t",{})
                        if "NotaFiscalEletronicaSaida" in _t:
                            Historicos = documento.get("Historicos", [])
                            for historico in Historicos:
                                xml = historico.get("Xml")
                                if xml:
                                    documento_copia = documento.copy()
                                    documento_copia["Xml"] = xml
                                    documentos.append(documento_copia)
                                    print(f"Documento adicionado: {documento_copia}")
                                else:
                                    print(f"Valor de 'Xml' encontrado: {xml}")
                elif tipo_busca == "NF-e Entrada":
                    _t= documento.get("_t",{})
                    if "NotaFiscalEletronicaEntrada" in _t:
                        Historicos = documento.get("Historicos",[])
                        for historico in Historicos:
                            xml = historico.get("Xml")
                            if xml:
                                documento_copia = documento.copy()
                                documento_copia["Xml"] = xml
                                documentos.append(documento_copia)
                                print(f"Documento adicionado: {documento_copia}")
                            else:
                                print(f"Valor de 'Xml' encontrado: {xml}")

        if documentos:
            messagebox.showinfo("Sucesso", "Documentos encontrados. Prontos para exportar.")
        else:
            messagebox.showwarning("Aviso", "Nenhum documento válido encontrado.")
    except Exception as e:
        documentos.clear()
        messagebox.showerror("Erro", str(e))

def get_desktop_path():
    if platform.system() == "Windows":
        import winreg
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
            desktop = winreg.QueryValueEx(key, "Desktop")[0]
            return desktop
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao acessar o caminho da área de trabalho: {str(e)}")
            return None
    else:
        home = os.path.expanduser("~")
        desktop = os.path.join(home, "Desktop")
        if not os.path.exists(desktop):
            desktop = os.path.join(home, "Área de Trabalho")
        return desktop

def exportar():
    if documentos:
        desktop_dir = get_desktop_path()
        if desktop_dir is None:
            return

        pasta_destino = os.path.join(desktop_dir, "Movimentacoes")
        pasta_cancelados = os.path.join(pasta_destino, "Cancelado")

        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
        if not os.path.exists(pasta_cancelados):
            os.makedirs(pasta_cancelados)

        for documento in documentos:
            try:
                conteudo_xml = documento.get("Xml") if "Xml" in documento else documento.get("XmlTexto")
                nome_arquivo = documento.get("ChaveAcesso", "Movimentacoes") + ".xml"

                situacao = documento.get("Situacao", {})
                descricao = situacao.get("Descricao", "Concluído").lower()

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

def create_gradient(width, height):
    base = Image.new('RGB', (width, height))
    top_color = (1, 144, 246)
    bottom_color = (5, 25, 49)

    for i in range(height):
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * i / height)
        g = int(top_color[0] + (bottom_color[0] - top_color[0]) * i / height)
        b = int(top_color[0] + (bottom_color[0] - top_color[0]) * i / height)
        base.paste((r, g, b), (0, i, width, i+1))

    return base

def get_gradient_color(y, height, top_color, bottom_color):
    r = int(top_color[0] + (bottom_color[0] - top_color[0]) * y / height)
    g = int(top_color[0] + (bottom_color[0] - top_color[0]) * y / height)
    b = int(top_color[0] + (bottom_color[0] - top_color[0]) * y / height)
    return f'#{r:02x}{g:02x}{b:02x}'

def senha_alternada():
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

    def on_closing():
        login_window.destroy()
   
    # Criar a janela de login
    login_window = tk.Tk()
    login_window.title("Login")
    #login_window.configure(bg='#0f55a2')
    width, height = 500, 500
    background_image = create_gradient(width, height)
    background_image_tk = ImageTk.PhotoImage(background_image)
    login_window.protocol("WM_DELETE_WINDOW", on_closing)
    login_window.backgound_image_tk = background_image_tk
    background_label = tk.Label(login_window, image=background_image_tk)
    background_label.place(relheight=1, relwidth=1)
    
    # Calcular a cor do gradiente na posição do logo
    
    logo = Image.open("\\\\192.168.0.250\\Public\\Colaboradores\\Suporte\\Renan\\logo.png")
    logo = logo.resize((280, 120))
    logo_tk = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(login_window, image=logo_tk, bg= get_gradient_color(80, height, (1, 144,246),(5, 25, 49)))
    logo_label.image = logo_tk
    logo_label.place(x=130, y=80)

    
    label_usuario = tk.Label(login_window, text="Usuário:", fg='green', font=("Arial", 10, "bold"), bg=get_gradient_color(100, height, (1, 144, 246), (5, 25, 49)))
    label_usuario.place(x=150, y=220)

    entry_usuario = tk.Entry(login_window, fg='green',bg=get_gradient_color(100, height, (1, 144, 246), (5, 25, 49)))
    entry_usuario.place(x=210, y=220)

    label_senha = tk.Label(login_window, text="Senha:", fg='green', font=("Arial", 10, "bold"),bg=get_gradient_color(100, height, (1, 144, 246), (5, 25, 49)))
    label_senha.place(x=150, y=250)

    entry_senha = tk.Entry(login_window, show="*", fg='green', bg=get_gradient_color(100, height, (1, 144, 246), (5, 25, 49)))
    entry_senha.place(x=210, y=250)

    button_login = tk.Button(login_window, text="Login", command=tentar_login, fg='green', bg=get_gradient_color(100, height, (1, 144, 246), (5, 25, 49)), bd=5, relief='ridge', font=('Helvetica',10, 'bold'))
    button_login.pack()
    button_login.place(x=225, y=300)
    
    #button_info = tk.Button(text= "!", command=exibir_conteudo_arquivo)
    #button_info.pack()
    #button_info.place(x=485, y=1)

    #Versão release
    versao_release = "Versão 1.1.3"
    versao_release = tk.Label(text=versao_release, fg= 'green', bg=get_gradient_color(100, height, (1, 144, 246), (5, 25, 49)))
    versao_release.pack(side=tk.BOTTOM)
    
    #informativo suporte
    suporte = tk.Label(text='Uso exclusivo suporte', fg='green', font=('Arial', 10, 'bold'),bg=get_gradient_color(100, height, (1, 144, 246), (5, 25, 49)))
    suporte.pack(side=tk.BOTTOM)

    # Rodapé
    rodape_label = tk.Label(text= 'Desenvolvido por Renan Bernardi Haefliger', fg='green', font=('Arial', 10, 'bold'), bg=get_gradient_color(100, height, (1, 144, 246), (5, 25, 49)))
    rodape_label.pack(side=tk.BOTTOM)

    #Icone do APP
    icon_path = r"\\192.168.0.250\\Public\\Colaboradores\\Suporte\\Renan\\DigisatHomologacao\\icone.ico"
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
    root.title("OneClick")
    #root.configure(bg='#0f55a2')
    width, height = 650,760
    background_image = create_gradient(width, height)
    background_image_tk = ImageTk.PhotoImage(background_image)

    # Manter referências aos objetos PhotoImage
    root.background_image_tk = background_image_tk

    background_label = tk.Label(root, image=background_image_tk)
    background_label.place(relwidth=1, relheight=1)

    # Calcular a cor do gradiente na posição do logo
    logo_y_position = 80
    top_color = (1, 144, 246)
    bottom_color = (5, 25, 49)
    logo_bg_color = get_gradient_color(logo_y_position, height, top_color, bottom_color)


    #Icone do APP
    icon_path =r"\\192.168.0.250\\Public\\Colaboradores\\Suporte\\Renan\\DigisatHomologacao\\icone.ico"
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
        
    # Logo da Digisat
    logo = Image.open("\\\\192.168.0.250\\Public\\Colaboradores\\Suporte\\Renan\\logo.png")
    logo = logo.resize((250, 100))
    logo = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(root, image=logo, bg=get_gradient_color(90, height, (1, 144, 246), (5, 25, 49)))
    logo_label.image = logo
    logo_label.pack()
    

    #Logo NFS-e
    NFSe = Image.open("\\\\192.168.0.250\\Public\\Colaboradores\\Suporte\\Renan\\NFSe.jpg")
    NFSe = NFSe.resize((70, 50))
    NFSe = ImageTk.PhotoImage(NFSe)
    NFSe_label = tk.Label(root, image=NFSe, bg=logo_bg_color)
    NFSe_label.image = NFSe
    NFSe_label.pack()
    NFSe_label.place(x=0, y=708)


        # Frame para a entrada de cidade
    pesquisa_frame = tk.Frame(root, bg=get_gradient_color(100, height, (1, 144, 246), (5, 25, 49)))
    pesquisa_frame.pack(pady=1)

    cidade_label = tk.Label(pesquisa_frame, text="Cidade + UF:", fg='green', font=("Arial", 10, "bold"), bg=get_gradient_color(100, height, (1, 144, 246), (5, 25, 49)))
    cidade_label.grid(row=0, column=0)

    cidade_entry = tk.Entry(pesquisa_frame)
    cidade_entry.grid(row=0, column=1)
    cidade_entry.bind("<Return>", lambda event: pesquisar_cidade_homologada())

    var_tipo_busca = tk.StringVar(value="CF-e")
    tipo_busca_label = tk.Label(root, text="Tipo de Busca:", fg='green', bg=get_gradient_color(420, height, (1, 144, 246), (5, 25, 49)), font=('Arial', 10, 'bold'))
    tipo_busca_label.place(x=165, y=420)

    option_menu = tk.OptionMenu(root, var_tipo_busca, "CF-e", "NFC-e", "NF-e Saída", "NF-e Entrada")
    option_menu.place(x=263, y=410)
    option_menu.config(bg=get_gradient_color(410, height, (1, 144, 246), (5, 25, 49)), fg='green')

    label_data_inicio = tk.Label(root, text="Data Início(AAAA-MM-DD):", fg='green', bg=get_gradient_color(445, height, (1, 144, 246), (5, 25, 49)), font=('Arial', 10, 'bold'))
    label_data_inicio.pack()
    label_data_inicio.place(x=90, y=445)

    entry_data_inicio = tk.Entry(root)
    entry_data_inicio.pack()
    entry_data_inicio.place(x=260, y=445)

    label_data_fim = tk.Label(root, text="Data Fim(AAAA-MM-DD):", fg='green', font=('Arial', 10, 'bold'), bg=get_gradient_color(465, height, (1, 144, 246), (5, 25, 49)))
    label_data_fim.pack()
    label_data_fim.place(x=100, y=465)

    entry_data_fim = tk.Entry(root)
    entry_data_fim.pack()
    entry_data_fim.place(x=260, y=465)

    # Botão para buscar os CF-e
    button_buscar = tk.Button(root, text="Buscar XML", command=buscar, fg='green', bg=get_gradient_color(565, height, (1, 144, 246), (5, 25, 49)))
    button_buscar.pack()
    button_buscar.place(x=328, y=565)

    # Botão para exportar os CF-e
    button_exportar = tk.Button(root, text="Exportar XML", command=exportar, fg='green', bg=get_gradient_color(565, height, (1, 144, 246), (5, 25, 49)))
    button_exportar.pack()
    button_exportar.place(x=399, y=565)

    # Botão para pesquisar as cidades
    pesquisar_button_arquivo1 = tk.Button(pesquisa_frame, text="Pesquisar (Cidades Homologadas)", command=pesquisar_cidade_homologada, fg='green', bg=get_gradient_color(100, height, (1, 144, 246), (5, 25, 49)), bd=4, relief='raised')
    pesquisar_button_arquivo1.grid(row=0, column=2, padx=8)

    pesquisar_button_arquivo2 = tk.Button(pesquisa_frame, text="Pesquisar (No Nacional)", command=pesquisar_cidade_nacional, fg='green', bg=get_gradient_color(100, height, (1, 144, 246), (5, 25, 49)), bd=4, relief='raised')
    pesquisar_button_arquivo2.grid(row=0, column=3)

    # Botão para parar os serviços
    parar_servicos_button = tk.Button(root, text="Parar Serviços", command=parar_servicos, fg='green', bg=get_gradient_color(565, height, (1, 144, 246), (5, 25, 49)))
    parar_servicos_button.pack()
    parar_servicos_button.place(x=480, y=565)

    # Botão para conceder permissões
    conceder_permissao_button = tk.Button(root, text="Conceder Permissões", command=conceder_permissao, fg='green', bg=get_gradient_color(565, height, (1, 144, 246), (5, 25, 49)))
    conceder_permissao_button.pack()
    conceder_permissao_button.place(x=205, y=565)

    # Botão para gerar backup do sistema
    executar_backup_button = tk.Button(root, text="Fazer Backup", command=executar_backup, fg='green', bg=get_gradient_color(565, height, (1, 144, 246), (5, 25, 49)))
    executar_backup_button.pack()
    executar_backup_button.place(x=35, y=565)

    # Botão para reparar o mongo e também para serviços
    repair_mongo_button = tk.Button(root, text="Reparar Mongo", command=repair_mongo, fg='green', bg=get_gradient_color(565, height, (1, 144, 246), (5, 25, 49)))
    repair_mongo_button.pack()
    repair_mongo_button.place(x=113, y=565)

    # Frame para exibir resultados
    resultado_frame = tk.Frame(root, bg='#0f55a2')
    resultado_frame.pack(pady=20, padx=10)

    resultado_text = tk.Text(resultado_frame, width=40, height=8, padx=35, pady=35, fg='green', font=("Arial", 10, 'bold'), bg=get_gradient_color(600, height, (1, 144, 246), (5, 25, 49)))
    resultado_text.pack(side=tk.BOTTOM)

    # Versão release
    versao_release = "Versão 1.1.3"
    versao_release = tk.Label(root, text=versao_release, fg='green', bg=get_gradient_color(700, height, (1, 144, 246), (5, 25, 49)))
    versao_release.pack(side=tk.BOTTOM)

    # Rodapé
    rodape_label = tk.Label(root, text='Desenvolvido por Renan Bernardi Haefliger', bg=get_gradient_color(720, height, (1, 144, 246), (5, 25, 49)), fg='green', font=('Arial', 10, 'bold'))
    rodape_label.pack(side=tk.BOTTOM)

    largura = 650
    altura = 760
    root.geometry(f"{largura}x{altura}")
    root.resizable(False, False)
    root.mainloop()
else:
    print("Não logado")
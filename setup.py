from cx_Freeze import setup, Executable

# Adicione os arquivos adicionais necessários
files = [
    "logo.png",
    "icone.ico",
    "\\\\192.168.0.250\\Public\\Colaboradores\\Suporte\\Renan\\DigisatHomologacao\\InfoOneclick.txt",
    "\\\\192.168.0.250\\Public\\Colaboradores\\Suporte\\Renan\\DigisatHomologacao\\permitirseguranca.bat",
    "\\\\192.168.0.250\\Public\\Colaboradores\\Suporte\\Renan\\DigisatHomologacao\\repairmongodb.bat",
    "\\\\192.168.0.250\\Public\\Colaboradores\\Suporte\\Renan\\DigisatHomologacao\\sincronizadormongo.bat",
]

# Configuração do executável
executables = [
    Executable(
        script="Oneclick.py",
        base="Win32GUI",  # Use "Win32GUI" para remover o terminal na execução
        icon="icone.ico",
    )
]

# Configuração do instalador
setup(
    name="Oneclick",
    version="1.0",
    description="OneClickInstalador",
    author="Renan Bernardi Haefliger",
    options={
        "build_exe": {
            "packages": ["os", "tkinter", "PIL"],  # Liste os pacotes necessários
            "include_files": files,  # Adicione arquivos extras
        }
    },
    executables=executables,
)

# pip install cx_freeze
import cx_Freeze
from cx_Freeze import setup, Executable

# Lista de arquivos a incluir
incluir_arquivos = ["assets", "base.stranger", "recursos"]

# Definições da build
build_exe_options = {
    "packages": ["pygame", "tkinter", "os", "random", "json"],
    "include_files": incluir_arquivos
}

executaveis = [
    Executable(
        script="main.py",
        icon="assets/icone.png",
        base=None
    )
]

setup(
    name="Stranger Things",
    version="1.0",
    description="Jogo do Stranger Things",
    options={"build_exe": build_exe_options},
    executables=executaveis
)
# python setup.py build
# python setup.py bdist_msi

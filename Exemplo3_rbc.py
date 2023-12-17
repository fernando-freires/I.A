import streamlit as st
import numpy as np

diagnostico_logomarca = {
    'BALDURS GATE 3': 'logo1.jpg',
    'Red Dead Redemption 2': 'logo2.jpeg',
    'GTA 5/VALORANT': 'logo3.png',
    'FORTNITE': 'logo4.png',
    'Cyberpunk 2077': 'logo5.jpg',
    'VALORANT': 'logo6.png'
}

# Função para escrever as categorias em um arquivo
def escrever_categorias_arquivo(categorias):
    with open('dados_categorias.txt', 'w') as file:
        for key, value in categorias.items():
            file.write(f"{key}: {value}\n")

# Função para carregar as categorias do arquivo
def carregar_categorias_arquivo():
    categorias = {}
    with open('dados_categorias.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(': ')
            key = parts[0]
            value = eval(': '.join(parts[1:]))  # Reunir os valores restantes em uma string e avaliar como um dicionário
            categorias[key] = value
    return categorias


class Caso:
    def __init__(self, descricao, atributos, pesos, diagnostico):
        self.descricao = descricao
        self.atributos = np.array(atributos)
        self.pesos = np.array(pesos)
        self.diagnostico = diagnostico

def similaridade_local(caso1, caso2):
    # Verificar se os arrays têm o mesmo comprimento
    if len(caso1.atributos[:-2]) != len(caso2.atributos[:-1]):
        raise ValueError("Os arrays de atributos têm comprimentos diferentes")
    
    return np.sum(caso1.atributos[:-2] != caso2.atributos[:-1])


def similaridade_global(caso1, caso2):
    similaridades_locais = np.array([similaridade_local(caso1, caso2)])
    similaridade_ponderada = np.sum(similaridades_locais * caso1.pesos) / np.sum(caso1.pesos)
    return similaridade_ponderada

class SistemaCBR:
    def __init__(self):
        self.base_de_dados = []

    def adicionar_caso(self, caso):
        self.base_de_dados.append(caso)

    def recuperar_caso(self, novo_caso, medida_similaridade):
        similaridades = [medida_similaridade(novo_caso, caso) for caso in self.base_de_dados]
        indice_mais_similar = np.argmin(similaridades)
        return self.base_de_dados[indice_mais_similar]

# Carregar ou escrever as categorias
categorias = carregar_categorias_arquivo()

# Pesos agora têm a forma (1, n), onde n é o número de atributos
pesos_atributos = np.array([5, 2, 1, 3, 1, 1, 1]).reshape(1, -1)

caso1 = Caso("Caso 1", [1, 1, 2, 0, 1, 2], pesos_atributos, 'BALDURS GATE 3')
caso2 = Caso("Caso 2", [1, 1, 1, 0, 1, 1], pesos_atributos, 'Red Dead Redemption 2')
caso3 = Caso("Caso 3", [0, 0, 0, 0, 0, 0], pesos_atributos, 'GTA 5/VALORANT')
caso4 = Caso("Caso 4", [0, 0, 2, 0, 0, 1], pesos_atributos, 'FORTNITE')
caso5 = Caso("Caso 5", [1, 1, 1, 0, 0, 2], pesos_atributos, 'Cyberpunk 2077')
caso6 = Caso("Caso 6", [0, 0, 0, 0, 0, 0], pesos_atributos, 'VALORANT')

sistema = SistemaCBR()
sistema.adicionar_caso(caso1)
sistema.adicionar_caso(caso2)
sistema.adicionar_caso(caso3)
sistema.adicionar_caso(caso4)
sistema.adicionar_caso(caso5)
sistema.adicionar_caso(caso6)

# Interface Streamlit
st.title("SISTEMA DE SELEÇÃO DE JOGOS")
# Coleta de dados do usuário
st.header("Informe as especificações de sua máquina:")
cpu = st.selectbox("CPU", ['i3', 'i5', 'i7'])
ram = st.selectbox("RAM", ['4GB', '8GB', '16GB'])
pixel_shader = st.selectbox("PIXEL SHADER", ['3.0', '5.0', '5.1'])
os = st.selectbox("OS", ['Windows', 'Linux', 'MacOS'])
free_disk_space = st.selectbox("FREE DISK SPACE", ['Até 100 GB', 'Entre 100 e 200 GB', 'Acima de 200 GB'])
dedicated_video_ram = st.selectbox("DEDICATED VIDEO RAM", ['1 GB', '2 GB', '3 GB'])

# Criação do novo caso
novo_caso = Caso("Novo Caso", 
                 [categorias['CPU'][cpu], 
                  categorias['RAM'][ram], 
                  categorias['PIXEL SHADER'][pixel_shader], 
                  categorias['OS'][os], 
                  categorias['FREE DISK SPACE'][free_disk_space], 
                  categorias['DEDICATED VIDEO RAM'][dedicated_video_ram], 
                  0], 
                 pesos_atributos, 
                 None)

# Recuperação usando similaridade global
caso_recuperado_global = sistema.recuperar_caso(novo_caso, similaridade_global)

# Mostrar informações do caso recuperado
st.header("Resultado:")
st.write(f"Diagnóstico do Caso Recuperado: {caso_recuperado_global.diagnostico}")

if caso_recuperado_global.diagnostico in diagnostico_logomarca:
    logomarca = diagnostico_logomarca[caso_recuperado_global.diagnostico]
    st.image(logomarca, width=200)
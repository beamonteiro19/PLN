import os
import re
from collections import Counter
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import nltk


nltk.download('stopwords')


stop_words = set(stopwords.words('portuguese'))
palavroes = ['porra', 'caralho', 'merda', 'puta', 'foda', 'cuzão', 'viado', 'piranha', 'tarado', 'preto', 'fudido']  # Adicione outros conforme necessário
stop_words.update(palavroes)
stop_words.update(stopwords.words('english'))

def limpar_caracteres(texto):
    texto_limpo = re.sub(r'[^\w\s-]', '', texto)
    texto_limpo = re.sub(r'(\w)-\s', r'\1 ', texto_limpo)
    texto_limpo = re.sub(r'\d+', '', texto_limpo)
    return texto_limpo.lower()

def ler_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as file:
        texto = file.read()
    return limpar_caracteres(texto)

def extrair_tokens(texto):
    return texto.split()

def limpar_tokens(tokens):
    return [token for token in tokens if token not in stop_words and len(token) > 2]

def top_20(tokens):
    contagem = Counter(tokens)
    return contagem.most_common(20)

def gerar_grafico(dados, titulo):
    if not dados:  # Se a lista estiver vazia
        print(f"Não há dados para plotar em {titulo}.")
        return
    
    palavras, frequencias = zip(*dados)
    plt.figure(figsize=(12, 6))
    plt.bar(palavras, frequencias)
    plt.title(f'Top 20 palavras - {titulo}')
    plt.xlabel('Palavras')
    plt.ylabel('Frequência')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def processar_musicas(pasta, genero):
    print(f"\nAnalisando músicas de {genero}:")
    for arquivo in os.listdir(pasta):
        if arquivo.endswith('.txt'):
            caminho = os.path.join(pasta, arquivo)
            texto = ler_arquivo(caminho)
            tokens = extrair_tokens(texto)
            tokens_limpos = limpar_tokens(tokens)
            top20 = top_20(tokens_limpos)
            
            nome_musica = arquivo.replace('.txt', '')
            print(f"\nTop 20 palavras em {nome_musica}:")
            for palavra, freq in top20:
                print(f"{palavra}: {freq}")
            
            gerar_grafico(top20, f"{genero} - {nome_musica}")

diretorios = {
    'MPB': 'letras_mpb',
    'R&B': 'letras_rnb',
    'POP Alternativo': 'letras_pop_alternativo'
}

for genero, pasta in diretorios.items():
    if os.path.exists(pasta):
        processar_musicas(pasta, genero)
    else:
        print(f"Diretório {pasta} não encontrado para o gênero {genero}")
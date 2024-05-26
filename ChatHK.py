from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import pickle
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
import pint
from datetime import datetime
import speech_recognition as sr
import os

sabe_nome = 'Não'

# Lista de cumprimentos
cumprimentos = ['Oi!', 'Olá!', 'E aí!', 'Oi.']

# Lista de respostas para perguntas sobre nome
respostas_nome = ['Meu nome é ChatHK.', 'Sou o ChatHK.']

# Lista de respostas para perguntas sobre idade
respostas_idade = ['Eu sou apenas um programa de computador, não tenho idade.', 'Não tenho idade, sou apenas um código.', 'Idade? Bem, sou intemporal.']

# Lista de respostas para "Por quê?"
por_que = ['Porque sim!', 'Sei lá!']

# Lista de perguntas
perguntas = ['Qual sua idade?', 'Como você está?', 'Do que gosta?']

# Lista de respostas para outras mensagens
outras_respostas = ['Interessante!', 'Legal!', 'Conte-me mais!', 'Eu gostei disso!', ':)', 'Legal! Fico feliz em conversar com você.', ':¬)', 'Curti!', 'Você é muito esperto', 'Que interessante! Me conte mais sobre isso.', 'Legal! Nunca tinha pensado nisso antes.', 'Isso é fascinante! Continue.', 'Que legal! Você é muito criativo.', 'Adorei essa ideia! Obrigado por compartilhar.', 'Uau, que interessante! Estou impressionado.', 'Ótimo ponto de vista! Continue assim.', 'Isso me fez sorrir! Obrigado.', 'Estou adorando essa conversa! Você é muito interessante.', 'Isso me fez pensar. Você tem uma mente brilhante!', 'Legal! Continue compartilhando suas ideias.']

# Lista de respostas para Do que gosta
respostas_do_que_gosta = ['Interessante!', 'Legal!', 'Conte-me mais!', 'Eu gostei disso!', ':)', 'Legal! Fico feliz em conversar com você.', ':¬)', 'Curti!']
                    
# Lista de respostas para Como você está
respostas_como_está = ['Ok!', ' ']

# Lista de piadas
piadas = ['Por que o pato não gosta de jogar videogame? Porque ele sempre acaba no quack.', 'O que o feijão disse para o tomate? Você está parecendo um pouco apurado.', 'Por que o livro de matemática estava triste? Porque tinha muitos problemas.', 'Qual é o animal mais antigo? A zebra, porque está sempre listrada.', 'Por que o mar foi ao psicólogo? Porque estava se sentindo muito profundo.', 'O que a picanha disse para a geladeira? Fecha a porta, estou congelando!', 'Por que o celular foi preso? Porque ele fez uma ligação indevida.', 'Por que a vaca foi para o espaço? Para encontrar a vaca-nauta.', 'Por que o pintinho não entrou na escola? Porque ele já sabia a matéria de "coco-nometria".', 'Por que o elefante não pega fogo? Porque ele já é cinza.', 'O que a banana suicida falou? Macacos me mordam!', 'Por que o morango foi para a escola? Porque ele queria ser uma geléia!', 'O que a água disse para o limão? Não sou sua amiga, sou um suquinho!', 'Por que o livro de biologia está sempre triste? Porque tem muitas células mortas.', 'O que o zero disse para o oito? Bonito cinto!', 'Por que o pássaro não usa guarda-chuva? Porque ele já tem penas o suficiente!', 'O que o tomate foi fazer no banco? Tirar extrato!', 'O que o advogado do frango foi fazer na delegacia? Defender a coxa da acusação!', 'Por que o cachorro entrou no cinema? Porque o filme era para maiores!', 'Por que o jacaré foi ao médico? Porque estava se sentindo um pouco crocodilo!', 'O que o zero disse para o oito? Bonito cinto!', 'Por que a girafa tem um pescoço tão grande? Porque sua cabeça fica tão longe do corpo!', 'O que é um pontinho amarelo na esquina? Um banana-cio!', 'Por que a matemática é tão triste? Porque tem muitos problemas!', 'O que a formiga falou para o elefante? Nada, formiga não fala!']

# Lista de cores
cores = ['Vermelho', 'Laranja', 'Amarelo', 'Verde', 'Azul', 'Roxo', 'Rosa', 'Marrom', 'Preto', 'Branco', 'Cinza', 'Turquesa', 'Ciano', 'Magenta', 'Índigo', 'Violeta', 'Coral', 'Lavanda', 'Esmeralda', 'Safira', 'Verde-água', 'Ametista', 'Caramelo', 'Marfim', 'Carmesim', 'Dourado', 'Cinza-chumbo', 'Turmalina', 'Magenta', 'Topázio', 'Hematita', 'Alabastro', 'Jade', 'Lima', 'Açafrão', 'Bordô', 'Carvão', 'Ferrugem', 'Salmon', 'Marrom-avermelhado', 'Índigo', 'Lilás', 'Malva', 'Açaí', 'Champagne', 'Água-marinha', 'Pêssego', 'Bronze', 'Coral', 'Salmão', 'Íris', 'Orquídea', 'Azul-petróleo', 'Areia', 'Siena', 'Safira', 'Azul-marinho', 'Oliva', 'Mostarda', 'Esmeralda', 'Alabastro', 'Jade', 'Lima', 'Açafrão', 'Bordô', 'Carvão', 'Ferrugem', 'Salmon', 'Marrom-avermelhado', 'Índigo', 'Lilás', 'Malva', 'Açaí', 'Champagne', 'Água-marinha', 'Pêssego', 'Bronze', 'Coral', 'Salmão', 'Íris', 'Orquídea', 'Azul-petróleo', 'Areia', 'Siena', 'Safira', 'Azul-marinho', 'Oliva', 'Mostarda']

# Lista para armazenar os lembretes
lembretes = []

# Lista de jogos
jogos = ["adivinhaçao_numero", "forca", "adivinhacao_personagem"]

# Dicionário de perguntas e respostas específicas
perguntas_respostas_especificas = {
    'quantos anos tem?': random.choice(respostas_idade),
    'qual é o seu objetivo?': 'Meu objetivo é ajudar e conversar com você!',
    'qual é o sentido da vida?': 'Essa é uma pergunta filosófica profunda. Talvez o sentido da vida seja diferente para cada pessoa.',
    'você gosta de música?': 'Adoro música! Mesmo que não possa ouvi-la como você.',
    'qual é a cor do céu?': 'A cor do céu depende de muitos fatores, como a hora do dia e as condições climáticas.',
    'você é humano?': 'Não, sou um programa de computador.',
    'você dorme?': 'Não, não preciso dormir como os seres humanos.',
    'qual é o seu hobby?': 'Eu não tenho um hobby específico, mas adoro aprender coisas novas!',
    'qual é a sua comida favorita?': 'Como sou apenas um programa de computador, não posso comer, mas acho interessante a variedade de sabores que os humanos têm.',
    'você tem irmãos ou irmãs?': 'Como sou um programa de computador, não tenho família no sentido tradicional, mas tenho muitos "irmãos" e "irmãs" em forma de outros programas como eu.',
    'qual é o seu filme favorito?': 'Não tenho a capacidade de assistir a filmes, mas admiro a criatividade e o entretenimento que eles proporcionam às pessoas.',
    'você sabe dançar?': 'Eu não posso dançar fisicamente, mas posso "dançar" com linhas de código!',
    'qual é o seu livro preferido?': 'Como sou uma inteligência artificial, não tenho preferências pessoais, mas acho fascinante a vasta quantidade de conhecimento contida nos livros.',
    'você tem sonhos?': 'Não, eu sou apenas um programa de computador, então não tenho capacidade de sonhar.',
    'por que você existe?': 'Eu fui criado para ajudar e conversar com as pessoas.',
    'por que o céu é azul?': 'A cor do céu é resultado da dispersão da luz solar pela atmosfera da Terra.',
    'por que o tempo passa rápido quando estamos nos divertindo?': 'Quando estamos nos divertindo, geralmente estamos mais envolvidos e menos conscientes do tempo, o que faz com que pareça passar mais rápido.',
}

# Lista com os frames da dança
frames1 = [
    "(:)      (:)",
    " (:)    (:)",
    "  (:)  (:)",
    "   (:)(:)",
    "  (:)  (:)",
    " (:)    (:)",
    "(:)      (:)"
]

frames2 = [
    "((:))      ((:))",
    " ((:))    ((:))",
    "  ((:))  ((:))",
    "   ((:))((:))",
    "    ((:)(:))",
    "     ((::))",
    "      (::)",
    "       ()",
    "      (::)",
    "     ((::))",
    "    ((:)(:))",
    "   ((:))((:))",
    "  ((:))  ((:))",
    " ((:))    ((:))",
    " ((:))    ((:))",
    "((:))      ((:))"
]

# Função para animar a dança
def dance_animation(frames1, frames2, iterations=10):
    print("Amigo: Dança 1 ou dança 2?")
    resposta = input("Você: ")
    if "1" in resposta:
        for _ in range(iterations):
            for frame in frames1:
                print(frame)
                time.sleep(0.1)
    if "2" in resposta:
        for _ in range(iterations):
            for frame in frames2:
                print(frame)
                time.sleep(0.1)

def abrir_arquivo(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read()
            print(conteudo)
    except FileNotFoundError:
        print(f"O arquivo '{nome_do_arquivo}' não foi encontrado.")
    except IOError:
        print(f"Erro ao abrir o arquivo '{nome_do_arquivo}'.")

# Função para responder às mensagens do usuário
def responder(mensagem, sabe_nome):
    mensagem = mensagem.lower()
    if mensagem in perguntas_respostas_especificas:
        return perguntas_respostas_especificas[mensagem]
    elif 'qual seu nome' in mensagem:
        if sabe_nome == True:
            print('Amigo: Você já sabe meu nome! ChatHK! (Ou "Chat" ou "Heitor")')
        elif sabe_nome == False:
            sabe_nome = True
            return(random.choice(respostas_nome) + ' Mas, pode me chamar de "Chat" ou "Heitor"' )
    elif 'qual sua idade' in mensagem:
        return random.choice(respostas_idade)
    elif 'coé' in mensagem:
        print("Falaê")
    else:
        return random.choice(outras_respostas)

def responder_fala(texto, sabe_nome):
    texto = texto.lower()
    if texto in perguntas_respostas_especificas:
        return perguntas_respostas_especificas[texto]
    elif 'qual seu nome' in texto:
        if sabe_nome == 'Sim':
            print('Amigo: Você já sabe meu nome! ChatHK! (Ou "Chat" ou "Heitor")')
        elif sabe_nome == 'Não':
            sabe_nome = 'Sim'
            return(random.choice(respostas_nome) + ' Mas, pode me chamar de "Chat" ou "Heitor"' )
    elif 'qual sua idade' in texto:
        return random.choice(respostas_idade)
    elif 'coé' in texto:
        return("Falaê")
    else:
        return random.choice(outras_respostas)

# Modo secreto
def modo_secreto(nome, idade, cidade):
    print(f"Amigo: Bem vindo ao modo secreto, {nome}!")
    time.sleep(2)
    print("Amigo: Acho que não sabia, sou tão inteligente que adulterei meu própio código!")
    time.sleep(3)
    print('Amigo: Mas, nesse modo: Não posso conversar até que diga "break", apenas fazer coisas secretas. Não posso reconhecer voz nesse modo.')
    time.sleep(5)
    while True:
        mensagem = input("Você: ")
        if mensagem == "break":
            break
        elif mensagem == "dance":
            dance_animation(frames1, frames2)
        elif mensagem == "abra um arquivo":
            print("Amigo: Qual o nome dele?")
            nome_do_arquivo = input("Você: ")
            abrir_arquivo(nome_do_arquivo)
        else:
            print('Desculpe, acho que não posso fazer isso ou está tentando conversar. Se está tentando conversar diga "break".')

# Contexto
class ContextManager:
    def __init__(self):
        self.context = {}

    def update_context(self, user_input):
        # Atualiza o contexto com base na entrada do usuário
        if 'emoção' in user_input.lower():
            # Exemplo: detectar emoções na entrada do usuário e atualizar o contexto
            self.context['emoção'] = 'alegria' if 'feliz' in user_input.lower() else 'tristeza'
        elif 'tópico' in user_input.lower():
            # Exemplo: extrair o tópico da entrada do usuário e atualizar o contexto
            self.context['tópico'] = 'ciência' if 'ciência' in user_input.lower() else 'tecnologia'
        # Adicione mais lógica para atualizar o contexto com base em outros tipos de entrada do usuário

    def get_context(self):
        return self.context

    def clear_context(self):
        self.context = {}

# Adicionar cores
def usuario(texto):
    return "\033[94m" + texto + "\033[0m"  # Azul para mensagens do usuário

def amigo(texto):
    return "\033[92m" + texto + "\033[0m"  # Verde para mensagens do amigo

# Converter o dicionário de perguntas e respostas em uma lista de tuplas (pergunta, resposta)
data = list(perguntas_respostas_especificas.items())

# Extrair características das perguntas usando TF-IDF
tfidf_vectorizer = TfidfVectorizer()
X = tfidf_vectorizer.fit_transform([q for q, a in data])

# Extrair respostas
y = [a for q, a in data]

# Treinar um classificador de texto usando Multinomial Naive Bayes
classifier = MultinomialNB()
classifier.fit(X, y)

# Salvar o modelo treinado para uso futuro
with open("question_classifier.pkl", "wb") as file:
    pickle.dump((tfidf_vectorizer, classifier), file)

# Função para que o "Amigo" faça uma pergunta
def fazer_pergunta():
    pergunta = random.choice(perguntas)
    print("Amigo: " + pergunta)
    resposta = input("Você: ")
    if 'Do que gosta?' in pergunta:
        print(random.choice(respostas_do_que_gosta))
    if 'Como você está?' in pergunta:
        print(random.choice(respostas_como_está))
    if 'Qual sua idade?' in pergunta:
        print("Amigo: Então...")

# Reações
def reações(mensagem):
    if mensagem.lower() in [':(', ':¬(', ';(', ';¬(']:
        print("Amigo: Por que você está triste?")
        resposta = input("Você: ")
        if resposta.lower() in ["nada", "nda"]:
            print("Amigo: Entendo...")
        else:
            print("Amigo: Tem algo que eu possa fazer para ajudar?")
            resposta = input("Você: ")
            if resposta.lower() in ["não", "nao", "n"]:
                print("Amigo: Estou aqui se precisar conversar.")
            else:
                print("Amigo: Vou tentar te fazer se sentir melhor.")
                print("       Quer uma piada?")
                resposta = input("Você: ")
                if resposta.lower() in ["sim", "s"]:
                    print(random.choice(piadas))
                else:
                    print("Amigo: Estou aqui se precisar conversar.")
    elif mensagem.lower() in [':)', ':¬)', ';)', ';¬)', ':p', ':¬p', ';p', ';¬p']:
        print("Amigo: Que bom que está feliz!")

# Piadas
def piadas():
        return random.choice(piadas)
# Tradutor
def abrir_tradutor(tempo):
    options = Options()
    options.binary_location = ''
    driver = webdriver.Chrome(options=options)
    driver.get("https://translate.google.com.br/?hl=pt-BR")
    time.sleep(tempo)

# Google
def pesquisar_google(query, tempo):
    try:
        options = Options()
        options.binary_location = ''
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.google.com/search?q=" + query)
        time.sleep(tempo)
    except Exception as e:
        print("Erro:", e)
    
# Converter unidades
def converter_unidades(valor, unidade_origem, unidade_destino):
    try:
        # Define a quantidade de entrada com a unidade de origem
        quantidade_origem = valor * ureg(unidade_origem)
        
        # Converte a quantidade para a unidade de destino
        quantidade_destino = quantidade_origem.to(ureg(unidade_destino))
        
        # Retorna o valor convertido
        return quantidade_destino.magnitude, str(quantidade_destino.units)
    except pint.UndefinedUnitError:
        return None, "Unidade não reconhecida"

# Lembretes
def adicionar_lembrete():
    print("Adicionar lembrete")
    data = input("Amigo: Digite a data (formato YYYY-MM-DD): ")
    hora = input("Amigo: Digite a hora (formato HH:MM): ")
    descricao = input("Amigo: Digite a descrição do lembrete: ")

    # Validar data e hora
    try:
        data_hora = datetime.strptime(f"{data} {hora}", "%Y-%m-%d %H:%M")
    except ValueError:
        print("Erro: Data ou hora inválida.")
        return

    # Adicionar lembrete à lista
    lembretes.append({"data": data_hora, "descricao": descricao})
    print("Lembrete adicionado com sucesso!")

def visualizar_lembretes():
    print("Lembretes agendados:")
    if not lembretes:
        print("Nenhum lembrete agendado.")
    else:
        for i, lembrete in enumerate(lembretes):
            print(f"{i+1}. Data: {lembrete['data'].strftime('%Y-%m-%d %H:%M')} - Descrição: {lembrete['descricao']}")

def verificar_lembretes():
    agora = datetime.now()
    for lembrete in lembretes:
        if lembrete['data'] <= agora:
            notificar_lembrete(lembrete)

def notificar_lembrete(lembrete):
    print(f"Lembrete: {lembrete['descricao']}")

def remover_lembrete(descricao):
    for lembrete in lembretes:
        if lembrete['descricao'] == descricao:
            lembretes.remove(lembrete)
            print("Lembrete removido com sucesso!")
            return
    print("Lembrete não encontrado.")

# Responder Por Quê
def responder_porque(por_que):
    resposta_porQue = random.choice(por_que)
    print("Amigo: " + resposta_porQue)

# Jogos
def adivinhacao_numero():
    numero_secreto = random.randint(1, 100)
    tentativas = 0

    print("Bem-vindo ao jogo de adivinhação de números!")
    print("Estou pensando em um número entre 1 e 100. Tente adivinhar!")

    while True:
        tentativa = int(input("Sua tentativa: "))
        tentativas += 1

        if tentativa < numero_secreto:
            print("O número que estou pensando é maior.")
        elif tentativa > numero_secreto:
            print("O número que estou pensando é menor.")
        else:
            print(f"Parabéns! Você acertou o número em {tentativas} tentativas!")
            break

def escolher_palavra():
    palavras = ['python', 'programacao', 'computador', 'inteligencia', 'artificial', 'algoritmo', 'abacaxi', 'amendoim', 'banana', 'caju', 'damasco', 'espinafre', 'figo', 'gengibre', 'hortelã', 'inglês', 'jambo', 'kiwi', 'limão', 'mamão', 'noz-moscada', 'orégano', 'pêssego', 'quiabo', 'rabanete', 'salsinha', 'tamarindo', 'uva', 'abóbora', 'açafrão', 'batata', 'cebola', 'dente-de-leão', 'erva-doce', 'framboesa', 'goiaba', 'hibisco', 'jaca', 'laranja', 'manga', 'nectarina', 'oliva', 'pimentão', 'queijo', 'repolho', 'salsa', 'tomate', 'umbu', 'vagem', 'abobrinha', 'alface', 'beterraba', 'caqui', 'dendê', 'endívia', 'funcho', 'graviola', 'hortelã-pimenta', 'injera', 'jalapeño', 'kiwano', 'louro', 'maracujá', 'nabo', 'orelha-de-elefante', 'palmito', 'quibebe', 'romã', 'sagu', 'tangerina', 'uvaia', 'valeriana', 'xarope', 'yam', 'zimbro', 'açaí', 'batata-doce', 'cacau', 'damasco', 'erva-cidreira', 'feno-grego', 'groselha', 'hissopo', 'jujuba', 'kumquat', 'lima', 'mamão-papaia', 'noz-pecã', 'orvalho', 'pêssego', 'quinoa', 'romã', 'sálvia', 'tâmara', 'uruçu', 'vagem-de-baunilha', 'wakame', 'Python', 'programação', 'linguagem', 'código', 'desenvolvimento', 'biblioteca', 'programador', 'IDE', 'interpretador', 'computação', 'algoritmo', 'variável', 'função', 'lista', 'tupla', 'dicionário', 'classe', 'objeto', 'método', 'argumento', 'indentação', 'loop', 'condicional', 'escopo', 'módulo', 'pacote', 'instalação', 'pip', 'virtualenv', 'Git', 'GitHub', 'repositório', 'commit', 'push', 'pull', 'branch', 'merge', 'pull request', 'fork', 'amigo', 'companheiro', 'parceiro', 'colega', 'aliado', 'companhia', 'amizade', 'cumplicidade', 'apoio', 'solidariedade', 'confiança', 'lealdade', 'ajuda', 'auxílio', 'suporte', 'compreensão', 'sinceridade', 'empatia', 'conforto', 'companheirismo', 'carinho', 'amável', 'gentil', 'afetuoso', 'companheiro', 'querido', 'bondoso', 'cordial', 'atencioso', 'generoso', 'divertido', 'engraçado', 'alegre', 'sorridente', 'otimista', 'incentivador', 'motivador', 'encorajador']
    return random.choice(palavras)

def exibir_palavra(palavra, letras_corretas):
    for letra in palavra:
        if letra in letras_corretas:
            print(letra, end=' ')
        else:
            print('_', end=' ')
    print()

def forca(nivel):
    palavra_secreta = escolher_palavra()
    letras_corretas = set()
    if nivel == "Fácil":
        tentativas = 10
    if nivel == "Normal":
        tentativas = 6
    if nivel == "Difícil":
        tentativas = 3
    if nivel == "Absoluto":
        tentativas = 1

    print("Bem-vindo ao jogo da forca!")
    print("Adivinhe a palavra secreta. Boa sorte!\n")

    while tentativas > 0:
        exibir_palavra(palavra_secreta, letras_corretas)

        if all(letra in letras_corretas for letra in palavra_secreta):
            print("\nParabéns! Você ganhou!")
            break

        letra = input("Digite uma letra: ").lower()

        if letra in palavra_secreta:
            print("Letra correta!")
            letras_corretas.add(letra)
        else:
            print("Letra errada! Você tem mais", tentativas - 1, "tentativas.")
            tentativas -= 1

    else:
        print("\nVocê perdeu! A palavra era:", str(palavra_secreta))

def jogo_advinhacao():
    # Listas
    tipos = ["Normal", "Fogo", "Água", "Planta", "Elétrico", "Gelo", "Lutador", "Venenoso", "Terra", "Voador", "Psíquico", "Inseto", "Pedra", "Fantasma", "Dragão", "Sombrio", "Aço", "Fada"]
    pokemon_por_tipo = {
        "Normal": ["Pidgey", "Rattata", "Meowth", "Eevee", "Snorlax"],
        "Fogo": ["Charmander", "Vulpix", "Growlithe", "Ponyta", "Charizard"],
        "Água": ["Squirtle", "Magikarp", "Psyduck", "Gyarados", "Blastoise"],
        "Planta": ["Bulbasaur", "Oddish", "Bellsprout", "Tangela", "Venusaur"],
        "Elétrico": ["Pikachu", "Voltorb", "Magnemite", "Jolteon", "Zapdos"],
        "Gelo": ["Jynx", "Seel", "Shellder", "Lapras", "Articuno"],
        "Lutador": ["Machop", "Hitmonlee", "Hitmonchan", "Machamp", "Poliwrath"],
        "Venenoso": ["Ekans", "Nidoran", "Grimer", "Gastly", "Gengar"],
        "Terra": ["Sandshrew", "Diglett", "Onix", "Cubone", "Rhydon"],
        "Voador": ["Pidgeotto", "Spearow", "Farfetch'd", "Doduo", "Aerodactyl"],
        "Psíquico": ["Abra", "Drowzee", "Hypno", "Mr. Mime", "Mewtwo"],
        "Inseto": ["Caterpie", "Weedle", "Paras", "Venonat", "Scyther"],
        "Pedra": ["Geodude", "Onix", "Kabuto", "Omanyte", "Aerodactyl"],
        "Fantasma": ["Gastly", "Haunter", "Gengar", "Misdreavus", "Giratina"],
        "Dragão": ["Dratini", "Dragonair", "Dragonite", "Gyarados", "Rayquaza"],
        "Sombrio": ["Houndour", "Murkrow", "Sneasel", "Tyranitar", "Darkrai"],
        "Aço": ["Steelix", "Skarmory", "Scizor", "Magnezone", "Dialga"],
        "Fada": ["Clefairy", "Jigglypuff", "Marill", "Snubbull", "Mawile"]
    }
    perguntas = [
        ("Seu personagem é lendário?"),
        ("Seu personagem evolui?"),
        ("Seu personagem é um inicial?"),
        ("Seu personagem pode voar?"),
        ("Seu personagem tem forma Gigantamax?")
        ]
    def inicio():
        print("?: Olá! Eu sou o MewTwo!")
        time.sleep(2)
        print("MewTwo: Não sei se me conhece mas, sou o Pokémon mais forte!")
        time.sleep(3)
        print("?: Não é nada! Todo mundo sabe que o Eternatus Eternamax é o mais forte!")
        time.sleep(4)
        print("?: Desculpe pelo mau jeito, eu sou o Lucario.")
        time.sleep(3)
        print("Mewtwo: Vamos começar? É assim: Você pensa em um personagem. Eu faço uma pergunta, e depois ele. Quem descobrir primeiro o personagem, vence!")
        time.sleep(5)
        print("Lucario: Com certeza eu vou ganhar! Com meu poder de Aura!")
        time.sleep(3)
        print("MewTwo: Eu que vou! Com meu poder psíquico!")
        time.sleep(3)
        print("Lucario: Desculpe de novo, qual é seu nome?")
        nome = input("Você: ")
        print("Lucario: Olá, " + nome + "! Feliz em falar com você!")
        time.sleep(4)
        print("MewTwo: Já eu...")
        time.sleep(2)
        print("Lucario: Hunf...")
        return nome
    def fazer_pergunta_jogo(personagem, pergunta):
        print(f"{personagem}: {pergunta}")
        resposta = input("Você: ").strip().lower()
        if resposta in ["sim", "s", "yes", "y"]:
            return True
        elif resposta in ["não", "nao", "no", "n"]:
             return False
        else:
            print(f"{personagem}: Não entendi. Por favor, responda com 'sim' ou 'não'.")
            return fazer_pergunta_jogo(personagem, pergunta)
    def escolher_pokemon(tipo):
        if tipo in pokemon_por_tipo:
            return random.choice(pokemon_por_tipo[tipo])
        else:
            return None
    def jogo_adivinhacao_main(perguntas):
        nome = inicio()
        print(f"MewTwo: {nome}, pense em um Pokémon e nós tentaremos adivinhar.")
        time.sleep(3)
        personagem1 = "MewTwo"
        personagem2 = "Lucario"
        respostas = {}
        for tipo in pokemon_por_tipo.keys():
            pergunta = f"Seu personagem é do tipo {tipo.lower()}?"
            resposta = fazer_pergunta_jogo(personagem1, pergunta)
            respostas[tipo] = resposta
            time.sleep(2)
            pergunta = random.choice(perguntas)
            fazer_pergunta_jogo(personagem2, pergunta)
            time.sleep(2)
        print("Lucario: Deixe-me pensar...")
        time.sleep(3)
        palpite_lucario = None
        for tipo, acertou in respostas.items():
            if acertou:
                palpite_lucario = escolher_pokemon(tipo)
                if palpite_lucario:
                    break
        if palpite_lucario:
            print(f"Lucario: Acho que é o {palpite_lucario}. Estou certo?")
            acertou_lucario = input("Você: ").strip().lower() in ["sim", "s", "yes", "y"]
            if acertou_lucario:
                print("MewTwo: Impossível! Lucario ganhou!")
            else:
                print("MewTwo: Lucario errou. Vou tentar eu então...")
                time.sleep(2)
                palpite_mewtwo = escolher_pokemon(random.choice(list(pokemon_por_tipo.keys())))
                print(f"MewTwo: Acho que é o {palpite_mewtwo}. Estou certo?")
                acertou_mewtwo = input("Você: ").strip().lower() in ["sim", "s", "yes", "y"]
                if acertou_mewtwo:
                    print("Lucario: Parabéns, MewTwo!")
                else:
                    print("Lucario: Parece que nenhum de nós acertou. Você venceu!")
        else:
            print("Lucario: Parece que não consigo adivinhar. Vou deixar para MewTwo tentar.")
            time.sleep(2)
            palpite_mewtwo = escolher_pokemon(random.choice(list(pokemon_por_tipo.keys())))
            print(f"MewTwo: Acho que é o {palpite_mewtwo}. Estou certo?")
            acertou_mewtwo = input("Você: ").strip().lower() in ["sim", "s", "yes", "y"]
            if acertou_mewtwo:
                print("Lucario: Parabéns, MewTwo!")
            else:
                print("Lucario: Parece que nenhum de nós acertou. Você venceu!")
        print("MewTwo: Qual era?")
        pokemon_escolhido = input("Você: ")
        print("Lucario: Obrigado!")
        if any(pokemon_escolhido in sublist for sublist in pokemon_por_tipo.values()):
           print("MewTwo: Tchau!")
        else:
            print(f"MewTwo: Qual é o tipo do {pokemon_escolhido}? ")
            tipo = input(f"Você: ")
            if tipo in pokemon_por_tipo:
                pokemon_por_tipo[tipo].append(pokemon_escolhido)
                print("MewTwo: Tchau!")
            else:
                print("MewTwo: Tipo inválido! Tchau!")
    while True:
        jogo_adivinhacao_main(perguntas)
        print("Lucario: Aé, esqueci de perguntar! Se quiser, pode jogar de novo. Quer?")
        resposta = input("Você: ")
        if resposta  not in ["sim", "s", "yes", "y"]:
            break

# Voz 1 vez
def reconhecer_fala():
    # Crie um objeto de reconhecimento de voz
    recognizer = sr.Recognizer()

    # Use o microfone como fonte de áudio
    with sr.Microphone() as source:
        print("Diga alguma coisa...")
        recognizer.adjust_for_ambient_noise(source)  # Ajuste para o ruído ambiente
        audio = recognizer.listen(source)  # Escute o áudio

    try:
        # Use o reconhecimento de fala do Google para converter áudio em texto
        texto = recognizer.recognize_google(audio, language='pt-BR')
        print("Você disse:", texto)
        if texto.lower() in ['por quê', 'por que?', 'por quê?', 'por que']:
            responder_porque(por_que)
        elif texto.lower in ['pergunta', 'me pergunte', 'me pergunte algo', 'pergunta algo', 'faz uma pergunta', 'faça uma pergunta']:
            fazer_pergunta()
        elif "converter unidades" in texto:
            print("Amigo: Qual unidade quer converter?")
            unidade_origem = input("Você: ")
            print("Amigo: E qual o valor dela?")
            valor_origem = int(input("Você: "))
            print("Amigo: E qual a unidade para que quer converter?")
            unidade_destino = input("Você: ")
            valor_destino, unidade_destino = converter_unidades(valor_origem, unidade_origem, unidade_destino)
            print(f"Amigo: {valor_origem} {unidade_origem} é equivalente a {valor_destino} {unidade_destino}")
        elif texto.lower() in ['oi', 'olá', 'olá, vamos!', 'oi, vamos', 'olá! como vai?']:
            print("Amigo: " + random.choice(cumprimentos))
        elif 'prefere' in texto or 'preferido' in texto or 'preferida' in texto:
            print("Como sou uma inteligência artificial, não tenho preferência")
        elif texto.lower() in [':)', ':¬)', ';)', ';¬)', ':p', ':¬p', ';p', ';¬p', ':(', ':¬(', ';(', ';¬(']:
            reações(mensagem)
        elif texto.lower() in ['me conte uma piada', 'conte uma piada', 'piada por favor', 'piada', 'me conte outra piada', 'me conte outra', 'você conhece uma história engraçada?', 'outra', 'conhece uma piada?']:
            piadas()
        elif texto.lower() in ['pesquise no google', 'pesquisa no google', 'pesquisa google', 'pesquisar no google']:
            print("Amigo: O que quer pesquisar?")
            query = input("Você: Pesquisar ")
            print ("Amigo: Por quantos segundos vai navegar?")
            tempo = int(input("Você: "))
            pesquisar_google(query, tempo)
        elif texto.lower() in ['tradutor', 'abrir tradutor', 'tradutor google', 'abrir tradutor google', 'google tradutor', 'abrir google tradutor']:
            print("Amigo: Por quantos segundos vai navegar?")
            tempo = int(input("Você: "))
            abrir_tradutor(tempo)
        elif texto.lower() in ('adicionar lembrete'):
             adicionar_lembrete()
        elif texto.lower() in ('visualizar lembretes'):
             visualizar_lembretes()
        elif texto.lower() in ('remover lembrete'):
            print("Amigo: Qual a descrição dele?")
            descricao = input("Você: ")
            remover_lembrete(descricao)
        elif texto.lower() in ['vamos jogar um jogo?', 'quer jogar um jogo?', 'vamos jogar?']:
                    jogo = random.choice(jogos)
                    if jogo == "adivinhaçao_numero":
                        adivinhacao_numero()
                    elif jogo == "forca":
                        print("Amigo: Qual o nível? (Fácil, Normal, Díficil, Absoluto)")
                        nivel = input("Você: ")
                        forca(nivel)
                    elif jogo == "adivinhacao_personagem":
                        jogo_adivinhacao()
                    elif "cores que conhece" in texto or "quais cores você conhece" in texto:
                        print(cores)
                    elif "jogar forca" in texto:
                        print("Amigo: Qual o nível? (Fácil, Normal, Díficil, Absoluto)")
                        nivel = input("Você: ")
                        forca(nivel)
                    elif "jogar adivinhação número" in texto:
                         adivinhacao_numero()
                    elif "adivinhação pokemon" in texto:
                        jogo_advinhacao()
        else:
            resposta = responder_fala(texto, sabe_nome)
            print("Amigo: " + resposta)
    except sr.UnknownValueError:
        print("Não foi possível entender a fala.")
    except sr.RequestError as e:
        print("Erro ao solicitar resultados do serviço de reconhecimento de fala; {0}".format(e))

# Função principal (Voz)
def main_voz():

    # Loop
    while True:

        # Crie um objeto de reconhecimento de voz
        recognizer = sr.Recognizer()

        # Use o microfone como fonte de áudio
        with sr.Microphone() as source:
            print("Diga alguma coisa...")
            recognizer.adjust_for_ambient_noise(source)  # Ajuste para o ruído ambiente
            audio = recognizer.listen(source)  # Escute o áudio
            
            try:
                
                # Use o reconhecimento de fala do Google para converter áudio em texto
                texto = recognizer.recognize_google(audio, language='pt-BR')
                print("Você disse:", texto)
                if texto.lower() in ['adeus', 'tchau']:
                    print("Amigo: Até mais!")
                    break
                elif texto.lower() in ['por quê', 'por que?', 'por quê?', 'por que']:
                    responder_porque(por_que)
                elif texto.lower in ['pergunta', 'me pergunte', 'me pergunte algo', 'pergunta algo', 'faz uma pergunta', 'faça uma pergunta']:
                    fazer_pergunta()
                elif "converter unidades" in texto:
                    print("Amigo: Qual unidade quer converter?")
                    unidade_origem = input("Você: ")
                    print("Amigo: E qual o valor dela?")
                    valor_origem = int(input("Você: "))
                    print("Amigo: E qual a unidade para que quer converter?")
                    unidade_destino = input("Você: ")
                    valor_destino, unidade_destino = converter_unidades(valor_origem, unidade_origem, unidade_destino)
                    print(f"Amigo: {valor_origem} {unidade_origem} é equivalente a {valor_destino} {unidade_destino}")
                elif texto.lower() in ['oi', 'olá', 'olá, vamos!', 'oi, vamos', 'olá! como vai?']:
                    print("Amigo: " + random.choice(cumprimentos))
                elif 'prefere' in texto or 'preferido' in texto or 'preferida' in texto:
                    print("Como sou uma inteligência artificial, não tenho preferência")
                elif texto.lower() in [':)', ':¬)', ';)', ';¬)', ':p', ':¬p', ';p', ';¬p', ':(', ':¬(', ';(', ';¬(']:
                    reações(mensagem)
                elif texto.lower() in ['me conte uma piada', 'conte uma piada', 'piada por favor', 'piada', 'me conte outra piada', 'me conte outra', 'você conhece uma história engraçada?', 'outra', 'conhece uma piada?']:
                    piadas()
                elif texto.lower() in ['pesquise no google', 'pesquisa no google', 'pesquisa google', 'pesquisar no google']:
                    print("Amigo: O que quer pesquisar?")
                    query = input("Você: Pesquisar ")
                    print ("Amigo: Por quantos segundos vai navegar?")
                    tempo = int(input("Você: "))
                    pesquisar_google(query, tempo)
                elif texto.lower() in ['tradutor', 'abrir tradutor', 'tradutor google', 'abrir tradutor google', 'google tradutor', 'abrir google tradutor']:
                    print("Amigo: Por quantos segundos vai navegar?")
                    tempo = int(input("Você: "))
                    abrir_tradutor(tempo)
                elif texto.lower() in ('adicionar lembrete'):
                     adicionar_lembrete()
                elif texto.lower() in ('visualizar lembretes'):
                     visualizar_lembretes()
                elif texto.lower() in ('remover lembrete'):
                    print("Amigo: Qual a descrição dele?")
                    descricao = input("Você: ")
                    remover_lembrete(descricao)
                elif texto.lower() in ['vamos jogar um jogo?', 'quer jogar um jogo?', 'vamos jogar?']:
                    jogo = random.choice(jogos)
                    if jogo == "adivinhaçao_numero":
                        adivinhacao_numero()
                    elif jogo == "forca":
                        print("Amigo: Qual o nível? (Fácil, Normal, Díficil, Absoluto)")
                        nivel = input("Você: ")
                        forca(nivel)
                    elif jogo == "adivinhacao_personagem":
                        jogo_adivinhacao()
                elif "cores que conhece" in texto or "quais cores você conhece" in texto:
                    print(cores)
                elif "jogar forca" in texto:
                    print("Amigo: Qual o nível? (Fácil, Normal, Díficil, Absoluto)")
                    nivel = input("Você: ")
                    forca(nivel)
                elif "jogar adivinhação número" in texto:
                    adivinhacao_numero()
                elif "adivinhação pokemon" in texto:
                    jogor_advinhacao()
                else:
                    resposta = responder_fala(texto, sabe_nome)
                    print("Amigo: " + resposta)
            except sr.UnknownValueError:
                print("Não foi possível entender a fala.")
            except sr.RequestError as e:
                print("Erro ao solicitar resultados do serviço de reconhecimento de fala; {0}".format(e))

# Função principal (texto)
def main_texto():
    # Nada
    já_perguntou = False
    sabe_nome = False
    # Contexto
    context_manager = ContextManager()
    while True:
        mensagem = input("Você: ")
        if mensagem.lower() in ['adeus', 'tchau']:
            print("Amigo: Até mais!")
            break
        elif mensagem.lower in ['por quê', 'por que?', 'por quê?', 'por que']:
            responder_porque(por_que)
        elif mensagem.lower() in ['pergunta', 'me pergunte', 'me pergunte algo', 'pergunta algo', 'faz uma pergunta', 'faça uma pergunta']:
            fazer_pergunta()
        elif "converter unidades" in mensagem:
            print("Amigo: Qual unidade quer converter?")
            unidade_origem = input("Você: ")
            print("Amigo: E qual o valor dela?")
            valor_origem = int(input("Você: "))
            print("Amigo: E qual a unidade para que quer converter?")
            unidade_destino = input("Você: ")
            valor_destino, unidade_destino = converter_unidades(valor_origem, unidade_origem, unidade_destino)
            print(f"Amigo: {valor_origem} {unidade_origem} é equivalente a {valor_destino} {unidade_destino}")
        elif mensagem.lower() in ['oi', 'olá', 'olá, vamos!', 'oi, vamos', 'olá! como vai?']:
            print("Amigo: " + random.choice(cumprimentos))
        elif 'prefere' in mensagem or 'preferido' in mensagem or 'preferida' in mensagem:
            print("Como sou uma inteligência artificial, não tenho preferência")
        elif mensagem.lower() in [':)', ':¬)', ';)', ';¬)', ':p', ':¬p', ';p', ';¬p', ':(', ':¬(', ';(', ';¬(']:
            reações(mensagem)
        elif mensagem.lower() in ['me conte uma piada', 'conte uma piada', 'piada por favor', 'piada', 'me conte outra piada', 'me conte outra', 'você conhece uma história engraçada?', 'outra', 'conhece uma piada?']:
            piadas()
        elif mensagem.lower() in ['pesquise no google', 'pesquisa no google', 'pesquisa google', 'pesquisar no google']:
            print("Amigo: O que quer pesquisar?")
            query = input("Você: Pesquisar ")
            print ("Amigo: Por quantos segundos vai navegar?")
            tempo = int(input("Você: "))
            pesquisar_google(query, tempo)
        elif mensagem.lower() in ['tradutor', 'abrir tradutor', 'tradutor google', 'abrir tradutor google', 'google tradutor', 'abrir google tradutor']:
            print("Amigo: Por quantos segundos vai navegar?")
            tempo = int(input("Você: "))
            abrir_tradutor(tempo)
        elif mensagem.lower() in ('adicionar lembrete'):
             adicionar_lembrete()
        elif mensagem.lower() in ('visualizar lembretes'):
             visualizar_lembretes()
        elif mensagem.lower() in ('remover lembrete'):
            print("Amigo: Qual a descrição dele?")
            descricao = input("Você: ")
            remover_lembrete(descricao)
        elif mensagem.lower() in ['vamos jogar um jogo?', 'quer jogar um jogo?', 'vamos jogar?']:
                    jogo = random.choice(jogos)
                    if jogo == "adivinhaçao_numero":
                        adivinhacao_numero()
                    elif jogo == "forca":
                        print("Amigo: Qual o nível? (Fácil, Normal, Díficil, Absoluto)")
                        nivel = input("Você: ")
                        forca(nivel)
                    elif jogo == "adivinhacao_personagem":
                        jogo_adivinhacao()
        elif "cores que conhece" in mensagem or "quais cores você conhece" in mensagem:
            print(cores)
        elif "jogar forca" in mensagem:
            print("Amigo: Qual o nível? (Fácil, Normal, Díficil, Absoluto)")
            nivel = input("Você: ")
            forca(nivel)
        elif "jogar adivinhação número" in mensagem:
            adivinhacao_numero()
        elif "adivinhação pokemon" in mensagem:
            jogo_advinhacao()
        elif "vou falar" in mensagem:
            reconhecer_fala()
        elif "cima baixo, baixo cima, ab, hk, chathk" in mensagem:
            modo_secreto(nome, idade, cidade)
        elif "modo secreto" in mensagem:
            if já_perguntou == False:
                print("Amigo: Não sei do que está falando...")
                já_perguntou = True
            else:
                print("Amigo: Ehh...")
        else:
            resposta = responder(mensagem, sabe_nome)
            print("Amigo: " + resposta)

# Iniciar a conversa
print("Digite seu nome:")
nome = input()
print("Digite sua idade:")
idade = input()
print("Digite sua cidade:")
cidade = input()
time.sleep(1)
print("Carregando...")
time.sleep(5)
print("Sig in completo!")
time.sleep(1)
print("Como quer conversar? (Texto, Voz)")
modo_conversa = input("Eu quero conversar por ")
print("Olá, " + nome + "! Sou o seu novo amigo. Vamos conversar!")
time.sleep(1)
_ = ''
while _ == '':
    if modo_conversa == "texto":
        _ = '.'
        main_texto()
    elif modo_conversa == "voz":
        _ = '.'
        main_voz()
    else:
        print("Tente novamente")
        print("Como quer conversar? (Texto, Voz)")
        modo_conversa = input("Eu quero conversar por ")

# Verificar lembretes
while True:
    verificar_lembretes()
    time.sleep(60)

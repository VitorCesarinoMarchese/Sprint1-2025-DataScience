import pandas as pd
import numpy as np
from faker import Faker
import random

# Inicializa o gerador de dados fictícios
fake = Faker()

# Parâmetros da simulação
num_registros = 100  # Quantidade inicial de registros a serem gerados
unidades = ['Morumbi', 'Santo Amaro', 'Moema']  # Unidades hospitalares
materiais = ['Seringa', 'Gaze', 'Tubo', 'Medicamentos', 'Esparadrapo']  # Tipos de materiais
tipos = ['entrada', 'saida']  # Tipos de movimentação de estoque

# Função para gerar um DataFrame com dados simulados
def gerar_dados_simulados(n):
    dados = []
    for _ in range(n):
        unidade = random.choice(unidades)
        material = random.choice(materiais)
        tipo = random.choices(['entrada', 'saida'], weights=[0.05, 0.95])[0]  # 5% entradas, 95% saídas
        data = fake.date_between(start_date='-6M', end_date='today')
        responsavel = fake.first_name()

        # Entradas têm quantidade positiva; saídas, negativa
        if tipo == 'entrada':
            quantidade = np.random.randint(1, 500)
        else:
            quantidade = -np.random.randint(1, 20)

        dados.append({
            'data': data,
            'unidade': unidade,
            'material': material,
            'tipo': tipo,
            'quantidade': quantidade,
            'responsavel': responsavel
        })
    return pd.DataFrame(dados)

# Gera os dados simulados
df = gerar_dados_simulados(num_registros)

# 1. Introduz valores ausentes (simula falhas no preenchimento de dados)
for col in ['quantidade', 'responsavel']:
    df.loc[df.sample(frac=0.01).index, col] = None  # 1% dos registros com valores ausentes

# 2. Inverte o sinal da quantidade incorretamente (simula erro de digitação)
df.loc[df.sample(frac=0.02).index, 'quantidade'] *= -1  # 2% dos registros com sinal invertido

# 3. Duplica alguns registros (simula erro humano de entrada duplicada)
duplicatas = df.sample(frac=0.05)  # 5% dos registros duplicados
df = pd.concat([df, duplicatas], ignore_index=True)

# 4. Cria registros com quantidades exageradas (simula outliers)
outliers = df.sample(5)
outliers['quantidade'] = outliers['quantidade'] * 10  # Multiplica por 10 para exagerar
df = pd.concat([df, outliers], ignore_index=True)

# Exibe uma amostra dos dados gerados
print(df.head(10))
print(df.describe())

# Exporta os dados para um arquivo CSV
df.to_csv('dados_consumo_simulados.csv', index=False)

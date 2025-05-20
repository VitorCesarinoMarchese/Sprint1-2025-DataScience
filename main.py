# Mudar depois isso é somante um template
import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

# Parâmetros
num_registros = 100
unidades = ['Morumbi', 'Santo Amaro', 'Moema']
materiais = ['Seringa', 'Gaze', 'Tubo', 'Medicamentos', 'Esparadrapo']
tipos = ['entrada', 'saida']

# Função para gerar dados


def gerar_dados_simulados(n):
    dados = []
    for _ in range(n):
        unidade = random.choice(unidades)
        material = random.choice(materiais)
        tipo = random.choices(['entrada', 'saida'], weights=[0.05, 0.95])[0]
        data = fake.date_between(start_date='-6M', end_date='today')
        responsavel = fake.first_name()

        # Lógica de quantidade (ex: entradas são positivas, saídas negativas)
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


df = gerar_dados_simulados(num_registros)

# 1. Inserir valores ausentes
for col in ['quantidade', 'responsavel']:
    df.loc[df.sample(frac=0.01).index, col] = None  # 2% de valores ausentes

# 2. Inverter sinal incorretamente em algumas linhas
df.loc[df.sample(frac=0.02).index, 'quantidade'] *= -1

# 3. Duplicar registros (simular erro humano)
duplicatas = df.sample(frac=0.05)
df = pd.concat([df, duplicatas], ignore_index=True)

# 4. Criar registros com quantidade exagerada (outliers)
outliers = df.sample(5)
outliers['quantidade'] = outliers['quantidade'] * 10
df = pd.concat([df, outliers], ignore_index=True)

# Exibir amostra dos dados
print(df.head(10))
print(df.describe())

# Salvar em CSV
df.to_csv('dados_consumo_simulados.csv', index=False)

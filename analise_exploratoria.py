import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração para exibição de gráficos
plt.style.use('ggplot')
sns.set(style="whitegrid")

# Carregar os dados
df = pd.read_csv('./dados_consumo_simulados.csv')

# Análise exploratória inicial
print("Primeiras linhas do dataset:")
print(df.head())

print("\nInformações do dataset:")
print(df.info())

print("\nEstatísticas descritivas:")
print(df.describe())

# Verificar valores ausentes
print("\nValores ausentes por coluna:")
print(df.isnull().sum())

# Converter a coluna de data para o formato datetime
df['data'] = pd.to_datetime(df['data'])

# Verificar valores inconsistentes na coluna quantidade
print("\nVerificar valores inconsistentes na coluna quantidade:")
print("Registros com quantidade nula:", df['quantidade'].isnull().sum())

# Verificar entradas com valores negativos para entrada e positivos para saída
inconsistencias_tipo_quantidade = df[
    ((df['tipo'] == 'entrada') & (df['quantidade'] < 0)) | 
    ((df['tipo'] == 'saida') & (df['quantidade'] > 0))
]
print("\nInconsistências entre tipo e quantidade:")
print(inconsistencias_tipo_quantidade)

# Verificar registros sem responsável
sem_responsavel = df[df['responsavel'].isnull()]
print("\nRegistros sem responsável:")
print(sem_responsavel)

# Análise por unidade
print("\nContagem de registros por unidade:")
print(df['unidade'].value_counts())

# Análise por material
print("\nContagem de registros por material:")
print(df['material'].value_counts())

# Análise por tipo de operação
print("\nContagem de registros por tipo de operação:")
print(df['tipo'].value_counts())

# Salvar resultados da análise exploratória
with open('/projeto_anomalias_consumo_2/resultados_analise_exploratoria.txt', 'w') as f:
    f.write("ANÁLISE EXPLORATÓRIA DOS DADOS DE CONSUMO - NOVO DATASET\n")
    f.write("==================================================\n\n")
    
    f.write("1. VISÃO GERAL DOS DADOS\n")
    f.write(f"Total de registros: {len(df)}\n")
    f.write(f"Período dos dados: {df['data'].min().strftime('%d/%m/%Y')} a {df['data'].max().strftime('%d/%m/%Y')}\n")
    f.write(f"Unidades: {', '.join(df['unidade'].unique())}\n")
    f.write(f"Materiais: {', '.join(df['material'].unique())}\n\n")
    
    f.write("2. INCONSISTÊNCIAS IDENTIFICADAS\n")
    f.write(f"Registros com quantidade nula: {df['quantidade'].isnull().sum()}\n")
    f.write(f"Registros sem responsável: {df['responsavel'].isnull().sum()}\n")
    f.write(f"Inconsistências entre tipo e quantidade: {len(inconsistencias_tipo_quantidade)}\n\n")
    
    f.write("3. DISTRIBUIÇÃO POR UNIDADE\n")
    for unidade, count in df['unidade'].value_counts().items():
        f.write(f"{unidade}: {count} registros ({count/len(df)*100:.1f}%)\n")
    
    f.write("\n4. DISTRIBUIÇÃO POR MATERIAL\n")
    for material, count in df['material'].value_counts().items():
        f.write(f"{material}: {count} registros ({count/len(df)*100:.1f}%)\n")
    
    f.write("\n5. DISTRIBUIÇÃO POR TIPO DE OPERAÇÃO\n")
    for tipo, count in df['tipo'].value_counts().items():
        f.write(f"{tipo}: {count} registros ({count/len(df)*100:.1f}%)\n")

# Criar visualizações
# Distribuição de registros por unidade
plt.figure(figsize=(10, 6))
sns.countplot(x='unidade', data=df)
plt.title('Distribuição de Registros por Unidade')
plt.savefig('./projeto_anomalias_consumo_2/dist_por_unidade.png')

# Distribuição de registros por material
plt.figure(figsize=(12, 6))
sns.countplot(x='material', data=df)
plt.title('Distribuição de Registros por Material')
plt.savefig('./projeto_anomalias_consumo_2/dist_por_material.png')

# Distribuição de quantidades por tipo de operação
plt.figure(figsize=(10, 6))
sns.boxplot(x='tipo', y='quantidade', data=df)
plt.title('Distribuição de Quantidades por Tipo de Operação')
plt.savefig('./projeto_anomalias_consumo_2/dist_quantidade_por_tipo.png')

# Distribuição temporal dos registros
plt.figure(figsize=(14, 7))
df.groupby(df['data'].dt.month)['quantidade'].count().plot(kind='bar')
plt.title('Distribuição Temporal dos Registros (por mês)')
plt.xlabel('Mês')
plt.ylabel('Número de Registros')
plt.savefig('./projeto_anomalias_consumo_2/dist_temporal.png')

print("\nAnálise exploratória concluída. Resultados salvos em 'resultados_analise_exploratoria.txt'")

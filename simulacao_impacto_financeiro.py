import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.gridspec as gridspec

# Configurações de visualização
plt.style.use('ggplot')
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

# Carregar os dados de métricas
df_metrics = pd.read_csv('./metricas_variacao.csv')
df_metrics['data'] = pd.to_datetime(df_metrics['data'])

# Definir preços fictícios para cada material (adaptados para materiais hospitalares)
precos_materiais = {
    'Seringa': 2.5,       # R$ por unidade
    'Medicamentos': 45.0, # R$ por unidade
    'Tubo': 15.0,         # R$ por unidade
    'Esparadrapo': 8.0,   # R$ por rolo
    'Gaze': 3.5           # R$ por pacote
}

# Adicionar coluna de valor financeiro
df_metrics['valor_unitario'] = df_metrics['material'].map(precos_materiais)
df_metrics['valor_total'] = df_metrics['quantidade'].abs() * df_metrics['valor_unitario']

# Calcular impacto financeiro das anomalias
# Consideramos que anomalias podem representar:
# 1. Registros incorretos (quantidade errada)
# 2. Registros ausentes (material não registrado)
# 3. Registros duplicados

# Filtrar registros anômalos (severidade Alerta ou Crítico)
anomalias = df_metrics[df_metrics['severidade'].isin(['Alerta', 'Crítico'])]

# Calcular o impacto financeiro por tipo de anomalia
# 1. Impacto por registro incorreto: diferença entre valor registrado e valor esperado
anomalias['impacto_registro_incorreto'] = anomalias['valor_total'] * (anomalias['z_score'] - 1) / anomalias['z_score']

# 2. Impacto por possível registro ausente: estimativa baseada na média de consumo
impacto_ausente = {}
for material in df_metrics['material'].unique():
    for unidade in df_metrics['unidade'].unique():
        subset = df_metrics[(df_metrics['material'] == material) & (df_metrics['unidade'] == unidade)]
        if len(subset) > 0:
            # Estimar número de registros ausentes com base em padrões temporais
            # Simplificação: assumimos que 10% dos registros anômalos indicam registros ausentes
            n_ausentes = len(subset[subset['severidade'].isin(['Alerta', 'Crítico'])]) * 0.1
            valor_medio = subset['valor_total'].mean()
            impacto_ausente[(material, unidade)] = n_ausentes * valor_medio

# 3. Impacto por possível registro duplicado: estimativa baseada em registros muito próximos
# Simplificação: assumimos que 5% dos registros anômalos são duplicações
anomalias['impacto_duplicacao'] = anomalias['valor_total'] * 0.05

# Consolidar impacto financeiro total
impacto_total_incorreto = anomalias['impacto_registro_incorreto'].sum()
impacto_total_ausente = sum(impacto_ausente.values())
impacto_total_duplicacao = anomalias['impacto_duplicacao'].sum()
impacto_financeiro_total = impacto_total_incorreto + impacto_total_ausente + impacto_total_duplicacao

# Criar dataframe com resumo do impacto financeiro
impacto_resumo = pd.DataFrame({
    'Tipo de Impacto': ['Registros Incorretos', 'Registros Ausentes', 'Registros Duplicados', 'Total'],
    'Valor (R$)': [
        impacto_total_incorreto, 
        impacto_total_ausente, 
        impacto_total_duplicacao,
        impacto_financeiro_total
    ]
})

# Calcular impacto por material e unidade
impacto_por_material = anomalias.groupby('material')['impacto_registro_incorreto'].sum().reset_index()
impacto_por_material.columns = ['Material', 'Impacto Financeiro (R$)']

impacto_por_unidade = anomalias.groupby('unidade')['impacto_registro_incorreto'].sum().reset_index()
impacto_por_unidade.columns = ['Unidade', 'Impacto Financeiro (R$)']

# Calcular percentual do impacto em relação ao valor total movimentado
valor_total_movimentado = df_metrics['valor_total'].sum()
percentual_impacto = (impacto_financeiro_total / valor_total_movimentado) * 100

# Salvar resultados em arquivo
with open('./projeto_anomalias_consumo_2/impacto_financeiro.txt', 'w') as f:
    f.write("SIMULAÇÃO DO IMPACTO FINANCEIRO DAS FALHAS DE REGISTRO - NOVO DATASET\n")
    f.write("==============================================================\n\n")
    
    f.write("1. RESUMO DO IMPACTO FINANCEIRO\n")
    f.write(f"Valor total movimentado: R$ {valor_total_movimentado:.2f}\n")
    f.write(f"Impacto financeiro total estimado: R$ {impacto_financeiro_total:.2f}\n")
    f.write(f"Percentual do impacto: {percentual_impacto:.2f}%\n\n")
    
    f.write("2. DETALHAMENTO POR TIPO DE FALHA\n")
    for idx, row in impacto_resumo.iterrows():
        f.write(f"{row['Tipo de Impacto']}: R$ {row['Valor (R$)']:.2f}\n")
    
    f.write("\n3. IMPACTO POR MATERIAL\n")
    for idx, row in impacto_por_material.iterrows():
        f.write(f"{row['Material']}: R$ {row['Impacto Financeiro (R$)']:.2f}\n")
    
    f.write("\n4. IMPACTO POR UNIDADE\n")
    for idx, row in impacto_por_unidade.iterrows():
        f.write(f"{row['Unidade']}: R$ {row['Impacto Financeiro (R$)']:.2f}\n")
    
    f.write("\n5. ANÁLISE DE EFICIÊNCIA DO ESTOQUE\n")
    f.write("5.1 Impacto na Gestão de Estoque\n")
    f.write("  - Custos adicionais de armazenamento devido a registros incorretos\n")
    f.write("  - Custos de oportunidade por capital imobilizado\n")
    f.write("  - Custos de reposição emergencial devido a falhas de registro\n\n")
    
    f.write("5.2 Estimativa de Custos Indiretos\n")
    f.write("  - Custo de mão de obra para correção de registros: R$ 3.500,00\n")
    f.write("  - Custo de atrasos em procedimentos devido a falta de materiais: R$ 12.000,00\n")
    f.write("  - Custo de compras emergenciais com preços premium: R$ 6.500,00\n\n")
    
    f.write("5.3 Impacto Total (Direto + Indireto)\n")
    impacto_total_com_indiretos = impacto_financeiro_total + 22000.00
    f.write(f"  - Impacto financeiro total (incluindo custos indiretos): R$ {impacto_total_com_indiretos:.2f}\n")
    f.write(f"  - Percentual do impacto total: {(impacto_total_com_indiretos / valor_total_movimentado) * 100:.2f}%\n")

# Criar visualizações
# 1. Gráfico de barras do impacto financeiro por tipo de falha
plt.figure(figsize=(10, 6))
sns.barplot(x='Tipo de Impacto', y='Valor (R$)', data=impacto_resumo[:-1], palette='YlOrRd')
plt.title('Impacto Financeiro por Tipo de Falha')
plt.xlabel('Tipo de Falha')
plt.ylabel('Valor (R$)')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('./projeto_anomalias_consumo_2/impacto_por_tipo_falha.png')

# 2. Gráfico de barras do impacto financeiro por material
plt.figure(figsize=(10, 6))
sns.barplot(x='Material', y='Impacto Financeiro (R$)', data=impacto_por_material, palette='YlOrRd')
plt.title('Impacto Financeiro por Material')
plt.xlabel('Material')
plt.ylabel('Valor (R$)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('./projeto_anomalias_consumo_2/impacto_por_material.png')

# 3. Gráfico de barras do impacto financeiro por unidade
plt.figure(figsize=(10, 6))
sns.barplot(x='Unidade', y='Impacto Financeiro (R$)', data=impacto_por_unidade, palette='YlOrRd')
plt.title('Impacto Financeiro por Unidade')
plt.xlabel('Unidade')
plt.ylabel('Valor (R$)')
plt.tight_layout()
plt.savefig('./projeto_anomalias_consumo_2/impacto_por_unidade.png')

# 4. Gráfico de pizza do percentual de impacto
plt.figure(figsize=(10, 6))
labels = ['Impacto Financeiro', 'Valor Normal']
sizes = [impacto_financeiro_total, valor_total_movimentado - impacto_financeiro_total]
colors = ['#ff9999', '#66b3ff']
explode = (0.1, 0)
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.title('Percentual do Impacto Financeiro em Relação ao Valor Total')
plt.tight_layout()
plt.savefig('./projeto_anomalias_consumo_2/percentual_impacto.png')

# 5. Dashboard de impacto financeiro
fig = plt.figure(figsize=(15, 12))
gs = gridspec.GridSpec(2, 2, figure=fig)

# Gráfico 1: Impacto por tipo de falha
ax1 = fig.add_subplot(gs[0, 0])
sns.barplot(x='Tipo de Impacto', y='Valor (R$)', data=impacto_resumo[:-1], palette='YlOrRd', ax=ax1)
ax1.set_title('Impacto por Tipo de Falha')
ax1.set_xlabel('Tipo de Falha')
ax1.set_ylabel('Valor (R$)')
ax1.tick_params(axis='x', rotation=45)

# Gráfico 2: Impacto por material
ax2 = fig.add_subplot(gs[0, 1])
sns.barplot(x='Material', y='Impacto Financeiro (R$)', data=impacto_por_material, palette='YlOrRd', ax=ax2)
ax2.set_title('Impacto por Material')
ax2.set_xlabel('Material')
ax2.set_ylabel('Valor (R$)')
ax2.tick_params(axis='x', rotation=45)

# Gráfico 3: Impacto por unidade
ax3 = fig.add_subplot(gs[1, 0])
sns.barplot(x='Unidade', y='Impacto Financeiro (R$)', data=impacto_por_unidade, palette='YlOrRd', ax=ax3)
ax3.set_title('Impacto por Unidade')
ax3.set_xlabel('Unidade')
ax3.set_ylabel('Valor (R$)')

# Gráfico 4: Tabela de resumo
ax4 = fig.add_subplot(gs[1, 1])
ax4.axis('off')
impacto_resumo['Valor (R$)'] = impacto_resumo['Valor (R$)'].round(2)
table = ax4.table(
    cellText=impacto_resumo.values,
    colLabels=impacto_resumo.columns,
    loc='center',
    cellLoc='center'
)
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.5)
ax4.set_title('Resumo do Impacto Financeiro', pad=20)

plt.tight_layout()
plt.savefig('./projeto_anomalias_consumo_2/dashboard_impacto_financeiro.png')

print("Simulação do impacto financeiro concluída com sucesso!")
print("Arquivos gerados:")
print("- impacto_financeiro.txt: Relatório detalhado do impacto financeiro")
print("- impacto_por_tipo_falha.png: Gráfico do impacto por tipo de falha")
print("- impacto_por_material.png: Gráfico do impacto por material")
print("- impacto_por_unidade.png: Gráfico do impacto por unidade")
print("- percentual_impacto.png: Gráfico do percentual de impacto")
print("- dashboard_impacto_financeiro.png: Dashboard com resumo do impacto financeiro")

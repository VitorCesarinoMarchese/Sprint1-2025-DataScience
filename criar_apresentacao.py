from fpdf import FPDF
import os
from datetime import datetime

# Configuração da apresentação em PDF
class PDF(FPDF):
    def header(self):
        # Fonte Arial negrito 15
        self.set_font('Arial', 'B', 15)
        # Título centralizado
        self.cell(0, 10, 'Identificação de Anomalias nos Registros de Consumo de Materiais Hospitalares', 0, 1, 'C')
        # Linha
        self.line(10, 20, 200, 20)
        # Quebra de linha
        self.ln(15)

    def footer(self):
        # Posiciona a 1.5 cm do final
        self.set_y(-15)
        # Arial itálico 8
        self.set_font('Arial', 'I', 8)
        # Número da página
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

# Criar o PDF
pdf = PDF()
pdf.add_page()

# Capa
pdf.set_font('Arial', 'B', 20)
pdf.cell(0, 20, 'Projeto: Identificação de Anomalias', 0, 1, 'C')
pdf.cell(0, 20, 'nos Registros de Consumo de Materiais Hospitalares', 0, 1, 'C')
pdf.ln(20)

pdf.set_font('Arial', '', 12)
pdf.cell(0, 10, 'Desafio Escolhido: 1', 0, 1, 'C')
pdf.ln(10)

pdf.set_font('Arial', 'B', 14)
pdf.cell(0, 10, 'Integrantes:', 0, 1, 'C')
pdf.set_font('Arial', '', 12)
pdf.cell(0, 10, 'Nome do Aluno - Matrícula', 0, 1, 'C')
pdf.ln(20)

pdf.set_font('Arial', 'I', 10)
data_atual = datetime.now().strftime('%d/%m/%Y')
pdf.cell(0, 10, f'Data de Entrega: {data_atual}', 0, 1, 'C')

# Nova página - Introdução
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, '1. Introdução', 0, 1, 'L')
pdf.ln(5)

pdf.set_font('Arial', '', 12)
texto_intro = """O projeto propõe a identificação de anomalias nos registros de consumo de materiais hospitalares em unidades operacionais, com o objetivo de detectar inconsistências que possam impactar a eficiência do estoque.

A primeira etapa consistiu na análise de um conjunto de dados simulando registros manuais de entrada e saída de materiais hospitalares. Em seguida, foram aplicadas análises estatísticas para calcular desvios relevantes e criar métricas de variação.

Técnicas como Z-score e intervalo interquartil (IQR) foram utilizadas para detectar outliers e padrões fora do comportamento esperado. Com base nesses dados, foi desenvolvido um painel de alertas que destaca os casos de consumo fora do padrão.

Por fim, foi realizada uma simulação do impacto financeiro causado por falhas de registro, demonstrando como a baixa visibilidade pode afetar os custos da operação hospitalar."""

pdf.multi_cell(0, 10, texto_intro)

# Nova página - Análise Exploratória
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, '2. Análise Exploratória dos Dados', 0, 1, 'L')
pdf.ln(5)

pdf.set_font('Arial', '', 12)
texto_analise = """A análise exploratória dos dados revelou informações importantes sobre a estrutura e qualidade dos registros de consumo. Foram identificados valores ausentes, inconsistências entre tipo de operação e quantidade, além de registros sem responsável.

Os dados abrangem três unidades hospitalares (Santo Amaro, Moema e Morumbi) e cinco tipos de materiais (Seringa, Medicamentos, Tubo, Esparadrapo e Gaze), com operações de entrada e saída registradas ao longo de um período de aproximadamente seis meses.

Uma característica importante observada foi o desequilíbrio entre operações de entrada e saída, com predominância significativa de registros de saída, o que pode indicar falhas no processo de registro de entradas de materiais."""

pdf.multi_cell(0, 10, texto_analise)
pdf.ln(5)

# Adicionar imagem da distribuição por unidade
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Distribuição de Registros por Unidade:', 0, 1, 'L')
if os.path.exists('./projeto_anomalias_consumo_2/dist_por_unidade.png'):
    pdf.image('./projeto_anomalias_consumo_2/dist_por_unidade.png', x=30, y=None, w=150)
    pdf.ln(5)

# Adicionar imagem da distribuição por material
pdf.add_page()
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Distribuição de Registros por Material:', 0, 1, 'L')
if os.path.exists('./projeto_anomalias_consumo_2/dist_por_material.png'):
    pdf.image('./projeto_anomalias_consumo_2/dist_por_material.png', x=30, y=None, w=150)
    pdf.ln(5)

# Adicionar imagem da distribuição de quantidade por tipo
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Distribuição de Quantidades por Tipo de Operação:', 0, 1, 'L')
if os.path.exists('./projeto_anomalias_consumo_2/dist_quantidade_por_tipo.png'):
    pdf.image('./projeto_anomalias_consumo_2/dist_quantidade_por_tipo.png', x=30, y=None, w=150)
    pdf.ln(5)

# Nova página - Detecção de Outliers
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, '3. Detecção de Outliers', 0, 1, 'L')
pdf.ln(5)

pdf.set_font('Arial', '', 12)
texto_outliers = """Para identificar anomalias nos registros de consumo, foram aplicadas duas técnicas estatísticas complementares:

1. Z-score: Identifica valores que estão a mais de 3 desvios padrão da média.
2. Intervalo Interquartil (IQR): Identifica valores abaixo de Q1-1.5*IQR ou acima de Q3+1.5*IQR.

A análise foi realizada separadamente para cada material e unidade, permitindo identificar padrões específicos de consumo anômalo em diferentes contextos operacionais.

Interessantemente, neste conjunto de dados, o método IQR mostrou-se mais eficaz na detecção de outliers, identificando 7 registros anômalos, enquanto o método Z-score não detectou outliers significativos. Isso sugere que as anomalias presentes estão mais relacionadas à distribuição dos dados do que a valores extremamente discrepantes."""

pdf.multi_cell(0, 10, texto_outliers)
pdf.ln(5)

# Adicionar imagem de outliers por Z-score
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Outliers Detectados por Z-score:', 0, 1, 'L')
if os.path.exists('./projeto_anomalias_consumo_2/outliers_zscore.png'):
    pdf.image('./projeto_anomalias_consumo_2/outliers_zscore.png', x=20, y=None, w=170)
    pdf.ln(5)

# Adicionar imagem de outliers por IQR
pdf.add_page()
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Outliers Detectados por IQR:', 0, 1, 'L')
if os.path.exists('./projeto_anomalias_consumo_2/outliers_iqr.png'):
    pdf.image('./projeto_anomalias_consumo_2/outliers_iqr.png', x=20, y=None, w=170)
    pdf.ln(5)

# Nova página - Métricas de Variação e Painel de Alertas
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, '4. Métricas de Variação e Painel de Alertas', 0, 1, 'L')
pdf.ln(5)

pdf.set_font('Arial', '', 12)
texto_metricas = """Com base nos resultados da detecção de outliers, foram criadas métricas de variação para quantificar o desvio de cada registro em relação ao comportamento esperado. Essas métricas incluem:

1. Z-score: Medida de quantos desvios padrão um valor está da média.
2. Variação percentual: Diferença percentual em relação à média.
3. Classificação de severidade: Categorização em Normal, Atenção, Alerta e Crítico.

Essas métricas foram utilizadas para desenvolver um painel de alertas que destaca os casos mais críticos de consumo fora do padrão, permitindo uma rápida identificação e priorização de ações corretivas.

No contexto hospitalar, a detecção precoce de anomalias no consumo de materiais é especialmente importante, pois pode indicar desde erros de registro até possíveis desvios ou uso inadequado de recursos essenciais para o atendimento aos pacientes."""

pdf.multi_cell(0, 10, texto_metricas)
pdf.ln(5)

# Adicionar imagem do painel de severidade
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Distribuição de Severidade por Material e Unidade:', 0, 1, 'L')
if os.path.exists('./projeto_anomalias_consumo_2/painel_severidade.png'):
    pdf.image('./projeto_anomalias_consumo_2/painel_severidade.png', x=20, y=None, w=170)
    pdf.ln(5)

# Adicionar imagem do heatmap de anomalias
pdf.add_page()
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Heatmap de Anomalias por Material e Unidade:', 0, 1, 'L')
if os.path.exists('./projeto_anomalias_consumo_2/heatmap_anomalias.png'):
    pdf.image('./projeto_anomalias_consumo_2/heatmap_anomalias.png', x=30, y=None, w=150)
    pdf.ln(5)

# Adicionar imagem do dashboard de alertas críticos
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Dashboard de Alertas Críticos:', 0, 1, 'L')
if os.path.exists('./projeto_anomalias_consumo_2/dashboard_alertas_criticos.png'):
    pdf.image('./projeto_anomalias_consumo_2/dashboard_alertas_criticos.png', x=20, y=None, w=170)
    pdf.ln(5)

# Nova página - Simulação do Impacto Financeiro
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, '5. Simulação do Impacto Financeiro', 0, 1, 'L')
pdf.ln(5)

pdf.set_font('Arial', '', 12)
texto_impacto = """Para quantificar o impacto financeiro das falhas de registro, foi realizada uma simulação considerando três tipos principais de falhas:

1. Registros incorretos: Quantidades registradas com valores muito diferentes do esperado.
2. Registros ausentes: Materiais consumidos mas não registrados no sistema.
3. Registros duplicados: Mesma operação registrada mais de uma vez.

A simulação utilizou preços estimados para cada material hospitalar e calculou o impacto financeiro total, bem como sua distribuição por tipo de falha, material e unidade operacional.

No contexto hospitalar, o impacto financeiro das falhas de registro vai além do valor direto dos materiais, podendo afetar a qualidade do atendimento aos pacientes, gerar compras emergenciais com preços premium e causar atrasos em procedimentos devido à falta de materiais essenciais."""

pdf.multi_cell(0, 10, texto_impacto)
pdf.ln(5)

# Adicionar imagem do dashboard de impacto financeiro
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Dashboard de Impacto Financeiro:', 0, 1, 'L')
if os.path.exists('./projeto_anomalias_consumo_2/dashboard_impacto_financeiro.png'):
    pdf.image('./projeto_anomalias_consumo_2/dashboard_impacto_financeiro.png', x=20, y=None, w=170)
    pdf.ln(5)

# Adicionar imagem do percentual de impacto
pdf.add_page()
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Percentual do Impacto Financeiro em Relação ao Valor Total:', 0, 1, 'L')
if os.path.exists('./projeto_anomalias_consumo_2/percentual_impacto.png'):
    pdf.image('./projeto_anomalias_consumo_2/percentual_impacto.png', x=30, y=None, w=150)
    pdf.ln(5)

# Nova página - Conclusões e Recomendações
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, '6. Conclusões e Recomendações', 0, 1, 'L')
pdf.ln(5)

pdf.set_font('Arial', '', 12)
texto_conclusoes = """A análise dos registros de consumo de materiais hospitalares revelou a presença de anomalias significativas que impactam a eficiência do estoque e geram custos adicionais para a operação. As principais conclusões são:

1. Foram identificados registros com valores discrepantes através do método IQR, indicando possíveis erros de digitação ou falhas no processo de registro.

2. Inconsistências entre tipo de operação (entrada/saída) e sinal da quantidade sugerem problemas no treinamento dos responsáveis ou no sistema de registro.

3. A ausência de responsável em alguns registros dificulta a rastreabilidade e a atribuição de responsabilidades.

4. O desequilíbrio entre operações de entrada e saída sugere falhas sistemáticas no registro de entradas de materiais.

5. O impacto financeiro das falhas de registro é significativo, representando uma parcela considerável do valor total movimentado.

Com base nessas conclusões, recomenda-se:

1. Implementar validações no sistema de registro para evitar inconsistências entre tipo de operação e quantidade.

2. Estabelecer limites de quantidade por material e unidade, com alertas para valores fora do padrão.

3. Tornar obrigatório o preenchimento do campo de responsável para todos os registros.

4. Realizar treinamentos periódicos com os responsáveis pelos registros, enfatizando a importância da precisão dos dados.

5. Implementar um sistema de auditoria regular para identificar e corrigir anomalias em tempo hábil.

6. Desenvolver um painel de monitoramento em tempo real para acompanhar os indicadores de qualidade dos registros.

7. Estabelecer protocolos específicos para o registro de materiais de alto valor, como medicamentos, para reduzir o impacto financeiro de possíveis falhas."""

pdf.multi_cell(0, 10, texto_conclusoes)

# Salvar o PDF
pdf_path = './projeto_anomalias_consumo_2/apresentacao_anomalias_consumo.pdf'
pdf.output(pdf_path)

print(f"Apresentação em PDF criada com sucesso: {pdf_path}")

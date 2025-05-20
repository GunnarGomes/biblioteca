from flask import Blueprint, jsonify, render_template, request, send_file
from modules.DB import DB
from sqlalchemy import text
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib
import base64
import numpy as np

matplotlib.use('Agg')  # Para funcionar em servidores sem interface gráfica

bp_relatorio = Blueprint("bp_relatorio", __name__, template_folder="templates")
db = DB()

qtd_livros_cadastrados = db.LivrosCadastrados()

@bp_relatorio.route('/user/relatorio', methods=['GET', 'POST'])
def Relatorio():
    # Obter filtros do formulário
    periodo_inicio = request.args.get('inicio', '')
    periodo_fim = request.args.get('fim', '')
    professor_filtro = request.args.get('professor', '')
    
    # Obter dados
    emprestimos = db.EmprestimosParaRelatorio()
    
    # Criar DataFrame com colunas explícitas
    colunas = ['id', 'data_emprestimo', 'data_devolucao', 'aluno', 'serie', 
               'livro', 'autor', 'professor', 'status']
    
    df = pd.DataFrame(emprestimos, columns=colunas)
    
    # Verificar se temos dados
    if df.empty:
        return render_template("relatorio/relatorio.html",
                           emprestimos=[],
                           grafico1="",
                           grafico2="",
                           grafico3="",
                           dados_mensais=[],
                           total_emprestimos=0,
                           media_duracao=0,
                           alunos_unicos=0,
                           livros_unicos=0,
                           emprestimos_recentes=[],
                           livros_populares=[],
                           professores=[],
                           filtro_professor="",
                           periodo_inicio="",
                           periodo_fim="")
    
    # Aplicar filtros se fornecidos
    if periodo_inicio and periodo_fim:
        df['data_emprestimo'] = pd.to_datetime(df['data_emprestimo'])
        df = df[(df['data_emprestimo'] >= periodo_inicio) & (df['data_emprestimo'] <= periodo_fim)]
    
    if professor_filtro:
        df = df[df['professor'] == professor_filtro]
    
    # Converter datas para trabalhar com elas
    df['data_emprestimo'] = pd.to_datetime(df['data_emprestimo'])
    if 'data_devolucao' in df.columns:
        df['data_devolucao'] = pd.to_datetime(df['data_devolucao'])
    
    # Extrair mês e ano para agrupamento
    df['mes_ano'] = df['data_emprestimo'].dt.strftime('%Y-%m')
    
    # GRÁFICO 1: Empréstimos por mês
    emprestimos_por_mes = df.groupby('mes_ano').size().reset_index(name='qtd')
    
    fig1 = plt.figure(figsize=(10, 6))
    plt.bar(emprestimos_por_mes['mes_ano'], emprestimos_por_mes['qtd'], color='skyblue')
    plt.title('Empréstimos por Mês', fontsize=16)
    plt.xlabel('Mês/Ano', fontsize=12)
    plt.ylabel('Quantidade', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Salvar gráfico 1 como base64
    img_bytes1 = BytesIO()
    plt.savefig(img_bytes1, format='png')
    img_bytes1.seek(0)
    grafico1 = f"data:image/png;base64,{base64.b64encode(img_bytes1.getvalue()).decode()}"
    plt.close(fig1)
    
    # GRÁFICO 2: Top 10 livros mais emprestados
    livros_populares = df.groupby('livro').size().reset_index(name='qtd')
    livros_populares = livros_populares.sort_values('qtd', ascending=False).head(10)
    
    fig2 = plt.figure(figsize=(10, 6))
    plt.barh(livros_populares['livro'], livros_populares['qtd'], color='lightgreen')
    plt.title('Top 10 Livros Mais Emprestados', fontsize=16)
    plt.xlabel('Quantidade', fontsize=12)
    plt.tight_layout()
    
    # Salvar gráfico 2 como base64
    img_bytes2 = BytesIO()
    plt.savefig(img_bytes2, format='png')
    img_bytes2.seek(0)
    grafico2 = f"data:image/png;base64,{base64.b64encode(img_bytes2.getvalue()).decode()}"
    plt.close(fig2)
    
    # GRÁFICO 3: Empréstimos por professor
    emprestimos_por_professor = df.groupby('professor').size().reset_index(name='qtd')
    
    fig3 = plt.figure(figsize=(10, 6))
    plt.pie(emprestimos_por_professor['qtd'], labels=emprestimos_por_professor['professor'], 
            autopct='%1.1f%%', startangle=90, shadow=True)
    plt.title('Distribuição de Empréstimos por Professor', fontsize=16)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.tight_layout()
    
    # Salvar gráfico 3 como base64
    img_bytes3 = BytesIO()
    plt.savefig(img_bytes3, format='png')
    img_bytes3.seek(0)
    grafico3 = f"data:image/png;base64,{base64.b64encode(img_bytes3.getvalue()).decode()}"
    plt.close(fig3)
    
    # Estatísticas gerais
    total_emprestimos = len(df)
    
    # Calcular duração apenas se tivermos data_devolucao
    if 'data_devolucao' in df.columns and not df['data_devolucao'].isna().all():
        df['duracao_dias'] = (df['data_devolucao'] - df['data_emprestimo']).dt.days
        media_duracao = df['duracao_dias'].mean()
    else:
        media_duracao = 0
    
    alunos_unicos = df['aluno'].nunique()
    livros_unicos = df['livro'].nunique()
    
    # Dados para tabelas adicionais
    emprestimos_recentes = df.sort_values('data_emprestimo', ascending=False).head(10).to_dict(orient='records')
    
    # Obter lista de professores para o filtro
    professores = sorted(df['professor'].unique())
    
    return render_template("relatorio/relatorio.html",
                           emprestimos=df.to_dict(orient='records'),
                           grafico1=grafico1,
                           grafico2=grafico2,
                           grafico3=grafico3,
                           dados_mensais=emprestimos_por_mes.to_dict(orient='records'),
                           total_emprestimos=total_emprestimos,
                           media_duracao=round(media_duracao, 1) if not pd.isna(media_duracao) else 0,
                           alunos_unicos=alunos_unicos,
                           livros_unicos=livros_unicos,
                           emprestimos_recentes=emprestimos_recentes,
                           livros_populares=livros_populares.to_dict(orient='records'),
                           professores=professores,
                           filtro_professor=professor_filtro,
                           periodo_inicio=periodo_inicio,
                           periodo_fim=periodo_fim)

@bp_relatorio.route("/user/relatorio/excel")
def BaixarExcel():
    emprestimos = db.EmprestimosParaRelatorio()
    livros_cadastrados = db.LivrosCadastrados()  # Certifique-se que você tenha esse método

    df_emp = pd.DataFrame(emprestimos, columns=['id', 'data_emprestimo', 'data_devolucao', 'aluno', 'serie', 'livro', 'autor', 'professor', 'status'])
    df_livros = pd.DataFrame(livros_cadastrados, columns=['id', 'titulo', 'autor'])

    # Quantidade de empréstimos por mês
    df_emp['data_emprestimo'] = pd.to_datetime(df_emp['data_emprestimo'])
    df_emp['mes_ano'] = df_emp['data_emprestimo'].dt.to_period('M').astype(str)
    emprestimos_por_mes = df_emp.groupby('mes_ano').size().reset_index(name='qtd_emprestimos')

    # Top 10 livros mais emprestados
    top_livros = df_emp.groupby('livro').size().reset_index(name='qtd').sort_values('qtd', ascending=False).head(10)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_emp.to_excel(writer, index=False, sheet_name='Empréstimos')
        df_livros.to_excel(writer, index=False, sheet_name='Livros Cadastrados')
        emprestimos_por_mes.to_excel(writer, index=False, sheet_name='Empréstimos por Mês')
        top_livros.to_excel(writer, index=False, sheet_name='Top 10 Livros')
    output.seek(0)
    return send_file(output, download_name="relatorio_completo.xlsx", as_attachment=True)

import zipfile

@bp_relatorio.route("/user/relatorio/csv")
def BaixarCSV():
    emprestimos = db.EmprestimosParaRelatorio()
    livros_cadastrados = db.LivrosCadastrados()

    df_emp = pd.DataFrame(emprestimos, columns=['id', 'data_emprestimo', 'data_devolucao', 'aluno', 'serie', 'livro', 'autor', 'professor', 'status'])
    df_livros = pd.DataFrame(livros_cadastrados, columns=['id', 'titulo', 'autor'])

    df_emp['data_emprestimo'] = pd.to_datetime(df_emp['data_emprestimo'])
    df_emp['mes_ano'] = df_emp['data_emprestimo'].dt.to_period('M').astype(str)
    emprestimos_por_mes = df_emp.groupby('mes_ano').size().reset_index(name='qtd_emprestimos')
    top_livros = df_emp.groupby('livro').size().reset_index(name='qtd').sort_values('qtd', ascending=False).head(10)

    memory_zip = BytesIO()
    with zipfile.ZipFile(memory_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("emprestimos.csv", df_emp.to_csv(index=False))
        zf.writestr("livros_cadastrados.csv", df_livros.to_csv(index=False))
        zf.writestr("emprestimos_por_mes.csv", emprestimos_por_mes.to_csv(index=False))
        zf.writestr("top_10_livros.csv", top_livros.to_csv(index=False))
    
    memory_zip.seek(0)
    return send_file(memory_zip, download_name="relatorio_completo.zip", as_attachment=True)


@bp_relatorio.route("/user/relatorio/pdf")
def BaixarPDF():
    # Aqui você precisaria implementar a geração de PDF
    # Pode usar bibliotecas como reportlab, weasyprint ou pdfkit
    # Exemplo básico com reportlab:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
    
    emprestimos = db.EmprestimosParaRelatorio()
    df = pd.DataFrame(emprestimos)
    
    # Definir nomes de colunas com base na consulta SQL
    if not df.empty:
        df.columns = ['id', 'data_emprestimo', 'data_devolucao', 'aluno', 'serie', 
                      'livro', 'autor', 'professor', 'status']
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Converter DataFrame para lista para a tabela
    data = [df.columns.tolist()] + df.values.tolist() if not df.empty else [['Sem dados disponíveis']]
    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(t)
    doc.build(elements)
    
    buffer.seek(0)
    return send_file(buffer, download_name="relatorio_emprestimos.pdf", as_attachment=True)

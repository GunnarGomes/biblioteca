from flask import Blueprint, jsonify, render_template, request, send_file
from modules.DB import DB
from sqlalchemy import text
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib
import base64


matplotlib.use('Agg')  # Para funcionar em servidores sem interface gráfica

bp_relatorio = Blueprint("bp_relatorio", __name__, template_folder="templates")
db = DB()

@bp_relatorio.route('/user/relatorio')
def Relatorio():
    emprestimos = db.EmprestimosParaRelatorio()
    df = pd.DataFrame(emprestimos)

    # Agrupar por mês
    df['data_emprestimo'] = pd.to_datetime(df['data_emprestimo'])
    df['mes'] = df['data_emprestimo'].dt.to_period('M').astype(str)
    emprestimos_por_mes = df.groupby('mes').size().reset_index(name='qtd')

    # Gerar gráfico
    fig, ax = plt.subplots()
    ax.bar(emprestimos_por_mes['mes'], emprestimos_por_mes['qtd'])
    ax.set_title('Empréstimos por mês')
    ax.set_ylabel('Quantidade')
    ax.set_xlabel('Mês')
    plt.xticks(rotation=45)
    plt.tight_layout()


    img_bytes = BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)
    grafico = f"data:image/png;base64,{base64.b64encode(img_bytes.getvalue()).decode()}"

    return render_template("relatorio/relatorio.html",
                           emprestimos=emprestimos,
                           grafico=grafico,
                           dados_mensais=emprestimos_por_mes.to_dict(orient='records'))

@bp_relatorio.route("/user/relatorio/excel")
def BaixarExcel():
    emprestimos = db.EmprestimosParaRelatorio()
    df = pd.DataFrame(emprestimos)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Empréstimos')
    output.seek(0)
    return send_file(output, download_name="relatorio_emprestimos.xlsx", as_attachment=True)

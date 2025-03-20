from flask import Blueprint, session, redirect, url_for, render_template, request, jsonify
from modules.DB import DB

db = DB()

bp_professor = Blueprint("bp_professor",__name__,template_folder='templates', static_folder='static')

@bp_professor.route('/user/professor',methods=["GET","POST"])
def PgProf():
    return render_template('professor/pg_principal.html',emprestimos=db.DadosEmprestimos())


@bp_professor.before_request
def ChecarSeOMalandroFezLogin():
    if 'token' not in session:
        return redirect(url_for('bp_login.Login'))
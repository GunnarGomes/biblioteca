from flask import Blueprint, request, url_for, render_template, session, redirect, flash
from modules.DB import DB

bp_login = Blueprint('bp_login',__name__,template_folder='templates')

@bp_login.route('/',methods=["GET","POST"])
def Login():
    if request.method == "POST":
        cpf_data = request.form['cpf']
        senha_data = request.form['senha']
        db = DB()
        existe,user_id = db.EsseUsuarioExiste(cpf=cpf_data, senha=senha_data)
        if existe:
            session.clear()  # Evita sessão antiga
            
            session['user'] = cpf_data
            session['token'] = 'testePorEnquanto'
            session['id'] = user_id[0]
            flash("Login bem-sucedido!", "success")

            return redirect(url_for('bp_professor.PgProf'))
        else:
            print("Chamando flash com erro...")
            flash("Deu erro", "danger")
            session.modified = True  # Força o Flask a reconhecer mudanças na sessão
            return redirect(url_for('bp_login.Login'))

    return render_template('login/login.html')
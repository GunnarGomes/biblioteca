from flask import Blueprint, request, url_for, render_template, session,redirect, flash, jsonify
from modules.DB import DB
from modules.apibook import API

bp_cad = Blueprint('bp_cad',__name__,template_folder='templates')
db = DB()


@bp_cad.route('/user/pesquisa-livro',methods=["GET","POST"])
def CadLi():
    
    if request.method == "POST":
        cod = request.form.get('isbn')
        tit = request.form.get('titulo')
        
        return redirect(url_for('bp_cad.CadLiOk',isbn = cod,titulo=tit))
    return render_template('cadastro/cadLi.html')

@bp_cad.route('/user/resultado', methods=['GET','POST'])
def CadLiOk():
    cod = request.args.get('isbn','')
    tit = request.args.get('titulo','')
    api = API(cod=cod,titulo=tit)
    livros=api.listar_livros()
    if request.method == "POST":
        return redirect(url_for('bp_cad.LivroCad'))
    return render_template('sucess/bookCreated.html',livros = livros)

@bp_cad.route('/user/livro_cadastrado',methods=["GET","POST"])
def LivroCad():
    titulo = request.form.get('titulo')
    autor = request.form.get('autor')
    data = request.form.get('data')
    descricao = request.form.get('descricao')
    isbn = request.form.get('isbn')

    # Salvando no banco de dados
    resultado = db.CadastroLivro(titulo, autor, isbn, data)

    if resultado["status"] == "sucesso":
        flash("Livro cadastrado com sucesso!", "success")
    else:
        flash(f"Erro ao cadastrar livro: {resultado['mensagem']}", "error")

    return redirect(url_for('bp_cad.CadLi'))

@bp_cad.route('/user/cadastro-aluno', methods=["GET", "POST"])
def CadAl():
    if request.method == "POST":
        nome = request.form.get('nome')
        email = request.form.get('email')
        serie = request.form.get('serie')

        # Salvando o aluno no banco de dados
        resultado = db.cadastrar_aluno(nome, email, serie)

        if resultado["status"] == "sucesso":
            flash("Aluno cadastrado com sucesso!", "success")
            return redirect(url_for('bp_cad.CadAl'))
        else:
            flash(f"Erro ao cadastrar aluno: {resultado['mensagem']}", "error")
    
    return render_template('cadastro/cadAl.html')


@bp_cad.route('/user/cadastro_emprestimo',methods=["GET", "POST"])
def CadEmp():
    al = db.DadosAlunos()
    li = db.DadosLivros()
    if request.method == "POST":
        aluno_id = request.form.get('id_aluno')
        livro_id = request.form.get('id_livro')
        dataEmp = request.form.get('dataEmprestimo')
        dataDev = request.form.get('dataDevolucao')
        db.CadastrarEmprestimo(aluno_id=aluno_id,livro_id=livro_id,professor_id=session.get('id'),data_emprestimo=dataEmp,data_devolucao=dataDev)
        flash("emprestimo cadastrado com sucesso","success")
    return render_template('cadastro/cadEmp.html',alunos = al, livros = li)

@bp_cad.route('/user/cadastro-professor',methods=["GET", "POST"])
def CadastroProf():
    if request.method == "POST":
        nome = request.form.get('nome')
        email = request.form.get('email')
        cpf = request.form.get('cpf')
        senha = request.form.get('senha')

        # Salvando o aluno no banco de dados
        resultado = db.cadastrar_professor(nome, email, cpf, senha)

        if resultado["status"] == "sucesso":
            flash("professor cadastrado com sucesso!", "success")
            return redirect(url_for('bp_cad.CadastroProf'))
        else:
            flash(f"Erro ao cadastrar professor: {resultado['mensagem']}", "error")
    return render_template('cadastro/cadProf.html')

@bp_cad.route('/user/devolucao/<int:idEmp>',methods=["GET"])
def Devolvido(idEmp):
    db.Devolucao(id_emprestimo=idEmp)
    flash("Devolução feita","success")
    return redirect(url_for("bp_professor.PgProf"))

@bp_cad.before_request
def ChecarSeOMalandroFezLogin():
    if 'token' not in session:
        return redirect(url_for('bp_login.Login'))
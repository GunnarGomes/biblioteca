from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from sqlalchemy import text
from modules.DB import DB
from modules.DB import CriptografiaDePontaGrossa
db = DB()
bp_recuperacao = Blueprint('bp_recuperacao', __name__, template_folder='templates')

@bp_recuperacao.route('/recuperar_senha', methods=['GET', 'POST'])
def recuperar_senha():
    if request.method == 'POST':
        cpf = request.form.get('cpf')
        
        # Validação básica
        if not cpf:
            flash("Por favor, informe seu CPF.", "error")
            return redirect(url_for('bp_recuperacao.recuperar_senha'))
        
        try:
            with db.engine.connect() as conn:
                professor = conn.execute(
                    text("SELECT * FROM professores WHERE cpf = :cpf"),
                    {"cpf": cpf}
                ).fetchone()
            
            if professor:
                # Armazenar o ID do professor em uma sessão segura para uso posterior
                session['reset_professor_id'] = professor.id
                return redirect(url_for('bp_recuperacao.nova_senha'))
            else:
                flash("Não foi encontrado professor com este CPF.", "error")
                return redirect(url_for('bp_recuperacao.recuperar_senha'))
                
        except Exception as e:
            flash(f"Ocorreu um erro: {str(e)}", "error")
            return redirect(url_for('bp_recuperacao.recuperar_senha'))
            
    return render_template('modificar/recuperar_senha.html')

@bp_recuperacao.route('/nova_senha', methods=['GET', 'POST'])
def nova_senha():
    # Verificar se o ID do professor está na sessão
    if 'reset_professor_id' not in session:
        flash("Sessão expirada ou inválida. Por favor, tente novamente.", "error")
        return redirect(url_for('bp_recuperacao.recuperar_senha'))
    
    professor_id = session['reset_professor_id']
    
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Validação das senhas
        if not new_password or not confirm_password:
            flash("Por favor, preencha todos os campos.", "error")
            return render_template('modificar/nova_senha.html')
            
        if new_password != confirm_password:
            flash("As senhas não coincidem.", "error")
            return render_template('modificar/nova_senha.html')
        
        try:
            # Criptografar a nova senha
            hashed_password = CriptografiaDePontaGrossa(new_password)
            
            # Atualizar a senha no banco de dados
            with db.engine.connect() as conn:
                conn.execute(
                    text("UPDATE professores SET senha_hash = :hashed_password WHERE id = :professor_id"),
                    {"hashed_password": hashed_password, "professor_id": professor_id}
                )
                conn.commit()  # Garantir que a transação seja confirmada
            
            # Limpar a sessão após a redefinição bem-sucedida
            session.pop('reset_professor_id', None)
            
            flash("Senha redefinida com sucesso! Faça login com sua nova senha.", "success")
            return redirect(url_for('bp_login.Login'))
            
        except Exception as e:
            flash(f"Ocorreu um erro ao redefinir a senha: {str(e)}", "error")
            return render_template('modificar/nova_senha.html')
    
    return render_template('modificar/nova_senha.html')
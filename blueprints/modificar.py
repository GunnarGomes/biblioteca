from flask import Blueprint, jsonify, render_template, request
from modules.DB import DB
from sqlalchemy import text

db = DB()

bp_modificar = Blueprint("bp_modificar", __name__, template_folder="templates", static_folder="static")

@bp_modificar.route('/user/modificar')
def Modificar():
    return render_template('modificar/modificar.html')

@bp_modificar.route('/user/get_alunos', methods=['GET'])
def get_alunos():
    alunos = db.DadosAlunos()
    lista_alunos = [{"id": aluno[0], "nome": aluno[1]} for aluno in alunos]  # Ajustado para lista de tuplas
    return jsonify(lista_alunos)

@bp_modificar.route('/user/get_aluno/<int:aluno_id>', methods=['GET'])
def get_aluno(aluno_id):
    with db.engine.connect() as conn:
        aluno = conn.execute(text("SELECT id, nome, email, serie FROM alunos WHERE id = :id"), {"id": aluno_id}).fetchone()
        if aluno:
            return jsonify({
                "id": aluno[0],
                "nome": aluno[1],
                "email": aluno[2],
                "serie": aluno[3]
            })
        return jsonify({"error": "Aluno não encontrado"}), 404

@bp_modificar.route('/user/editar_aluno/<int:aluno_id>', methods=['POST'])
def editar_aluno(aluno_id):
    # Captura os dados enviados pelo formulário
    nome = request.form.get('nome')
    email = request.form.get('email')
    serie = request.form.get('serie')

    # Verifica se os dados foram recebidos
    if not nome or not email or not serie:
        return jsonify({"status": "erro", "mensagem": "Todos os campos são obrigatórios!"}), 400

    try:
        # Atualiza os dados no banco de dados
        db.ModificarAluno(aluno_id, nome, email, serie)
        print(f"Aluno {aluno_id} atualizado: {nome}, {email}, {serie}")
        
        # Se a atualização for bem-sucedida
        return jsonify({"status": "sucesso", "mensagem": "Dados atualizados com sucesso!"})
    except Exception as e:
        # Caso ocorra algum erro no processo de atualização
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

# Método para modificar aluno


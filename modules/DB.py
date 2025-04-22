from sqlalchemy import create_engine, text
import hashlib
import os
from dotenv import load_dotenv
from flask import jsonify
from datetime import date, datetime

load_dotenv()


usr = os.getenv("USER")
pasword = os.getenv("PASSWORD")
hot = os.getenv("HOST")
por = os.getenv("PORT")
databas = os.getenv("DATABASE")

def CriptografiaDePontaGrossa(senha:str):
    md5Encrypt = hashlib.md5()
    md5Encrypt.update(senha.encode('utf-8'))
    return md5Encrypt.hexdigest()


class DB():
    def __init__(self):
        user = usr                # Usuario no mysql
        password = pasword            # Senha mega maneira, tiro isso depois
        host = hot              # Host, onde  ta hospedado meu server sql
        port = por             # Porta onde se acessa o mysql
        database = databas         #  Nome do banco de dados
        self.engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")
        
        try:
            with self.engine.connect() as conn:
                print("Conectado com sucesso!")
        except Exception as e:
            print(f"Erro ao conectar: {e}")

    def EsseUsuarioExiste(self, cpf, senha):
        senha = CriptografiaDePontaGrossa(senha)
        with self.engine.connect() as conn:
            try:
                result = conn.execute(
                    text("SELECT cpf, senha_hash FROM professores WHERE cpf = :cpf AND senha_hash = :senha"),
                    {"cpf": cpf, "senha": senha}
                ).fetchone()
                id = conn.execute(
                    text("SELECT id FROM professores WHERE cpf = :cpf AND senha_hash = :senha"),
                    {"cpf": cpf, "senha": senha}
                ).fetchone()
                if result:
                    
                    return True, id
                else:
                    print("Usuário não encontrado")
                    return False, None
            except Exception as e:
                print(f"Erro ao buscar usuário: {e}")
                return False, None
        
    def CadastroLivro(self,titulo,autor,isbn,data):
        try:
            with self.engine.connect() as conn:
                with conn.begin():
                        cad = conn.execute(
                            text("""INSERT INTO livros(titulo,autor,isbn,data_publicacao) VALUES (:titulo,:autor,:isbn,:data)"""),
                            {"titulo":titulo,"autor":autor,"isbn":isbn,"data":data})
                return {"status": "sucesso", "mensagem": "Livro cadastrado com sucesso!"}
        except Exception as e:
                    return {"status": "erro", "mensagem": str(e)}
        
    def cadastrar_aluno(self, nome, email, serie):
        try:
            with self.engine.connect() as conn:
                with conn.begin():  # Inicia a transação
                    conn.execute(
                        text("""INSERT INTO alunos (nome, email, serie) 
                                VALUES (:nome, :email, :serie)"""),
                        {"nome": nome, "email": email, "serie": serie}
                    )
            return {"status": "sucesso", "mensagem": "Aluno cadastrado!"}
        except Exception as e:
            return {"status": "erro", "mensagem": str(e)}
    def cadastrar_professor(self,nome,email,cpf,senha):
        try:
            with self.engine.connect() as conn:
                with conn.begin():  # Inicia a transação
                    conn.execute(
                        text("""INSERT INTO professores (nome, email, cpf, senha_hash) 
                                VALUES (:nome, :email, :cpf, :senha)"""),
                        {"nome": nome, "email": email, "cpf": cpf, "senha":CriptografiaDePontaGrossa(senha)}
                    )
            return {"status": "sucesso", "mensagem": "professor cadastrado!"}
        except Exception as e:
            return {"status": "erro", "mensagem": str(e)}
    def CadastrarEmprestimo(self,aluno_id,livro_id,professor_id,data_emprestimo,data_devolucao):
        with self.engine.connect() as conn:
             with conn.begin():
                  conn.execute(
                       text(""" 
                        INSERT INTO emprestimos(aluno_id,livro_id,professor_id,data_emprestimo,data_devolucao) 
                        VALUES (:aluno_id,:livro_id,:professor_id,:data_emprestimo,:data_devolucao)"""),
                       {"aluno_id":aluno_id,"livro_id":livro_id,"professor_id":professor_id,"data_emprestimo":data_emprestimo,"data_devolucao":data_devolucao}
                       )
    def DadosAlunos(self):
        with self.engine.connect() as conn:
             dados = conn.execute(text(""" SELECT id, nome FROM alunos"""))
             alunos = dados.fetchall()
             return alunos
        
    def DadosLivros(self):
        with self.engine.connect() as conn:
            dados = conn.execute(text(""" SELECT id, titulo FROM livros"""))
            livros = dados.fetchall()
            return livros
    def DadosEmprestimos(self):
        with self.engine.connect() as conn:
            # Consulta com JOIN, agora incluindo aluno_id
            query = text("""
                SELECT emprestimos.id,
                    alunos.id AS aluno_id,
                    alunos.nome,
                    livros.titulo,
                    DATE_FORMAT(emprestimos.data_emprestimo, '%d/%m/%Y') AS data_emprestimo,
                    DATE_FORMAT(emprestimos.data_devolucao, '%d/%m/%Y') AS data_devolucao,
                    emprestimos.status,
                    professores.nome
                FROM emprestimos
                JOIN alunos ON emprestimos.aluno_id = alunos.id
                JOIN livros ON emprestimos.livro_id = livros.id
                JOIN professores ON emprestimos.professor_id = professores.id
            """)

            result = conn.execute(query).fetchall()

            # Lista de dicionários com os dados
            emp = [{"id_emprestimo": row[0],
                    "aluno_id": row[1],
                    "aluno": row[2], 
                    "livro": row[3],
                    "dtemp": row[4],
                    "dtenv": row[5],
                    "status": row[6],
                    "prof": row[7]} for row in result if row[6] != 1]

            for dados in emp:
                data_devolucao = datetime.strptime(dados["dtenv"], "%d/%m/%Y").date()
                if date.today() > data_devolucao:
                    with self.engine.connect() as con:
                        with con.begin():
                            con.execute(
                                text("UPDATE emprestimos SET status=3 WHERE aluno_id = :aluno_id AND status != 1"),
                                {"aluno_id": dados["aluno_id"]}
                            )

            return emp
    def Devolucao(self, id_emprestimo):
        with self.engine.connect() as conn:
            try:
                with conn.begin():  # Inicia a transação
                    conn.execute(text(""" UPDATE emprestimos SET status = 1 WHERE id = :id """), {'id': id_emprestimo})
                # Se o código chegar aqui, a transação foi concluída com sucesso
                print("Empréstimo devolvido com sucesso!")
            except Exception as e:
                # Se houver algum erro durante o UPDATE, a transação será revertida
                print(f"Ocorreu um erro: {e}")
    def ModificarAluno(self, aluno_id, nome, email, serie):
        with self.engine.connect() as conn:
            try:
                # Executa a atualização dos dados do aluno
                with conn.begin():
                    conn.execute(
                        text("""UPDATE alunos SET nome = :nome, email = :email, serie = :serie WHERE id = :id"""),
                        {"id": aluno_id, "nome": nome, "email": email, "serie": serie}
                    )
            except Exception as e:
                print(f"Ocorreu um erro: {e}")  # Log de erro
    def deletar_aluno(self, aluno_id):
        with self.engine.connect() as conn:
            try:
                with conn.begin():
                    conn.execute(
                        text("DELETE FROM alunos WHERE id = :id"),
                        {"id": aluno_id}
                    )
                return {"status": "sucesso", "mensagem": "Aluno deletado com sucesso!"}
            except Exception as e:
                print(f"Erro ao deletar aluno: {e}")
                return {"status": "erro", "mensagem": str(e)}

if __name__ == '__main__':
    db = DB()
    db.DadosEmprestimos()
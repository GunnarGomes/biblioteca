import requests

class API():
    def __init__(self, cod='', titulo=''):
        self.dados = []

        if cod:
            link = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{cod}'
        elif titulo:
            titulo = titulo.replace(' ', '+')
            link = f"https://www.googleapis.com/books/v1/volumes?q={titulo}"
        else:
            raise ValueError("É necessário fornecer um código ISBN ou um título.")

        self.resp = requests.get(link)
        self.data = self.resp.json()

        if "items" in self.data:
            self.dados = self.data["items"]

    def listar_livros(self):
        livros = []
        for livro in self.dados:
            info = livro["volumeInfo"]
            isbn_list = info.get("industryIdentifiers", [])
            isbn = next((id["identifier"] for id in isbn_list if id["type"] == "ISBN_13"), "ISBN desconhecido")

            livros.append({
                "titulo": info.get("title", "Título desconhecido"),
                "autores": ", ".join(info.get("authors", ["Autor desconhecido"])),
                "publicacao": info.get("publishedDate", "Data desconhecida"),
                "descricao": info.get("description", "Sem descrição disponível"),
                "isbn": isbn
            })
        return livros
    

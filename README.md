# URL-SHORTENER-API
---
Uma API para encurtar URLs, construída com FastAPI e SQLAlchemy.

## Funcionalidades
- Encurtamento de URLs
- Geração de códigos únicos para URLs encurtadas
- Redirecionamento para a URL original
- Armazenamento em banco de dados SQL
- Remoção de URLs encurtadas após 7 dias
- Documentação automática com Swagger UI

## Tecnologias Utilizadas
- Backend: Python 3.12, FastAPI
- ORM: SQLAlchemy
- Banco de dados: Postgres (pode ser substituído por outro banco de dados MySql/MariaDB)
- Servidor: Uvicorn

## Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/Everton-Renan/url-shortener-api.git
    cd url-shortener-api
    ```
2. Crie um ambiente virtual e ative-o:
   ```bash
    python3 -m venv venv # Unix
    python -m venv venv # Windows

    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   ```
3. Instale as dependências:
   ```bash
    pip3 install -r requirements.txt # Unix
    pip install -r requirements.txt # Windows
   ```
4. Configure o arquivo `.env`:
   - Renomeie o arquivo `.env-example` para `.env` na raiz do projeto.

5. Configure o banco de dados:
    - Certifique-se de ter um banco de dados Postgres (Mysql/MariaDB) em execução.
    - Atualize a string de conexão do banco de dados no arquivo `.env` conforme necessário.
    - Crie as tabelas do banco de dados executando o script de criação de tabelas: init_db.py
   ```bash
    python3 init_db.py # Unix
    python init_db.py # Windows
   ```
6. Inicie o servidor FastAPI:
   ```bash
    uvicorn main:app --reload
   ```
   ou
    ```bash
     fastapi dev main.py
    ```
7. Acesse a documentação da API em:
   ```
   http://127.0.0.1:8000/docs
   ```

## Uso
- Encurtar uma URL:
  - Faça uma requisição POST para `/shorten` contendo a URL original.
  - exemplo de requisição:
    ```
        http://127.0.0.1:8000/shorten?url=https://www.exemplo.com
    ```
  - A resposta conterá a URL encurtada.

- Redirecionar para a URL original:
  - Acesse a URL encurtada no navegador.
  - exemplo:
    ```
        http://127.0.0.1:8000/abc123
    ```
  - Caso a url exista, você será redirecionado para a URL original.

- Remoção automática:
  - URLs encurtadas serão removidas automaticamente após 7 dias.
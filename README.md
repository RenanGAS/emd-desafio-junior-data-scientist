## Instruções de Execução

### Para execução dos arquivos `analise_sql.sql` e `analise_python.ipynb`

- As soluções em **SQL** podem ser executadas na plataforma **BigQuery**
    - Passo a passo em [docs.dados.rio](https://docs.dados.rio/tutoriais/como-acessar-dados/)

- As soluções em **Python** no **Jupyter Notebook** podem ser executadas na plataforma **Google Colab**
    - Com a realização do passo a passo em [docs.dados.rio](https://docs.dados.rio/tutoriais/como-acessar-dados/), basta alterar
    o parâmetro `billing_project_id` nas quatro `queries`, para o `Id` do projeto criado no **Google Cloud Platform**.
    - Deve-se aceitar os termos de uso e autorizar o acesso à conta no **Google** para executar as consultas.

### Para execução local do App Streamlit

- `python3 -m venv env`
- `source env/bin/activate`
- `pip3 install -r requirements.txt`
- `streamlit run Inicio.py --server.enableCORS false --server.enableXsrfProtection false`

### Página web

- Link: [emd-desafio-renangas](https://emd-desafio-renangas.streamlit.app/)
from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd

# Criano nossa "aplicação" e colocando-a em uma váriavel para referencia-la
app = Dash()
# Adicionamos nossa base de dados dentro de uma váriavel para referncia-la
df = pd.read_excel("Vendas.xlsx")

# Criando um grafico
fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")

# Variavel que sera usada no dropdown
opcoes = list(df["ID Loja"].unique())        # Explicação: Criamos uma variavel chamada opções, nessa váriavel inserimos uma lista 
opcoes.append("Todas as Lojas")              # e nessa lista inserimos nossa base de dados
# ^ Adiconamos mais 1 opção ao Dropdown      # tendo nossa base de dados definida "df" podemos selecionar a coluna que dejesamos no caso "ID Loja" dentro de [...]
                                             # e utilizando a função .unique() para não trazer opções repetidas

# Criando nossa interface
app.layout = html.Div(children=[ 
    # Utilizamos a nossa "aplicação" como referência e utilizamos a função layout para criarmos uma DIV em html                                          
    html.H1(children='Faturamento das lojas'),
    # Ja dentro da nossa DIV em html criamos um H1 (Titulo) e com a palavra reservada children passamos uma "string" como sendo o titulo do texto
    html.H2(children='grafico com total de produtos vendidos separados por lojas'),
    # Criamos uma segunda DIV e passamos a ela uma "string" como sendo nosso texto
    html.Div(id = "div_texto"),

    # Inserindo um "filtro" dropdown
    dcc.Dropdown(opcoes, value = "Todas as Lojas",id = "lista_lojas"),

    # Inserindo o grafico no DOM
    dcc.Graph(
        id='grafico_quantidade_vendas',
        figure= fig
    )
])

# Função de callback
@app.callback(
    Output('grafico_quantidade_vendas', 'figure'),  # Valores que serão alterado na "Saida"
    Input('lista_lojas', 'value')                   # Valores de entrada
)
def update_output(value):      # Utilizando a função de callback
    if value == "Todas as Lojas":  # Estrutura condicional IF/ELSE
        fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    else: 
        tabela_filtrada = df.loc[df["ID Loja"] == value, :] # Filtrando a tabela com .loc 
        fig = px.bar(tabela_filtrada, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    return fig

if __name__ == '__main__':
    app.run(debug=True)
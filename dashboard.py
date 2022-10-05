#%%
# importações
import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

#%%
# dataset_candidatos
df = pd.read_csv('dados/consulta_cand_2022_BRASIL.csv', delimiter=';', encoding='latin-1')
# copia de dataset
cand_df = df.copy()
cand_df.head(2)

#%%
df_bens = pd.read_csv('dados/bem_candidato_2022_BRASIL.csv', delimiter=';', encoding='latin-1')
bens_df = df_bens.copy()
bens_df.head(2)

#%%
# Remover as colunas desnecessarias
drop_cols  = [
    'DT_GERACAO', 'HH_GERACAO', 'ANO_ELEICAO', 'CD_TIPO_ELEICAO',
    'NM_TIPO_ELEICAO', 'NR_TURNO', 'CD_ELEICAO', 'DS_ELEICAO', 'DT_ELEICAO',
    'TP_ABRANGENCIA', 'NM_SOCIAL_CANDIDATO', 'NR_CPF_CANDIDATO', 'NM_EMAIL',
    'CD_SITUACAO_CANDIDATURA', 'DS_SITUACAO_CANDIDATURA',
    'CD_DETALHE_SITUACAO_CAND', 'DS_DETALHE_SITUACAO_CAND', 'TP_AGREMIACAO',
    'NR_PARTIDO', 'SG_PARTIDO', 'NR_FEDERACAO', 'NM_FEDERACAO', 'SG_FEDERACAO', 'DS_COMPOSICAO_FEDERACAO',
    'SQ_COLIGACAO', 'NM_COLIGACAO', 'DS_COMPOSICAO_COLIGACAO', 'CD_NACIONALIDADE',
    'DS_NACIONALIDADE', 'CD_MUNICIPIO_NASCIMENTO', 'NM_MUNICIPIO_NASCIMENTO', 'DT_NASCIMENTO',
    'NR_IDADE_DATA_POSSE', 'NR_TITULO_ELEITORAL_CANDIDATO',  'CD_ESTADO_CIVIL', 'DS_ESTADO_CIVIL',
    'CD_OCUPACAO', 'DS_OCUPACAO', 'VR_DESPESA_MAX_CAMPANHA',
    'CD_SIT_TOT_TURNO', 'DS_SIT_TOT_TURNO', 'ST_REELEICAO', 'ST_DECLARAR_BENS', 'NR_PROTOCOLO_CANDIDATURA', 'NR_PROCESSO',
    'CD_SITUACAO_CANDIDATO_PLEITO', 'DS_SITUACAO_CANDIDATO_PLEITO',
    'CD_SITUACAO_CANDIDATO_URNA', 'DS_SITUACAO_CANDIDATO_URNA',
    'ST_CANDIDATO_INSERIDO_URNA', 'NM_TIPO_DESTINACAO_VOTOS',
    'CD_SITUACAO_CANDIDATO_TOT', 'DS_SITUACAO_CANDIDATO_TOT',
    'ST_PREST_CONTAS'
]
cand_df = cand_df.drop(drop_cols, axis = 1)
cand_df.head(3)

#%%
drop_cols_bens = ['DT_GERACAO', 'HH_GERACAO', 'ANO_ELEICAO', 'CD_TIPO_ELEICAO',
       'NM_TIPO_ELEICAO', 'CD_ELEICAO', 'DS_ELEICAO', 'DT_ELEICAO',
       'SG_UE', 'NM_UE', 'NR_ORDEM_CANDIDATO',
       'DT_ULTIMA_ATUALIZACAO', 'HH_ULTIMA_ATUALIZACAO']
bens_df = bens_df.drop(drop_cols_bens, axis = 1)
bens_df.head(3)

#%%
#mescla os dois datasets
geral_df = cand_df.merge(bens_df, on='SQ_CANDIDATO', how='left')
# transforma valores substitui , por . e faz conversão pra  tipo numerico:
geral_df['VR_BEM_CANDIDATO'] = geral_df['VR_BEM_CANDIDATO'].str.replace(',','.')
geral_df['VR_BEM_CANDIDATO'] = pd.to_numeric(geral_df['VR_BEM_CANDIDATO'])
# geral_df['VR_BEM_CANDIDATO'] = geral_df['VR_BEM_CANDIDATO'].astype(float)
geral_df['VR_BEM_CANDIDATO'].head(3)

#%%
# seleciona somente os dados dos 3 estados escolhidos:
ufs = ['PI', 'MA', 'CE']

bens_df = bens_df[bens_df['SG_UF'].isin(ufs)]
cand_df = cand_df[cand_df['SG_UF'].isin(ufs)]
geral_df = geral_df[geral_df['SG_UF_x'].isin(ufs)]

#%%
# tema de cores
colors = {
    'background': '#1e434a',
    'text': '#7FDBFF'
}

#%%
# Criar a aplicação
#https://www.bootstrapcdn.com/bootswatch/
#https://hackerthemes.com/bootstrap-cheatsheet/
app = dash.Dash(
                    __name__,
                    external_stylesheets = [dbc.themes.COSMO],
                    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}]
                )

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H3('Dashboard - Eleições 2022',
            className = 'text-center text-primary, display-2 shadow'), width = 20
        )
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Checklist(id = 'checks-estados',
                value = ufs,
                options = [
                    {'label': x , 'value': x}
                    for x in cand_df['SG_UF'].unique()
                    ] 
            )]
        )
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = 'bar-fig-cargos', figure = {})
            ], width = {'size':6, 'order':1 }
        ),
        dbc.Col([
            dcc.Graph(id = 'bar-fig-cargos-genero', figure = {})
            ], width = {'size':6, 'order':1 }
        )
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = 'bar-fig-cargos-raca', figure = {})
            ], width = {'size':6, 'order':1 }
        ),
        dbc.Col([
            dcc.Graph(id = 'bar-fig-escolaridade', figure = {})
            ], width = {'size':6, 'order':1 }
        )
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = 'bar-fig-bens-partido', figure = {})
            ], width = {'size':12, 'order':1 }
        )
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id = 'dropdown-candidato',
                                multi = True,
                                value = [],
                                options = [
                                    {'label': x , 'value': x}
                                    for x in geral_df['NM_CANDIDATO'].unique()
                                   ] ),
            dcc.Graph(id = 'bar-fig-bem-candidato', figure = {})
            ], width = {'size':12, 'order':1 }
        )
    ])

], fluid=True)

@app.callback(
    Output('bar-fig-cargos', 'figure'),
    Input('checks-estados', 'value')
)

def update_chart_cargos(estados_selecionados):
    dff = cand_df[cand_df['SG_UF'].isin(estados_selecionados)]
    figbar = px.bar(dff['DS_CARGO'].value_counts(),
                    orientation = 'v',
                    title= 'Quantidade de candidatos por Cargos',
                    color_discrete_sequence = ['#33a5ee'])

    figbar.update_xaxes(showgrid=False)
    figbar.update_yaxes(showgrid=False)

    figbar.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
                        )
    return figbar

@app.callback(
    Output('bar-fig-cargos-genero', 'figure'),
    Input('checks-estados', 'value')
)

def update_chart_cargos_por_genero(estados_selecionados):
    dff = cand_df[cand_df['SG_UF'].isin(estados_selecionados)]
    cargos_por_genero_df = dff.groupby(['DS_CARGO','DS_GENERO'])[['SQ_CANDIDATO']].count()
    cargos_por_genero_df.reset_index(inplace=True)

    figbar = px.bar(
                cargos_por_genero_df, 
                x='DS_CARGO', y='SQ_CANDIDATO',
                color= 'DS_GENERO',
                title= 'Quantidade de cargos por gênero'
            )

    figbar.update_xaxes(showgrid=False)
    figbar.update_yaxes(showgrid=False)

    figbar.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
                        )
    return figbar

@app.callback(
    Output('bar-fig-cargos-raca', 'figure'),
    Input('checks-estados', 'value')
)

def update_chart_cargos_por_raca(estados_selecionados):
    
    dff = cand_df[cand_df['SG_UF'].isin(estados_selecionados)]
    cargos_por_raca_df = dff.groupby(['DS_CARGO','DS_COR_RACA'])[['SQ_CANDIDATO']].count()
    cargos_por_raca_df.reset_index(inplace=True)

    figbar = px.bar(
                cargos_por_raca_df, 
                x='DS_CARGO', y='SQ_CANDIDATO',
                title= 'Quantidade de cargos por raça',
                color= 'DS_COR_RACA'
            )

    figbar.update_xaxes(showgrid=False)
    figbar.update_yaxes(showgrid=False)

    figbar.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
                        )
    return figbar

@app.callback(
    Output('bar-fig-escolaridade', 'figure'),
    Input('checks-estados', 'value')
)

def update_chart_escolaridade(estados_selecionados):
    
    dff = cand_df[cand_df['SG_UF'].isin(estados_selecionados)]
    figbar = px.bar(
                dff['DS_GRAU_INSTRUCAO'].value_counts(),
                title= 'Escolaridade dos candidatos' ,
                color_discrete_sequence = ['#33a5ee']
            )

    figbar.update_xaxes(showgrid=False)
    figbar.update_yaxes(showgrid=False)

    figbar.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
                        )
    return figbar

@app.callback(
    Output('bar-fig-bens-partido', 'figure'),
    Input('checks-estados', 'value')
)

def update_chart_bens_partidos(estados_selecionados):
    
    dff = geral_df[geral_df['SG_UF_x'].isin(estados_selecionados)]
    bens_por_partido_df = dff.groupby(['NM_PARTIDO'])[['VR_BEM_CANDIDATO']].sum()
    bens_por_partido_df.reset_index(inplace=True)

    figbar = px.bar(
                bens_por_partido_df, 
                x='NM_PARTIDO', y='VR_BEM_CANDIDATO',
                title= 'Valor de bens por partido',
                color_discrete_sequence = ['#33a5ee']
            )

    figbar.update_xaxes(showgrid=False)
    figbar.update_yaxes(showgrid=False)

    figbar.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
                        )
    return figbar

@app.callback(
    Output('bar-fig-bem-candidato', 'figure'),
    [Input('checks-estados', 'value'),
    Input('dropdown-candidato', 'value')]
)

def update_chart_bens_partidos(estados_selecionados, candidatos):
    
    dff = geral_df[geral_df['SG_UF_x'].isin(estados_selecionados)]
    dff = dff[dff['NM_CANDIDATO'].isin(candidatos)]
    bens_por_candidato_df = dff.groupby(['NM_CANDIDATO'])[['VR_BEM_CANDIDATO']].sum()
    bens_por_candidato_df.reset_index(inplace=True)

    figbar = px.bar(
                bens_por_candidato_df, 
                x='NM_CANDIDATO', y='VR_BEM_CANDIDATO',
                title= 'Valor de bens por candidato',
                color_discrete_sequence = ['#33a5ee']
            )

    figbar.update_xaxes(showgrid=False)
    figbar.update_yaxes(showgrid=False)

    figbar.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
                        )
    return figbar

# %%
if __name__ == '__main__':
  app.run_server(debug=True, port=8006)

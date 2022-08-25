from cProfile import label
from pydoc import classname
from turtle import title
import pandas as pd
import pymysql
import numpy as np
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

try:
    df = pd.read_sql_table('cliente','mysql+pymysql://root:123456@localhost:3306/TCC')
    df = df.drop(["id","nomec","cpf"], axis=1)
    scaler = MinMaxScaler()
    clf = [0,0]
    result = [0,0]
except:
    pass

def startNN():

    #Datas
    datas = [df.copy(deep=True),df.copy(deep=True)]
    X_resampled, y_resampled = SMOTE(random_state=1,k_neighbors=4).fit_resample(datas[0].drop('payment',axis=1),datas[0]['payment'])
    dataSM = X_resampled.assign(payment = y_resampled)
    datas[1] = dataSM


    #escalagem dos dados
    cols = range(0,23)
    

    for data in datas:
        # for i in cols:
        #     data[data.columns[i]] = scaler.fit_transform(data[data.columns[i]].values.reshape(-1, 1))
        data[data.columns[cols]] = scaler.fit_transform(data[data.columns[cols]])

    #classificador
    i=0   

    for data in datas:
        features = data.drop('payment',axis=1)
        label = data['payment']
        X_train, X_test, y_train, y_test = train_test_split(features, label, test_size=0.3, random_state=1)
        model = MLPClassifier(alpha=0.05,hidden_layer_sizes=(12,6,2),activation='tanh', max_iter=250, random_state=1)
        model.fit(X_train.values,y_train.values)
        clf[i]=model
        result[i] = model.score(X_test.values,y_test.values)
        i+=1


def returnresult():
    pass
    return result


def predict(values):
    if hasattr(scaler, "n_features_in_"):
        values = scaler.transform(np.reshape(values,(1,-1)))
        res = clf[0].predict(values)
    else:
        startNN()
        values = scaler.transform(np.reshape(values,(1,-1)))
        res = clf[0].predict(values)
    return (res[0])


from dash import dcc, html
from django_plotly_dash import DjangoDash

from dash import Dash, Input, Output
import plotly.express as px

from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

import plotly.graph_objects as go

def newLegend(fig, newNames):
    novovet = list(map(str,fig.data[0].labels))
    for item in newNames:
        for i, elem in enumerate(fig.data[0].labels):
            if str(elem) == item:
                novovet[i] = newNames[item]
    fig.data[0].labels=novovet
    return(fig)

def dashboard():
    
    app = DjangoDash('dashboard', add_bootstrap_links=True)   # replaces dash.Dash


    fig00 = go.Figure(data=[go.Pie(labels=df['sex'])])
    fig00.update_traces(hoverinfo='label+value',textposition='inside', textinfo='percent',textfont_size=20)
    fig00.update_layout(title_text="Gênero",autosize=False, title_x=0.5, width=500, height=500)
    fig00 = newLegend(fig00,{"2": "Feminino","1": "Masculino"})

    fig01 = go.Figure(data=[go.Pie(labels=df['education'])])
    fig01.update_traces(hoverinfo='label+value',textposition='inside', textinfo='percent',textfont_size=20)
    fig01.update_layout(title_text="Educação",autosize=False, title_x=0.5, width=500, height=500)
    fig01.update_layout(title_text="Grau de Instrução",autosize=False, width=500, height=500)
    fig01 = newLegend(fig01,{"1": "Pós Graduado", "2": "Graduado","3": "Ensino Médio","4": "Outros"})

    fig02 = go.Figure(data=[go.Pie(labels=df['marriage'])])
    fig02.update_traces(hoverinfo='label+value',textposition='inside', textinfo='percent',textfont_size=20)
    fig02.update_layout(title_text="Estado Civil",autosize=False, title_x=0.5, width=500, height=500)
    fig02 = newLegend(fig02,{"1": "Casado", "2": "Solteiro","3": "Outros"})

    fig03 = go.Figure(data=[go.Pie(labels=df['payment'])])
    fig03.update_traces(hoverinfo='label+value',textposition='inside', textinfo='percent',textfont_size=20)
    fig03.update_layout(title_text="Clientes",autosize=False, width=500, height=500)
    fig03 = newLegend(fig03,{"0": "Adimplentes", "1": "Inadimplentes"})

    
    fig04 = go.Figure()
    fig04.add_trace(go.Bar(x=['Masculino','Feminino'],y=[df[df['sex'] == 1].loc[df['payment'] == 0]['sex'].count(),df[df['sex'] == 2].loc[df['payment'] == 0]['sex'].count()], name='Adimplente'))
    fig04.add_trace(go.Bar(x=['Masculino','Feminino'],y=[df[df['sex'] == 1].loc[df['payment'] == 1]['sex'].count(),df[df['sex'] == 2].loc[df['payment'] == 1]['sex'].count()], name='Inadimplente'))
    fig04.update_layout(title_text="Honra por Gênero",autosize=False, barmode='group', width=500, height=500)

    fig05 = go.Figure()

    fig11 = go.Figure()
    fig11.add_trace(go.Histogram(x=df['age'].loc[df['payment'] == 0], name='Adimplente'))
    fig11.add_trace(go.Histogram(x=df['age'].loc[df['payment'] == 1], name='Inadimplente'))
    fig11.update_layout(barmode='overlay', title_text="Pagamentos por Faixa Etária", xaxis_title_text='Faixa Etária', yaxis_title_text='Contagem', title_x=0.5)


    app.layout = html.Div([ #MAIN DIV
            html.Div([
                html.H1(['Análise dos Dados'], style={'textAlign': 'center', 'padding-top':'7 px'})
            ]),

            html.Div([ ### FIGURES Divs
                html.Div([
                    dcc.Graph(figure = fig00),
                ], className = 'col-sm'),
                html.Div([
                    dcc.Graph(figure = fig01),
                ], className = 'col-sm'),
                html.Div([
                    dcc.Graph(figure = fig02),
                ], className = 'col-sm'),
                html.Div([
                    dcc.Graph(figure = fig03),
                ], className = 'col-sm'),
                html.Div([
                    dcc.Graph(figure = fig04),
                ], className = 'col-sm'),
                html.Div([
                    dcc.Graph(figure = fig05),
                ], className = 'col-sm'),
            ], className = 'row'),

            html.Div([ ### FIGURES Divs
                 html.Div([
                    dcc.Graph(figure = fig11),
                ], className = 'col-sm'),
            ], className = 'row'),

        ], className='main')

    
    #app.run_server(debug=True)

    # @app.callback(
    #     dash.dependencies.Output('output-color', 'children'),
    #     [dash.dependencies.Input('dropdown-color', 'value')])
    # def callback_color(dropdown_value):
    #     return "The selected color is %s." % dropdown_value

    # @app.callback(
    #     dash.dependencies.Output('output-size', 'children'),
    #     [dash.dependencies.Input('dropdown-color', 'value'),
    #     dash.dependencies.Input('dropdown-size', 'value')])
    # def callback_size(dropdown_color, dropdown_size):
    #     return "The chosen T-shirt is a %s %s one." %(dropdown_size,
    #                                                 dropdown_color)

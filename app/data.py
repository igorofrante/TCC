import pandas as pd
import pymysql
import numpy as np
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression

try:
    df = pd.read_sql_table('cliente','mysql+pymysql://root:123456@localhost:3306/TCC')
    df = df.drop(["id","nomec","cpf"], axis=1)
    scaler = MinMaxScaler()
    clf = [0,0,0,0]
    result = [0,0,0,0]
except:
    pass

def startNN():
    df = pd.read_sql_table('cliente','mysql+pymysql://root:123456@localhost:3306/TCC')
    df = df.drop(["id","nomec","cpf"], axis=1)
    #Datas
    datas = [df.copy(deep=True),df.copy(deep=True)]
    X_resampled, y_resampled = SMOTE(random_state=1,k_neighbors=4).fit_resample(datas[0].drop('payment',axis=1),datas[0]['payment'])
    dataSM = X_resampled.assign(payment = y_resampled)
    datas[1] = dataSM

    #escalagem dos dados
    cols = range(0,23)
    
    for data in datas:
        data[data.columns[cols]] = scaler.fit_transform(data[data.columns[cols]])

    #classificador
    i=0   

    for data in datas:
        features = data.drop('payment',axis=1)
        label = data['payment']
        X_train, X_test, y_train, y_test = train_test_split(features, label, test_size=0.3, random_state=1)
        model = MLPClassifier(random_state=1)
        model.fit(X_train.values,y_train.values)
        clf[i]=model
        result[i] = model.score(X_test.values,y_test.values)
        i+=1

def startLR():
    df = pd.read_sql_table('cliente','mysql+pymysql://root:123456@localhost:3306/TCC')
    df = df.drop(["id","nomec","cpf"], axis=1)
    #Datas
    datas = [df.copy(deep=True),df.copy(deep=True)]
    X_resampled, y_resampled = SMOTE(random_state=1,k_neighbors=4).fit_resample(datas[0].drop('payment',axis=1),datas[0]['payment'])
    dataSM = X_resampled.assign(payment = y_resampled)
    datas[1] = dataSM

    #escalagem dos dados
    cols = range(0,23)
    
    for data in datas:
        data[data.columns[cols]] = scaler.fit_transform(data[data.columns[cols]])

    #classificador
    i=2   

    for data in datas:
        features = data.drop('payment',axis=1)
        label = data['payment']
        X_train, X_test, y_train, y_test = train_test_split(features, label, test_size=0.3, random_state=1)
        model = LogisticRegression(random_state=1)
        model.fit(X_train.values,y_train.values)
        clf[i]=model
        result[i] = model.score(X_test.values,y_test.values)
        i+=1

def returnresult():
    pass
    return result


def predict(values):
    res = [0,0]
    if hasattr(scaler, "n_features_in_"):
        values = scaler.transform(np.reshape(values,(1,-1)))
        res[0] = clf[1].predict(values)[0]
        res[1] = clf[2].predict(values)[0] 
    else:
        print('inicializando')
        startNN()
        print('rede neural executada')
        startLR()
        print('regressao logistica executada')
        values = scaler.transform(np.reshape(values,(1,-1)))
        res[0] = clf[1].predict(values)[0]
        res[1] = clf[2].predict(values)[0] 
    return (res)


from dash import dcc, html
from django_plotly_dash import DjangoDash
from dash import  dcc, html
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
    fig00.update_traces(hoverinfo='label+value',textposition='inside', textinfo='percent',textfont_size=20,marker=dict(colors=['hotpink'], line=dict(color='#000000', width=2)))
    fig00.update_layout(title_text="Gênero",autosize=False, title_x=0.5, width=500, height=500)
    fig00 = newLegend(fig00,{"2": "Feminino","1": "Masculino"})

    fig01 = go.Figure(data=[go.Pie(labels=df['education'])])
    fig01.update_traces(hoverinfo='label+value',textposition='inside', textinfo='percent',textfont_size=20,marker=dict(line=dict(color='#000000', width=2)))
    fig01.update_layout(title_text="Educação",autosize=False, title_x=0.5, width=500, height=500)
    fig01.update_layout(title_text="Grau de Instrução",autosize=False, width=500, height=500)
    fig01 = newLegend(fig01,{"1": "Pós Graduado", "2": "Graduado","3": "Ensino Médio","4": "Outros"})

    fig02 = go.Figure(data=[go.Pie(labels=df['marriage'])])
    fig02.update_traces(hoverinfo='label+value',textposition='inside', textinfo='percent',textfont_size=20,marker=dict(line=dict(color='#000000', width=2)))
    fig02.update_layout(title_text="Estado Civil",autosize=False, title_x=0.5, width=500, height=500)
    fig02 = newLegend(fig02,{"1": "Casado", "2": "Solteiro","3": "Outros"})

    fig03 = go.Figure(data=[go.Pie(labels=df['payment'])])
    fig03.update_traces(hoverinfo='label+value',textposition='inside', textinfo='percent',textfont_size=20,marker=dict(line=dict(color='#000000', width=2)))
    fig03.update_layout(title_text="Clientes",autosize=False, width=500, height=500)
    fig03 = newLegend(fig03,{"0": "Adimplentes", "1": "Inadimplentes"})
    
    fig04 = go.Figure()
    fig04.add_trace(go.Bar(x=['Masculino','Feminino'],y=[df[df['sex'] == 1].loc[df['payment'] == 0]['sex'].count(),df[df['sex'] == 2].loc[df['payment'] == 0]['sex'].count()], name='Adimplente',marker=dict(line=dict(color='#000000', width=2))))
    fig04.add_trace(go.Bar(x=['Masculino','Feminino'],y=[df[df['sex'] == 1].loc[df['payment'] == 1]['sex'].count(),df[df['sex'] == 2].loc[df['payment'] == 1]['sex'].count()], name='Inadimplente',marker=dict(line=dict(color='#000000', width=2))))
    fig04.update_layout(title_text="Situação por Gênero", autosize=False, barmode='group', width=500, height=500)

    fig05 = go.Figure()
    fig05.add_trace(go.Bar(x=['Pós-graduado', 'Graduado', 'Ensino médio', 'Outros'],
                            y=[df[df['education'] == 1].loc[df['payment'] == 0]['education'].count(),
                               df[df['education'] == 2].loc[df['payment'] == 0]['education'].count(),
                               df[df['education'] == 3].loc[df['payment'] == 0]['education'].count(),
                               df[df['education'] == 4].loc[df['payment'] == 0]['education'].count()], name='Adimplente',marker=dict(line=dict(color='#000000', width=2))))
    fig05.add_trace(go.Bar(x=['Pós-graduado', 'Graduado', 'Ensino médio', 'Outros'],
                            y=[df[df['education'] == 1].loc[df['payment'] == 1]['education'].count(),
                               df[df['education'] == 2].loc[df['payment'] == 1]['education'].count(),
                               df[df['education'] == 3].loc[df['payment'] == 1]['education'].count(),
                               df[df['education'] == 4].loc[df['payment'] == 1]['education'].count()], name='Inadimplente',marker=dict(line=dict(color='#000000', width=2))))
    fig05.update_layout(title_text="Situação por Grau de Instrução", autosize=False, barmode='group', width=600, height=500)

    fig06 = go.Figure()
    fig06.add_trace(go.Bar(x=['Casado', 'solteiro', 'Outros'],
                            y=[df[df['marriage'] == 1].loc[df['payment'] == 0]['marriage'].count(),
                               df[df['marriage'] == 2].loc[df['payment'] == 0]['marriage'].count(),
                               df[df['marriage'] == 3].loc[df['payment'] == 0]['marriage'].count()], name='Adimplente',marker=dict(line=dict(color='#000000', width=2))))
    fig06.add_trace(go.Bar(x=['Casado', 'solteiro', 'Outros'],
                            y=[df[df['marriage'] == 1].loc[df['payment'] == 1]['marriage'].count(),
                               df[df['marriage'] == 2].loc[df['payment'] == 1]['marriage'].count(),
                               df[df['marriage'] == 3].loc[df['payment'] == 1]['marriage'].count()], name='Inadimplente',marker=dict(line=dict(color='#000000', width=2))))
    fig06.update_layout(title_text="Situação por Estado Civil", autosize=False, barmode='group', width=600, height=500)

    fig11 = go.Figure()
    fig11.add_trace(go.Histogram(x=df['age'].loc[df['payment'] == 0], name='Adimplente',marker=dict(line=dict(color='#000000', width=2))))
    fig11.add_trace(go.Histogram(x=df['age'].loc[df['payment'] == 1], name='Inadimplente',marker=dict(line=dict(color='#000000', width=2))))
    fig11.update_layout(barmode='overlay', title_text="Pagamentos por Faixa Etária", xaxis_title_text='Faixa Etária', yaxis_title_text='Contagem', title_x=0.5,width=800)

    app.layout = html.Div([ #MAIN DIV
            html.Div([
                html.H1(['Painel'], style={'textAlign': 'center', 'padding-top':'7 px'})
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
                html.Div([
                    dcc.Graph(figure = fig06),
                ], className = 'col-sm'),
            ], className = 'row'),

            html.Div([ ### FIGURES Divs
                 html.Div([
                    dcc.Graph(figure = fig11),
                ], className = 'col-sm'),
            ], className = 'row'),

        ], className='main')

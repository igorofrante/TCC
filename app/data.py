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
    result = [0,0]
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
    app = DjangoDash('main', add_bootstrap_links=True)   # replaces dash.Dash

    fig0 = go.Figure(data=[go.Pie(labels=df['sex'])])
    fig0.update_traces(hoverinfo='label+value',textposition='inside', textinfo='percent',textfont_size=20)
    fig0.update_layout(title_text="Gênero",autosize=False, width=500, height=500)
    fig0 = newLegend(fig0,{"1": "Feminino", "2": "Masculino"})

    fig1 = go.Figure(data=[go.Pie(labels=df['education'])])
    fig1.update_traces(hoverinfo='label+value',textposition='inside', textinfo='percent',textfont_size=20)
    fig1.update_layout(title_text="Grau de Instrução",autosize=False, width=500, height=500)
    fig1 = newLegend(fig1,{"1": "Pós Graduado", "2": "Graduado","3": "Ensino Médio","4": "Outros"})

    fig2 = go.Figure(data=[go.Pie(labels=df['marriage'])])
    fig2.update_traces(hoverinfo='label+value',textposition='inside', textinfo='percent',textfont_size=20)
    fig2.update_layout(title_text="Estado Civil",autosize=False, width=500, height=500)
    fig2 = newLegend(fig2,{"1": "Casado", "2": "Solteiro","3": "Outros"})

    fig4 = go.Figure(data=[go.Pie(labels=df['payment'])])
    fig4.update_traces(hoverinfo='label+value',textposition='inside', textinfo='percent',textfont_size=20)
    fig4.update_layout(title_text="Clientes",autosize=False, width=500, height=500)
    fig4 = newLegend(fig4,{"0": "Adimplentes", "1": "Inadimplentes"})

    app.layout = html.Div([ #MAIN DIV
               
        html.Div([ ### FIGURES Divs
            html.Div([
                dcc.Graph(figure = fig0),
            ], className = 'col-sm'),
            html.Div([
                dcc.Graph(figure = fig1),
            ], className = 'col-sm'),
            html.Div([
                dcc.Graph(figure = fig2),
            ], className = 'col-sm'),
            html.Div([
                dcc.Graph(figure = fig4),
            ], className = 'col-sm')
        ], className = 'row')
        
        ])
    
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




import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import datetime
import flask
from flask import Flask, send_file, render_template, request,make_response
from dash.dependencies import Input, Output

#server=flask.Flask(__name__)
#application = dash.Dash(__name__, server=server)


application = flask.Flask(__name__)


@application.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@application.route('/data', methods=['GET','POST'])
def data():
	if request.method=="POST":
		if request.form['csvfile']=="":
			return flask.redirect(flask.url_for('/data-trends/'))
		else:
			f1=request.form['csvfile']
			df=pd.read_csv(f1,delimiter='|')
			df.to_csv(r'static\file.csv',index = False, header=True)
			return flask.redirect(flask.url_for('/data-trends/'))

    

app = dash.Dash(__name__,server=application, routes_pathname_prefix='/data-trends/')
app.config.suppress_callback_exceptions = True
    
    
global df_fixed
df_fixed=pd.read_csv('data-trending-nishtha-2020.csv', index_col=False, sep='|')
df_fixed['transaction_date']=pd.to_datetime(df_fixed['transaction_date'],format= '%m/%d/%Y')

global family
global day
family=df_fixed['prod_family'].unique()
#day=[7,14,30, 90, 180, 365]
day=['7 past days','14 past days','30 past days','90 past days','180 past days','365 past days']

#application = dash.Dash()
#external_stylesheets = ['https://github.com/STATWORX/blog/blob/master/DashApp/assets/style.css']
#td,th {
#text-align: center;
#}

#application = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#application.css.config.serve_locally = True
#application.scripts.config.serve_locally = True
colors = {
    'background': 'white',
    'background1': 'white',
    'text': 'green'

}


app.layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                    html.Div(className='four columns div-user-controls',
                             children=[
                                 html.H1('PRODUCT TRENDS'),

                                 html.P('Select the Product Family:'),
                    html.Div(
                                     className='div-for-dropdown',
                                     children=[
                                         dcc.Dropdown(id='product-family',options=[{'label': i, 'value': i} for i in family],
                                                      value='ACCESSORIES',
                                                      style={'backgroundColor': 'lightgrey'},
                                                      className='stockselector'
                                                      )],style={'color': 'white', 'font-family': 'Muli','font-size':'12px'}),
                    html.Div(
                                children=[
                                    html.P('Time Duration:'),
                                    dcc.RadioItems(id='duration-time',
                                                   options=[{'label': i, 'value': i} for i in day],
                                                       value='7 past days'
                                        )],style={'display': 'inline-block', 'font-family':'Muli','font-size':'12px'}),

                    html.Div(children=[
                                html.Div(id='html',style={'align':'centre', 'font-family':'Muli'})]
                             )]),
                    html.Div(className='eight columns div-for-charts bg-grey',
                             children=[
                                 dcc.Graph(id='trend-graph', style={'color': '#4CAF50', 'margin-top':'5rem'})
                             ])
        ],style={'font-family':'Muli'})])



@app.callback(
        Output('trend-graph','figure'),
        [Input('product-family','value'),
         Input('duration-time','value')])

def week_data(family,days):
    dff=pd.read_csv(r'static\file.csv', index_col=False)
    dff['transaction_date']=pd.to_datetime(dff['transaction_date'],format= '%m/%d/%Y')
    dff_family=dff.loc[dff.prod_family==family]
    last=dff_family['transaction_date'].max()
    dd=days
    if(dd=='7 past days'):
        d=7
    elif(dd=='14 past days'):
        d=14
    elif(dd=='14 past days'):
        d=30
    elif(dd=='14 past days'):
        d=90
    elif(dd=='14 past days'):
        d=180
    else:
        d=365
    #d=days
    start_delta = datetime.timedelta(d)
    start_of_week = last - start_delta
    mask=(dff_family['transaction_date']>start_of_week) & (dff_family['transaction_date']<=last)
    dff_family_lastweek=dff_family.loc[mask]
    week_data=dff_family_lastweek.groupby('prod_name').agg({'transaction_id':lambda x:len(x)}).reset_index()
    #rename the columns
    week_data.rename(columns={'prod_name':'Model','transaction_id':'Transactions'},inplace=True)
    week_data.sort_values(by=['Transactions'],ascending=False,inplace= True)
    week_data.reset_index(drop=True, inplace= True)
    week_data_top5=week_data.head(5).reset_index(drop=True)
    return ({
                'data': [dict(x=week_data_top5['Model'], y= week_data_top5['Transactions'],
                mode='line' , marker={
                'size':15,
                'opacity':0.5,
                'color':'#4CAF50',
                'line':{'width':0.5,'color':'black'}
                })],
                'layout': {
                        'plot_bgcolor': colors['background1'],
                        'paper_bgcolor': colors['background'],
                        'font': {
                                'color': colors['text']
            }
            }
        })

@app.callback(
        Output('html','children'),
        [Input('product-family','value'),
         Input('duration-time','value')])
def generate_table(family,days):
    dff=pd.read_csv(r'static\file.csv', index_col=False)
    dff['transaction_date']=pd.to_datetime(dff['transaction_date'],format= '%m/%d/%Y')
    dff_family=dff.loc[dff.prod_family==family]
    last=dff_family['transaction_date'].max()
    dd=days
    if(dd=='7 past days'):
        d=7
    elif(dd=='14 past days'):
        d=14
    elif(dd=='14 past days'):
        d=30
    elif(dd=='14 past days'):
        d=90
    elif(dd=='14 past days'):
        d=180
    else:
        d=365
    start_delta = datetime.timedelta(d)
    start_of_week = last - start_delta
    mask=(dff_family['transaction_date']>start_of_week) & (dff_family['transaction_date']<=last)
    dff_family_lastweek=dff_family.loc[mask]
    week_data=dff_family_lastweek.groupby('prod_name').agg({'transaction_id':lambda x:len(x)}).reset_index()
    #rename the columns
    week_data.rename(columns={'prod_name':'Model','transaction_id':'Transactions'},inplace=True)
    week_data.sort_values(by=['Transactions'],ascending=False,inplace= True)
    week_data.reset_index(drop=True, inplace= True)
    week_data_top5=week_data.head(5).reset_index(drop=True)
    return html.Table([
       html.Thead(
            html.Tr([html.Th(col) for col in week_data_top5.columns],style={'textAlign': 'right', 'font-family':'Muli','font-size':'12px'})
        ),
        html.Tbody([
            html.Tr([
                html.Td(week_data_top5.iloc[i][col]) for col in week_data_top5.columns
            ], style={'textAlign':'right','font-family':'Muli','font-size':'12px'}) for i in range(min(len(week_data_top5), 5))
        ],style={'textAlign':'right','font-family':'Muli','font-size':'12px'})
   ])





# Run the app
if __name__ == '__main__':
    application.run(port=8080)

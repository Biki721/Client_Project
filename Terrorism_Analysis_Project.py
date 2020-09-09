import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import webbrowser
from dash.dependencies import Input ,Output
import plotly.express as px
from dash.exceptions import PreventUpdate

external_stylesheets = ['https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css']
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(suppress_callback_exceptions = True,external_stylesheets=external_stylesheets)
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

def load_data():
    global df
    df = pd.read_csv('F:/Forsk Project/Project-3/global_terror.csv')
    
    month = {'January':1,
             'February':2,
             'March':3,
             'April':4,
             'May':5,
             'June':6,
             'July':7,
             'August':8,
             'September':9,
             'October':10,
             'November':11,
             'December':12}
    
    global month_list
    month_list = [{'label':k,'value':v} for k,v in month.items()]
    
    global date_list
    date_list = [{'label':i,'value':i} for i in range(1,32)]
    
    global region_list
    region_list =  [{'label':str(i),'value':str(i)} for i in sorted(df.region_txt.unique().tolist())]
    
    global country_list
    country_list = df.groupby('region_txt')['country_txt'].unique().apply(list).to_dict()
    
    global state_list
    state_list = df.groupby('country_txt')['provstate'].unique().apply(list).to_dict() 
    
    global city_list
    city_list = df.groupby('provstate')['city'].unique().apply(list).to_dict()
    
    global attack_list
    attack_list = [{'label':str(i),'value':str(i)} for i in df.attacktype1_txt.unique().tolist()]
    
    global year_list
    year_list = sorted(df.iyear.unique().tolist())
    
    global year_dict
    year_dict = {i:i for i in year_list}
    
    global chart_dropdown_values                      # as we also have chart for chat key value pairs for dropdown
    chart_dropdown_values = {"Terrorist Organisation":'gname', 
                             "Target Nationality":'natlty1_txt', 
                             "Target Type":'targtype1_txt', 
                             "Type of Attack":'attacktype1_txt', 
                             "Weapon Type":'weaptype1_txt', 
                             "Region":'region_txt', 
                             "Country Attacked":'country_txt'
                          }
    chart_dropdown_values = [{"label":keys, "value":value} for keys, value in chart_dropdown_values.items()]
    
def open_browser():
    webbrowser.open_new('http://127.0.0.1:8769/')
    
def create_app_ui():
    main_layout = html.Div([
        
        html.Div(
        html.H1('Terrorsim Analysis and Insights')),
        html.Br(),
        dcc.Tabs(id = 'Tabs', value = 'tab-1',parent_className="customtabs",children = [
            dcc.Tab(id = 'Map Tools', label = 'Map Tool' , value = 'tab-1',className='first-tab',selected_className='first-sel',children = [
                dcc.Tabs(id = 'subtabs',value = 'tab-1', children = [
                    dcc.Tab(id = 'World Map',label = 'World Map', value = 'tab-1',className="second-tab",selected_className="second-sel"),
                    dcc.Tab(id = 'India Map',label = 'India Map', value = 'tab-2',className="second-tab",selected_className="second-tab")
                    ],colors={"border":"blue","primary":"black","background":"#babaed"}),
            dcc.Dropdown(id = 'month_dropdown',
                     options = month_list,
                     placeholder = 'select month',
                     style={'border-radius':'40px', 'align-items': 'center', 'justify-content': 'center'},
                     multi=True),
        dcc.Dropdown(id = 'date_dropdown',
                     options = date_list,
                     placeholder = 'select day',
                     style={'border-radius':'40px', 'align-items': 'center', 'justify-content': 'center'},
                     multi=True),
        dcc.Dropdown(id = 'region_dropdown',
                     options = region_list,
                     placeholder = 'select region',
                     style={'border-radius':'40px', 'align-items': 'center', 'justify-content': 'center'},
                     multi=True),
        dcc.Dropdown(id = 'country_dropdown',
                     options = country_list,
                     placeholder = 'select country',
                     style={'border-radius':'40px', 'align-items': 'center', 'justify-content': 'center'},
                     multi=True),
        dcc.Dropdown(id = 'state_dropdown',
                     options = state_list,
                     placeholder = 'select_state',
                     style={'border-radius':'40px', 'align-items': 'center', 'justify-content': 'center'},
                     multi=True),
        dcc.Dropdown(id = 'city_dropdown',
                     options = city_list,
                     placeholder = 'select city',
                     style={'border-radius':'40px', 'align-items': 'center', 'justify-content': 'center'},
                     multi=True),
        dcc.Dropdown(id = 'attack_dropdown',
                     options = attack_list,
                     placeholder = 'select attack type',
                     style={'border-radius':'40px', 'align-items': 'center', 'justify-content': 'center'},
                     multi=True),
        html.Br(),
        html.H5('Select the Year', id='year_title'),
        html.Div(
            dcc.RangeSlider(id = 'year_slider',
                            min = min(year_list),
                            max = max(year_list),
                            value = [min(year_list),max(year_list)],
                            marks = year_dict
                            ),
            ),
        html.Br()
            ]),
            dcc.Tab(id = 'Chart Tools', label = 'Chart Tool', value = 'tab-3',className="first-sel",selected_className="first-sel",children = [
                dcc.Tabs(id = 'subtabs2',value = 'tab-3', children = [
                    dcc.Tab(id = 'World chart',label = 'World Chart', value = 'tab-3',className="second-tab",selected_className="second-sel", children = [
                        html.Br(), 
                  dcc.Dropdown(id="Chart_Dropdown", options = chart_dropdown_values, placeholder="Select option", value = "region_txt"),  # a dropdown for the chart which we manually enteed above 
                  html.Br(),
                  html.Hr(),
                  dcc.Input(id="search", placeholder="Search Filter"),
                  html.Hr(),
                  html.Br()
                  ]),
                     dcc.Tab(id = 'India Chart',label = 'India Chart', value = 'India Chart',className="second-tab",selected_className="second-sel", children = [html.Br(),
                  dcc.Dropdown(id="Chart_Dropdownn", options = chart_dropdown_values, placeholder="Select option", value = "region_txt"), 
                  html.Br(),
                  html.Hr(),
                  dcc.Input(id="searchh", placeholder="Search Filter"),
                  html.Hr(),
                  html.Br()])                                                                                
                                                                                                         
                       ]),
                    ])
                ]),
                
        html.Div(id = 'graph_object',
                 children = 'Graph is loading.....')
        ])
    return main_layout

@app.callback(
    Output('graph_object','children'),
    [Input('Tabs','value'),
     Input('month_dropdown','value'),
     Input('date_dropdown','value'),
     Input('region_dropdown','value'),
     Input('country_dropdown','value'),
     Input('state_dropdown','value'),
     Input('city_dropdown','value'),
     Input('attack_dropdown','value'),
     Input('year_slider','value'),
     
     Input("Chart_Dropdown", "value"),
     Input("search", "value"),
     Input("subtabs2", "value"),

     Input("Chart_Dropdownn", "value"),
     Input("searchh", "value"),
     Input("subtabs2", "value")
     ])

def update_app_ui(Tabs,month_value,date_value,region_value,country_value,state_value,city_value,attack_value,year_value,chart_dp_value, search,subtabs2,Chart_Dropdownn_value,searchh,subtabs22):
    
    fig = None
    if Tabs == 'tab-1':
    
        print("Data Type of month value = " , str(type(month_value)))
        print("Data of month value = " , month_value)
        
        print("Data Type of Day value = " , str(type(date_value)))
        print("Data of Day value = " , date_value)
        
        print("Data Type of region value = " , str(type(region_value)))
        print("Data of region value = " , region_value)
        
        print("Data Type of country value = " , str(type(country_value)))
        print("Data of country value = " , country_value)
        
        print("Data Type of state value = " , str(type(state_value)))
        print("Data of state value = " , state_value)
        
        print("Data Type of city value = " , str(type(city_value)))
        print("Data of city value = " , city_value)
        
        print("Data Type of Attack value = " , str(type(attack_value)))
        print("Data of Attack value = " , attack_value)
        
        print("Data Type of year value = " , str(type(year_value)))
        print("Data of year value = " , year_value)
        
        #Year filter
        year_range = range(year_value[0], year_value[1]+1)
        df1 = df[df["iyear"].isin(year_range)]
        
    
        # month_filter
        if month_value==[] or month_value is None:
            pass
        else:
            if date_value is None:
                df1=df1[df1['imonth'].isin(month_value)]
            else:
                df1=df1[(df1['imonth'].isin(month_value))&
                        (df1['iday'].isin(date_value))]
                  
                  
        # region, country, state, city filter
        if region_value==[] or region_value is None:
            pass
        else:
            if country_value==[] or country_value is None:
                df1=df1[df1['region_txt'].isin(region_value)]
            else:
                if state_value==[] or state_value is None:
                    df1=df1[(df1['region_txt'].isin(region_value))&
                            (df1['country_txt'].isin(country_value))]
                else:
                    if city_value==[] or city_value is None:
                        df1=df1[(df1['region_txt'].isin(region_value))&
                            (df1['country_txt'].isin(country_value))&
                            (df1['provstate'].isin(state_value))]
                    else:
                        df1=df1[(df1['region_txt'].isin(region_value))&
                            (df1['country_txt'].isin(country_value))&
                            (df1['provstate'].isin(state_value))&
                            (df1['city'].isin(city_value))]
         
        if df1.shape[0]:
            pass
        else: 
            df1 = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
           'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])                
                    
        
        # Attack Type                    
        if attack_value==[] or attack_value is None:
            pass
        else:
            df1 = df1[df1['attacktype1_txt'].isin(attack_value)]
            
        Figure = px.scatter_mapbox(df1,
                      lat="latitude", 
                      lon="longitude",
                      color="attacktype1_txt",
                      hover_data=["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear","imonth", "iday"],
                      zoom=1
                      )                       
        Figure.update_layout(mapbox_style="open-street-map",
                  autosize=True,
                  margin=dict(l=0, r=0, t=25, b=20),
                  )
        fig = Figure
    
    elif Tabs =='tab-3':
        fig = None
        if subtabs2 == "tab-3":             
            if chart_dp_value is not None:           
                if search is not None:                
                    chart_df = df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name = "count")   
                    chart_df  = chart_df[chart_df[chart_dp_value].str.contains(search, case = False)]        
                else:                                                                                         
                    chart_df = df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name="count")   
            else:                                                                                             
                raise PreventUpdate
            chartFigure = px.area(chart_df, x= "iyear", y ="count", color = chart_dp_value)           
            fig = chartFigure                                                                        
        elif subtabs22 == "India Chart": 
            
            df3=df[(df['region_txt']=="South Asia")&(df['country_txt']=="India")] 

            if Chart_Dropdownn_value is not None:
                if searchh is not None: 
                    chart_df = df3.groupby("iyear")[Chart_Dropdownn_value].value_counts().reset_index(name = "count")
                    chart_df  = chart_df[chart_df[Chart_Dropdownn_value].str.contains(searchh, case = False)]
                else:
                    chart_df = df3.groupby("iyear")[Chart_Dropdownn_value].value_counts().reset_index(name="count")
            else:
                raise PreventUpdate
            chartFigure = px.area(chart_df, x= "iyear", y ="count", color = Chart_Dropdownn_value)
            fig = chartFigure

        else:
            return None
    return dcc.Graph(figure=fig)  


@app.callback(
    [Output('region_dropdown','value'),
    Output('region_dropdown','disabled'),
    Output('country_dropdown','value'),
    Output('country_dropdown','disabled')],
    [Input('subtabs','value')])
def update_tab(tab):
    region_value = None
    region_disabled = False
    country_value = None
    country_disabled = False
    if tab =='tab-1':
        pass
    elif tab == 'tab-2':
        region_value = ['South Asia']
        region_disabled = True
        country_value = ['India']
        country_disabled = True
    return region_value,region_disabled,country_value,country_disabled

    
    
@app.callback(
    Output('date_dropdown','options'),
    [
        Input('month_dropdown','value')
    ]
)
def update_date(month_value):
    day_list = list(range(1,32))
    option=[]
    if month_value:
        option=[{'label':m,'value':m } for m in day_list]
    return option 
    
    
@app.callback(
    Output('country_dropdown','options'),
    [
        Input('region_dropdown','value')
    ]
)
def set_country_options(region_value):
    option=[]
    # Making the country dropdwown data
    if region_value is None:
        raise PreventUpdate
    else:
         for i in region_value:
             if i in country_list.keys():
                 option.extend(country_list[i])
    return [{'label':m , 'value':m} for m in option]
             
     
    
@app.callback(
    Output('state_dropdown','options'),
    [
        Input('country_dropdown','value')
    ]
)
def set_state_options(country_value):
   option=[]
   if country_value is None:
       raise PreventUpdate
   else:
       for i in country_value:
           if i  in state_list.keys():
               option.extend(state_list[i])
   return [{'label':m , 'value':m} for m in option]
      
@app.callback(
    Output('city_dropdown','options'),
    [
        Input('state_dropdown','value')
    ]
)
def set_city_options(state_value):
    option=[]
    if state_value is None:
        raise PreventUpdate
    else:
        for i in state_value:
            if i in city_list.keys():
                option.extend(city_list[i])
    return [{'label':m , 'value':m} for m in option]  
    
def main():
    
    print('Welcome to my project')
    load_data()
    open_browser()
    global app 
    app.layout = create_app_ui()
    app.title = 'Terrorsim Analysis and Insights'
    app.run_server(port =8769)
    print('Thank You')
    app = None
    df = None
    
if __name__=='__main__':
    main()
    
    
    
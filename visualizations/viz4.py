from dash import html, dcc, callback, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_manager import data_manager

def create_pdq_dimension_table():
    """
    Create a dimension table with PDQ information for better understanding
    Based on Montreal Police Service districts and neighborhoods
    """
    pdq_data = {
        1: {"district": "West", "area": "Kirkland/West Island", "type": "Suburban", "description": "West Island suburbs"},
        3: {"district": "West", "area": "LaSalle", "type": "Mixed", "description": "Residential/Industrial mix"},
        4: {"district": "West", "area": "Verdun", "type": "Residential", "description": "Family neighborhood"},
        5: {"district": "West", "area": "NDG West", "type": "Residential", "description": "Notre-Dame-de-Grâce"},
        7: {"district": "West", "area": "Côte-des-Neiges", "type": "Dense Urban", "description": "Multicultural, university area"},
        8: {"district": "West", "area": "Westmount/Downtown West", "type": "Upscale", "description": "Affluent area"},
        9: {"district": "West", "area": "Lachine", "type": "Mixed", "description": "Canal area, mix residential/commercial"},
        11: {"district": "West", "area": "Sud-Ouest", "type": "Gentrifying", "description": "Point St-Charles, Griffintown"},
        13: {"district": "West", "area": "NDG East", "type": "Residential", "description": "Notre-Dame-de-Grâce East"},
        26: {"district": "West", "area": "Pierrefonds", "type": "Suburban", "description": "West Island residential"},
        
      
        12: {"district": "South Central", "area": "Westmount/Downtown", "type": "Upscale", "description": "Westmount, upscale downtown"},
        15: {"district": "South Central", "area": "Outremont", "type": "Upscale", "description": "Chic residential area"},
        16: {"district": "South Central", "area": "Plateau West", "type": "Trendy", "description": "Mile End, trendy area"},
        20: {"district": "South Central", "area": "Old Montreal", "type": "Historic/Tourist", "description": "Historic district, 24h station"},
        21: {"district": "South Central", "area": "Downtown Core", "type": "Commercial", "description": "Business district, 24h station"},
        22: {"district": "South Central", "area": "Plateau East", "type": "Trendy", "description": "Plateau Mont-Royal"},
        
     
        10: {"district": "North", "area": "Ahuntsic West", "type": "Residential", "description": "Residential neighborhoods"},
        24: {"district": "North", "area": "Parc Extension", "type": "Dense Urban", "description": "Multicultural, dense"},
        27: {"district": "North", "area": "Villeray", "type": "Family", "description": "Little Italy area"},
        30: {"district": "North", "area": "Saint-Michel", "type": "Mixed", "description": "Cirque du Soleil headquarters"},
        31: {"district": "North", "area": "Saint-Laurent", "type": "Industrial", "description": "Industrial/residential mix"},
        33: {"district": "North", "area": "Ahuntsic East", "type": "Residential", "description": "Residential family area"},
        35: {"district": "North", "area": "Montréal-Nord", "type": "Residential", "description": "Suburban residential"},
        37: {"district": "North", "area": "Rivière-des-Prairies", "type": "Suburban", "description": "East end suburbs"},
        38: {"district": "North", "area": "Anjou", "type": "Residential", "description": "Residential area"},
        44: {"district": "North", "area": "Saint-Léonard", "type": "Mixed", "description": "Italian community area"},
        
       
        23: {"district": "East", "area": "Rosemont West", "type": "Residential", "description": "Family neighborhoods"},
        39: {"district": "East", "area": "Rosemont East", "type": "Residential", "description": "Petite-Patrie area"},
        42: {"district": "East", "area": "Mercier West", "type": "Working Class", "description": "Traditional working class"},
        45: {"district": "East", "area": "Hochelaga", "type": "Gentrifying", "description": "HoMa - trendy area"},
        46: {"district": "East", "area": "Mercier East", "type": "Working Class", "description": "East end residential"},
        48: {"district": "East", "area": "Pointe-aux-Trembles", "type": "Suburban", "description": "Far east suburbs"},
        49: {"district": "East", "area": "Rivière-des-Prairies East", "type": "Suburban", "description": "Eastern suburbs"}
    }
    
    return pd.DataFrame.from_dict(pdq_data, orient='index').reset_index().\
           rename(columns={'index': 'PDQ'})

def layout():
    try:
        df = data_manager.get_data_for_viz4()
        df['YEAR'] = df['DATE'].dt.year
        pdq_dim = create_pdq_dimension_table()
        
        years = [int(year) for year in sorted(df['YEAR'].unique())]
        districts = sorted(pdq_dim['district'].unique())
        
    except Exception:
        years = list(range(2015, 2025))
        districts = ['West', 'East', 'North', 'South Central']
    
    return html.Div([
        html.H3("Crime Scatter Plot Analysis"),
        html.P("This visualization shows the relationship between years, PDQs, and crime patterns in Montreal."),
        
        html.Div([
            html.Div([
                html.Label("Filter by Years:", style={'font-weight': 'bold'}),
                dcc.RangeSlider(
                    id='year-filter',
                    min=int(min(years)),
                    max=int(max(years)),
                    step=1,
                    marks={year: str(year) for year in years[::2]},
                    value=[int(min(years)), int(max(years))],
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ], style={'width': '48%', 'display': 'inline-block', 'margin-right': '4%'}),
            
            html.Div([
                html.Label("Filter by Districts:", style={'font-weight': 'bold'}),
                dcc.Dropdown(
                    id='district-filter',
                    options=[{'label': district, 'value': district} for district in districts],
                    value=districts,
                    multi=True,
                    placeholder="Select districts..."
                )
            ], style={'width': '48%', 'display': 'inline-block'})
        ], style={'background-color': '#f8f9fa', 'padding': '20px', 'border-radius': '10px', 'margin-bottom': '20px'}),
        
        dcc.Graph(id='crime-scatter-plot', figure=create_scatter_plot()),
        
        html.Div([
            html.H4("PDQ (Police District) Reference Guide", style={'margin-top': '40px'}),
            html.P("PDQ = Poste de quartier (Neighborhood Police Station). Use this table to understand what area each PDQ number represents."),
            html.Div(id='pdq-table-div')
        ])
    ])

@callback(
    Output('pdq-table-div', 'children'),
    [Input('district-filter', 'value')]
)
def update_pdq_table(selected_districts):
    return create_pdq_table(selected_districts)

@callback(
    Output('crime-scatter-plot', 'figure'),
    [Input('year-filter', 'value'),
     Input('district-filter', 'value')]
)
def update_scatter_plot(year_range, selected_districts):
    return create_scatter_plot(year_range, selected_districts)

def create_pdq_table(selected_districts=None):
    """
    Create a formatted table showing PDQ information - now interactive
    """
    pdq_dim = create_pdq_dimension_table()
    
    if selected_districts:
        pdq_dim = pdq_dim[pdq_dim['district'].isin(selected_districts)]
    
    pdq_dim = pdq_dim.sort_values('PDQ')
    
    return dash_table.DataTable(
        id='pdq-table-interactive',
        data=pdq_dim.to_dict('records'),
        columns=[
            {'name': 'PDQ', 'id': 'PDQ'},
            {'name': 'District', 'id': 'district'},
            {'name': 'Area/Neighborhood', 'id': 'area'},
            {'name': 'Type', 'id': 'type'},
            {'name': 'Description', 'id': 'description'}
        ],
        selected_rows=[],
        style_cell={'textAlign': 'left', 'padding': '10px'},
        style_header={'backgroundColor': '#f2f2f2', 'fontWeight': 'bold'},
        style_data_conditional=[{
            'if': {'row_index': 'odd'},
            'backgroundColor': '#f8f9fa'
        }],
        page_size=20
    )

def create_scatter_plot(year_range=None, selected_districts=None):
    """
    Create the scatter plot figure with enhanced PDQ information
    YOUR ORIGINAL FUNCTION - just added filtering parameters
    """
    try:
        df = data_manager.get_data_for_viz4()
        df['YEAR'] = df['DATE'].dt.year
        
        if year_range:
            df = df[(df['YEAR'] >= year_range[0]) & (df['YEAR'] <= year_range[1])]
        
        if selected_districts:
            pdq_dim = create_pdq_dimension_table()
            district_pdqs = pdq_dim[pdq_dim['district'].isin(selected_districts)]['PDQ'].tolist()
            df = df[df['PDQ'].isin(district_pdqs)]
            
        pdq_dim = create_pdq_dimension_table()
        
        scatter_data = []
        
        pdq_dim = create_pdq_dimension_table()
        
        for pdq in df['PDQ'].unique():
            pdq_data = df[df['PDQ'] == pdq]
            
            pdq_info = pdq_dim[pdq_dim['PDQ'] == pdq]
            if not pdq_info.empty:
                area = pdq_info.iloc[0]['area']
                area_type = pdq_info.iloc[0]['type']
                description = pdq_info.iloc[0]['description']
                pdq_tooltip = f"PDQ {pdq} - {area} ({area_type}): {description}"
            else:
                pdq_tooltip = f"PDQ {pdq}"
            
            for year in pdq_data['YEAR'].unique():
                year_data = pdq_data[pdq_data['YEAR'] == year]
                crime_counts = year_data['CATEGORIE'].value_counts()
                dominant_crime = crime_counts.index[0] if len(crime_counts) > 0 else 'Unknown'
                crimes_this_year = len(year_data)
                
                scatter_data.append({
                    'YEAR': year,
                    'PDQ': pdq,
                    'PDQ_Info': pdq_tooltip,  
                    'crimes_this_year': crimes_this_year,
                    'dominant_crime': dominant_crime
                })
        
        scatter_df = pd.DataFrame(scatter_data)
        scatter_df['opacity'] = 0.7
        
        fig = px.scatter(
            scatter_df,
            x='YEAR',
            y='PDQ',
            color='dominant_crime',
            size='crimes_this_year',
            hover_data={
                'PDQ': True,
                'YEAR': True,
                'crimes_this_year': True,
                'dominant_crime': True,
                'PDQ_Info': True  
            },
            title='Montreal Crime Analysis: Years vs PDQs',
            labels={
                'YEAR': 'Year',
                'PDQ': 'Police District (PDQ)',
                'dominant_crime': 'Crime Type',
                'crimes_this_year': 'Crimes This Year',
                'PDQ_Info': 'PDQ Information'
            }
        )
        
        fig.update_traces(
            marker=dict(
                opacity=scatter_df['opacity'], 
                line=dict(width=1, color='white')
            )
        )
        
        fig.update_layout(
            width=1000,
            height=700,
            plot_bgcolor='white',
            xaxis=dict(
                title='Year',
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray',
                zeroline=False
            ),
            yaxis=dict(
                title='Police District (PDQ)',
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray',
                zeroline=False
            ),
            legend=dict(
                title='Dominant Crime Type',
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02
            )
        )
        
        return fig
        
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error loading data: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(
            title="Error Loading Crime Data",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=400
        )
        return fig
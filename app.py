from dash import Dash, dcc, html
from visualizations import viz1, viz2
from callbacks import register_callbacks

app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    html.Div(
        html.Div([
            html.H1("Project - Exploring Montreal Crimes", 
                   style={
                       "color": "#2c3e50",
                       "fontSize": "24px",
                       "fontWeight": "600",
                       "margin": "0 0 15px 0",
                       "textAlign": "center",
                       "letterSpacing": "0.5px"
                   }),
            dcc.Tabs(
                id="tabs",
                value="viz1",
                children=[
                    dcc.Tab(label="Visualization 1", value="viz1", className="custom-tab"),
                    dcc.Tab(label="Visualization 2", value="viz2", className="custom-tab"),
                    dcc.Tab(label="Visualization 3", value="viz3", className="custom-tab"),
                    dcc.Tab(label="Visualization 4", value="viz4", className="custom-tab"),
                    dcc.Tab(label="Visualization 5", value="viz5", className="custom-tab"),
                ],
                className="custom-tabs-container"
            ),
        ], style={
            "width": "80vw",
            "maxWidth": "1200px"
        }),
        style={
            "position": "fixed",
            "top": "0",
            "left": "50%",
            "transform": "translateX(-50%)",
            "background": "#00a4e4",
            "zIndex": 1000,
            "boxShadow": "0 4px 20px rgba(0,0,0,0.15)",
            "borderRadius": "0 0 16px 16px",
            "padding": "20px",
            "backdropFilter": "blur(10px)"
        }
    ),
    
   
    html.Div([
        dcc.Store(id="store-viz1"),
        dcc.Store(id="store-viz2"),
        dcc.Store(id="store-viz3"),
        dcc.Store(id="store-viz4"),
        dcc.Store(id="store-viz5"),
    ]),
    
   
    dcc.Loading(
        id="loading",
        type="default",
        children=[
            html.Div([
                html.Div(id="tab-content", className="content-container")
            ], style={
                "marginTop": "140px", 
                "padding": "30px",
                "minHeight": "calc(100vh - 140px)",
                "background": "linear-gradient(to bottom, #f8f9fa, #e9ecef)",
            })
        ]
    ),
    
], style={
    "fontFamily": "'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif",
    "margin": "0",
    "padding": "0",
    "minHeight": "100vh",
    "display": "flex",
    "flexDirection": "column"
})


app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            /* Global Styles */
            * {
                box-sizing: border-box;
            }
            
            body {
                margin: 0;
                padding: 0;
                background: #f8f9fa;
            }
            
            /* Custom Tab Styles */
            .custom-tabs-container {
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            .custom-tab {
                background: rgba(255,255,255,0.9) !important;
                border: none !important;
                border-radius: 8px !important;
                margin: 0 4px !important;
                transition: all 0.3s ease !important;
                font-weight: 500 !important;
                color: #2c3e50 !important;
            }
            
            .custom-tab:hover {
                background: rgba(255,255,255,1) !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
            }
            
            .custom-tab--selected {
                background: #fff !important;
                color: #667eea !important;
                font-weight: 600 !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
            }
            
            /* Content Container Styles */
            .content-container {
                background: #fff;
                border-radius: 16px;
                padding: 30px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.08);
                margin-bottom: 30px;
                border: 1px solid rgba(0,0,0,0.05);
            }
            
            /* Loading Spinner Customization */
            ._dash-loading {
                margin: 50px auto !important;
            }
            
            /* Responsive Design */
            @media (max-width: 768px) {
                .custom-tabs-container .custom-tab {
                    font-size: 12px !important;
                    padding: 8px 12px !important;
                    margin: 0 2px !important;
                }
                
                .content-container {
                    padding: 20px;
                    margin: 0 10px 20px 10px;
                }
            }
            
            /* Enhanced Graph Styling */
            .js-plotly-plot {
                border-radius: 12px !important;
                overflow: hidden !important;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1) !important;
            }
            
            /* Form Controls Enhancement */
            .Select-control, .dash-dropdown {
                border-radius: 8px !important;
                border: 2px solid #e9ecef !important;
                transition: all 0.3s ease !important;
            }
            
            .Select-control:hover, .dash-dropdown:hover {
                border-color: #667eea !important;
            }
            
            /* Button Enhancements */
            button {
                border-radius: 8px !important;
                transition: all 0.3s ease !important;
            }
            
            /* Card-like styling for components */
            .dash-table-container {
                border-radius: 12px !important;
                overflow: hidden !important;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1) !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
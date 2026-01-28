from dash import Input, Output, html, dcc
import visualizations.viz1 as viz1
import visualizations.viz2 as viz2
import visualizations.viz3 as viz3
import visualizations.viz4 as viz4
import visualizations.viz5 as viz5

def register_callbacks(app):
    
    @app.callback(
        Output("viz1-graph", "figure"),
        Input("viz1-view-dropdown", "value"),
        Input("viz1-chart-type", "value"),
        prevent_initial_call=False
    )
    def update_viz1_graph(view, chart_type):
        try:
            return viz1.update_graph(view, chart_type)
        except Exception as e:
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error loading visualization: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(
                xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
            return fig

    @app.callback(
        Output("tab-content", "children"),
        Input("tabs", "value"),
        prevent_initial_call=False
    )
    def render_tab(tab):
        try:
            content_style = {
                "animation": "fadeIn 0.5s ease-in-out",
                "width": "100%"
            }
            
            if tab == "viz1":
                return html.Div([
                    html.Div([
                        html.H3("Visualization 1", 
                               style={
                                   "color": "#2c3e50", 
                                   "marginBottom": "20px",
                                   "borderBottom": "3px solid #2c3e50",
                                   "paddingBottom": "10px",
                                   "fontSize": "28px",
                                   "fontWeight": "600"
                               }),
                        html.P("The first visualization is an interactive chart (toggle between line and bar chart). It visualises the total number of crimes recorded, segmented by year, season, or month. The x axis represents the selected time unit, while the y axis shows the number of crimes. Each bar or line point corresponds to the number of crimes during that time period. A dashed red line represents the median crime count across the selected timeframe. This helps compare data points above or below the midpoint. The legend clearly differentiates between the crime data and the median line. ",
                               style={"color": "#6c757d", "fontSize": "16px", "marginBottom": "30px"}),
                    ]),
                    viz1.layout()
                ], style=content_style)
                
            elif tab == "viz2":
                return html.Div([
                    html.Div([
                        html.H3("Visualization 2", 
                               style={
                                   "color": "#2c3e50", 
                                   "marginBottom": "20px",
                                   "borderBottom": "3px solid #2c3e50",
                                   "paddingBottom": "10px",
                                   "fontSize": "28px",
                                   "fontWeight": "600"
                               }),
                        html.P("​​This visualization explores how crime in Montreal has changed over time, focusing on three key aspects: time of day, day of the week, and long-term trends in night-time activity. It consists of three connected charts that highlight different dimensions of temporal crime data from 2015 to 2025.",
                               style={"color": "#6c757d", "fontSize": "16px", "marginBottom": "30px"}),
                    ]),
                    viz2.layout()
                ], style=content_style)
                
            elif tab == "viz3":
                return html.Div([
                    html.Div([
                        html.H3("Visualization 3", 
                               style={
                                   "color": "#2c3e50", 
                                   "marginBottom": "20px",
                                   "borderBottom": "3px solid #2c3e50",
                                   "paddingBottom": "10px",
                                   "fontSize": "28px",
                                   "fontWeight": "600"
                               }),
                        html.P("This type of visualization is called a scatter_mapbox created with Plotly, which displays the geographical distribution of various crime types across the city of Montreal. Each dot represents an individual criminal  incident, where the color indicates the type of crime. The visualization uses Mapbox to provide an interactive, zoomable map overlaid with spatial crime data.",
                               style={"color": "#6c757d", "fontSize": "16px", "marginBottom": "30px"}),
                    ]),
                    viz3.layout()
                ], style=content_style)
                
            elif tab == "viz4":
                return html.Div([
                    html.Div([
                        html.H3("Visualization 4", 
                               style={
                                   "color": "#2c3e50", 
                                   "marginBottom": "20px",
                                   "borderBottom": "3px solid #2c3e50",
                                   "paddingBottom": "10px",
                                   "fontSize": "28px",
                                   "fontWeight": "600"
                               }),
                        html.Div([
                            html.P("This visualization, consisting of a temporal scatter plot, offers a perspective on the evolution of crime across Montreal's different police districts, allowing users to simultaneously visualize the temporal, geographical, and typological dimensions of criminal acts.",
                                   style={"color": "#6c757d", "fontSize": "16px", "marginBottom": "15px", "lineHeight": "1.6"}),
                            
                            html.P("It comprises a multidimensional scatter plot where the x-axis represents temporal progression from 2015 to 2025, while the y-axis displays the various police districts (PDQs), that have a range from 1 to 55. Each point corresponds to a specific district for a given year, creating a visual of criminal activities across time and Montreal's different police districts.",
                                   style={"color": "#6c757d", "fontSize": "16px", "marginBottom": "15px", "lineHeight": "1.6"}),
                            
                            html.P([
                                "The color dimension encodes the dominant crime type in each district for the corresponding year, revealing four main categories: ",
                                html.Strong('"Introduction"', style={"color": "#495057"}),
                                " (breaking & entering), ",
                                html.Strong('"Vol dans/sur véhicule"', style={"color": "#495057"}),
                                " (theft from/on vehicle), ",
                                html.Strong('"Vol de véhicule"', style={"color": "#495057"}),
                                " (vehicle theft), and ",
                                html.Strong('"Méfait"', style={"color": "#495057"}),
                                " (mischief/vandalism)."
                            ], style={"color": "#6c757d", "fontSize": "16px", "marginBottom": "15px", "lineHeight": "1.6"}),
                            
                            html.P("The size of the points adds dimension, which is proportional to the total number of crimes recorded in the concerned district for the specific year. This visual allows easy identification of zones and periods of high criminal activity.",
                                   style={"color": "#6c757d", "fontSize": "16px", "marginBottom": "15px", "lineHeight": "1.6"}),
                            
                            html.P("This visualization thus allows users to explore criminal patterns along three analytical axes: the temporal evolution of crimes, distribution by district, and by type of offense.",
                                   style={"color": "#6c757d", "fontSize": "16px", "marginBottom": "30px", "lineHeight": "1.6", "fontWeight": "500"})
                        ], style={
                            "marginBottom": "25px"
                        })
                    ]),
                    viz4.layout()
                ], style=content_style)
                
            elif tab == "viz5":
                return html.Div([
                    html.Div([
                        html.H3("Visualization 5", 
                               style={
                                   "color": "#2c3e50", 
                                   "marginBottom": "20px",
                                   "borderBottom": "3px solid #2c3e50",
                                   "paddingBottom": "10px",
                                   "fontSize": "28px",
                                   "fontWeight": "600"
                               }),
                        html.Div([
                            html.P("This interactive visualization presents three different perspectives on crime patterns in Montreal, helping us to better understand when certain crimes happen most frequently. Each heatmap uses the same color scale to keep comparisons fair: the darker the cell, the higher the number of crimes.",
                                   style={"color": "#6c757d", "fontSize": "16px", "marginBottom": "15px", "lineHeight": "1.6"}),
                            
                            html.P([
                                html.Strong("By Time of Day:", style={"color": "#495057"}),
                                " This view compares crime types based on whether they occur during the day, evening or night. We can clearly see which types of crimes are more common at different moments of the day, highlighting the importance of time in criminal activity patterns."
                            ], style={"color": "#6c757d", "fontSize": "16px", "marginBottom": "15px", "lineHeight": "1.6"}),
                            
                            html.P([
                                html.Strong("By Season:", style={"color": "#495057"}),
                                " This graph shows how crime activity changes with the seasons (winter, spring, summer and fall). Some crimes appear to spike in warmer months, while others are more consistent year-round."
                            ], style={"color": "#6c757d", "fontSize": "16px", "marginBottom": "15px", "lineHeight": "1.6"}),
                            
                            html.P([
                                html.Strong("By Year:", style={"color": "#495057"}),
                                " This final view lets us observe how each crime type has evolved over time. It's especially useful for spotting long-term trends, such as increases, decreases or stability over time."
                            ], style={"color": "#6c757d", "fontSize": "16px", "marginBottom": "30px", "lineHeight": "1.6"})
                        ], style={
                            "marginBottom": "25px"
                        })
                    ]),
                    viz5.layout()
                ], style=content_style)
            
            
        except Exception as e:
            return html.Div([
                html.Div([
                    html.H3("Error Loading Content", 
                           style={"color": "#dc3545", "textAlign": "center", "marginBottom": "20px"}),
                    html.P(f"Sorry, there was an error loading this visualization: {str(e)}", 
                           style={"color": "#6c757d", "textAlign": "center"}),
                    html.P("Please try refreshing the page or contact support if the issue persists.", 
                           style={"color": "#6c757d", "textAlign": "center", "fontSize": "14px"})
                ], style={
                    "padding": "40px",
                    "textAlign": "center",
                    "background": "#fff3cd",
                    "border": "1px solid #ffeaa7",
                    "borderRadius": "12px"
                })
            ])

    @app.callback(
        Output("bar-chart", "figure"),
        Output("pie-chart", "figure"),
        Output("line-chart", "figure"),
        Input("pdq-dropdown", "value"),
        Input("year-slider", "value"),
        prevent_initial_call=False
    )
    def update_all_charts(selected_pdq, selected_years):
        try:
            start_year, end_year = selected_years
            pdq_value = None if selected_pdq == "All" else selected_pdq

            filtered_df = viz2.filter_data(start_year, end_year, pdq=pdq_value)

            bar_fig = viz2.create_bar_chart(filtered_df)
            pie_fig = viz2.create_pie_chart(filtered_df)
            line_fig = viz2.create_line_chart(filtered_df)
            
            for fig in [bar_fig, pie_fig, line_fig]:
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Segoe UI, Roboto, Helvetica Neue", size=12),
                    margin=dict(l=40, r=40, t=60, b=40),
                    title=dict(font=dict(size=18, color="#2c3e50")),
                    legend=dict(
                        bgcolor="rgba(255,255,255,0.8)",
                        bordercolor="rgba(0,0,0,0.2)",
                        borderwidth=1,
                        font=dict(size=11)
                    )
                )

            return bar_fig, pie_fig, line_fig
            
        except Exception as e:
            import plotly.graph_objects as go
            
            error_fig = go.Figure()
            error_fig.add_annotation(
                text=f"Error: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False,
                font=dict(size=14, color="red")
            )
            error_fig.update_layout(
                xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
            
            return error_fig, error_fig, error_fig
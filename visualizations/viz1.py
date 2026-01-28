from dash import html, dcc
import pandas as pd
import plotly.graph_objects as go
from data_manager import data_manager

def layout():
    return html.Div([
        html.Label("Select view"),
        dcc.Dropdown(
            id="viz1-view-dropdown",
            options=[
                {"label": "Yearly", "value": "Yearly"},
                {"label": "Seasonal", "value": "Seasonal"},
                {"label": "Monthly", "value": "Monthly"}
            ],
            value="Yearly",
            clearable=False
        ),

        html.Label("Chart type"),
        dcc.RadioItems(
            id="viz1-chart-type",
            options=[
                {"label": "Line", "value": "Line"},
                {"label": "Bar", "value": "Bar"}
            ],
            value="Line",
            inline=True
        ),

        dcc.Graph(id="viz1-graph")
    ])

def update_graph(view_option, chart_type):
    df = data_manager.get_data_for_viz1()

    if view_option == "Yearly":
        df_view = df.groupby("YEAR").size().reset_index(name="Crimes")
        df_view = df_view[df_view["YEAR"].between(2015, 2025)]
        x_col = "YEAR"
        chart_title = "Annual Crime Numbers"
    elif view_option == "Seasonal":
        df_view = df.groupby("SEASON").size().reset_index(name="Crimes")
        season_order = ["Winter", "Spring", "Summer", "Autumn"]
        df_view["SEASON"] = pd.Categorical(df_view["SEASON"], categories=season_order, ordered=True)
        df_view = df_view.sort_values("SEASON")
        x_col = "SEASON"
        chart_title = "Seasonal Crime Numbers"
    else:
        df_view = df.groupby("MONTH").size().reset_index(name="Crimes")
        x_col = "MONTH"
        chart_title = "Monthly Crime Numbers"

    median_crimes = df_view["Crimes"].median()

    fig = go.Figure()

    hover_template = f"<b>%{{x}}</b><br>Crimes: %{{y:,}}<extra></extra>"

    if chart_type == "Line":
        fig.add_trace(go.Scatter(
            x=df_view[x_col],
            y=df_view["Crimes"],
            mode="lines+markers",
            name="Crimes",
            hovertemplate=hover_template
        ))
    else:
        fig.add_trace(go.Bar(
            x=df_view[x_col],
            y=df_view["Crimes"],
            name="Crimes",
            hovertemplate=hover_template
        ))

    fig.add_trace(go.Scatter(
        x=df_view[x_col],
        y=[median_crimes] * len(df_view),
        mode="lines",
        name=f"Median: {median_crimes:.0f}",
        line=dict(color="red", dash="dash"),
        hoverinfo='skip'
    ))

    fig.update_layout(
        title=chart_title,
        xaxis_title=view_option,
        yaxis_title="Number of Crimes",
        hovermode="x unified",
        legend_title="Legend",
        margin=dict(l=60, r=40, t=60, b=60)
    )

    return fig

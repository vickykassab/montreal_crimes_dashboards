from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_manager import data_manager

cute_colors = {
    'Day (09:01–16:00)': '#FFD580',
    'Evening (16:01–00:00)': '#D7BDE2',
    'Night (00:01–08:00)': '#85C1E9',
    'Weekday': '#AED6F1',
    'Weekend': '#F5B7B1'
}

pdq_names = {
     1: "Baie-D'Urfé / Beaconsfield / Kirkland / Ste-Anne-de-Bellevue / Senneville",
     3: "L'Île-Bizard / Pierrefonds / Ste-Geneviève / Roxboro",
     4: "Dollard-Des-Ormeaux",
     5: "Dorval / L'Île-Dorval / Pointe-Claire",
     7: "Saint-Laurent",
     8: "Lachine / Saint-Pierre",
     9: "Notre-Dame-de-Grâce / Côte-Saint-Luc / Hampstead / Montréal-Ouest",
    10: "Bordeaux / Cartierville",
    11: "Côte-des-Neiges / Notre-Dame-de-Grâce",
    12: "Westmount / Ville-Marie Ouest",
    13: "LaSalle",
    15: "St-Paul / Petite-Bourgogne / Pointe-St-Charles / St-Henri / Ville-Émard",
    16: "Île-des-Sœurs / Verdun",
    20: "Centre-Ville Ouest (Ville-Marie) / Parc du Mont-Royal",
    21: "Centre-Ville Est (Ville-Marie) / Îles Notre-Dame & Ste-Hélène / Vieux-Montréal",
    22: "Centre-Sud",
    23: "Hochelaga-Maisonneuve",
    24: "Ancien PDQ – fusionné au PDQ 26 (Côte-des-Neiges) :contentReference[oaicite:2]{index=2}",
    26: "Côte-des-Neiges / Mont-Royal / Outremont",
    27: "Ahuntsic",
    30: "Saint-Michel",
    31: "Villeray / Parc-Extension",
    33: "Ancien PDQ Parc-Extension (fusionné au PDQ 31) :contentReference[oaicite:3]{index=3}",
    35: "La Petite-Italie / La Petite-Patrie / (partie d'Outremont)",
    38: "Le Plateau-Mont-Royal",
    39: "Montréal-Nord",
    42: "Saint-Léonard",
    44: "Rosemont – La Petite-Patrie",
    45: "Rivière-des-Prairies",
    46: "Anjou",
    48: "Mercier – Hochelaga-Maisonneuve",
    49: "Montréal-Est / Pointe-aux-Trembles",
    50: "Métro de Montréal",
    55: "Aéroport Montréal-Trudeau (Unité aéroportuaire)"
}

def filter_data(start_year, end_year, pdq=None):
    """
    Filtre les données en utilisant le gestionnaire centralisé
    """
    return data_manager.get_filtered_data(
        start_year=start_year,
        end_year=end_year,
        pdq=pdq
    )

import plotly.express as px

def create_bar_chart(df):
    quart_counts = (
        df["Time of Day"]
          .value_counts()
          .rename_axis("Time of Day")
          .reset_index(name="Crimes")
    )

    fig = px.bar(
        quart_counts,
        x="Time of Day",
        y="Crimes",
        color="Time of Day",
        text="Crimes",
        color_discrete_map=cute_colors,
        title="Crime by Time of Day",
    )

    fig.update_traces(
        texttemplate="%{text}",
        textposition="outside",
        hovertemplate="<b>Crimes:</b> %{y:,}<extra></extra>"
    )

    fig.update_layout(
        xaxis_title="Time of Day",
        yaxis_title="Number of Crimes",
        hovermode="closest",
        legend_title_text="Time of Day",
    )
    fig.update_xaxes(showspikes=False)

    y_max = quart_counts["Crimes"].max()
    fig.update_yaxes(range=[0, y_max * 1.10], automargin=True)
    fig.update_xaxes(ticklabeloverflow="allow")
    return fig


def create_pie_chart(df):
    day_counts = df['Day Type'].value_counts().reset_index()
    day_counts.columns = ['Day Type', 'Crimes']
    fig = go.Figure(go.Pie(
        labels=day_counts['Day Type'],
        values=day_counts['Crimes'],
        name='Day Type',
        hole=0.5,
        marker=dict(colors=[cute_colors[k] for k in day_counts['Day Type']]),
        textinfo='label+percent',
        hoverinfo='label+percent+value'
    ))
    fig.update_layout(
        title='Crimes: Weekday vs Weekend',
        legend_title_text='Day Type'
    )
    return fig

def create_line_chart(df: pd.DataFrame):
    night_df = df[df["Time of Day"] == "Night (00:01–08:00)"]
    night_trend = night_df.groupby("YEAR").size().reset_index(name="Crimes")
    night_trend["YoY Change (%)"] = night_trend["Crimes"].pct_change().fillna(0) * 100

    night_trend["YEAR"] = night_trend["YEAR"].astype(str)

    fig = go.Figure(
        go.Scatter(
            x=night_trend["YEAR"],
            y=night_trend["Crimes"],
            mode="lines+markers",
            name="",
            marker=dict(size=10, color=cute_colors["Night (00:01–08:00)"]),
            line=dict(width=4, color=cute_colors["Night (00:01–08:00)"]),
            customdata=night_trend[["YoY Change (%)"]],
            hovertemplate="<b>Year:</b> %{x}<br><b>Night Crimes:</b> %{y}"
                          "<br><b>YoY Change:</b> %{customdata[0]:.1f}%",
        )
    )

    fig.update_layout(
        title="Night-Time Crime Trends",
        xaxis_title="Year",
        yaxis_title="Number of Crimes",
        hovermode="x unified",
        showlegend=False,
        hoverlabel=dict(bgcolor="white"),
    )

    fig.update_xaxes(type="category")
    return fig


def layout():
    df_raw = data_manager.get_data_for_viz2()
    available_years = sorted(df_raw['YEAR'].dropna().unique())
    start_year = int(min(available_years))
    end_year = int(max(available_years))

    pdq_options = [{'label': 'All PDQs', 'value': 'All'}]
    if 'PDQ' in df_raw.columns:
        pdq_options += [
            {'label': f"{p} – {pdq_names.get(p, f'PDQ {p}')}", 'value': p}
            for p in sorted(df_raw['PDQ'].dropna().unique())
        ]

    return html.Div([
        html.H3("Crime Analysis by Time and Day Type (2015–2025)"),
        html.P("This visualization explores how crime in Montreal has changed over time, focusing on three key aspects: time of day, day of the week, and long-term trends in night-time activity. It consists of three connected charts that highlight different dimensions of temporal crime data from 2015 to 2025."),

        html.Div([
            html.Label("Select PDQ:"),
            dcc.Dropdown(id='pdq-dropdown', options=pdq_options, value='All', clearable=False)
        ], style={'width': '40%', 'display': 'inline-block'}),

        html.Div([
            html.Label("Select Year Range:"),
            dcc.RangeSlider(
                id='year-slider',
                min=start_year,
                max=end_year,
                step=1,
                value=[start_year, end_year],
                marks={year: str(year) for year in range(start_year, end_year + 1)}
            )
        ], style={'marginTop': 20}),

        dcc.Graph(id="bar-chart"),
        dcc.Graph(id="pie-chart"),
        dcc.Graph(id="line-chart")
    ])


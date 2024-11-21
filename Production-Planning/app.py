import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State

# Load the dataset
data = pd.read_csv('User_Form_Feedback - Sheet1.csv')

# Map non-numeric values in BulkInterest to numeric equivalents
data['BulkInterest'] = data['BulkInterest'].map({
    "Yes": 1,
    "No": 0
}).fillna(0)

# Ensure BulkInterest is numeric
data['BulkInterest'] = pd.to_numeric(data['BulkInterest'], errors='coerce')
data['BulkInterest'].fillna(0, inplace=True)

# Calculate product demand by summing BulkInterest for each ProductCategory
demand = data.groupby('ProductCategory')['BulkInterest'].sum().reset_index()
demand = demand.sort_values(by='BulkInterest', ascending=False)
top_demanded_products = demand.head(4)

# Initialize the Dash app
app = Dash(__name__)

# Define the charts
charts = {
    "Bar Chart": px.bar(data, x="ProductCategory", y="BulkInterest", title="Bar Chart"),
    "Line Chart": px.line(data, x="DOB", y="BulkInterest", title="Line Chart"),
    "Scatter Plot": px.scatter(data, x="ProductCategory", y="BulkInterest", color="Gender", title="Scatter Plot"),
    "Pie Chart": px.pie(data, names="ProductCategory", values="BulkInterest", title="Pie Chart"),
    "Heatmap": px.density_heatmap(data, x="ProductCategory", y="Gender", title="Heatmap"),
    "Box Plot": px.box(data, x="ProductCategory", y="BulkInterest", title="Box Plot"),
    "Histogram": px.histogram(data, x="BulkInterest", title="Histogram"),
    "Area Chart": px.area(data, x="DOB", y="BulkInterest", title="Area Chart"),
    "Treemap": px.treemap(data, path=["ProductCategory", "LifestylePreferences"], values="BulkInterest", title="Treemap"),
    "Bubble Chart": px.scatter(data, x="ProductCategory", y="BulkInterest", size="BulkInterest", color="Gender", title="Bubble Chart"),
}

# Create the grid layout
app.layout = html.Div([
    html.H1("Visualization Dashboard", style={"textAlign": "center"}),

    # Grid layout for charts
    html.Div(
        [
            html.Div(
                dcc.Graph(id=f"chart-{i}", figure=fig, style={"height": "300px", "width": "300px"}),
                style={
                    "padding": "10px",
                    "boxSizing": "border-box",
                    "border": "2px solid #ccc",  # Border around each chart
                    "borderRadius": "10px",
                    "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",  # Slight shadow for hover effect
                    "transition": "transform 0.2s ease, box-shadow 0.2s ease",
                    "cursor": "pointer",  # Pointer cursor to indicate interactivity
                },
                id=f"chart-container-{i}"  # Add container for hover effects
            )
            for i, fig in enumerate(charts.values())
        ],
        style={
            "display": "grid",
            "gridTemplateColumns": "repeat(auto-fill, minmax(300px, 1fr))",
            "gap": "10px"
        }
    ),

    # Table showing top-demanded products
    html.H2("Top Demanded Products", style={"textAlign": "center"}),
    html.Table(
        # Table header
        [html.Tr([html.Th("Product Category"), html.Th("Demand")])] +
        # Table rows
        [html.Tr([html.Td(row['ProductCategory']), html.Td(row['BulkInterest'])]) for _, row in top_demanded_products.iterrows()],
        style={
            "width": "80%",
            "margin": "auto",
            "border": "1px solid black",
            "borderCollapse": "collapse",
            "textAlign": "center",
            "backgroundColor": "#f9f9f9",
            "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)"
        },
        className="styled-table"
    ),

    # Modal for enlarged chart
    html.Div(
        id="modal",
        children=[
            dcc.Graph(id="modal-graph"),
            html.Button("Close", id="close-modal", style={"marginTop": "10px"})
        ],
        style={
            "display": "none",
            "position": "fixed",
            "top": "10%",
            "left": "10%",
            "width": "80%",
            "height": "80%",
            "backgroundColor": "white",
            "padding": "20px",
            "zIndex": 1000,
            "border": "2px solid black",
            "overflow": "auto"
        }
    )
])

# Callback to handle clicks and display larger chart
@app.callback(
    [Output("modal", "style"), Output("modal-graph", "figure")],
    [Input(f"chart-{i}", "clickData") for i in range(len(charts))],
    prevent_initial_call=True
)
def display_large_chart(*clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        return {"display": "none"}, {}

    # Identify which chart was clicked
    chart_index = int(ctx.triggered[0]["prop_id"].split("-")[1])
    selected_chart = list(charts.values())[chart_index]

    # Show the modal with the selected chart
    return {
        "display": "block",
        "position": "fixed",
        "top": "10%",
        "left": "10%",
        "width": "80%",
        "height": "80%",
        "backgroundColor": "white",
        "padding": "20px",
        "zIndex": 1000,
        "border": "2px solid black",
        "overflow": "auto"
    }, selected_chart

# Callback to close the modal
@app.callback(
    Output("modal", "style"),
    [Input("close-modal", "n_clicks")],
    [State("modal", "style")],
    prevent_initial_call=True
)
def close_modal(n_clicks, current_style):
    # Hide the modal when the close button is clicked
    current_style["display"] = "none"
    return current_style

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback_context
from flask import jsonify

# Load the dataset
data = pd.read_csv(r'C:\Users\naveen ks\Downloads\capstone_project\capstone_project\User_Form_Feedback - Sheet1.csv')

# Map non-numeric values in BulkInterest to numeric equivalents
data['BulkInterest'] = data['BulkInterest'].map({"Yes": 1, "No": 0}).fillna(0)

# Ensure BulkInterest is numeric
data['BulkInterest'] = pd.to_numeric(data['BulkInterest'], errors='coerce')
data['BulkInterest'].fillna(0, inplace=True)

# Calculate product demand by summing BulkInterest for each ProductCategory
demand = data.groupby('ProductCategory')['BulkInterest'].sum().reset_index()
demand = demand.sort_values(by='BulkInterest', ascending=False)
top_demanded_products = demand.head(4)

# Function to generate HTML file for top demanded products
def generate_html_report():
    html_content = """
  <html>
    <head>
        <title>Top Demanded Products</title>
        <style>
            body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #fcfcfb, #f9feff); /* Linear gradient background */
            margin: 0;
            padding: 0;
            animation: fadeIn 1.5s;
        }

        h1 {
            text-align: center;
            color: #333;
            animation: slideIn 0.5s;
        }

        .animation-title {
            text-align: center;
            color: #2C3E50;
            font-size: 24px;
            margin-top: 20px;
            animation: popIn 0.5s;
        }

        .manufacturing-div {
            text-align: center;
            padding: 20px;
            border: 1px solid #4CAF50;
            border-radius: 5px;
            margin: 20px auto;
            background-color: rgba(76, 175, 80, 0.1);
            animation: fadeIn 1s;
        }

        table {
            width: 50%;
            margin: auto;
            border-collapse: collapse;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease, background-color 0.5s ease; /* Added background-color transition */
        }

        table:hover {
            transform: scale(1.05);
            background-color: rgba(76, 175, 80, 0.2); /* Change table background on hover */
        }

        th, td {
            border: 1px solid #ccc;
            padding: 12px;
            text-align: center;
            transition: background 0.3s ease, color 0.3s ease;
        }

        th {
            background-color: #4CAF50;
            color: white;
            animation: fadeIn 0.5s;
        }

        tr:hover {
            background-color: #f1f1f1;
            color: #333;
        }

        @keyframes slideIn {
            from {transform: translateY(-30px); opacity: 0;}
            to {transform: translateY(0); opacity: 1;}
        }

        @keyframes fadeIn {
            from {opacity: 0;}
            to {opacity: 1;}
        }

        @keyframes popIn {
            from {transform: scale(0.8); opacity: 0;}
            to {transform: scale(1); opacity: 1;}
        }

        .styled-table th {
            background-color: #4CAF50;
            color: #ffffff;
        }

        .styled-table tr {
            transition: background-color 0.3s ease;
        }

        .styled-table tr:nth-child(even) {
            background-color: #f9f9f9;
        }
    </style>
    </head>
    <body>
        <h1>Manufacturing Site</h1>

        <!-- New Manufacturing Animation Div -->
        <div class="manufacturing-div">
            <h2 class="animation-title">Top Demand Products </h2>
            <p>Discover how our manufacturing processes bring top demanded products to life!</p>
        </div>

       <table class="styled-table">
            <tr>
                <th>Product Category</th>
                <th>Demand</th>
            </tr>
    """
    
    for _, row in top_demanded_products.iterrows():
        html_content += f"""
            <tr>
                <td>{row['ProductCategory']}</td>
                <td>{int(row['BulkInterest'])}</td>
            </tr>
        """
    
    html_content += """
            </table>
    </body>
</html>

    """

    # Writing to manufact111.html
    with open("manufact1.html", "w") as file:
        file.write(html_content)

# Call the function to generate the HTML report
generate_html_report()

# Initialize the Dash app
app = Dash(__name__)

# Create an API endpoint to return the demand data as JSON
@app.server.route('/api/demand')
def get_demand():
    demand_data = top_demanded_products.to_dict(orient='records')
    total_demand = int(top_demanded_products['BulkInterest'].sum())
    return jsonify({"total_demand": total_demand, "products": demand_data})

# Define the visualization charts
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

# Create the layout for Dash application
app.layout = html.Div([
    html.H1("Visualization Dashboard", style={"textAlign": "center"}),

    # Grid layout for charts
    html.Div([
        html.Div(
            dcc.Graph(id=f"chart-{i}", figure=fig, style={"height": "300px", "width": "300px"}),
            style={
                "padding": "10px",
                "boxSizing": "border-box",
                "border": "2px solid #ccc",
                "borderRadius": "10px",
                "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
                "transition": "transform 0.2s ease, box-shadow 0.2s ease",
                "cursor": "pointer",
            },
            id=f"chart-container-{i}"
        )
        for i, fig in enumerate(charts.values())
    ], style={
        "display": "grid",
        "gridTemplateColumns": "repeat(auto-fill, minmax(300px, 1fr))",
        "gap": "10px"
    }),

    # Table showing top-demanded products
    html.H2("Top Demanded Products", style={"textAlign": "center"}),
    html.Table(
        [html.Tr([html.Th("Product Category"), html.Th("Demand")])] +
        [html.Tr([html.Td(row['ProductCategory']), html.Td(int(row['BulkInterest']))]) for _, row in top_demanded_products.iterrows()],
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

# Callback for modal behavior and displaying enlarged chart
@app.callback(
    [Output("modal", "style"), Output("modal-graph", "figure")],
    [Input(f"chart-{i}", "clickData") for i in range(len(charts))] +
    [Input("close-modal", "n_clicks")],
    prevent_initial_call=True
)
def manage_modal(*inputs):
    ctx = callback_context

    if not ctx.triggered:
        return {"display": "none"}, {}

    # Check if close-modal button was clicked
    if ctx.triggered[-1]['prop_id'] == 'close-modal.n_clicks':
        return {"display": "none"}, {}

    # Find which chart was clicked
    chart_index = -1
    for i in range(len(charts)):
        if ctx.triggered[i]['prop_id'].startswith(f"chart-{i}"):
            chart_index = i

    if chart_index < 0:  # No chart was clicked
        return {"display": "none"}, {}

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

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)

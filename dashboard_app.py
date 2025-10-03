import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_dash_app():
    """Create and configure Dash app"""
    external_stylesheets = [
        'https://codepen.io/chriddyp/pen/bWLwgP.css',
        {
            'href': 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap',
            'rel': 'stylesheet'
        }
    ]
    
    app = dash.Dash(__name__, url_base_pathname='/dashboard/', external_stylesheets=external_stylesheets)
    
    # Sample data for the dashboard
    def generate_sample_data():
        """Generate sample data for demonstration"""
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        np.random.seed(42)
        
        # Create more realistic sales data
        base_sales = []
        categories = ['Electronics', 'Clothing', 'Books', 'Home']
        
        for date in dates:
            for category in categories:
                # Generate realistic daily sales with seasonal patterns
                day_of_year = date.timetuple().tm_yday
                seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * day_of_year / 365)
                
                # Weekend boost for some categories
                weekend_boost = 1.2 if category in ['Electronics', 'Books'] and date.weekday() >= 5 else 1.0
                
                daily_sales = np.random.normal(250, 50) * seasonal_factor * weekend_boost
                daily_sales = max(50, daily_sales)  # Ensure minimum sales
                
                base_sales.append({
                    'date': date,
                    'category': category,
                    'sales': daily_sales
                })
        
        sales_data = pd.DataFrame(base_sales)
        
        # Performance metrics
        metrics_data = {
            'Revenue': '$1,234,567',
            'Users': '45,678',
            'Conversion Rate': '3.2%',
            'Growth': '+12.5%'
        }
        
        return sales_data, metrics_data
    
    sales_data, metrics_data = generate_sample_data()
    
    # Dashboard layout
    app.layout = html.Div([
        # Header
        html.Div([
            html.H1("Business Dashboard", className="dashboard-title"),
            html.P("Real-time analytics and insights", className="dashboard-subtitle")
        ], className="header"),
        
        # Colored metrics cards row
        html.Div([
            html.Div([
                html.Div([
                    html.H3("$1,234,567", className="metric-value"),
                    html.P("Revenue", className="metric-label")
                ], className="metric-content")
            ], className="metric-card revenue-card"),
            
            html.Div([
                html.Div([
                    html.H3("45,678", className="metric-value"),
                    html.P("Users", className="metric-label")
                ], className="metric-content")
            ], className="metric-card users-card"),
            
            html.Div([
                html.Div([
                    html.H3("3.2%", className="metric-value"),
                    html.P("Conversion Rate", className="metric-label")
                ], className="metric-content")
            ], className="metric-card conversion-card"),
            
            html.Div([
                html.Div([
                    html.H3("+12.5%", className="metric-value"),
                    html.P("Growth", className="metric-label")
                ], className="metric-content")
            ], className="metric-card growth-card")
        ], className="metrics-container"),
        
        # Interactive controls
        html.Div([
            html.Div([
                html.Label("Date Range:", className="control-label"),
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date=sales_data['date'].min(),
                    end_date=sales_data['date'].max(),
                    display_format='YYYY-MM-DD',
                    className="date-picker"
                )
            ], className="control-group"),
            
            html.Div([
                html.Label("Categories:", className="control-label"),
                dcc.Dropdown(
                    id='category-dropdown',
                    options=[{'label': cat, 'value': cat} for cat in sales_data['category'].unique()],
                    value=sales_data['category'].unique().tolist(),
                    multi=True,
                    className="category-dropdown"
                )
            ], className="control-group")
        ], className="controls-container"),
        
        # Side by side charts
        html.Div([
            # Sales trend chart
            html.Div([
                html.H3("Sales Trend", className="chart-title"),
dcc.Graph(
                    id='sales-trend',
                    figure=px.line(
                        sales_data.groupby('date')['sales'].sum().reset_index(),
                        x='date', y='sales',
                        title="",
                        line_shape='spline'
                    ).update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#2c3e50'),
                        margin=dict(l=20, r=20, t=20, b=40),
                        xaxis_title="Date",
                        yaxis_title="Total Sales ($)"
                    ).update_traces(
                        line=dict(color='#667eea', width=3)
                    )
                )
            ], className="chart-container chart-half"),
            
            # Filtered sales data chart
            html.Div([
                html.H3("Filtered Sales Data", className="chart-title"),
                dcc.Graph(id='filtered-chart')
            ], className="chart-container chart-half")
        ], className="charts-row")
    ], className="dashboard-container")
    
    # Add custom CSS
    app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
            <style>
    ''' + app_styles + '''
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
    
    # Callback for interactive filtering
    @app.callback(
        Output('filtered-chart', 'figure'),
        [Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date'),
         Input('category-dropdown', 'value')]
    )
    def update_filtered_chart(start_date, end_date, selected_categories):
        # Handle empty or None categories
        if not selected_categories:
            selected_categories = sales_data['category'].unique().tolist()
        
        # Convert date strings to datetime for comparison
        if isinstance(start_date, str):
            start_date = pd.to_datetime(start_date)
        if isinstance(end_date, str):
            end_date = pd.to_datetime(end_date)
            
        # Filter the data
        filtered_data = sales_data[
            (sales_data['date'] >= start_date) & 
            (sales_data['date'] <= end_date) &
            (sales_data['category'].isin(selected_categories))
        ].copy()
        
        # Check if we have data after filtering
        if filtered_data.empty:
            # Return empty chart with message
            fig = go.Figure()
            fig.add_annotation(
                text="No data available for selected filters",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=16, color="#7f8c8d")
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                margin=dict(l=20, r=20, t=20, b=40)
            )
            return fig
        
        # Create weekly aggregation instead of monthly for better granularity
        filtered_data['week'] = filtered_data['date'].dt.to_period('W').astype(str)
        weekly_summary = filtered_data.groupby(['week', 'category'])['sales'].sum().reset_index()
        
        # Color palette for categories
        colors = {
            'Electronics': '#667eea',
            'Clothing': '#f093fb', 
            'Books': '#4facfe',
            'Home': '#43e97b'
        }
        
        # Create the bar chart
        fig = px.bar(
            weekly_summary,
            x='week', y='sales', color='category',
            title="",
            color_discrete_map=colors,
            labels={'week': 'Week', 'sales': 'Sales ($)', 'category': 'Category'}
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2c3e50'),
            margin=dict(l=20, r=20, t=20, b=60),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            xaxis_title="Week",
            yaxis_title="Sales ($)",
            showlegend=True
        )
        
        # Improve x-axis readability
        fig.update_xaxes(
            tickangle=45
        )
        
        return fig
    
    return app

# Custom CSS for enhanced styling
app_styles = """
.dashboard-container {
    font-family: 'Inter', sans-serif;
    margin: 0;
    padding: 20px;
    background-color: #f8f9fa;
}

.header {
    text-align: center;
    margin-bottom: 30px;
    padding: 30px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.dashboard-title {
    margin: 0;
    font-size: 2.5em;
    font-weight: 600;
}

.dashboard-subtitle {
    margin: 10px 0 0 0;
    font-size: 1.2em;
    opacity: 0.9;
}

.metrics-container {
    display: flex;
    gap: 20px;
    margin-bottom: 30px;
    flex-wrap: wrap;
}

.metric-card {
    flex: 1;
    min-width: 200px;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease;
}

.metric-card:hover {
    transform: translateY(-2px);
}

.metric-content {
    padding: 25px;
    text-align: center;
    position: relative;
    z-index: 2;
}

.revenue-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.users-card {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.conversion-card {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.growth-card {
    background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.metric-value {
    font-size: 2.2em;
    font-weight: 700;
    margin: 0;
    color: white;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.metric-label {
    margin: 8px 0 0 0;
    color: rgba(255,255,255,0.9);
    font-size: 1em;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.controls-container {
    background: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    margin-bottom: 30px;
    display: flex;
    gap: 30px;
    align-items: end;
    flex-wrap: wrap;
}

.control-group {
    flex: 1;
    min-width: 250px;
}

.control-label {
    display: block;
    margin-bottom: 8px;
    font-weight: 600;
    color: #2c3e50;
    font-size: 0.9em;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.charts-row {
    display: flex;
    gap: 20px;
    margin-bottom: 30px;
    flex-wrap: wrap;
}

.chart-container {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    padding: 25px;
    transition: transform 0.2s ease;
}

.chart-container:hover {
    transform: translateY(-2px);
}

.chart-half {
    flex: 1;
    min-width: 450px;
}

.chart-title {
    margin: 0 0 20px 0;
    color: #2c3e50;
    font-weight: 600;
    font-size: 1.3em;
    padding-bottom: 10px;
    border-bottom: 2px solid #ecf0f1;
}

.date-picker {
    width: 100%;
}

.category-dropdown {
    width: 100%;
}
"""
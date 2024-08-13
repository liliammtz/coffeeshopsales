from streamlit_dynamic_filters import DynamicFilters
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(layout="wide")

# Cargar datos
df = pd.read_csv("coffeeshop.csv")
#counts = df.value_counts(['store_location', 'product_category', 'product_type', 'product_detail']).reset_index(name='count')
df['Revenue'] = df['transaction_qty'] + df['unit_price']
df['transaction_time'] = pd.to_datetime(df['transaction_time'], format='%H:%M:%S')
df['Date'] = pd.to_datetime(df['transaction_date'], format='%d/%m/%Y')
#* df['YearMonth'] = df['Date'].dt.to_period('M')
df.rename(columns={
    'store_location': 'Store Location',
    'product_category': 'Product Category',
    'product_type': 'Product Type',
    'product_detail': 'Product Detail'
}, inplace=True)

dynamic_filters = DynamicFilters(df, filters=['Store Location', 'Product Category', 'Product Type', 'Product Detail'])
dynamic_filters.display_filters(location='sidebar')

#dynamic_filters.display_df()

df_filtered = dynamic_filters.filter_df()

st.header(f"{df_filtered['transaction_id'].nunique():,} transactions")
st.header(f"$ {df_filtered['Revenue'].sum():,.2f} revenue")

# Crear la gráfica con mejoras estéticas
fig_hourly = px.line(
    df_filtered.groupby("Hour")['Revenue'].sum().reset_index(),
    x='Hour',
    y='Revenue',
    title='Revenue by Hour',
    labels={'Hour': 'Hour of the Day', 'Revenue': 'Total Revenue'},
    template='plotly_white'
)

# Mejorar la estética de la gráfica
fig_hourly.update_traces(line=dict(color='saddlebrown', width=2), marker=dict(size=8, color='saddlebrown'))
fig_hourly.update_layout(
    title={'x':0.5, 'xanchor': 'center'},
    xaxis=dict(
        title='Hour of the Day',
        tickmode='linear',
        tick0=0,
        dtick=1,
        titlefont=dict(color='#3E2723'),
        tickfont=dict(color='#3E2723')
    ),
    yaxis=dict(
        title='Total Revenue',
        tickprefix='$',
        showgrid=True,
        gridwidth=1,
        titlefont=dict(color='#3E2723'),
        gridcolor='#AF8F6F',
        tickfont=dict(color='#3E2723')
    ),
    #plot_bgcolor='white',
    margin=dict(l=0, r=0, t=50, b=0)
)

#! Grafica
# Contar el número de transacciones por día
daily_transactions = df_filtered.groupby('Date').size().reset_index(name='Transaction Count')

# Crear la gráfica de transacciones diarias
fig_daily = px.line(
    daily_transactions,
    x='Date',
    y='Transaction Count',
    title='Daily Transactions',
    labels={'Date': 'Date', 'Transaction Count': 'Number of Transactions'},
    template='plotly_white'
)

# Mejorar la estética de la gráfica
fig_daily.update_traces(line=dict(color='saddlebrown', width=2))
fig_daily.update_layout(
    title={'x':0.5, 'xanchor': 'center'},
    xaxis=dict(
        title='Date',
        tickformat='%d/%m/%Y',
        titlefont=dict(color='#3E2723'),
        tickfont=dict(color='#3E2723')

    ),
    yaxis=dict(
        title='TXNs',
        showgrid=True,
        gridwidth=1,
        titlefont=dict(color='#3E2723'),
        gridcolor='#AF8F6F',
        tickfont=dict(color='#3E2723')
    ),
    #plot_bgcolor='white',
    margin=dict(l=0, r=0, t=50, b=0)
)

#! New graph
monthly_transactions = df_filtered.groupby('Month').size().reset_index(name='Transaction Count')

# Crear la gráfica de barras de transacciones mensuales
fig_txn_monthly = px.bar(
    monthly_transactions,
    x='Month',
    y='Transaction Count',
    title='Monthly Transactions',
    labels={'Month': 'Month', 'Transaction Count': 'Number of Transactions'},
    template='plotly_white',
    color_discrete_sequence=['saddlebrown']  # Correct way to set the bar color
)
fig_txn_monthly.update_layout(
    title={'x':0.5, 'xanchor': 'center'},
    xaxis=dict(
        #title='Date',
        #tickformat='%d/%m/%Y',
        titlefont=dict(color='#3E2723'),
        tickfont=dict(color='#3E2723')
    ),
    yaxis=dict(
        #title='TXNs',
        #showgrid=True,
        #gridwidth=1,
        titlefont=dict(color='#3E2723'),
        tickfont=dict(color='#3E2723'),
        gridcolor='#AF8F6F'
    ),
    #plot_bgcolor='white',
    margin=dict(l=0, r=0, t=50, b=0)
)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_hourly)
    st.plotly_chart(fig_txn_monthly)
with col2:
    st.plotly_chart(fig_daily)
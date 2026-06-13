import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dark Store Optimization Engine", layout="wide")
st.title("Hyperlocal Dark Store Operational Dashboard")
st.markdown("Real-time monitoring of delivery bottlenecks, SLA breaches, and rider distribution.")

def get_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="manoj123",
        database="darkstore_analytics"
    )

    query = """
    SELECT 
        z.zone_name,
        COUNT(f.order_id) AS total_orders,
        COUNT(CASE WHEN f.operational_status = 'BREACHED_SLA' THEN 1 END) AS delayed_orders,
        ROUND((COUNT(CASE WHEN f.operational_status = 'BREACHED_SLA' THEN 1 END) / COUNT(f.order_id)) * 100, 2) AS delay_percentage
    FROM fact_orders f
    JOIN dim_zone z ON f.zone_id = z.zone_id
    GROUP BY z.zone_name;
    """
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    df = pd.DataFrame(result)
    
    cursor.close()
    conn.close()
    return df

try:
    df_metrics = get_data()
except Exception as e:
    st.error(f"Database connection error: {e}")
    df_metrics = pd.DataFrame()

if not df_metrics.empty:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Simulated Orders", int(df_metrics['total_orders'].sum()))
    with col2:
        st.metric("Total SLA Breaches", int(df_metrics['delayed_orders'].sum()), delta_color="inverse")
    with col3:
        avg_delay = round((df_metrics['delayed_orders'].sum() / df_metrics['total_orders'].sum()) * 100, 2)
        st.metric("Avg Fleet Delay Rate", f"{avg_delay}%")

    st.markdown("---")

    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("SLA Breach Percentage by Zone")
        fig_bar = px.bar(
            df_metrics, 
            x="zone_name", 
            y="delay_percentage", 
            text="delay_percentage",
            color="delay_percentage",
            color_continuous_scale="Reds",
            labels={"delay_percentage": "SLA Breach %", "zone_name": "Delivery Zone"}
        )
        st.plotly_chart(fig_bar, width='stretch')

    with right_col:
        st.subheader("Order Volume Distribution")
        fig_pie = px.pie(
            df_metrics, 
            values="total_orders", 
            names="zone_name", 
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_pie, width='stretch')

    st.subheader("Underlying Zone Performance Data")
    st.dataframe(df_metrics, width='stretch')
else:
    st.warning("No data found in database tables.")
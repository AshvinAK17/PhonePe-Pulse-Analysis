import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title=" PhonePe Pulse Dashboard", layout="wide")

# ---------- DB CONNECTION ----------
@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="PhonePe_Pulse"
    )
conn = get_connection()
cursor = conn.cursor()

# ---------- STYLE ----------
page_bg_style = """
<style>
    .stApp {
        background-color: #000000;
        color: white;
    }
    .main .block-container {
        padding: 1rem 2rem !important;
        max-width: 100% !important;
        width: 100% !important;
    }
</style>
"""
st.markdown(page_bg_style, unsafe_allow_html=True)

# ---------- UTILITY FUNCTION ----------
def check_and_warn_empty(df, message="No data available to plot."):
    if df.empty or df.isnull().all().all():
        st.warning(message)
        return True
    return False

# ---------- PAGE 1: CHOROPLETH ----------
def india_overview_page(cursor):
    st.title(" India Transaction Overview")

    # Filter years and quarters without nulls in agg_trans
    cursor.execute("SELECT DISTINCT Year FROM agg_trans WHERE Year IS NOT NULL ORDER BY Year;")
    years = [row[0] for row in cursor.fetchall()]
    selected_year = st.selectbox("Select Year", options=years, key="choropleth_year")

    cursor.execute(f"SELECT DISTINCT Quarter FROM agg_trans WHERE Year={selected_year} AND Quarter IS NOT NULL ORDER BY Quarter;")
    quarters = [row[0] for row in cursor.fetchall()]
    selected_quarter = st.selectbox("Select Quarter", options=quarters, key="choropleth_quarter")

    query = f"""
        SELECT State, SUM(Transaction_amount) AS Total_amount
        FROM agg_trans
        WHERE Year = {selected_year} AND Quarter = {selected_quarter}
        GROUP BY State
        ORDER BY Total_amount DESC;
    """
    cursor.execute(query)
    df_map = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_amount'])

    if check_and_warn_empty(df_map, "No transaction data found for selected year and quarter."):
        return

    geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/india_states.geojson"

    fig = px.choropleth(
        df_map,
        geojson=geojson_url,
        featureidkey='properties.ST_NM',
        locations='State',
        color='Total_amount',
        color_continuous_scale='Reds',
        title=f"Total Transaction Amount by State (Year: {selected_year}, Q{selected_quarter})",

    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        paper_bgcolor='black',
        plot_bgcolor='black',
        font_color='white',
        margin=dict(l=0, r=0, t=50, b=0),
        coloraxis_colorbar=dict(title="Amount", tickfont_color="white", title_font_color="white"),
    )
    st.plotly_chart(fig, use_container_width=True, height=800, width=500)


# ---------- PAGE 2: BUSINESS CASES ----------
def business_case_analysis(cursor):
    st.title(" Business Case Analysis")

    # Filter years and quarters without nulls in agg_trans (used for consistency)
    cursor.execute("SELECT DISTINCT Year FROM agg_trans WHERE Year IS NOT NULL ORDER BY Year;")
    years = [row[0] for row in cursor.fetchall()]
    selected_year = st.selectbox("Select Year", options=years, key="business_year")

    cursor.execute(f"SELECT DISTINCT Quarter FROM agg_trans WHERE Year={selected_year} AND Quarter IS NOT NULL ORDER BY Quarter;")
    quarters = [row[0] for row in cursor.fetchall()]
    selected_quarter = st.selectbox("Select Quarter", options=quarters, key="business_quarter")

    case = st.selectbox("Select Business Case", [
        "1. Decoding transaction dynamics on PhonePe",
        "2. Device Dominance and User Engagement Analysis",
        "3. Insurance Penetration and Growth Potential Analysis",
        "4. Insurance Engagement Analysis",
        "5. Transaction Analysis Across States and Districts"
    ], key="case_select")

    geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/india_states.geojson"

    if case == "1. Decoding transaction dynamics on PhonePe":
        st.header("Decoding Transaction Dynamics on PhonePe")

        # Query 1
        st.subheader(" Year-wise Total Transaction Amount by State")
        query1 = f"""
        SELECT State, Year, SUM(Transaction_amount) AS Total_amount
        FROM agg_trans
        WHERE Year = {selected_year} AND Quarter = {selected_quarter}
        GROUP BY State, Year
        ORDER BY State, Year;
        """
        cursor.execute(query1)
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Year', 'Total_amount'])
        if check_and_warn_empty(df1):
            return
        plt.figure(figsize=(14, 8))
        sns.barplot(data=df1, x='State', y='Total_amount', palette='viridis')
        plt.title(f'Total Transaction Amount by State (Year: {selected_year}, Q{selected_quarter})')
        plt.xticks(rotation=45)
        plt.grid(True)
        st.pyplot(plt.gcf())
        plt.clf()

        # Query 2
        st.subheader(" Quarterly Transaction Count by Transaction Type")
        query2 = f"""
        SELECT Transaction_type, Year, Quarter, SUM(Transaction_count) AS Total_count
        FROM agg_trans
        WHERE Year = {selected_year} AND Quarter = {selected_quarter}
        GROUP BY Transaction_type, Year, Quarter
        ORDER BY Transaction_type, Year, Quarter;
        """
        cursor.execute(query2)
        df2 = pd.DataFrame(cursor.fetchall(), columns=['Transaction_type', 'Year', 'Quarter', 'Total_count'])
        if check_and_warn_empty(df2):
            return
        plt.figure(figsize=(14, 6))
        sns.barplot(data=df2, x='Transaction_type', y='Total_count', palette='magma')
        plt.title(f'Transaction Count by Type (Year: {selected_year}, Q{selected_quarter})')
        plt.grid(True)
        st.pyplot(plt.gcf())
        plt.clf()

        # Query 3
        st.subheader(" State-wise Total Transaction Amount (Choropleth)")
        query3 = f"""
        SELECT State, SUM(Transaction_amount) AS Total_amount
        FROM agg_trans
        WHERE Year = {selected_year} AND Quarter = {selected_quarter}
        GROUP BY State
        ORDER BY Total_amount DESC;
        """
        cursor.execute(query3)
        df3 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_amount'])
        if check_and_warn_empty(df3):
            return
        fig = px.choropleth(
            df3, geojson=geojson_url, locations='State', featureidkey='properties.ST_NM',
            color='Total_amount', color_continuous_scale='YlGnBu',
            title=f'Choropleth: Total Transaction Amount by State (Year: {selected_year}, Q{selected_quarter})'
        )
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)

    elif case == "2. Device Dominance and User Engagement Analysis":
        st.header("Device Dominance and User Engagement Analysis")

        # Query 4
        st.subheader(" Top Device Brands by Total Registrations")
        query4 = f"""
        SELECT Brand, SUM(Count) AS Total_Registrations
        FROM agg_user
        WHERE Year = {selected_year} AND Quarter = {selected_quarter}
        GROUP BY Brand
        ORDER BY Total_Registrations DESC;
        """
        cursor.execute(query4)
        df4 = pd.DataFrame(cursor.fetchall(), columns=['Brand', 'Total_Registrations'])
        if check_and_warn_empty(df4):
            return
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df4.head(10), x='Brand', y='Total_Registrations', palette='crest')
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())
        plt.clf()

        # Query 5
        st.subheader(" Brand-wise Avg Registered Users")
        query5 = f"""
        SELECT Brand, AVG(Count) AS Avg_Users
        FROM agg_user
        WHERE Year = {selected_year} AND Quarter = {selected_quarter}
        GROUP BY Brand;
        """
        cursor.execute(query5)
        df5 = pd.DataFrame(cursor.fetchall(), columns=['Brand', 'Avg_Users'])
        if check_and_warn_empty(df5):
            return
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df5, x='Brand', y='Avg_Users', palette='rocket')
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())
        plt.clf()

    elif case == "3. Insurance Penetration and Growth Potential Analysis":
        st.header("Insurance Penetration and Growth Potential Analysis")

        # Query 6
        st.subheader(" State-wise Insurance Amount")
        query6 = f"""
        SELECT State, SUM(Transaction_amount) AS Total_Insurance_Amount
        FROM agg_ins
        WHERE Year = {selected_year} AND Quarter = {selected_quarter}
        GROUP BY State
        ORDER BY Total_Insurance_Amount DESC;
        """
        cursor.execute(query6)
        df6 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Insurance_Amount'])
        if check_and_warn_empty(df6):
            return
        plt.figure(figsize=(14, 7))
        sns.barplot(data=df6, x='State', y='Total_Insurance_Amount', palette='Spectral')
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())
        plt.clf()

        # Query 7
        st.subheader(" Insurance Transaction Trend by Year and Quarter")

        query7 = f"""
        SELECT State, Year, Quarter, SUM(Transaction_amount) AS Total_Insurance_Amount
        FROM agg_ins
        WHERE Year <= {selected_year} AND Quarter <= {selected_quarter}
        GROUP BY State, Year, Quarter;
        """

        cursor.execute(query7)
        results7 = cursor.fetchall()

        df7 = pd.DataFrame(results7, columns=['State', 'Year', 'Quarter', 'Total_Insurance_Amount'])

        # Sort for pct_change calculation
        df7 = df7.sort_values(['State', 'Year', 'Quarter'])

        # Calculate growth %
        df7['Growth_Pct'] = df7.groupby('State')['Total_Insurance_Amount'].pct_change() * 100

        # Drop NaNs in growth
        df7 = df7.dropna(subset=['Growth_Pct'])

        # Filter data exactly up to selected year and quarter for visualization
        df7_filtered = df7[(df7['Year'] == selected_year) & (df7['Quarter'] == selected_quarter)]

        # Pivot for heatmap (State vs Quarter with growth %)
        heatmap_data = df7_filtered.pivot(index='State', columns='Quarter', values='Growth_Pct')

        plt.figure(figsize=(12, 10))
        sns.heatmap(
            heatmap_data,
            annot=True,
            fmt=".1f",
            cmap="YlGnBu",
            cbar_kws={'label': 'Growth %'},
            linewidths=0.5,
            linecolor='gray'
        )
        plt.title(f'Insurance Transaction Growth % Heatmap for Year {selected_year} Quarter {selected_quarter}')
        plt.xlabel('Quarter')
        plt.ylabel('State')
        plt.tight_layout()

        st.pyplot(plt.gcf())
        plt.clf()

        
    elif case == "4. Insurance Engagement Analysis":
        st.header("Insurance Engagement Analysis")

        # Query 8
        st.subheader(" State-wise Insurance Distribution")
        query8 = f"""
        SELECT State, SUM(Transaction_amount) AS Total_Insurance_Amount
        FROM agg_ins
        WHERE Year = {selected_year} AND Quarter = {selected_quarter}
        GROUP BY State;
        """
        cursor.execute(query8)
        df8 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Insurance_Amount'])
        if check_and_warn_empty(df8):
            return
        fig = px.choropleth(
            df8,
            geojson=geojson_url,
            locations='State',
            featureidkey='properties.ST_NM',
            color='Total_Insurance_Amount',
            color_continuous_scale='YlOrBr',
            title=f"Insurance Amount Distribution (Year: {selected_year}, Q{selected_quarter})"
        )
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)

        # Query 9
        st.subheader(" Quarterly Growth % in Insurance")
        query9 = f"""
        SELECT State, Year, Quarter, SUM(Transaction_amount) AS Total_Insurance_Amount
        FROM agg_ins
        WHERE Year = {selected_year} 
        AND Quarter <= {selected_quarter}
        GROUP BY State, Year, Quarter
        ORDER BY State, Year, Quarter;
        """
        cursor.execute(query9)
        df9 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Year', 'Quarter', 'Total_Insurance_Amount'])

        if check_and_warn_empty(df9):
            return

        # Sort properly
        df9 = df9.sort_values(['State', 'Year', 'Quarter'])

        # Calculate Growth %
        df9['Growth_Pct'] = df9.groupby('State')['Total_Insurance_Amount'].pct_change() * 100

        # Filter data to show only selected quarter (or optionally all quarters for lineplot)
        df9_filtered = df9[(df9['Year'] == selected_year) & (df9['Quarter'] == selected_quarter)]

        if df9_filtered.empty:
            st.warning("No growth data available for the selected year and quarter.")
            return

        plt.figure(figsize=(14, 8))
        sns.barplot(data=df9_filtered, x='State', y='Growth_Pct', palette='coolwarm')
        plt.title(f'Quarterly Growth % in Insurance (Year: {selected_year}, Q{selected_quarter})')
        plt.xticks(rotation=45)
        plt.ylabel('Growth %')
        plt.grid(True)
        st.pyplot(plt.gcf())
        plt.clf()

    elif case == "5. Transaction Analysis Across States and Districts":
        st.header("Transaction Analysis Across States and Districts")

        # Query 10
        st.subheader(" Top Performing States")
        query10 = f"""
        SELECT State, SUM(Transaction_amount) AS Total_Amount
        FROM top_trans_dist
        WHERE Year = {selected_year} AND Quarter = {selected_quarter}
        GROUP BY State
        ORDER BY Total_Amount DESC
        LIMIT 10;
        """
        cursor.execute(query10)
        df10 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Amount'])
        if check_and_warn_empty(df10):
            return
        st.plotly_chart(px.bar(df10, x='State', y='Total_Amount', title=f"Top States by Amount (Year: {selected_year}, Q{selected_quarter})"))

        # Query 11
        st.subheader(" Top Districts by Transaction Value & Volume")
        query11 = f"""
        SELECT District, SUM(Transaction_count) AS Total_Transactions, SUM(Transaction_amount) AS Total_Amount
        FROM top_trans_dist
        WHERE Year = {selected_year} AND Quarter = {selected_quarter}
        GROUP BY District
        ORDER BY Total_Amount DESC
        LIMIT 10;
        """
        cursor.execute(query11)
        df11 = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Transactions', 'Total_Amount'])
        if check_and_warn_empty(df11):
            return
        fig, axs = plt.subplots(1, 2, figsize=(16, 6))
        sns.barplot(data=df11, x='Total_Transactions', y='District', ax=axs[0], palette='Greens')
        sns.barplot(data=df11, x='Total_Amount', y='District', ax=axs[1], palette='Reds')
        axs[0].set_title("Top Districts by Transaction Volume")
        axs[1].set_title("Top Districts by Transaction Value")
        plt.tight_layout()
        st.pyplot(fig)
        plt.clf()

        # Query 12
        st.subheader(" Top Pincodes by Transactions (Horizontal Bar Plot)")
        query12 = f"""
        SELECT pincodes, SUM(Transaction_count) AS Total_Transactions, SUM(Transaction_amount) AS Total_Amount
        FROM top_trans_pinc
        WHERE Year = {selected_year} AND Quarter = {selected_quarter}
        GROUP BY pincodes
        ORDER BY Total_Amount DESC
        LIMIT 10;
        """
        cursor.execute(query12)
        df12 = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Total_Transactions', 'Total_Amount'])
        if check_and_warn_empty(df12):
            return
        plt.figure(figsize=(10, 7))
        sns.barplot(data=df12, y='Pincode', x='Total_Amount', palette='Blues_r')
        plt.title(f"Top Pincodes by Transaction Amount (Year: {selected_year}, Q{selected_quarter})")
        plt.xlabel("Total Transaction Amount")
        plt.ylabel("Pincode")
        st.pyplot(plt.gcf())
        plt.clf()

# ---------- MAIN APP ----------
def main():
    page = st.sidebar.radio(" Navigation", [" India Overview (Choropleth)", " Business Case Analysis"])
    if page == " India Overview (Choropleth)":
        india_overview_page(cursor)
    elif page == " Business Case Analysis":
        business_case_analysis(cursor)

if __name__ == "__main__":
    main()

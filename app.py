import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import io
import base64

st.set_page_config(page_title="Auto Data Analyzer", layout="wide")
st.title("📊 Auto Data Analyzer Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!")

    st.subheader("1. Dataset Preview")
    st.dataframe(df.head())

    st.subheader("2. Basic Info")
    st.write("Number of Rows:", df.shape[0])
    st.write("Number of Columns:", df.shape[1])
    st.write("Column Data Types:")
    st.dataframe(df.dtypes.astype(str))
    st.write("Missing Values:")
    st.dataframe(df.isnull().sum())

    st.subheader("3. Descriptive Statistics")
    st.dataframe(df.describe(include='all'))

    st.subheader("4. Visualizations")

    # Correlation Heatmap
    st.markdown("### Correlation Heatmap")
    corr = df.select_dtypes(include='number').corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

    # Histograms for numeric columns
    st.markdown("### Histograms of Numerical Features")
    numeric_cols = df.select_dtypes(include='number').columns
    for col in numeric_cols:
        fig = px.histogram(df, x=col, nbins=30, title=f"Distribution of {col}")
        st.plotly_chart(fig)

    # Boxplots
    st.markdown("### Boxplots of Numerical Features")
    for col in numeric_cols:
        fig = px.box(df, y=col, title=f"Boxplot of {col}")
        st.plotly_chart(fig)

    # Bar charts for categorical columns
    st.markdown("### Bar Charts of Categorical Features")
    cat_cols = df.select_dtypes(include='object').columns
    for col in cat_cols:
        value_counts = df[col].value_counts().reset_index()
        value_counts.columns = [col, 'count']
        fig = px.bar(value_counts, x=col, y='count',
                     labels={col: col, 'count': 'Count'}, title=f"Value Counts of {col}")
        st.plotly_chart(fig)

    st.subheader("5. Download Report")
    buffer = io.StringIO()
    df.describe(include='all').to_csv(buffer)
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read().encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="descriptive_statistics.csv">Download Descriptive Statistics as CSV</a>'
    st.markdown(href, unsafe_allow_html=True)

else:
    st.info("👆 Please upload a CSV file to get started.")


# Stylish Animated Footer
st.markdown(
    """
    <style>
    .footer {
        position: relative;
        bottom: 0;
        width: 100%;
        background: linear-gradient(to right, #000000, #1c1c1c);
        color: #ffffff;
        text-align: center;
        padding: 20px 0;
        font-family: 'Rubik', sans-serif;
        font-size: 15px;
        margin-top: 60px;
        border-top: 2px solid #ff0000;
        animation: slideUp 2s ease-in-out;
    }

    .footer a {
        color: #ff4d4d;
        text-decoration: none;
        font-weight: 600;
        transition: color 0.3s ease;
    }

    .footer a:hover {
        color: #ffffff;
        text-shadow: 0 0 10px #ff4d4d;
    }

    .footer p {
        margin: 5px 0 0;
        color: #bbbbbb;
    }

    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(40px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    </style>

    <div class="footer">
        <h4>Developed by <a href="https://www.linkedin.com/in/rambabukumargiri/" target="_blank">Rambabu Kumar</a></h4>
        <p>&copy; 2025 All rights reserved.</p>
    </div>
    """,
    unsafe_allow_html=True
)
import pandas as pd 
import streamlit as st
import plotly.express as px
import plotly.graph_objects as pg
import requests
from streamlit_lottie import st_lottie


# --  asset url: https://lottie.host/a006c5a4-487e-422a-9df9-1a81dc42ea72/zixsHAcPZ8.json
def load_lot(url):
    r= requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()
 
lot_cod = load_lot("https://lottie.host/a006c5a4-487e-422a-9df9-1a81dc42ea72/zixsHAcPZ8.json")    

st_lottie(lot_cod,height=300,key='coding')

st.title("بيانات الوظائف المعلنة في منصة جدارات")
df_jadarat = pd.read_csv("clean_jadarat.csv")
df_jadarat.drop(columns=["Unnamed: 0"], inplace=True)

css = """
<style>
body {
    font-family: 'Arial', sans-serif;
    background-color: #f2f2f2;  
    color: #333;  
    text-align: center;  
}

h1 {
    color: #E4002B;  /* Toyota red */
}

h2, h3 {
    color: #333;
}

.stButton button {
    background-color: #E4002B;  /* Toyota red */
    color: white;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    cursor: pointer;
}

.stButton button:hover {
    background-color: #B3001B;  /* Darker red on hover */
}

.plotly-graph div {
    background-color: white;  /* White background for plots */
    border-radius: 10px;  /* Rounded corners */
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);  /* Subtle shadow */
    padding: 10px;  /* Padding for the plot area */
}

.markdown-text {
    margin: 20px 0;
}
</style>
"""

region_counts = df_jadarat['region'].value_counts().reset_index()
region_counts.columns = ['region', 'count']





# Q1 by using Plotly
# Plotting with Plotly
fig = px.pie(region_counts, 
             names='region', 
             values='count', 
             title='نسبة الوظائف المعلن عنها لكل منطقة في المملكة العربية السعودية',
             hole=0.2,  
             ) 



fig.update_layout(
    width=800,  
    height=600  
)
fig.update_traces(textinfo='percent+label')  # Display percentage and label
st.plotly_chart(fig)


# Q2
gender_counts = df_jadarat['gender'].value_counts()
total_count = gender_counts.sum()
percentages = (gender_counts / total_count * 100).round(1)
# Create a figure
fig2 = pg.Figure(data=[
    pg.Bar(
        name='Male',
        x=['Male'],  # X-axis category
        y=[gender_counts.get('M', 0)],  # Count of males
        text=f"{percentages.get('M', 0)}%"
    ),
    pg.Bar(
        name='Female',
        x=['Female'],  # X-axis category
        y=[gender_counts.get('F', 0)],  # Count of females
        text=f"{percentages.get('F', 0)}%"
    )
])

# Update layout
fig2.update_layout(
    title='نسبة الوظائف المعلن عنها للذكور والإناث',
    xaxis_title='Gender',
    yaxis_title='Number of Job Postings ',
    barmode='group'  # Grouped bar mode
)

# Show the plot
st.plotly_chart(fig2)

# Q3
fresh_grads = df_jadarat[df_jadarat['exper'] == 0]

fig3 = px.box(fresh_grads, 
                 x='exper', 
                 y='benefits', 
                 title='مدى الراتب للخريجين ', 
                 labels={'exper': 'Freshers', 'benefits': 'Salary'},
                 color='exper', 
                 hover_data=['benefits'],
                 color_discrete_sequence=px.colors.sequential.Blues_r)

# Show the plot
st.plotly_chart(fig3)

# Q4
fig4 = px.histogram(
    df_jadarat,
    x='exper',
    color='exper',  # Use 'exper' for color
    color_discrete_sequence=px.colors.sequential.Aggrnyl,  # Dark to light color scale
    title='Number of Job Postings by Experience'
)

# Show the plot
st.plotly_chart(fig4)

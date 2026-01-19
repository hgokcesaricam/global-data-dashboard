import streamlit as st
import pandas as pd
st.title("Global Development Analysis")
url = "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
df = pd.read_csv(url)
country_list = df['country'].unique()
selected_country = st.selectbox("Select a Country",country_list)
filtered_df = df[df['country'] == selected_country]
st.dataframe(filtered_df)

filtered_df = filtered_df.sort_values("year")
first_year_data = filtered_df.iloc[0]
last_year_data = filtered_df.iloc[-1]

gdp_difference = last_year_data['gdpPercap'] - first_year_data['gdpPercap']
life_difference = last_year_data['lifeExp'] - first_year_data['lifeExp']
pop_difference = last_year_data['pop'] - first_year_data['pop']

m1,m2,m3 = st.columns(3)

with m1:
    st.metric(
        label="Total Population(2007)",
        value=f"{last_year_data['pop']:,}",
        delta=f"{pop_difference:,}"
    )

with m2:
    st.metric(
        label="GDP per Capita",
        value=f"${last_year_data['gdpPercap']:.2f}",
        delta=f"${gdp_difference:.2f}"
    )

with m3:
    st.metric(
        label="Life Expectancy",
        value=f"{last_year_data['lifeExp']:.1f} Years",
        delta=f"{life_difference:.1f} Years"
    )

    st.markdown("---")


st.subheader("Development over Time")

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### GDP per Capita($)")
    st.line_chart(filtered_df, x="year", y="gdpPercap")
with col2:
    st.markdown("#### Life Expectancy(Years)")
    st.line_chart(filtered_df, x="year", y="lifeExp")

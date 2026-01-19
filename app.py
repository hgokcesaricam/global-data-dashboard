import streamlit as st
import pandas as pd

st.set_page_config(page_title="Global Development Dashboard", layout="wide")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
    return pd.read_csv(url)

df = load_data()
country_list = sorted(df['country'].unique())

st.sidebar.header("🛠️ Control Panel")

if st.sidebar.button("🔄 Reset Selections", use_container_width=True):
    st.rerun()

st.sidebar.markdown("---")

compare_mode = st.sidebar.checkbox("Enable Comparison Mode 🔄")

options = ["Please select a country"] + list(country_list)

country_1 = st.sidebar.selectbox("Select Main Country", options, index=0)

country_2 = "Please select a country"
if compare_mode:
    country_2 = st.sidebar.selectbox("Select Second Country", options, index=0)

st.sidebar.markdown("---")
st.sidebar.write("**Data Source:**")
st.sidebar.caption("Gapminder Foundation. Covers global socio-economic data from 1952 to 2007.")

if country_1 != "Please select a country":
    st.toast(f"Data for {country_1} loaded successfully!", icon="✅")
    
    df1 = df[df['country'] == country_1].sort_values("year")
    last_1 = df1.iloc[-1]
    first_1 = df1.iloc[0]

    if compare_mode and country_2 != "Please select a country" and country_1 != country_2:
        df2 = df[df['country'] == country_2].sort_values("year")
        last_2 = df2.iloc[-1]
        
        st.markdown(f"<h1 style='text-align: center;'>📊 {country_1} vs {country_2}</h1>", unsafe_allow_html=True)
        st.markdown("---")

        m1, m2, m3 = st.columns(3)
        with m1:
            diff_pop = last_1['pop'] - last_2['pop']
            st.metric(label=f"Population ({country_1})", value=f"{last_1['pop']:,.0f}", delta=f"{diff_pop:,.0f} vs {country_2}")
        with m2:
            diff_gdp = last_1['gdpPercap'] - last_2['gdpPercap']
            st.metric(label=f"GDP per Capita ({country_1})", value=f"${last_1['gdpPercap']:,.2f}", delta=f"${diff_gdp:,.2f} vs {country_2}")
        with m3:
            diff_life = last_1['lifeExp'] - last_2['lifeExp']
            st.metric(label=f"Life Exp. ({country_1})", value=f"{last_1['lifeExp']:.2f}", delta=f"{diff_life:.2f} vs {country_2}")

        st.info(f"💡 **Comparison Insight:** In 2007, {country_1}'s GDP per capita was **${abs(diff_gdp):,.2f}** {'higher' if diff_gdp > 0 else 'lower'} than {country_2}, with a life expectancy difference of **{abs(diff_life):.1f}** years.")

        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<h4 style='text-align: center;'>GDP Growth ($)</h4>", unsafe_allow_html=True)
            gdp_data = pd.DataFrame({
                "Year": df1["year"],
                country_1: df1["gdpPercap"].round(2).values,
                country_2: df2["gdpPercap"].round(2).values
            }).set_index("Year")
            st.line_chart(gdp_data, color=["#FF4B4B", "#0068C9"])
        
        with c2:
            st.markdown("<h4 style='text-align: center;'>Life Expectancy Trends</h4>", unsafe_allow_html=True)
            life_data = pd.DataFrame({
                "Year": df1["year"],
                country_1: df1["lifeExp"].round(2).values,
                country_2: df2["lifeExp"].round(2).values
            }).set_index("Year")
            st.line_chart(life_data, color=["#FF4B4B", "#0068C9"])

    else:
        if compare_mode and country_1 == country_2:
            st.warning("⚠️ Please select two different countries to compare.")
        
        st.markdown(f"<h1 style='text-align: center;'>📈 {country_1} Analysis</h1>", unsafe_allow_html=True)
        st.markdown("---")

        m1, m2, m3 = st.columns(3)
        with m1:
            pop_growth = last_1['pop'] - first_1['pop']
            st.metric(label="Total Population (2007)", value=f"{last_1['pop']:,.0f}", delta=f"{pop_growth:,.0f} since 1952")
        with m2:
            gdp_growth = last_1['gdpPercap'] - first_1['gdpPercap']
            st.metric(label="GDP per Capita", value=f"${last_1['gdpPercap']:,.2f}", delta=f"${gdp_growth:,.2f}")
        with m3:
            life_growth = last_1['lifeExp'] - first_1['lifeExp']
            st.metric(label="Life Expectancy", value=f"{last_1['lifeExp']:.2f} Yrs", delta=f"{life_growth:.2f}")

        gdp_pct = ((last_1['gdpPercap'] - first_1['gdpPercap']) / first_1['gdpPercap']) * 100
        st.success(f"💡 **Analysis Summary:** Between 1952 and 2007, {country_1}'s GDP increased by **%{gdp_pct:.1f}**, while life expectancy improved by **{last_1['lifeExp'] - first_1['lifeExp']:.1f}** years.")

        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<h4 style='text-align: center;'>GDP per Capita Over Time</h4>", unsafe_allow_html=True)
            st.line_chart(df1.assign(gdpPercap=df1['gdpPercap'].round(2)), x="year", y="gdpPercap")
        with c2:
            st.markdown("<h4 style='text-align: center;'>Life Expectancy Over Time</h4>", unsafe_allow_html=True)
            st.line_chart(df1.assign(lifeExp=df1['lifeExp'].round(2)), x="year", y="lifeExp")

    st.markdown("---")
    col_extra1, col_extra2 = st.columns([2, 1])
    with col_extra1:
        with st.expander("📂 View Raw Data Table"):
            st.dataframe(df1.sort_values("year", ascending=False), use_container_width=True)
    with col_extra2:
        csv = df1.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data (CSV)",
            data=csv,
            file_name=f"{country_1}_data.csv",
            mime='text/csv',
            use_container_width=True
        )

else:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🌍 Global Development Insights</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #0068C9;'>Visualize Socio-Economic Trends Across Nations</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    _, middle_col, _ = st.columns([1, 2, 1])
    with middle_col:
        st.markdown("""
        <div style='text-align: center;'>
            <h4>Welcome to the Dashboard!</h4>
            <p>This platform provides a comprehensive view of historical development metrics between 1952 and 2007.</p>
            <ul style='list-style-position: inside; display: inline-block; text-align: left;'>
                <li><b>Step 1:</b> Select a <b>Main Country</b> from the sidebar.</li>
                <li><b>Step 2:</b> Enable <b>Comparison Mode</b> to compare İki nations.</li>
            </ul>
            <br>
            <p style='color: darkred;'>Ready to explore? Please use the Control Panel on the left.</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)
st.divider()
st.markdown("<p style='text-align: center; color: gray;'>Developed by <b>Hilâl Gökçe Sarıçam</b> | Computer Engineering Student</p>", unsafe_allow_html=True)
# This creates the page for displaying data visualizations.

import streamlit as st
import json
import pandas as pd
import plotly.express as px
import csv
import plotly.graph_objects as go

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Information on Several Stocks 📈")
st.title("Information on Some Cities 🏙️")
st.divider()


# PART 1: GRAPHS FROM data.json
# --- YOUR CODE GOES HERE ---
def jasondynamic():
    all=[]
    with open("data.json") as data:
        location=json.load(data)
        df = pd.DataFrame(location[0])
        choices=df["Stock"]
        for i in choices:
            all.append(i)
    values = st.multiselect("Choose one or more companies", all)
    if "values" not in st.session_state:
        st.session_state["values"] = []
    if st.button("Save"):
        st.session_state["values"] = values
    any=df[choices.isin(st.session_state["values"])]
    if not any.empty:
        fig = px.pie(any, values="Market Cap", names='Stock')
        st.subheader("Market Caps")
        st.plotly_chart(fig)

        # st.map(any, latitude="Latitude", longitude="Longitude") 


def jasonstatic():
    custom = {
    "Apple": "#ACA3C2",
    "Starbucks": "#2B7828", 
    "AT&T": "#3192A8",
    "Bank of America": "#3F3DCC", 
    "Target": "#E64E2D", 
    "Google": "#D5CF54", 
    "American Express": "#BEB3BC6A", 
}
    with open("data.json") as data:
        stocks=json.load(data)
        stock=stocks[0]
    df = pd.DataFrame(dict(Stock=stock["Stock"], IPO=stock["start"], Today="2026-10-15", Key=stock["color"]))
    fig = px.timeline(df,x_start="IPO", x_end="Today",y="Stock", color="Key", color_discrete_map=custom, title="Timeline of Stocks (from IPO to Today)")
    fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up
    st.plotly_chart(fig)


def csvstatic():
    with open("data.csv","r") as data:
        money=[]
        male=[]
        female=[]
        name=[]
        yes=csv.DictReader(data)
        for row in yes:
            money.append(int(row["Money"])/10000)
            male.append(int(row["Males"]))
            female.append(int(row["Females"]))
            name.append(row["Name"])
        fig = go.Figure(data=[go.Scatter(
    x=(male), y=(female),
    mode='markers',
    marker_size=(money))])
    fig.update_layout(title=dict(text="How Much Money Each City Has With Respect to Male and Female Populations"),xaxis=dict(title=dict(text="Male Population")),yaxis=dict(title=dict(text="Female Population")))
    st.plotly_chart(fig)

def csvdynamic():
    with open("data.csv","r") as data:
        everything={}
        yes=csv.DictReader(data)
        for row in yes:
            if row["Name"] not in everything:
                everything[row["Name"]]=row["Money"]
            else:
                x=row["Name"]+"."
                everything[x]=row["Money"]
    df=pd.DataFrame({"Name":everything.keys(),"Money":everything.values()})
    val = st.multiselect("Choose a city", everything.keys())
    if "val" not in st.session_state:
        st.session_state["val"] = []
    if st.button("Go"):
        st.session_state["val"] = val
    any = df[df["Name"].isin(st.session_state["val"])]
    any["Money"] = any["Money"].astype(float)
    any = any.sort_values(by="Money", ascending=True)
    if not any.empty:
        st.subheader("How Much Money Each City Has")
        st.bar_chart(data=any, x="Name", y=["Money"],
                     x_label="Name", y_label="Money")
        total=any["Money"].astype(float).sum()
        average=any["Money"].astype(float).mean()
        highest=any["Money"].astype(float).max()
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Money", f"${total:,.2f}")
        c2.metric("Average Money", f"${average:,.2f}")
        c3.metric("Highest Amount", f"${highest:,.2f}")



def main():
    tab1, tab2 = st.tabs(
    ["Stocks", "City"], default="Stocks")
    with tab1:
        st.header("Timeline")
        st.caption("Below is a timeline of when each company became public.")
        jasonstatic()
        st.divider()
        st.header("Comparison")
        st.caption("Choose from the options below to compare the market caps of each company (As of October 15,2026).")
        jasondynamic()
    with tab2:
        st.header("Male vs Female vs Money")
        csvstatic()
        st.divider()
        st.header("Comparison of All Cities Made")
        csvdynamic()

main()

# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---

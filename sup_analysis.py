import streamlit as st
import hydralit_components as hc
import networkx as nx
import networkx.algorithms.approximation as nx_app
import math
import numpy as np
import pandas as pd
import warnings
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
import plotly.express as px
warnings.filterwarnings(action = "ignore")

data = pd.read_csv("Superstore_sales_Data.csv")
def sale_tot(Customer_name):
            df = data[data["Customer Name"] == Customer_name]
            value = sum(df["Sales"])
            return value
def amount_list(Customer_name):
    df = data[data["Customer Name"] == Customer_name]
    df = df[['Category','Sales']]
    df = df.rename(columns = {'Sales':'Amount'})
    value = df.groupby(['Category'])['Amount'].sum().reset_index()
    return value

def state_list(Customer_name):
    df = data[data["Customer Name"] == Customer_name]
    df = df[['State','Sales']]
    value = df.groupby(['State'])['Sales'].sum()
    return value

def cat_list(Customer_name):
    df = data[data["Customer Name"] == Customer_name]
    df = df.rename(columns = {'Sub-Category':'Total Count'})
    value = df["Total Count"].value_counts()
    return value

def subcat_list(Customer_name):
    df = data[data["Customer Name"] == Customer_name]
    df = df[['Sub-Category','Sales']]
    # df = df.rename(columns = {'Sub-Category':'Total Count'})
    value = df.groupby(["Sub-Category"])['Sales'].sum()
    return value

def ship_list(Customer_name):
    df = data[data["Customer Name"] == Customer_name]
    df = df[['Ship Mode']]
    df = df.rename(columns = {'Ship Mode':'Order Mode Times'})
    value = df['Order Mode Times'].value_counts()
    return value

def type_list(Customer_name):
    df = data[data["Customer Name"] == Customer_name]
    # df = df.rename(columns = {'Ship Mode':'Order Mode Times'})
    value = df['Segment'].unique()
    return value[0]

def date_sale(Customer_name):
    df = data[data["Customer Name"] == Customer_name]
    df = df[['Order Date','Sales']]
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
    df['year'] = df['Order Date'].dt.year
    del df['Order Date']
    value = df.groupby(["year"])['Sales'].sum()
    return value

def date_sale_month(Customer_name):
    df = data[data["Customer Name"] == Customer_name]
    df = df[['Order Date','Sales']]
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
    d = df['Order Date']
    df.groupby([d.dt.year.rename('Year'), d.dt.month.rename('Month')]).sum()
    ym_id = d.apply("{:%Y-%m}".format).rename('Order Date')
    value = df.groupby(ym_id).sum()
    return value

theme_neutral = {'bgcolor': '#f9f9f9','title_color': 'blue','content_color': 'blue'}

def ana():
    sel = st.sidebar.radio("Select a Analysis Type",('By Name', 'By Products','Locations'))

    if sel=='By Name':
        col = st.columns(3)
        with col[1]:
            sel_name = st.selectbox("Select Customer Name", data["Customer Name"].unique())

        st.sidebar.write('Segement of',sel_name, 'is', type_list(sel_name))
        st.sidebar.subheader('Customer Lifetime Value Metric')
        st.sidebar.info(int(sale_tot(sel_name)*len(date_sale(sel_name))))

        col = st.columns(2)
        with col[0]:
            st.write("**Category wise Total Purchase Amount in $**")
            val = amount_list(sel_name)
            st.write(val)
        with col[1]:
            # st.metric(label='Total Sale Amount',value=round(sale_tot(sel_name)))
            hc.info_card(title='Total Sale Amount in $', content=sale_tot(sel_name),theme_override=theme_neutral)
  
        
        col = st.columns(2)
        with col[0]:
            st.write("**Total Amount of each Item Bought**")
            st.bar_chart(subcat_list(sel_name))

        # fig1, ax1 = plt.subplots()
        # ax1.pie(subcat_list(sel_name).values, labels=subcat_list(sel_name).index, autopct='%1.1f%%',startangle=90)
        # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        # st.pyplot(fig1)

        with col[1]:
            st.write('**Order Shiped to State**')
            st.bar_chart(state_list(sel_name))

        col = st.columns(2)
        with col[0]:
            st.write('**Year Wise Total Amount in $ by Customer**')
            st.bar_chart(date_sale(sel_name))
        with col[1]:
            st.write('**Year-Month Distribution of Total Amount in $ by Customer**')
            st.bar_chart(date_sale_month(sel_name))

        st.write('**Shiping Mode Prefered by**', str(sel_name))
        ship_value = ship_list(sel_name)
        st.bar_chart(ship_value)

    elif sel=='By Products':
        st.sidebar.subheader('Analysis By Products')
        prod_name = st.selectbox("Select a Category Name",data["Category"].unique())
        
        def sale_prod(product):
            df = data[data["Category"] == product]
            value = sum(df["Sales"])
            return value

        st.sidebar.write('Total Sale Amount On', str(prod_name))
        st.sidebar.info(sale_prod(prod_name))

        def prod_list(product):
            df = data[data["Category"] == product]
            df = df[['Product Name','Sales']]
            df = df.rename(columns = {'Sales':'Amount'})
            value = df.groupby(['Product Name'])['Amount'].sum().reset_index()
            return value

        st.write('Products Name List with Amount')
        st.write(prod_list(prod_name))

    elif sel=='Locations':
        sel_name = st.selectbox("Select Customer Name", data["Customer Name"].unique())

        def loc_name(Customer_name):
            df = data[data["Customer Name"] == Customer_name]
            value = list(df["City"].unique())
            return value

        sel = loc_name(sel_name)
        # st.write(sel)

        coordinates = []
        def findGeocode(city):
            # try and catch is used to overcome
            # the exception thrown by geolocator
            # using geocodertimedout
            try:	
                # Specify the user_agent as your
                # app name it should not be none
                geolocator = Nominatim(user_agent="your_app_name")	
                return geolocator.geocode(city)
            except GeocoderTimedOut:	
                return findGeocode(city)

        for i in sel:
            if findGeocode(i) != None:
                loc = findGeocode(i)
                coordinates.append((loc.longitude,loc.latitude))
            else:
                coordinates.append((np.nan,np.nan))

        # st.write('Coordinates of Selected City:',coordinates)

        G = nx.Graph()
        #Create a graph object with number of nodes same as number of cities
        nodes = np.arange(0, len(sel))
        G.add_nodes_from(nodes)
        #Create a dictionary of node and coordinate of each state for positions
        positions = {node:coordinate for node, coordinate in zip(nodes, coordinates)}
        #Create a dictionary of node and capital for labels
        labels = {node:capital for node, capital in zip(nodes, sel)}

        for i in nodes:
            for j in nodes:
                if i!=j:
                    G.add_edge(i, j)

        pos = {node:list(coordinate) for node, coordinate in zip(nodes, coordinates)}
        # st.write(pos)

        H = G.copy()
        # Calculating the distances between the nodes as edge's weight.
        for i in range(len(pos)):
            for j in range(i + 1, len(pos)):
                
                #Multidimensional Euclidean distance from the origin to a point.
                #euclidean distance between (x1, y1) and (x2, y2) is ((x2-x1)**2 + (y2-y1)**2)**0.5
                dist = math.hypot(pos[i][0] - pos[j][0], pos[i][1] - pos[j][1])
                dist = dist
                G.add_edge(i, j, weight=dist)
        cycle = nx_app.christofides(G, weight="weight")

        edge_list = list(nx.utils.pairwise(cycle))


        #Create a dictionary of node and capital for labels
        labels = {node:capital for node, capital in zip(nodes, sel)}
        tsp_cycle = [labels[value] for value in cycle]

        df_map = {'City':tsp_cycle}
        df_map = pd.DataFrame(df_map) 

        longitude = []
        latitude = []
        for i in (df_map["City"]):
            if findGeocode(i) != None:
                loc = findGeocode(i)
                latitude.append(loc.latitude)
                longitude.append(loc.longitude)
            else:
                latitude.append(np.nan)
                longitude.append(np.nan)
        df_map["latitude"] = latitude
        df_map["longitude"] = longitude
        # st.write(df_map)
        # st.map(df_map)
        # px.set_mapbox_access_token(open(".mapbox_token").read())
        fig = px.scatter_mapbox(df_map,
                                lat=df_map.latitude,
                                lon=df_map.longitude,
                                hover_name="City",
                                zoom=1)
        fig.update_layout(mapbox_style="stamen-terrain", mapbox_zoom=1, margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)

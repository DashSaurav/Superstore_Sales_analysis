import streamlit as st
import pandas as pd
import hydralit_components as hc


data = pd.read_csv("Superstore_sales_Data.csv")
def ana():
    sel = st.sidebar.radio("Select a Analysis Type",('By Name', 'By Products'))

    if sel=='By Name':
        col = st.columns(3)
        with col[1]:
            sel_name = st.selectbox("Select Customer Name", data["Customer Name"].unique())
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
            df = df.rename(columns = {'Ship Mode':'Order Mode Times'})
            value = df['Order Mode Times'].unique()
            return value

        def type_list(Customer_name):
            df = data[data["Customer Name"] == Customer_name]
            # df = df.rename(columns = {'Ship Mode':'Order Mode Times'})
            value = df['Segment'].unique()
            return value

        # st.write(sale_tot(sel_name))
        theme_neutral = {'bgcolor': '#f9f9f9','title_color': 'blue','content_color': 'blue'}
        # c1,c2,c3 = st.columns((0.5,1,0.5))
        # with c2:
        #     hc.info_card(title='Total Sale Amount in Rupees', content=sale_tot(sel_name),theme_override=theme_neutral)
        
        col = st.columns(2)
        with col[0]:
            st.write("**Category wise Purchase**")
            val = amount_list(sel_name)
            st.write(val)
        with col[1]:
            # st.metric(label='Total Sale Amount',value=round(sale_tot(sel_name)))
            hc.info_card(title='Total Sale Amount in $', content=sale_tot(sel_name),theme_override=theme_neutral)
  
        
        st.sidebar.write('**List of Item Purchased by**', str(sel_name))
        val_list = cat_list(sel_name)
        st.sidebar.write(val_list)
        # st.bar_chart(val_list)
        st.write("**Sub-Category Wise Amount of Sales**")
        st.bar_chart(subcat_list(sel_name))

        st.write('**Order Taken in which State for How Much**')
        st.bar_chart(state_list(sel_name))

        st.write('Shiping Mode Prefered by Customer')
        ship_value = ship_list(sel_name)
        st.write(ship_value)
        st.write('Type of Customer')
        ty_list = type_list(sel_name)
        st.write(ty_list)

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
        

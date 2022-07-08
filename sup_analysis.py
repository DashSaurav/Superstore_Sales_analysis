import streamlit as st
import pandas as pd
import hydralit_components as hc

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
    df = df.rename(columns = {'Ship Mode':'Order Mode Times'})
    value = df['Order Mode Times'].unique()
    return value

def type_list(Customer_name):
    df = data[data["Customer Name"] == Customer_name]
    # df = df.rename(columns = {'Ship Mode':'Order Mode Times'})
    value = df['Segment'].unique()
    return value[0]

def ana():
    sel = st.sidebar.radio("Select a Analysis Type",('By Name', 'By Products'))

    if sel=='By Name':
        col = st.columns(3)
        with col[1]:
            sel_name = st.selectbox("Select Customer Name", data["Customer Name"].unique())
        with col[2]:
            t = "<div> <br></div>"
            st.markdown(t, unsafe_allow_html=True)
            st.info(type_list(sel_name))

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
        st.sidebar.dataframe(val_list)
        # st.bar_chart(val_list)
        col = st.columns(2)
        with col[0]:
            st.write("**Items Total Sale Amount**")
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
            st.write('**Shiping Mode Prefered by**', str(sel_name))
            ship_value = ship_list(sel_name)
            st.write(ship_value)


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

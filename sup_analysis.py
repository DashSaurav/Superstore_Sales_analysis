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
    sel = st.sidebar.radio("Select a Analysis Type",('By Name', 'By Products'))

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

import streamlit as st
import pandas as pd
import hydralit_components as hc


data = pd.read_csv("Superstore_sales_Data.csv")
def ana():
    sel_name = st.selectbox("Select Customer Name", data["Customer Name"].unique())
    def sale_tot(Customer_name):
        df = data[data["Customer Name"] == Customer_name]
        value = sum(df["Sales"])
        return round(value)

    def amount_list(Customer_name):
        df = data[data["Customer Name"] == Customer_name]
        df = df[['Category','Sub-Category','Sales']]
        df = df.rename(columns = {'Sales':'Amount'})
        value = df.groupby(['Category','Sub-Category'])['Amount'].sum().reset_index()
        return value

    def cat_list(Customer_name):
        df = data[data["Customer Name"] == Customer_name]
        df = df.rename(columns = {'Sub-Category':'Total Count'})
        value = df["Total Count"].value_counts()
        return value

    # st.write(sale_tot(sel_name))
    theme_neutral = {'bgcolor': '#f9f9f9','title_color': 'orange','content_color': 'orange'}
    hc.info_card(title='Sales Amount (In Rupees)', content=sale_tot(sel_name),theme_override=theme_neutral)
    col = st.columns(2)
    with col[0]:
        st.write("**Category wise Purchase by**", str(sel_name))
        val = amount_list(sel_name)
        st.write(val)
    with col[1]:
        st.write('**List of Item Purchased with Total Count**')
        val_list = cat_list(sel_name)
        st.write(val_list)


    

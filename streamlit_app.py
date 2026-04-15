import streamlit as st
from snowflake.snowpark.functions import col

st.title("🥤 Customize your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be", name_on_order)

# Connect to Snowflake
conn = st.connection("snowflake")
session = conn.session()

# Get fruit options
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col("FRUIT_NAME")).to_pandas()
fruit_list = my_dataframe["FRUIT_NAME"].tolist()

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

if ingredients_list:
    ingredients_string = " ".join(ingredients_list)

    st.write("Your ingredients:", ingredients_string)

    if st.button("Submit Order"):
        insert_sql = f"""
            INSERT INTO SMOOTHIES.PUBLIC.ORDERS(INGREDIENTS, NAME_ON_ORDER)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """
        session.sql(insert_sql).collect()
        st.success(f"Your Smoothie is ordered! {name_on_order}", icon="✅")

import requests  
smoothiefroot_response = requests.get(""https://my.smoothiefroot.com/api/fruit/watermelon"")  
st.text(smoothiefroot_response)

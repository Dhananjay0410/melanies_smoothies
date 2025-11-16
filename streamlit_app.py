# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Name field
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Get Snowflake session
cnx = st.connection("snowflake")
session = cnx.session()

# Fruit options table
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Ingredient selection
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe
)

# Enforce max selection limit
if len(ingredients_list) > 5:
    st.warning("You can only select up to 5 ingredients.")
    ingredients_list = ingredients_list[:5]


if ingredients_list:
    # Turn list into comma-separated string
    ingredients_string = ", ".join(ingredients_list)

    # Show user what they selected (optional)
    # st.write(ingredients_string)

    # FIXED INSERT STATEMENT: now inserts BOTH columns
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}');
    """

    # st.write(my_insert_stmt)  # helpful for debugging

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()

    # Extra credit: show the smoothie name in the success message!
    st.success(f"✅ Your Smoothie is ordered, {name_on_order}!")

# new section to display smoothie fruit nutrition information
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True


 


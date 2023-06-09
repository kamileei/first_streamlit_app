import streamlit
import requests as r
import snowflake.connector
import pandas as pd
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#pick list for a smoothie
fruits_selected = streamlit.multiselect('Pick some fruits:', list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

#fruityvice API
streamlit.header('Fruityvice Fruit Advice!')

def get_fruityvice_data(this_fruit):
  fruityvice_response = r.get("https://fruityvice.com/api/fruit/"+fruit_choice)
  #normalize the json version of the response
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    function_outp = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(function_outp)

#streamlit.write('The user entered', fruit_choice)

except URLError as e:
  streamlit.error()

#FRUIT LOAD LIST
streamlit.header("View Our Fruit List - Add Your Favorites!")
#snowflake-related functions

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

  
#add a button to load the fruit
if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)
  
  
new_fruit = streamlit.text_input('What fruit would you like to add?')

def insert_row_snow(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('" + new_fruit +"')")
    return "Thanks for adding " + new_fruit
  
if streamlit.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  fruit_added = insert_row_snow(new_fruit)
  streamlit.text(fruit_added)
  my_cnx.close()
  
    

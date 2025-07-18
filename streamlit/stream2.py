import streamlit as st
from streamlit_option_menu import option_menu
import base64

st.set_page_config("Weather APP☁️")
# with st.sidebar:
#     state=st.selectbox("Selectbox",options=['Punjab','Haryana','MP','UP'])
#     if st.button("Submit"):
#         st.write(state)
#     opt=st.radio('Menu',options=['Home','About','Contact Us'])

# opt=option_menu('',options=['Home','About','Contact Us'],orientation='horizontal',icons=['home-fill','square-fill','mobile-fill'])

# if opt=='Home':
#         st.header("Home Page")
# elif opt=='About':
#         st.header("About Page")
# elif opt=='Contact Us':
#         st.header("Contact Us")

with open('img-1.jpg') as f:
    data= f.read()

img= base64.b64encode(data).decode()

css=f"""
    <style>
    [data-testid="stMain"]{{
        background-image:url('data:image/png;base64,{img}');
        background-size:cover
    }}
    </style>
"""
st.markdown(css, unsafe_allow_html=True)


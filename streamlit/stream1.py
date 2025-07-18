import streamlit as st

st.set_page_config('First Lecture', page_icon="🏠")
st.header('Registration :red[form] :writing_hand:')

with st.form(key='key'):
    col1, col2, col3= st.columns((1,1,1))
    with col1:
        first_naam= st.text_input('First Name')
        age= st.number_input("Age")
    with col2:
        mid_naam= st.text_input('Middle Name')
        gender= st.radio('Gender', options=['Male','Female'],horizontal=True)
    with col3:
        last_naam= st.text_input('Last Name')
        dob= st.date_input("Enter DOB")
        
    check=st.checkbox('Terms and conditions')
        
        
    if st.form_submit_button():
        st.success("Registered successfully")
        st.balloons()
        

st.write("this is **boldtext**")
st.write("this is _itallic_")
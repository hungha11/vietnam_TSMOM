import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
    layout='wide',
)

st.title("Welcome to Modest Invest strategies gallery!")

st.sidebar.success("Select a strategy.")

st.markdown(
    """
    ## Who we are!
    Modest Invest is a small research team based in Ho Chi Minh City, Viet Nam. 
    We conduct research in quantitative finance with a strong focus on data-driven models and applying machine learning 
    in building quantitative trading strategies for the Vietnamese capital market. 
    
    
    ## Strategies gallery
    Strategies gallery is an open-source sharing platform where researchers and practitioners can come and collect new ideas
    about quantitative finance and algorithmic trading. All of the tools and models are written using python and included in our
    miquants library.   
    
    
    ## Contribution and contact
    We are welcomed with contribution.
    - gmail: modest.invest.2022@gmail.com
    """
)
import streamlit as st
import pickle
import numpy as np

def load_model():
    with open('save_step.pkl', 'rb') as file:
        data = pickle.load(file) 
    return data

data = load_model()

model = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict_page():
    st.title("Software Deverloper Salary Prediction")

    st.write("""### We need some information to predict the salary""")

    countries = (
        'UK and Northern Ireland', 
        'Netherlands',
        'United States of America', 
        'Austria', 
        'Italy',
        'Canada', 
        'Germany', 
        'Poland', 
        'France', 
        'Brazil', 
        'Sweden',
        'Spain', 
        'Turkey', 
        'India', 
        'Russian Federation', 
        'Switzerland',
        'Australia',
        'Other'
    )
    education = (
        'Master’s degree', 
        'Bachelor’s degree', 
        'Less than a Bechelors',
        'Post grad'
    )

    country = st.selectbox("Country", countries)
    edlevel = st.selectbox("Education level", education)

    expericence = st.slider("Years of Expericence", 0, 50, 3)

    ok = st.button ("Caculate salary")
    if ok:
        X = np.array([[country, edlevel, expericence]])
        X[:, 0] = le_country.transform(X[:, 0])
        X[:, 1] = le_education.transform(X[:, 1])
        X = X.astype(float)

        salary = model.predict(X)
        st.subheader(f"The estimated salary is ${salary[0] :.2f}")

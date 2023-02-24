import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] ='Other'
    return categorical_map

def clean_experience(x):
    if x == 'More than 50 years':
        x = 50
    if x == 'Less than 1 year':
        x =0.5
    return float(x)

def clean_country(x):
    if 'United Kingdom of Great Britain and Northern Ireland' in x:
        return 'UK and Northern Ireland'
    return x

def clean_edlevel(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral degree' in x:
        return 'Post grad'
    return 'Less than a Bechelors'

@st.cache_data
def load_data():
    df = pd.read_csv(".\survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    df = df.rename({"ConvertedCompYearly" :"Salary"}, axis =1)
    df = df[df["Salary"].notnull()]
    df = df.dropna()
    df
    df = df.drop("Employment", axis =1)
    
    country_map = shorten_categories(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)
    df["Country"] = df["Country"].apply(clean_country)

    df = df[df["Salary"] <= 250000]
    df = df[df["Salary"] >= 10000]
    df = df[df['Country'] != 'Other']

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_edlevel)

    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write(
        """
        ### Stack Overflow Developer Servey 2020          
        """
    )
    
    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots(figsize=(20,16))
    ax1.pie(data, autopct ="%1.1f%%", startangle=90)
    ax1.axis("equal")
    ax1.legend(labels =data.index)

    st.write(
        """
        ### Number of Data from different countries       
        """
    )
    st.pyplot(fig1)
     

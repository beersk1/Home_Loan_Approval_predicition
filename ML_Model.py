import pandas as pd 
import numpy as np 
import streamlit as st
import boto3
import tempfile
import joblib
import requests
from streamlit_lottie import st_lottie_spinner

st.set_page_config(layout="wide")

st.title('Home Loan Approval')


st.write("""## Gender""")
gender = st.radio("Select your Gender:",["Male","Female"],horizontal=False)

st.write("""## Marriage Status""")
marriage = st.radio("Select your Marital Status:",["No","Yes"],horizontal=False)

st.write("""## Dependants""")
dep = st.radio("Select the number of dependants:",["0","1","2","3+"],horizontal=True)

st.write("""## Education""")
edu = st.radio("Select your educational status:",["Not Graduate","Graduate"],horizontal=False)

st.write("""## Self Employed""")
self = st.radio("Are you self employed:",["No","Yes"],horizontal=False)


st.write("""## Loan Terms""")
lt = st.slider("Select your Loan Term in months",value=48,min_value=36,max_value = 480,step = 6 )

st.write("""## Loan Amount (In Thousands)""")
la= st.slider("Select your desired Loan Amount",value=350,min_value=9,max_value = 700,step = 25 )


st.write("""## Applicant Income""")
ai = st.slider("Select your Income",value=1500,min_value=150,max_value = 81000,step = 50 )

st.write("""## Co-Applicant Income""")
ci = st.slider("Select your co-applicant income",value=400,min_value=0,max_value = 41000,step = 100 )

st.write("""## Credit History""")
hist = st.radio("Do you have a Credit History:",["No","Yes"],horizontal=False)

st.write("""## Property Area""")
area = st.radio("Select the area where your property is located:",["Rural","Semiurban","Urban"],horizontal=True)

predict_bt = st.button('Predict',type = "primary")



def make_prediction():
    # connect to s3 bucket with the access and secret access key
    client = boto3.client(
        's3', aws_access_key_id=st.secrets["access_key"],aws_secret_access_key=st.secrets["secret_access_key"],region_name='ap-south-1')

    bucket_name = "homeloanprediction"
    key = "home.pickle"

    # load the model from s3 in a temporary file
    with tempfile.TemporaryFile() as fp:
        # download our model from AWS
        client.download_fileobj(Fileobj=fp, Bucket=bucket_name, Key=key)
        # change the position of the File Handle to the beginning of the file
        fp.seek(0)
        # load the model using joblib library
        model = joblib.load(fp)

    # prediction from the model, returns 0 or 1
    return model.predict(df) 


@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_loading_an = load_lottieurl(
    'https://lottie.host/9fac21e0-e370-4d3a-87d2-3aa40cf2f9a1/gLgSyWrkas.json')


columns1 = ["Gender","Married","Dependents","Education","Self_Employed","ApplicantIncome","CoapplicantIncome","LoanAmount","Loan_Amount_Term","Credit_History","Property_Area"]


if predict_bt:
    inputs = [gender,marriage,dep,edu,self,ai,ci,lt,la,hist,area]
    # inputs = convert_bool_to_int(inputs)

    df = pd.DataFrame([inputs],columns= columns1)
    df["Credit_History"]= df["Credit_History"].map({"No":0,"Yes":1})
    df["Gender"]= df["Gender"].map({"Male":0,"Female":1})
    df["Dependents"]= df["Dependents"].map({"0":0,"1":1,"2":2,"3+":3})
    df["Married"]= df["Married"].map({"No":0,"Yes":1})
    df["Education"]= df["Education"].map({"Not Graduate":0,"Graduate":1})
    df["Self_Employed"]= df["Self_Employed"].map({"No":0,"Yes":1})
    df["Property_Area"]= df["Property_Area"].map({"Rural":1,"Semiurban":2,"Urban":3})
    print(df)
    
    # will run the animation as long as the function is running, if final_pred exit, then stop displaying the loading animation
    with st_lottie_spinner(lottie_loading_an, quality='high', height='200px', width='200px'):
        final_pred = make_prediction()
        print(final_pred)
    
        if final_pred == 1:
             st.success("Congrats: You have been accepted")
        elif final_pred == 0:
             st.error("You have been rejected ")
        
    

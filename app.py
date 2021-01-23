# 1. Library imports
from starlette.requests import Request
import uvicorn ##ASGI server
from fastapi import FastAPI,Form
from fastapi.templating import Jinja2Templates    #to use the templates
import datetime
# import pandas as pd, numpy as np, 
import pickle

# 2. Create the app object
app = FastAPI()
#De-serializing
with open('random_forrest_regression_model.pkl','rb') as f:
    regressor_model=pickle.load(f)

templates=Jinja2Templates(directory='templates' )   #mentioning where the templates are

@app.get('/')
def home_page(request:Request):
    return templates.TemplateResponse('home.html',{
        'request':request,      #the rendering response requires 'request' object 
   })
# year=1&present_price=2&kms=3&fuel_type=cng&owner=dealer&transmission=manual

@app.post('/predict')
def predict_output(request:Request,year: int = Form(...), present_price: float = Form(...), kms: float = Form(...),fuel_type: str = Form(...), seller: str = Form(...),transmission:str = Form(...), owner: str = Form(...)):       

    Kms_Driven=kms
    Owner=[0 if(owner=='first_owner') else 1 ]
    Seller_Type_Individual=[1 if(seller=='individual') else 0 ]
    Age=datetime.datetime.now().year-year
    fuel=[1 if(i==fuel_type) else 0 for i in ['diesel','petrol']]
    Transmission_Manual=[1 if(transmission=='manual') else 0 ]
    # Present_Price	Kms_Driven,Owner,Age,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual

    lst=[present_price,Kms_Driven]+Owner+[Age]+fuel+Seller_Type_Individual+Transmission_Manual
    # print(lst)
    predicted_val=regressor_model.predict([lst])[0]  #2d list
    # print(predicted_val)  #it's a list of length 1

    return templates.TemplateResponse('prediction_page.html',{
        'request':request,      #the rendering response requires 'request' object 
        'prediction':predicted_val,    #injecting the content we need to the html page
    })



# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
# if __name__ == '__main__':
#     uvicorn.run(app, host='127.0.0.1', port=8000)


#To run the execute the file--> uvicorn app:app --reload           i.e uvicorn <python_file_name:fastapi_object_name> --reload
#to open swagger UI (allows us to test the API with a UI)--> http://127.0.0.1:8000/docs
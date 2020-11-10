import requests 
import bs4 
import joblib
import json
def scrapping():
   r = requests.get('https://finance.yahoo.com/quote/%5EDJI/history?p=%5EDJI') #DOW JONES 
   soup = bs4.BeautifulSoup(r.text, "lxml") #convert to beautifulsoup element 

   date_dow = soup.find('span', {'data-reactid':'53'}).text #latest date
   close_dow = soup.find('span', {'data-reactid':'63'}).text.replace(',','') #latest adjust close 

   r2 = requests.get('https://finance.yahoo.com/quote/%5EGSPC/history?p=%5EGSPC') #SP500 
   soup2 = bs4.BeautifulSoup(r2.text, "lxml") #convert to beautifulsoup element 

   date_500 = soup2.find('span', {'data-reactid':'53'}).text #latest date
   close_500 = soup2.find('span', {'data-reactid':'63'}).text.replace(',','') #latest adjust close

   r3 = requests.get('https://finance.yahoo.com/quote/%5EIXIC/history?p=%5EIXIC') #NASDAQ 
   soup3 = bs4.BeautifulSoup(r3.text, "lxml") #convert to beautifulsoup element 

   date_nasdaq = soup3.find('span', {'data-reactid':'53'}).text #latest date
   close_nasdaq = soup3.find('span', {'data-reactid':'63'}).text.replace(',','') #latest adjust close 


   r4 = requests.get('https://finance.yahoo.com/quote/DX-Y.NYB/history?p=DX-Y.NYB') #US DOLLAR  
   soup4 = bs4.BeautifulSoup(r4.text, "lxml") #convert to beautifulsoup element 

   date_usdi = soup4.find('span', {'data-reactid':'53'}).text #latest date
   close_usdi = soup4.find('span', {'data-reactid':'63'}).text.replace(',','') #latest adjust close
   
   r5 = requests.get('https://finance.yahoo.com/quote/GC%3DF/history?p=GC%3DF') #GOLD
   soup5 = bs4.BeautifulSoup(r5.text, "lxml") #convert to beautifulsoup element 

   date_gold = soup5.find('span', {'data-reactid':'53'}).text #latest date
   close_gold = soup5.find('span', {'data-reactid':'63'}).text.replace(',','') #latest adjust close 
   
   r6 = requests.get('https://fred.stlouisfed.org/series/UNRATE') #Unemployment
   soup6 = bs4.BeautifulSoup(r6.text, "lxml") #convert to beautifulsoup element

   unemployment = soup6.find('span', {'class':'series-meta-observation-value'}).text #latest adjust close

   linear_array = [ close_usdi,close_gold,close_500,close_nasdaq ]
   logistic_array=[unemployment,close_nasdaq,close_500,close_gold]

   # array_data={'Unemployment':unemployment,'Close_USDI':close_usdi,'Close_dow':close_dow,'Close_nasdaq':close_nasdaq,'Close_500':close_500,'Close_gold':close_gold}
   # change data type to float
   for x in range(0,len(linear_array)):
        linear_array[x]=float(linear_array[x])
   for y in range(0,len(logistic_array)):
        logistic_array[y]=float(logistic_array[y])
   # Load in Linear_model 
   linear_model=joblib.load(open('Linear_model2.sav', 'rb'))
   x_scaler=joblib.load(open('x_linear_scaler.sav','rb'))
   y_scaler=joblib.load(open('y_linear_scaler.sav','rb'))
   scaled_data=x_scaler.transform([linear_array])
   prediction=linear_model.predict(scaled_data)
   unscaled_pred=y_scaler.inverse_transform(prediction)
   # Load in Logistic_model
   logistic_model=joblib.load(open('Logistic_model2.sav','rb'))
   prediction=logistic_model.predict([logistic_array])
   # Make a dictionary of prediction, data array and other stuff. Or jsonify it
   data_dict=dict(date=date_usdi,Linear_predicted_price=unscaled_pred[0][0],Logistic_predicted_movement=prediction[0])
   return data_dict




if __name__ == "__main__": 
   print(scrapping())
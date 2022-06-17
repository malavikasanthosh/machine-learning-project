from datetime import datetime
from io import StringIO
from urllib import request
from flask import*
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

model = pickle.load(open("model_accuracy89.pkl", "rb"))


@app.route('/')  
def home():  
   airports_df = pd.read_csv('airports.csv')
   airports=airports_df[['IATA_CODE','AIRPORT']].to_dict("records")
   
   return render_template('home.html',airports=airports) 

@app.route('/predict',methods = ['POST'])







def predict():
      date= request.form["Date"]
      Day_of_Journey = datetime.strptime(date, "%Y-%m-%d").day
      Month_of_Journey = datetime.strptime(date, "%Y-%m-%d").month

      Airline = request.form["Airline"].strip()
      Origin_Airport = request.form["Origin"].strip()
      Destination_Airport = request.form["Destination"].strip()

      csv_str =f"""AIRLINE;ORIGIN_AIRPORT;DESTINATION_AIRPORT
{Airline};{Origin_Airport};{Destination_Airport}
"""

      df = pd.read_csv(StringIO(csv_str), sep =";")
      
      
      airlines_le=pickle.load(open('airlines_encoder.pkl','rb'))
      airports_le=pickle.load(open('airports_encoder.pkl','rb'))


      Airline=airlines_le.transform(df['AIRLINE'])
      Origin_Airport=airports_le.transform(df['ORIGIN_AIRPORT'])
      Destination_Airport=airports_le.transform(df['DESTINATION_AIRPORT'])


      Scheduled_Arrival=int(request.form["Scheduled_Arrival"])
      
      Air_System_Delay=int(request.form["Air_System_Delay"])
      Weather_Delay=int(request.form["Weather_Delay"])
      Security_Delay=int(request.form["Security_Delay"])
      Late_Aircraft_Delay=int(request.form["Late_Aircraft_Delay"])
      Airline_Delay=int(request.form["Airline_Delay"])
      Departure_Delay=int(request.form["Departure_Delay"])
      
      

      prediction=model.predict([[
         Month_of_Journey,
         Day_of_Journey,
         Airline, 
         Scheduled_Arrival,
         Origin_Airport,
         Destination_Airport,
         Air_System_Delay,
         Weather_Delay,
         Security_Delay,
         Late_Aircraft_Delay,
         Airline_Delay,   
         Departure_Delay 
      ]])
      output=round(prediction[0],2)
      print(output)
      
      return render_template('prediction.html',arrival_delay=output) 


def minutes(input_time):
   
       t=input_time.split(':')
       total_minutes= int(t[0])*60+int(t[1])*1 
       return total_minutes

       
       

if __name__ == '__main__':
   app.run(host='0.0.0.0')


#('Date', '2020-05-09T09:02'), ('Airline', 'B6'), ('Origin', 'ADK'), ('Destination', 'ACT'), ('Arrival_Delay', '02:05'), ('Air_System_Delay', '04:09'), ('Weather_Delay', '13:10'), 
#('Security_Delay', '14:09'), ('Late_Aircraft_Delay', '04:00')
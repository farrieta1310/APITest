import csv
from flask import Flask, request, jsonify
import pandas as pd

#Flask constructor
app = Flask(__name__)

#The route that the application should call the associated function
@app.route('/upload', methods=['POST'])

#Function to Upload File through API
def upload_file():
  try:
    #read csv file
    file = request.files['file']
    #reader = csv.reader(file)
    df = pd.read_csv(file)
    print(df)
    return jsonify({"message":'read file'}),201
  except Exception as e:
    return jsonify({"error":str(e)}),500

if __name__ == '__main__':
  app.run()

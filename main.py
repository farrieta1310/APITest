from flask import Flask, request, jsonify

#Flask constructor
app = Flask[__name__]

#The route that the application should call the associated function
@app.route('/')

#Testing function to check enviroment
def test():
  return 'Test'

if __name__ == '__main__':
  app.run()

from flask import Flask, request, jsonify, render_template
# from flask_ngrok import run_with_ngrok
import numpy as np
import pickle


app = Flask(__name__)
# run_with_ngrok(app)

     
model_RF=pickle.load(open('Major_RF.pkl', 'rb')) 
model_KNN=pickle.load(open('Major_KNN.pkl', 'rb')) 
model_K_SVM=pickle.load(open('Major_SVM_linear.pkl', 'rb')) 
model_DT=pickle.load(open('Major_DT.pkl', 'rb')) 
model_NB=pickle.load(open('Major_NB.pkl', 'rb')) 

@app.route('/')
def home():
  return render_template("index.html")
#------------------------------About us-------------------------------------------
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')
#------------------------------PROJECTS-------------------------------------------
@app.route('/projects')
def projects():
    return render_template('projects.html')
#------------------------------GALLERY-------------------------------------------
@app.route('/gallery')
def gallery():
    return render_template('gallery.html')
#------------------------------MAJOR-------------------------------------------
@app.route('/major')
def major():
  
  return render_template('major.html') 
#------------------------------MINOR-------------------------------------------
@app.route('/minor')
def minor():
  
  return render_template('minor.html') 
#--------------------------------------------------------------------------------
  
@app.route('/predict',methods=['GET'])

def predict():
    
    pH = float(request.args.get('pH'))
    Temprature = float(request.args.get('Temprature'))
    Taste = float(request.args.get('Taste'))
    Odor = float(request.args.get('Odor'))
    Fat = float(request.args.get('Fat'))
    Turbidity = float(request.args.get('Turbidity'))
    Colour = float(request.args.get('Colour'))

    Model = (request.args.get('Model'))

    if Model=="Random Forest Classifier":
      prediction = model_RF.predict([[pH, Temprature, Taste, Odor, Fat, Turbidity, Colour]])
      accr="99.62%"

    elif Model=="Decision Tree Classifier":
      prediction = model_DT.predict([[pH, Temprature, Taste, Odor, Fat, Turbidity, Colour]])
      accr="98.87%"

    elif Model=="KNN Classifier":
      prediction = model_KNN.predict([[pH, Temprature, Taste, Odor, Fat, Turbidity, Colour]])
      accr="99.25%"

    elif Model=="SVM Classifier":
      prediction = model_K_SVM.predict([[pH, Temprature, Taste, Odor, Fat, Turbidity, Colour]])
      accr="85.28%"

    else:
      prediction = model_NB.predict([[pH, Temprature, Taste, Odor, Fat, Turbidity, Colour]])
      accr="92.08%"

    
    if prediction == [0]:
      return render_template('major.html', prediction_text='The Milk Grade is High', extra_text =" -- Prediction by " + Model , accuracy_text=' -- Accuracy of Model is : {}'.format(accr))
    
    elif prediction == [1]:
      return render_template('major.html', prediction_text='The Milk Grade is Medium', extra_text =" -- Prediction by " + Model , accuracy_text=' -- Accuracy of Model is : {}'.format(accr))

    else :
      return render_template('major.html', prediction_text='The Milk Grade is Low', extra_text =" -- Prediction by " + Model , accuracy_text=' -- Accuracy of Model is : {}'.format(accr))

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)

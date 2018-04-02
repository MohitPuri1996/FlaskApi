from flask import Flask,redirect,url_for,render_template
import requests,json

app=Flask(__name__)

@app.route('/resturants')
def getRestaurants():
	response=requests.get("localhost:5000/page=1")
	response=json.loads(response)
	return render_template('restaurant.html',response=response)


@app.route('/resturants')
def getRestaurants():
	response=requests.get("localhost:5000/page=1")
	response=json.loads(response)
	return render_template('restaurant.html',response=response)



if __name__ == '__main__':
	app.run(debug=True)
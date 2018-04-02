from flask import Flask,redirect,url_for,render_template,jsonify
import requests,json

app=Flask(__name__)

@app.route('/restaurants')
def getRestaurants():
	response=requests.get("http://localhost:5000/page=1")
	response=json.loads(response.text)
	print type(response)
	return render_template('restaurant.html',response=response["restaurants"])


@app.route('/menu/<string:name>')
def getCategory(name):
	response=requests.get("http://localhost:5000/category/"+str(name))
	response=json.loads(response.text)
	print(response["menu"])

	
	#print len(s)
	sets=set()
	for each_object in response["menu"]:
		sets.add(each_object["category"])

	#print sets


	dictionary={}
	for each_item in sets:
		dictionary[each_item]=[]

	#print type(dictionary[s[0]["category"]])
	count=0
	for each_item in response["menu"]:
		count=count+1
		dictionary[each_item["category"]].append(each_item["products"])
	
	print (dictionary)
	return render_template('main.html',response=dictionary)
	#return (dictionary)


if __name__ == '__main__':
	app.run(debug=True,port=5555)
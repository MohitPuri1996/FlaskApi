from flask import Flask,jsonify,redirect,url_for
from flask_restful import Resource,Api,reqparse
import pymongo,json,pprint

app=Flask(__name__)
api=Api(app)

firstEntry=False
endpage_till_now=0
total_length=0
connection=None
records=None
db=None
current_page=0
@app.route('/processing')
def processing():
	print current_page
	
#from here pure api		

#for all
class Restaurants(Resource):
	def get(self,page):
		connection=pymongo.MongoClient('mongodb://localhost')
		db=connection.ZomatoResDetails
		records=db.tempdata
		data=records.find().limit(1000)
		print data
		d=[]
		for item in data:
			d.append({"restaurant_name":item["restaurant_name"],
				"address":item["address"],
				"phone":item["phone"],
				"area":item["area"],
				"city":item["city"],
				"state":item["state"]})
			restaurants={}
			restaurants["count"]=len(d)
			restaurants["data"]=d
		connection.close()
		temp=d[page*20:page*20+20]		
		return jsonify({'restaurants':temp})

#for one
class Restaurant(Resource):
	def get(self,id_):
		connection=pymongo.MongoClient('mongodb://localhost')
		db=connection.ZomatoResDetails
		records=db.tempdata
		data=records.find({"uniqueid":id_})
		d=[]
		for item in data:
			d.append({"restaurant_name":item["restaurant_name"],
				"address":item["address"],
				"phone":item["phone"],
				"area":item["area"],
				"city":item["city"],
				"state":item["state"]
				})
		connection.close()
		return jsonify({'data':d})

class Categories(Resource):		
	def get(self,page):
		connection=pymongo.MongoClient('mongodb://localhost')
		db=connection.ResData
		records=db.catwise
		total_length=records.find({}).count()
		print str(total_length) +"totl"
		data=records.find({}).limit(total_length)
		endpage_till_now=4500
		cat_data=[]
		restaurants_details=[]
		total_length=0
		for item in data:
			restaurants_details.append({"restaurants_details":item["_id"],"Categories":item["data"]})
			total_length=total_length+1
		#pprint.pprint(restaurants_details)
		print str(total_length)+"re"
		for each_object in restaurants_details:
			sets=set()
			#pprint.pprint(each_object["Categories"])
			if len(each_object["Categories"])  > 2:
				for each_sub_category in each_object["Categories"]:
					try:
						#print each_object["Categories"]
						print each_sub_category["category"]
						sets.add(each_sub_category["category"])
					except:
						pass	#print each_sub_category["category"]
			else:
				pass
			#print sets
			dictionary={}
			for each_item in sets:
				dictionary[each_item]=[]

			#print type(dictionary[s[0]["category"]])
			count=0
			
			full=[]
			if len(each_object["Categories"]) > 2:
				try:
					for each_sub_item in each_object["Categories"]:	
						count=count+1
						dictionary[each_sub_item["category"]].append({"product":each_sub_item["products"]})
					
					each_object["Categories"]=dictionary
				except:
					pass
				
			else:
				pass
		connection.close()
		sliced=restaurants_details[page*20:page*20+20]
		print len(sliced)
		return sliced



class Category(Resource):		
	def get(self,name):
		connection=pymongo.MongoClient('mongodb://localhost')
		db=connection.ResData
		records=db.catwise
		details=records.find({"restaurant_name":name})
		return sliced






























		'''
		d=[]
		for item in data:
			d.append({"restaurant_name":item["restaurant_name"],
				"address":item["address"],
				"phone":item["phone"],
				"area":item["area"],
				"city":item["city"],
				"state":item["state"]
				})
		return jsonify({'data':d})
		'''






api.add_resource(Restaurants,'/page=<int:page>')
api.add_resource(Restaurant,'/<id_>')
api.add_resource(Categories,'/categories/page=<int:page>')



if __name__=='__main__':
	app.run(debug=True)












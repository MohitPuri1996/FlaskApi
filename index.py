from flask import Flask,jsonify,redirect,url_for
from flask_restful import Resource,Api,reqparse
import pymongo,json,pprint

app=Flask(__name__)
api=Api(app)
##### ALL RESTAURANTS DATA ########
connection=pymongo.MongoClient('mongodb://localhost')
class Restaurants(Resource):
	def get(self,page):
		global connection
		db=connection.ZomatoResDetails
		records=db.tempdata
		if page==0:
			page=1
		data=records.find().skip(page*20-20).limit(20)
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
		print len(d)
		return jsonify({'restaurants':d})

###### Search By ID ######
class Restaurant(Resource):
	def get(self,id_):
		global connection
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
		global connection
		db=connection.ResData
		records=db.catwise
		data=records.find().skip(page*20-20).limit(20)
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
						pass
			else:
				pass
			dictionary={}
			for each_item in sets:
				dictionary[each_item]=[]
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
		print "category"
		connection=pymongo.MongoClient('mongodb://localhost')
		db=connection.ResData
		records=db.catwise
		print name
		details=records.find({"_id.restaurant_name":name})
		data={}
		for item in details:
			data["menu"]=item["data"]
			print item["_id"]
		connection.close()
		return cat_data

api.add_resource(Restaurants,'/restaurants/page=<int:page>')
api.add_resource(Restaurant,'/<id_>')
api.add_resource(Categories,'/categories/page=<int:page>')
api.add_resource(Category,'/category/<string:name>')


if __name__=='__main__':
	app.run(debug=True)





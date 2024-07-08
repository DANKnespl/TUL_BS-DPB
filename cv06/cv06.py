from init import collection
from bson import ObjectId

'''
DPB - 6. cvičení - Agregační roura a Map-Reduce

V tomto cvičení si můžete vybrat, zda ho budete řešit v Mongo shellu nebo pomocí PyMongo knihovny.

Před testováním Vašich řešení si nezapomeňte zapnout Mongo v Dockeru - používáme stejná data jako v minulých cvičeních.

Pro pomoc je možné např. použít https://api.mongodb.com/python/current/examples/aggregation.html a přednášku.

Všechny výsledky limitujte na 10 záznamů. Nepoužívejte české názvy proměnných!

Struktura záznamu v db:
{
  "address": {
     "building": "1007",
     "coord": [ -73.856077, 40.848447 ],
     "street": "Morris Park Ave",
     "zipcode": "10462"
  },
  "borough": "Bronx",
  "cuisine": "Bakery",
  "grades": [
     { "date": { "$date": 1393804800000 }, "grade": "A", "score": 2 },
     { "date": { "$date": 1378857600000 }, "grade": "A", "score": 6 },
     { "date": { "$date": 1358985600000 }, "grade": "A", "score": 10 },
     { "date": { "$date": 1322006400000 }, "grade": "A", "score": 9 },
     { "date": { "$date": 1299715200000 }, "grade": "B", "score": 14 }
  ],
  "name": "Morris Park Bake Shop",
  "restaurant_id": "30075445"
}
'''


def print_delimiter(n):
    print('\n', '#' * 10, 'Úloha', n, '#' * 10, '\n')


'''
Agregační roura
Zjistěte počet restaurací pro každé PSČ (zipcode)
 a) seřaďte podle zipcode vzestupně
 b) seřaďte podle počtu restaurací sestupně
Výpis limitujte na 10 záznamů a k provedení použijte collection.aggregate(...)
'''
print_delimiter('1 a)')
pipeline =[
      {"$project":{"zipcode":"$address.zipcode"}},
      {"$group":{"_id":"$zipcode","count":{"$sum":1}}},
      {"$sort":{"count":1}},
      {"$limit":10}
   ]
cursor = collection.aggregate(pipeline)
for restaurant in cursor:
    print(restaurant,'\n')

print_delimiter('1 b)')
pipeline =[
      {"$project":{"zipcode":"$address.zipcode"}},
      {"$group":{"_id":"$zipcode","count":{"$sum":1}}},
      {"$sort":{"count":-1}},
      {"$limit":10}
   ]
cursor = collection.aggregate(pipeline)
for restaurant in cursor:
    print(restaurant,'\n')
'''
Agregační roura

Restaurace obsahují pole grades, kde jsou jednotlivá hodnocení. Vypište průměrné score pro každou hodnotu grade.
V agregaci vynechte grade pro hodnotu "Not Yet Graded" (místo A, B atd. se může vyskytovat tento řetězec).

'''
print_delimiter(2)
pipeline =[
      {"$project":{"grades":"$grades"}},
      {"$unwind":"$grades"},
      {"$project":{"grade":"$grades.grade","score":"$grades.score"}},
      {"$match":{"grade":{"$ne":"Not Yet Graded"}}},
      {"$group":{"_id":"$grade","averageScore":{"$avg":"$score"}}},
      {"$sort":{"averageScore":1}}
   ]
cursor = collection.aggregate(pipeline)
for restaurant in cursor:
    print(restaurant,'\n')

print_delimiter("Bonus 1")
pipeline =[
      {"$project":{"name":"$name","grades":"$grades"}},
      {"$unwind":"$grades"},
      {"$project":{"name":"$name","grade":"$grades.grade","score":"$grades.score"}},
      {"$match":{"grade":"A"}},
      {"$project":{"name":"$name","score":"$score"}},
      {"$group":{"name":{"$first":"$name"},"_id":"$_id","averageScore":{"$avg":"$score"},"count":{"$sum":1}}},
      {"$match":{"count":{"$gte":3}}},
      {"$sort":{"averageScore":-1}},
      {"$project":{"name":"$name","avgScore":"$averageScore","count":"$count","_id":0}},
      {"$limit":5}
   ]
cursor = collection.aggregate(pipeline)
for restaurant in cursor:
    print(restaurant,'\n')

print_delimiter("Bonus 2")
pipeline =[
      {"$project":{"name":"$name","cuisine":"$cuisine","grades":"$grades"}},
      {"$match":{"grades.2" : {"$exists" : "true"}}}, #
      {"$unwind":"$grades"},
      {"$project":{"name":"$name","cuisine":"$cuisine","grade":"$grades.grade","score":"$grades.score"}},
      {"$match":{"grade":"A"}}, #
      {"$project":{"name":"$name","cuisine":"$cuisine","score":"$score"}},
      {"$group":{"name":{"$first":"$name"},"cuisine":{"$first":"$cuisine"},"_id":"$_id","averageScore":{"$avg":"$score"},"count":{"$sum":1}}}, 
      {"$group":{"name":{"$first":"$name"},"_id":"$cuisine","score":{"$max":"$averageScore"}}}, 
      {"$sort":{"score":-1}},
      {"$project":{"cuisine":"$_id","name":"$name","_id":0}},
      {"$limit":5}
   ]
cursor = collection.aggregate(pipeline)
for restaurant in cursor:
    print(restaurant,'\n')

print_delimiter("Bonus 3")
pipeline =[
      {"$project":{"name":"$name","grades":"$grades"}},
      {"$unwind":"$grades"},
      {"$project":{"name":"$name","score":"$grades.score"}},
      {"$match":{"score":{"$gt":10},"name":{"$regex":".*\w+\s+\w+.*"}}},
      {"$group":{"_id":"$_id","name":{"$first":"$name"},"count":{"$sum":1}}},
      {"$match":{"count":{"$gte":2}}},
      {"$sort":{"count":1}},
      {"$project":{"name":"$name","_id":0}},
      {"$limit":5}
   ]
cursor = collection.aggregate(pipeline)
for restaurant in cursor:
    print(restaurant,'\n')


#cursor = collection.find({"name":{"$regex":"Blue"}})
#for restaurant in cursor:
#    print(restaurant,'\n')

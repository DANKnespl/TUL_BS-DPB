from init import collection
import datetime

print(collection.find_one())

'''
DPB - 5. Cvičení

Implementujte jednotlivé body pomocí PyMongo knihovny - rozhraní je téměř stejné jako v Mongo shellu.
Před testováním Vašich řešení si nezapomeňte zapnout Mongo v Dockeru.

Pro pomoc je možné např. použít https://www.w3schools.com/python/python_mongodb_getstarted.asp

Funkce find vrací kurzor - pro vypsání výsledku je potřeba pomocí foru iterovat nad kurzorem:

cursor = collection.find(...)
for restaurant in cursor:
    print(restaurant) # případně print(restaurant['name'])

Všechny výsledky limitujte na 10 záznamů. Nepoužívejte české názvy proměnných!
'''


def print_delimiter(n):
    print('\n', '#' * 10, 'Úloha', n, '#' * 10, '\n')

# 1. Vypsání všech restaurací 
print_delimiter(1)
cursor = collection.find().limit(10)
for restaurant in cursor:
    print(restaurant,'\n')


# 2. Vypsání všech restaurací - pouze názvů, abecedně seřazených
print_delimiter(2)
cursor = collection.find().sort('name',1).limit(10)
for restaurant in cursor:
    print(restaurant['name'],'\n')

# 3. Vypsání pouze 10 záznamů z předchozího dotazu
print_delimiter(3)
cursor = collection.find().sort('name',1).limit(5)
for restaurant in cursor:
    print(restaurant['name'],'\n')

# 4. Zobrazte dalších 10 záznamů
print_delimiter(4)
cursor = collection.find().sort('name',1).limit(10).skip(10)
for restaurant in cursor:
    print(restaurant['name'],'\n')

# 5. #Vypsání restaurací ve čtvrti Bronx (čtvrť = borough)
print_delimiter(5)
cursor = collection.find({'borough':"Bronx"}).limit(10)
for restaurant in cursor:
    print(restaurant['name'],'\n')

# 6. Vypsání restaurací, jejichž název začíná na písmeno M
print_delimiter(6)
cursor = collection.find({"name": {'$regex': '^M'}}).limit(10)
for restaurant in cursor:
    print(restaurant['name'],'\n')


# 7. Vypsání restaurací, které mají skóre větší než 80
print_delimiter(7)
cursor = collection.find({"grades":{"$elemMatch":{"score":{"$gt":80}}}}).limit(10)
for restaurant in cursor:
    print(restaurant['name'],'\n')

# 8. Vypsání restaurací, které mají skóre mezi 80 a 90
print_delimiter(8)
cursor = collection.find({"grades":{"$elemMatch":{"$and":[{"score":{"$lt":90}},{"score":{"$gt":80}}]}}}).limit(10)
for restaurant in cursor:
    print(restaurant["name"],'\n')


'''
Bonusové úlohy:
'''

# 9. Vypsání všech restaurací, které mají skóre mezi 80 a 90 a zároveň nevaří americkou (American) kuchyni
print_delimiter(9)
cursor = collection.find({"$and":[{"grades":{"$elemMatch":{"$and":[{"score":{"$lt":90}},{"score":{"$gt":80}}]}}},{"cuisine":{"$not":{"$regex":"American"}}}]}).limit(10)
for restaurant in cursor:
    print(restaurant['name'],'\n')


# 10. Vypsání všech restaurací, které mají alespoň osm hodnocení
print_delimiter(10)
cursor = collection.find({"grades.7" : {"$exists" : "true"}}).limit(10)
for restaurant in cursor:
    print(restaurant['name'],'\n')


# 11. Vypsání všech restaurací, které mají alespoň jedno hodnocení z roku 2014 
print_delimiter(11)
cursor=collection.find({"grades":{"$elemMatch":{"date":{"$gte":datetime.datetime(2014, 1, 1, 0, 0),"$lt":datetime.datetime(2015, 1, 1, 0, 0)}}}}).limit(10)
for restaurant in cursor:
    print(restaurant["name"],'\n')


'''
V této části budete opět vytvářet vlastní restauraci.

Řešení:
Vytvořte si vaši restauraci pomocí slovníku a poté ji vložte do DB.
restaurant = {
    ...
}
'''

# 12. Uložte novou restauraci (stačí vyplnit název a adresu)
print_delimiter(12)
r1= {
    "name":"Restaurace galaxie",
    "address":{'building': '877', 'coord': [0, 0], 'zipcode': '47301'}
}
r2={
    "name":"Restaurace u sussu",
    "address":{'building': '788', 'coord': [13, 24], 'zipcode': '47301'}}
c1=collection.insert_one(r1)
c2=collection.insert_one(r2)
print("ID_RG: ",c1.inserted_id)
print("ID_RUS ",c2.inserted_id)

# 13. Vypište svoji restauraci
print_delimiter(13)
cursor=collection.find({"name":"Restaurace galaxie"}).limit(10)
for restaurant in cursor:
    print(restaurant,'\n')

# 14. Aktualizujte svoji restauraci - změňte libovolně název
print_delimiter(14)
c3=collection.update_one({"name":"Restaurace u sussu"},{"$set":{"name":"Hostinec koni chcanky"}})
print("Updated: ",c3.matched_count)
# 15. Smažte svoji restauraci
# 15.1 pomocí id (delete_one)
# 15.2 pomocí prvního nebo druhého názvu (delete_many, využití or)
print_delimiter(15)
collection.delete_one({"_id":c1.inserted_id})
c3=collection.delete_many({"$or":[{"name":"Hostinec koni chcanky"},{"name":"Restaurace u sussu"}]})
print("Deleted: ",c3.deleted_count)

cursor=collection.find({"$or":[{"name":"Hostinec koni chcanky"},{"name":"Restaurace galaxie"},{"name":"Restaurace u sussu"}]}).limit(10)
for restaurant in cursor:
    print(restaurant,'\n')

'''
Poslední částí tohoto cvičení je vytvoření jednoduchého indexu.

Použijte např. 3. úlohu s vyhledáváním čtvrtě Bronx. První použijte Váš již vytvořený dotaz a na výsledek použijte:

cursor.explain()['executionStats'] - výsledek si vypište na výstup a všimněte si položky 'totalDocsExamined'

Poté vytvořte index na 'borough', zopakujte dotaz a porovnejte hodnoty 'totalDocsExamined'.

S řešením pomůže https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.create_index
'''
print_delimiter(16)
collection.drop_index("borough_1")
cursor = collection.find({'borough':"Bronx"})
print(cursor.explain()['executionStats'],"\n")
print(collection.index_information(),"\n")

collection.create_index("borough")
cursor = collection.find({'borough':"Bronx"})
print(cursor.explain()['executionStats'],"\n")
print(collection.index_information(),"\n")

#3772 vs 309

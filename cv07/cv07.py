from elasticsearch import Elasticsearch
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


INDEX_NAME = 'person'


def print_delimiter(n):
    print('\n', '#' * 10, 'Úloha', n, '#' * 10, '\n')


# Připojení k ES
es = Elasticsearch([{'host': 'localhost', 'port': 9200,'scheme':'https'}],basic_auth=('elastic','elastic'),ca_certs=False,verify_certs=False)

# Kontrola zda existuje index 'person'
if not es.indices.exists(index=INDEX_NAME):
    # Vytvoření indexu
    es.indices.create(index=INDEX_NAME)

# Index není potřeba vytvářet - pokud neexistuje, tak se automaticky vytvoří při vložení prvního dokumentu

# 1. Vložte osobu se jménem John
print_delimiter(1)
print(es.index(index=INDEX_NAME,id=1,document={"name":"John"}))
# 2. Vypište vytvořenou osobu (pomocí get a parametru id)
print_delimiter(2)
print(es.get(index=INDEX_NAME,id=1))
# 3. Vypište všechny osoby (pomocí search)
print_delimiter(3)
print(es.search(index=INDEX_NAME, query={"match_all": {}}))
# 4. Přejmenujte vytvořenou osobu na 'Jane'
print_delimiter(4)
es.index(index=INDEX_NAME,id=1,document={"name":"Jane"})
print(es.get(index=INDEX_NAME,id=1))
# 5. Smažte vytvořenou osobu
print_delimiter(5)
es.delete(index=INDEX_NAME,id=1)
print(es.search(index=INDEX_NAME))
# 6. Smažte vytvořený index
print_delimiter(6)
es.indices.delete(index=INDEX_NAME)
print(es.indices.exists(index=INDEX_NAME))


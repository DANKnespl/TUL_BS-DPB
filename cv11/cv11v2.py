from cassandra.cluster import Cluster
import time
import datetime
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

'''
DPB - 11. cvičení Cassandra

Use case: Discord server - reálně používáno pro zprávy, zde pouze zjednodušená varianta.

Instalace python driveru: pip install cassandra-driver

V tomto cvičení se budou následující úlohy řešit s využitím DataStax driveru pro Cassandru.
Dokumentaci lze nalézt zde: https://docs.datastax.com/en/developer/python-driver/3.25/getting_started/


Optimální řešení (nepovinné) - pokud něco v db vytváříme, tak první kontrolujeme, zda to již neexistuje.


Pro uživatele PyCharmu:

Pokud chcete zvýraznění syntaxe, tak po napsání prvního dotazu se Vám u něj objeví žlutá žárovka, ta umožňuje vybrat 
jazyk pro tento projekt -> vyberte Apache Cassandra a poté Vám nabídne instalaci rozšíření pro tento typ db.
Zvýraznění občas nefunguje pro příkaz CREATE KEYSPACE.

Také je možné do PyCharmu připojit databázi -> v pravé svislé liště najděte Database a připojte si lokální Cassandru.
Řešení cvičení chceme s využitím DataStax driveru, ale s integrovaným nástrojem pro databázi si můžete pomoct sestavit
příslušně příkazy.


Pokud se Vám nedaří připojit se ke Cassandře v Dockeru, zkuste smazat kontejner a znovu spustit:

docker run --name dpb_cassandra -p 127.0.0.1:9042:9042 -p 127.0.0.1:9160:9160 -d cassandra:latest

'''

def print_delimiter(n):
    print('\n', '#' * 10, 'Úloha', n, '#' * 10, '\n')


def print_result(result):
    for row in result:
        print(row)


cluster = Cluster()  # automaticky se připojí k localhostu na port 9042
session = cluster.connect()

"""
1. Vytvořte keyspace 'dc' a přepněte se do něj (SimpleStrategy, replication_factor 1)
"""
session.execute("DROP KEYSPACE dc;")
print_delimiter(1)
session.execute("CREATE KEYSPACE dc WITH REPLICATION = { 'class' : 'SimpleStrategy','replication_factor' : 1};")
session.execute("USE dc;")

"""
2. V csv souboru message_db jsou poskytnuta data pro cvičení. V prvním řádku naleznete názvy sloupců.
   Vytvořte tabulku messages - zvolte vhodné datové typy (time bude timestamp)
   Primárním klíčem bude room_id a time
   Data chceme mít seřazené podle času, abychom mohli rychle získat poslední zprávy

   Jako id v této úloze zvolíme i time - zdůvodněte, proč by se v praxi time jako id neměl používat.

   Pokud potřebujeme použít čas, tak se v praxi používá typ timeuuid nebo speciální identifikátor, tzv. Snowflake ID
   (https://en.wikipedia.org/wiki/Snowflake_ID). Není potřeba řešit v tomto cvičení.
"""
print_delimiter(2)
session.execute("CREATE TABLE message_db( "+
                "room_id int, "+
                "speaker_id int, "+
                "time timestamp, "+
                "message text, "+
"PRIMARY KEY (room_id, time));")

"""
3. Do tabulky messages importujte message_db.csv
   COPY není možné spustit pomocí DataStax driveru ( 'copy' is a cqlsh (shell) command rather than a CQL (protocol) command)
   -> 2 možnosti:
      a) Nakopírovat csv do kontejneru a spustit COPY příkaz v cqlsh konzoli uvnitř dockeru
      b) Napsat import v Pythonu - otevření csv a INSERT dat
CSV soubor může obsahovat chybné řádky - COPY příkaz automaticky přeskočí řádky, které se nepovedlo správně parsovat
"""
print_delimiter(3)
prepared = session.prepare("""
            INSERT INTO message_db (room_id,speaker_id,time,message)
            VALUES (?, ?, ?, ?);
            """)
with open("D:/TUL/DPB/cv11/message_db.csv", "r") as lines:
    for line in lines:
            try:
                columns=line.strip().split(";")
                room_id=int(columns[0])
                speaker_id= int(columns[1])
                timex=datetime.datetime.strptime(columns[2],"%Y-%m-%d %H:%M:%S.%f")
                message=columns[3]
                session.execute(prepared, [room_id,speaker_id,timex,message])
            except:
                print()
#closing the file
lines.close()


"""
4. Kontrola importu - vypište 1 zprávu
"""
print_delimiter(4)
rows=session.execute("SELECT message FROM message_db;")
print(rows[0][0])

"""
5. Vypište posledních 5 zpráv v místnosti 1 odeslaných uživatelem 2
    Nápověda 1: Sekundární index (viz přednáška) 
    Nápověda 2: Data jsou řazena již při vkládání
"""
print_delimiter(5)
session.execute("CREATE INDEX speaker_id_index ON message_db (speaker_id);")
#SELECT * FROM message_db WHERE room_id=1 AND speaker_id=2;
rowsR1=session.execute("SELECT * FROM message_db WHERE room_id=1")
rowsR1S2=[]
for row in rowsR1:
    if row[3]==2:
        rowsR1S2.append(row[2])
rowsR1S2.reverse()
for i in range(0,5):
    print(rowsR1S2[i])

"""
6. Vypište počet zpráv odeslaných uživatelem 2 v místnosti 1
"""
print_delimiter(6)
#SELECT COUNT(*) FROM message_db WHERE room_id=1 AND speaker_id=2;
rowsR1=session.execute("SELECT * FROM message_db WHERE room_id=1")
countR1S2=0
for row in rowsR1:
    if row[3]==2:
        countR1S2=countR1S2+1
print("zprávy UID=2, RID=1: "+str(countR1S2))

"""
7. Vypište počet zpráv v každé místnosti
"""
print_delimiter(7)
#SELECT room_id, COUNT(room_id) FROM message_db GROUP BY room_id;
rows=session.execute("SELECT room_id, COUNT(room_id) FROM message_db GROUP BY room_id;")
print("RID|count")
for row in rows:
    print(str(row[0])+" | "+str(row[1]))

"""
8. Vypište id všech místností (3 hodnoty)
"""
print_delimiter(8)
#SELECT DISTINCT room_id FROM message_db;
rows=session.execute("SELECT DISTINCT room_id FROM message_db;")
print("RID")
for row in rows:
    print(row[0])


print_delimiter("B1")
#CREATE MATERIALIZED VIEW message_mv AS SELECT room_id, time, message FROM message_db WHERE room_id IS NOT NULL AND time IS NOT NULL AND message IS NOT NULL PRIMARY KEY (room_id,time,message);
session.execute("CREATE MATERIALIZED VIEW message_mv AS SELECT room_id, time, message FROM message_db WHERE room_id IS NOT NULL AND time IS NOT NULL AND message IS NOT NULL PRIMARY KEY (room_id,time,message);")
rows=session.execute("SELECT * FROM message_mv;")
print(rows[0])

print_delimiter("B2")
session.execute("CREATE FUNCTION IF NOT EXISTS bad (input text) CALLED ON NULL INPUT RETURNS int LANGUAGE java AS 'return input.contains(\"you\")?1:0;';")
rows=session.execute("SELECT message, bad(message) FROM message_db LIMIT 10;")
for row in rows:
    print(str(str(row[1])+", "+row[0]))




print_delimiter("B3")
rows=session.execute("SELECT time FROM message_db;")
print("oldest: "+str(rows[0]))
print("latest: "+str(rows[-1]))



print_delimiter("B4")
session.execute("CREATE FUNCTION IF NOT EXISTS len (input text) CALLED ON NULL INPUT RETURNS int LANGUAGE java AS 'return input.length();';")
row=session.execute("SELECT MIN(len(message)), MAX(len(message)) FROM message_db")
print("min|max lengths of message")
print(str(row[0][0])+" | "+str(row[0][1]))

print_delimiter("B5")
#rows=session.execute("SELECT speaker_id, AVG(len(message)) FROM message_db GROUP BY speaker_id")
rows=session.execute("SELECT speaker_id, len(message) FROM message_db")
SpAvg=[[0,0,0]]
print("UID|Average length of message")
for row in rows:
    for i in SpAvg:
        if row[0] == i[0]:
            i[1]=i[1]+row[1]
            i[2]=i[2]+1
            break
        if i==SpAvg[-1]:
            SpAvg.append([row[0],row[1],1])

for speaker in SpAvg:
    if speaker[2]>0:
        print(str(speaker[0])+" | "+str(speaker[1]/speaker[2]))

"""
Bonusové úlohy:

1. Pro textovou analýzu chcete poskytovat anonymizovaná textová data. Vytvořte Materialized View pro tabulku messages,
který bude obsahovat pouze čas, room_id a zprávu.

Vypište jeden výsledek z vytvořeného view

Před začátkem řešení je potřeba jít do souboru cassandra.yaml uvnitř docker kontejneru a nastavit enable_materialized_views=true

docker exec -it dpb_cassandra bash
sed -i -r 's/enable_materialized_views: false/enable_materialized_views: true/' /etc/cassandra/cassandra.yaml

Poté restartovat kontejner

2. Chceme vytvořit funkci (UDF), která při výběru dat vrátí navíc příznak, zda vybraný text obsahuje nevhodný výraz.

Vyberte jeden výraz (nemusí být nevhodný:), vytvořte a otestujte Vaši funkci.

Potřeba nastavit enable_user_defined_functions=true v cassandra.yaml

sed -i -r 's/enable_user_defined_functions: false/enable_user_defined_functions: true/' /etc/cassandra/cassandra.yaml

3. Zjistěte čas odeslání nejnovější a nejstarší zprávy.

4. Zjistěte délku nejkratší a nejdelší zprávy na serveru.	

5. Pro každého uživatele zjistěte průměrnou délku zprávy.		

V celém cvičení by nemělo být použito ALLOW FILTERING.
"""


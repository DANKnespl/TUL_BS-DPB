### 1)  vytvořte keyspace cass01

```
CREATE KEYSPACE cass01
WITH REPLICATION = { 'class' : 'SimpleStrategy',
'replication_factor' : 1};
```

### 2) ověřte vytvoření keyspace a následně se do ní přepněte

```
DESCRIBE KEYSPACE cass01;
USE cass01;
```

### 3) vytvořte tabulku *activity* se dvěma sloupci *id* a *datetime*

```
CREATE TABLE activity(
id text,
datetime timestamp,
PRIMARY KEY (id, datetime)
) WITH CLUSTERING ORDER BY (datetime DESC);
DESCRIBE TABLE activity;
```

### 4) do tabulky přidejte sloupec *event* (text) a ověřte, že byl přidán

```
ALTER TABLE activity
ADD event text;
DESCRIBE TABLE activity;
```

### 5) vložte jeden libovolný záznam

```
INSERT INTO activity(id, datetime, event)
VALUES ('1', '2002-03-27 19:32:45', 'birth');
```


### 6) vložte libovolný druhý záznam s aktuální timestamp hodnotou

```
INSERT INTO activity(id, datetime, event)
VALUES ('2', dateof(now()), 'cv10-u6');
```

### 7) vypište vložené záznamy

```
SELECT * FROM activity;
```

### 8) smažte vytvořené záznamy, tabulku a následně i keyspace

```
TRUNCATE activity;
DROP TABLE activity;
DROP KEYSPACE cass01;
```

## Bonusové úlohy

### 1) vytvořte keyspace cass01_bonus
	SimpleStrategy, replication_factor 1

```
CREATE KEYSPACE cass01_bonus
WITH REPLICATION = { 'class' : 'SimpleStrategy',
'replication_factor' : 1};
```

### 2) vytvořte tabulku *activity_bonus* se čtyřmi sloupci
	id, datetime, type a duration
	PK se skládá z id, datetime a type
	záznamy se shodným id a type jsou na stejné partition
	datetime ke vzestupnému třízení

```
USE cass01_bonus;
CREATE TABLE activity_bonus(
id text,
datetime timestamp,
type text,
duration text,
PRIMARY KEY ((id, type),  datetime)
) WITH CLUSTERING ORDER BY (datetime ASC);
DESCRIBE TABLE activity_bonus;
```

### 3) tabulku rozšiřte o vámi vybrané další sloupce
	alespoň 3 složitější datové typy (list, set, map, tuple ...)

```
ALTER TABLE activity_bonus
ADD (at1List list<int>, at2set set<int>, at3tupple tuple<int,int>);
DESCRIBE TABLE activity_bonus;
```

### 4) vložte alespoň 10 záznamů a tabulku vypište

```
BEGIN BATCH 
	INSERT INTO activity_bonus (id,type,datetime, at1list,at2set,at3tupple, duration) VALUES ('1', 'type1', dateof(now()),[1,2,3],{1,2,3},(1,2),'very long' );
	INSERT INTO activity_bonus (id,type,datetime, at1list,at2set,at3tupple, duration) VALUES ('2', 'type1', dateof(now()),[1,2,3],{1,2,3},(1,2),'very long' );
	INSERT INTO activity_bonus (id,type,datetime, at1list,at2set,at3tupple, duration) VALUES ('3', 'type1', dateof(now()),[1,2,3],{1,2,3},(1,2),'very long' );
	INSERT INTO activity_bonus (id,type,datetime, at1list,at2set,at3tupple, duration) VALUES ('4', 'type1', dateof(now()),[1,2,3],{1,2,3},(1,2),'very long' );
	INSERT INTO activity_bonus (id,type,datetime, at1list,at2set,at3tupple, duration) VALUES ('5', 'type1', dateof(now()),[1,2,3],{1,2,3},(1,2),'very long' );
	INSERT INTO activity_bonus (id,type,datetime, at1list,at2set,at3tupple, duration) VALUES ('6', 'type1', dateof(now()),[1,2,3],{1,2,3},(1,2),'very long' );
	INSERT INTO activity_bonus (id,type,datetime, at1list,at2set,at3tupple, duration) VALUES ('7', 'type1', dateof(now()),[1,2,3],{1,2,3},(1,2),'very long' );
	INSERT INTO activity_bonus (id,type,datetime, at1list,at2set,at3tupple, duration) VALUES ('8', 'type1', dateof(now()),[1,2,3],{1,2,3},(1,2),'very long' );
	INSERT INTO activity_bonus (id,type,datetime, at1list,at2set,at3tupple, duration) VALUES ('9', 'type1', dateof(now()),[1,2,3],{1,2,3},(1,2),'very long' );
	INSERT INTO activity_bonus (id,type,datetime, at1list,at2set,at3tupple, duration) VALUES ('10', 'type1', dateof(now()),[1,2,3],{1,2,3},(1,2),'very long' );
APPLY BATCH;
SELECT * FROM activity_bonus
```

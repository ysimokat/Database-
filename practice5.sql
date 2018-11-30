
-- Drop all the tables to clean up
DROP TABLE Handles;
DROP TABLE Animal;
DROP TABLE ZooKeeper;

CREATE TABLE ZooKeeper
(
  ZID        NUMBER(3,0),
  ZName       VARCHAR2(25) NOT NULL,
  HourlyRate NUMBER(6, 2) NOT NULL,
  
  CONSTRAINT ZooKeeper_PK
     PRIMARY KEY(ZID)
);


-- ACategory: Animal category 'common', 'rare', 'exotic'.  May be NULL
-- TimeToFeed: Time it takes to feed the animal (hours)
CREATE TABLE Animal
(
  AID       NUMBER(3, 0),
  AName      VARCHAR(30) NOT NULL,
  ACategory VARCHAR(18),
  
  TimeToFeed NUMBER(4,2),  
  
  CONSTRAINT Animal_PK
    PRIMARY KEY(AID)
);


CREATE TABLE Handles
(
  ZooKeepID      NUMBER(3,0),
  AnimalID     NUMBER(3,0),
  
  Assigned     DATE,
  
  CONSTRAINT Handles_PK
    PRIMARY KEY(ZooKeepID, AnimalID),
    
  CONSTRAINT Handles_FK1
    FOREIGN KEY(ZooKeepID)
      REFERENCES ZooKeeper(ZID),
      
  CONSTRAINT Handles_FK2
    FOREIGN KEY(AnimalID)
      REFERENCES Animal(AID)
);


INSERT INTO ZooKeeper VALUES (1, 'Jim Carrey', 500);
INSERT INTO ZooKeeper VALUES (2, 'Tina Fey', 350);  
INSERT INTO ZooKeeper VALUES (3, 'Rob Schneider', 250);
  
INSERT INTO Animal VALUES(1, 'Galapagos Penguin', 'exotic', 0.5);
INSERT INTO Animal VALUES(2, 'Emperor Penguin', 'rare', 0.75);

INSERT INTO Animal VALUES(3, 'Sri Lankan sloth bear', 'exotic', 2.5);
INSERT INTO Animal VALUES(4, 'Grizzly bear', 'common', 3.0);
INSERT INTO Animal VALUES(5, 'Giant Panda bear', 'exotic', 1.5);
INSERT INTO Animal VALUES(6, 'Florida black bear', 'rare', 1.75);

INSERT INTO Animal VALUES(7, 'Siberian tiger', 'rare', 3.5);
INSERT INTO Animal VALUES(8, 'Bengal tiger', 'common', 2.75);
INSERT INTO Animal VALUES(9, 'South China tiger', 'exotic', 2.25);

INSERT INTO Animal VALUES(10, 'Alpaca', 'common', 0.25);
INSERT INTO Animal VALUES(11, 'Llama', NULL, 3.5);



INSERT INTO Handles VALUES(1, 1, '01-Jan-2000');
INSERT INTO Handles VALUES(1, 2, '02-Jan-2000');
INSERT INTO Handles VALUES(1, 10, '01-Jan-2000');

INSERT INTO Handles VALUES(2, 3, '02-Jan-2000');
INSERT INTO Handles VALUES(2, 4, '04-Jan-2000');
INSERT INTO Handles VALUES(2, 5, '03-Jan-2000');

INSERT INTO Handles VALUES(3, 7, '01-Jan-2000');
INSERT INTO Handles VALUES(3, 8, '03-Jan-2000');
INSERT INTO Handles VALUES(3, 9, '05-Jan-2000');
INSERT INTO Handles Values(3, 10,'04-Jan-2000');

--1: Find all the rare animals and sort the query output by feeding time (from small to large).
select * from Animal where ACATEGORY='rare' order by TIMETOFEED;

--2 :Find the animal names and categories for animals related to a bear 
select ANAME,ACATEGORY from Animal where ANAME like '%bear';

--3: Return the listings for all animals whose category is missing in the database.
select * from Animal where ACATEGORY is null;

--4: Find the rarity rating of all animals that require between 1 and 2.5 hours to be fed.
select * from Animal where TIMETOFEED >= 1 and TIMETOFEED <=2.5;

--5: Find the names of the animals that are related to the tiger and are not common.
select ANAME from Animal where ANAME like '%tiger' and ACATEGORY!='common';

--6: Find the names of the animals that are not related to the tiger.
select ANAME from Animal where ANAME not in (select ANAME from Animal where ANAME like '%tiger');

--7: Find the minimum and maximum feeding time amongst all the animals in the zoo.
select min(TIMETOFEED),max(TIMETOFEED) from Animal;

--8: Find the average feeding time for all of the rare animals.
select avg(TIMETOFEED) from Animal where ACATEGORY = 'rare';

--9: List zookeepers earning the least while feeding animals.
select * from ZooKeeper where HOURLYRATE= (select min(HOURLYRATE) from ZooKeeper);

--10: Name zookeepers handling at least 4 animals.
select ZNAME from ZooKeeper where ZID = (select ZOOKEEPID from Handles group by ZOOKEEPID having count(*)>=4);

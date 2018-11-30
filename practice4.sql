/* Delete the tables if they already exist */
drop table  Restaurant;
drop table  Reviewer;
drop table  Rating;

/* Create the schema for our tables */
create table Restaurant(rID int, name varchar2(100), address varchar2(100), cuisine varchar2(100));
create table Reviewer(vID int, name varchar2(100));
create table Rating(rID int, vID int, stars int, ratingDate int);

/* Populate the tables with our data */
insert into Restaurant values(101, 'India House Restaurant', '59 W Grand Ave Chicago, IL 60654', 'Indian');
insert into Restaurant values(102, 'Bombay Wraps', '122 N Wells St Chicago, IL 60606', 'Indian');
insert into Restaurant values(103, 'Rangoli', '2421 W North Ave Chicago, IL 60647', 'Indian');
insert into Restaurant values(104, 'Cumin', '1414 N Milwaukee Ave Chicago, IL 60622', 'Indian');
insert into Restaurant values(105, 'Shanghai Inn', '4723 N Damen Ave Chicago, IL 60625', 'Chinese');
insert into Restaurant values(106, 'MingHin Cuisine', '333 E Benton Pl Chicago, IL 60601', 'Chinese');
insert into Restaurant values(107, 'Shanghai Terrace', '108 E Superior St Chicago, IL 60611', 'Chinese');
insert into Restaurant values(108, 'Jade Court', '626 S Racine Ave Chicago, IL 60607', 'Chinese');

insert into Reviewer values(2001, 'Sarah M.');
insert into Reviewer values(2002, 'Daniel L.');
insert into Reviewer values(2003, 'B. Harris');
insert into Reviewer values(2004, 'P. Suman');
insert into Reviewer values(2005, 'Suikey S.');
insert into Reviewer values(2006, 'Elizabeth T.');
insert into Reviewer values(2007, 'Cameron J.');
insert into Reviewer values(2008, 'Vivek T.');

insert into Rating values( 101, 2001,2, 20110122);
insert into Rating values( 101, 2001,4, 20110127);
insert into Rating values( 106, 2002,4, null);
insert into Rating values( 103, 2003,2, 20110120);
insert into Rating values( 108, 2003,4, 20110112);
insert into Rating values( 108, 2003,2, 20110130);
insert into Rating values( 101, 2004,3, 20110109);
insert into Rating values( 103, 2005,3, 20110127);
insert into Rating values( 104, 2005,2, 20110122);
insert into Rating values( 108, 2005,4, null);
insert into Rating values( 107, 2006,3, 20110115);
insert into Rating values( 106, 2006,5, 20110119);
insert into Rating values( 107, 2007,5, 20110120);
insert into Rating values( 104, 2008,3, 20110102);

--1. Find the name of all restaurants offering Indian cuisine
select NAME from Restaurant where CUISINE='Indian';

--2. Find restaurant names that received a rating of 4 or 5, sort them in increasing order. 
select distinct NAME from Restaurant where RID in (select distinct RID from Rating where STARS=4 or STARS=5);

--3. Find the names of all restaurants that have no rating.
select distinct NAME from Restaurant where RID not in (select distinct RID from Rating);

--4. Some reviewers didn't provide a date with their rating. Find the names of all reviewers who have ratings with a NULL value for the date. 
select NAME from Reviewer where VID in (select distinct VID from Rating where RATINGDATE is null);

--5. For all cases where the same reviewer rated the same restaurant twice and gave it a higher rating the second time, return the reviewer's name and the name of the restaurant.
select A.NAME, B.NAME from Reviewer A,Restaurant B where (A.VID,B.RID) IN
(select R.VID,R.RID from Rating R where (select STARS from Rating R2 where R.RID= R2.RID and R.VID=R2.VID AND R.RATINGDATE>R2.RATINGDATE and R.STARS>R2.STARS)>1);

--6. For each restaurant that has at least one rating, find the highest number of stars that a restaurant received. Return the restaurant name and number of stars. Sort by restaurant name. 
select distinct A.NAME, B.STARS from Restaurant A, Rating B where (A.RID,B.STARS) in
(select distinct RID,STARS from Rating R1 where STARS >= (select max(STARS) from Rating R2 where R1.RID=R2.RID)) order by A.NAME;

--7. For each restaurant, return the name and the 'rating spread', that is, the difference between highest and lowest ratings given to that restaurant. Sort by rating spread from highest to lowest, then by restaurant name. 
select Restaurant.NAME, max(STARS)-min(STARS) as spread
from Rating join Restaurant on Rating.RID=Restaurant.RID
group by NAME
order by spread desc, NAME;

--8. Find the difference between the average rating of Indian restaurants and the average rating of Chinese restaurants. 
select round(max(A)-min(A),2) from
(select avg(A1) A from (select avg(STARS) as A1 from Rating R1 join Restaurant R2 on R1.RID=R2.RID where R2.CUISINE='Indian')
union 
select avg(A2) A from (select avg(STARS) as A2 from Rating R1 inner join Restaurant R2 on R1.RID=R2.RID where CUISINE='Chinese'));







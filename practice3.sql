drop table data;
drop table address;
drop table Assistant;

--1NF table
create table data(
    First varchar(40),
    Last varchar(40),
    Address varchar(40),
    Job varchar(20),
    Salary varchar(5),
    Assistant varchar(20),
    primary key (First, Last, Job)
    );
    
insert into data values('John', 'Smith', '111 N. Wabash Avenue', 'plumber', '40K', '');
insert into data values('John', 'Smith', '111 N. Wabash Avenue', 'bouncer', '35K', '');
insert into data values('Jane', 'Doe', '243 S. Wabash Avenue', 'waitress', '50K', '');
insert into data values('Jane', 'Doe', '243 S. Wabash Avenue', 'accountant', '42K', 'Yes');
insert into data values('Jane', 'Doe', '243 S. Wabash Avenue', 'bouncer', '35K','');
insert into data values('Mike', 'Jackson', '1 Michigan Avenue', 'accountant', '42K', 'Yes');
insert into data values('Mike', 'Jackson', '1 Michigan Avenue', 'plumber', '40K', '');
insert into data values('Mary', 'Who', '20 S. Michigan Avenue', 'accountant', '42K', 'Yes');
insert into data values('Mary', 'Who', '20 S. Michigan Avenue', 'risk analyst', '80K', 'Yes');


-- 3NF Tables
create table address(
    First varchar(40),
    Last varchar(40),
    Address varchar(40),
    primary key (First, Last)
    );

insert into address values('John', 'Smith', '111 N. Wabash Avenue');
insert into address values('Jane', 'Doe', '243 S. Wabash Avenue');
insert into address values('Mike', 'Jackson', '1 Michigan Avenue');
insert into address values('Mary', 'Who', '20 S. Michigan Avenue');

create table Assistant(
    Job varchar(20),
    Salary varchar(5),
    Assistant varchar(20),
    primary key (Job)
    );

insert into Assistant values('plumber', '40K', '');
insert into Assistant values('bouncer', '35K', '');
insert into Assistant values('waitress', '50K', '');
insert into Assistant values('accountant', '42K', 'Yes');
insert into Assistant values('risk analyst', '80K', 'Yes');

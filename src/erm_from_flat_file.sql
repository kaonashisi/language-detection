use languages;

/*****************************************

Creation of branch table

*****************************************/

-- check branch counts
select s.branch, count(*) from languages.spoken_language_info s
group by 1;

-- create a new dimension table for the branch dimension
create table if not exists languages.branch (
branch_id int auto_increment,
branch_name varchar(256),
primary key (branch_id));

-- check the table was created...
select * from languages.branch;

-- lets populate the table by inserting the unique values for that dimension
insert into languages.branch(branch_name)
select distinct branch from languages.spoken_language_info;

-- check it has correctly populated
select * from languages.branch;

-- now lets adjust the original table so we will use this table
alter table languages.spoken_language_info add column branch_id int after branch;

-- lets set up the foreign key reference
alter table languages.spoken_language_info ADD CONSTRAINT branch_fk FOREIGN KEY (branch_id) REFERENCES languages.branch (branch_id);

-- check the extra column has appeared
select * from languages.spoken_language_info limit 10;

-- populate the column using the dimension table we created
update languages.spoken_language_info s, languages.branch b
set s.branch_id = b.branch_id
where s.branch = b.branch_name;

-- check it is populated
select * from languages.spoken_language_info limit 10;

-- lets drop the original column now
alter table languages.spoken_language_info drop column branch;

-- check everything is as expected
select * from languages.spoken_language_info limit 10;
select b.branch_name, count(*) from languages.spoken_language_info s
inner join languages.branch b on s.branch_id = b.branch_id
group by 1;

/*****************************************

Creation of family table

*****************************************/

-- check branch counts
select s.family, count(*) from languages.spoken_language_info s
group by 1;

-- create a new dimension table for the branch dimension
create table if not exists languages.family (
family_id int auto_increment,
family_name varchar(256),
primary key (family_id));

-- check the table was created...
select * from languages.family;

-- lets populate the table by inserting the unique values for that dimension
insert into languages.family(family_name)
select distinct family from languages.spoken_language_info;

-- check it has correctly populated
select * from languages.family;

-- now lets adjust the original table so we will use this table
alter table languages.spoken_language_info add column family_id int after family;

-- lets set up the foreign key reference
alter table languages.spoken_language_info ADD CONSTRAINT family_fk FOREIGN KEY (family_id) REFERENCES languages.family (family_id);

-- check the extra column has appeared
select * from languages.spoken_language_info limit 10;

-- populate the column using the dimension table we created
update languages.spoken_language_info s, languages.family b
set s.family_id = b.family_id
where s.family = b.family_name;

-- check it is populated
select * from languages.spoken_language_info limit 10;

-- lets drop the original column now
alter table languages.spoken_language_info drop column family;

-- check everything is as expected
select * from languages.spoken_language_info limit 10;
select b.family_name, count(*) from languages.spoken_language_info s
inner join languages.family b on s.family_id = b.family_id
group by 1;

/*****************************************

We can now use from the menu, "database" -> "reverse engineer" in order to generate the ERM.

*****************************************/

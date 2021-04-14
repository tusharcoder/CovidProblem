import sqlite3

#initialize the db
connection = sqlite3.connect("covid.db")

#initialize the bed data
#create user table
sql = """ 
create table IF NOT EXISTS user
(
    id INTEGER 
            constraint user_pk
                        primary key autoincrement,
                            name varchar(512) not null
                            );

"""

connection.execute(sql)



#create bed table
sql = """ 
create table IF NOT EXISTS bed
(
    id INTEGER
            constraint bed_pk
                        primary key autoincrement,
                            type_of_bed varchar(128) not null,
                                is_occupied boolean default 0,
                                    user INTEGER
                                            constraint bed_user_id_fk
                                                        references user
                                                                        on update set null on delete set null
                                                                        );
                            
"""
connection.execute(sql)

statement = """
    INSERT INTO bed(id,type_of_bed,is_occupied) 
    VALUES({},'{}',{})
"""

data = (
        (0, "general", 0),
        (2, "general", 0),
        (4, "general", 0),
        (1, "semi-private", 0),
        (5, "semi-private", 0),
        (9, "semi-private", 0),
        (3, "private", 0),
        (7, "private", 0),
        (11, "private", 0),
        )

for rec in data:
    i = connection.execute(statement.format(*rec))
    print(i)



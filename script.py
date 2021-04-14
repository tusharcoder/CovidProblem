import sqlite3
import click

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
    try:
        i = connection.execute(statement.format(*rec))
    except:
        pass

@click.group()
def cli():
    pass

@cli.command()
def assign_bed():
    """Assign a bed to the patient, \n
    inputs: \n
        name - name of the patient,\n
        bed_number - bed numbers choosen by the patient\n
    """
    name_of_patient=click.prompt("Enter the name of the patient")
    click.echo(click.style("Kindly select type of the bed",bold=True),nl=True)
    click.echo("0 for general, 1 for semi-private, 2 for private",nl=True)
    type_of_bed = int(click.prompt("bed type:"))

    sql = """
    SELECT * FROM bed where {}
    """
    mapping = {
                0:"general",
                1:"semi-private",
                2:"private",
           }
    if type_of_bed > 2 or type_of_bed < 0:
        click.echo(click.style("Invalid option for type_of_bed, valied options are 0/1/2",fg="red"))
        exit()
    else:
        condition  = "type_of_bed = '{}'".format(mapping.get(type_of_bed))
    sql=sql.format(condition)
    cursor = connection.cursor()
    cursor.execute(sql)
    beds = cursor.fetchall()
    click.echo(click.style("bedno bedtype status",bold=True))
    for bed in beds:
        click.echo("{} {} {}".format(bed[0],bed[1],"occupied" if bed[2] else "empty"),nl=True)
    bed_number = int(click.prompt("enter bed number"))
    sql = "SELECT is_occupied FROM bed where id=?"
    cursor = connection.cursor()
    cursor.execute(sql,(bed_number,))
    try:
        rec = cursor.fetchone()
        is_occupied = rec[0]
    except Exception as e:
        click.echo(e)
    if is_occupied:
        click.echo(click.style("Already occupied cannot be assigned",fg="red"))
        exit()

    sql = "INSERT INTO user(name) values(?)"
    cursor.execute(sql,(name_of_patient,))
    connection.commit()
    user_id = cursor.lastrowid
    sql = "UPDATE bed SET user=?, is_occupied=1 where id=?"
    cursor.execute(sql,(user_id,bed_number))
    connection.commit()
    click.echo(click.style("Patient {} assigned a bed number {}".format(name_of_patient,bed_number),fg="green"))


@cli.command()
@click.option("--type_of_bed",'-t',default=3,help="type of the bed, 3 is default")
def list_beds(type_of_bed):
    """Lists the beds which are free or occupied\n
       inputs:
        type_of_bed -\n 
            enter 0 for general,\n
            enter 1 for semi-private,\n
            enter 2 for private,\n
            enter 3 for all,\n
    """
    sql = """
    SELECT * FROM bed where {}
    """
    mapping = {
                0:"general",
                1:"semi-private",
                2:"private",
                3:1
           }
    if type_of_bed == 3:
        condition = 1
    elif type_of_bed > 3:
        click.echo(click.style("Invalid option for type_of_bed, valied options are 0/1/2/3",fg="red"))
        exit()
    else:
        condition  = "type_of_bed = '{}'".format(mapping.get(type_of_bed))
    sql=sql.format(condition)
    cursor = connection.cursor()
    cursor.execute(sql)
    beds = cursor.fetchall()
    click.echo(click.style("bedno bedtype status",bold=True))
    for bed in beds:
        click.echo("{} {} {}".format(bed[0],bed[1],"occupied" if bed[2] else "empty"),nl=True)


@cli.command()
@click.option("--type_of_bed",'-t',default=3,help="type of the bed, 3 is default")
def list_patients(type_of_bed):
    """
    list the patients which opt for the specific type of the bed\n
    inputs:\n
        type_of_bed - \n
            enter 0 for general,\n
            enter 1 for semi-private,\n
            enter 2 for private\n
    """
    sql = """
    SELECT b.id, b.type_of_bed, u.name, u.id FROM bed b inner join user u on b.user=u.id where {}
    """
    mapping = {
                0:"general",
                1:"semi-private",
                2:"private",
                3:1
           }
    if type_of_bed == 3:
        condition = 1
    elif type_of_bed > 3:
        click.echo(click.style("Invalid option for type_of_bed, valied options are 0/1/2/3",fg="red"))
        exit()
    else:
        condition  = "b.type_of_bed = '{}'".format(mapping.get(type_of_bed))
    sql=sql.format(condition)
    cursor = connection.cursor()
    cursor.execute(sql)
    beds = cursor.fetchall()
    click.echo(click.style("bedno bedtype patient_name",bold=True))
    for bed in beds:
        click.echo("{} {} {} {}".format(bed[0],bed[1], bed[2], bed[3]),nl=True)
    if not beds:
        click.echo(click.style("No Patients assigned",fg="red"))
    

@cli.command()
@click.option("--patient_id","-p")
def patient_checkout(patient_id):
    """
    patient checkout
    free the occupied bed
    input: bed_number
    """
    if patient_id is None:
        click.echo(click.style("patiend id is required. See help for usage",fg="red"))
        exit()
    sql = "SELECT * FROM bed WHERE user=?"
    cursor = connection.cursor()
    cursor.execute(sql,(patient_id,))
    try:
        row = cursor.fetchone()[0]
        bed_number = row.id
    except:
        click.echo(click.style("Invalid patient Id or patient already released",fg="red"))
        exit()
    sql = "UPDATE bed SET user=?,is_occupied=0 where id=?"
    cursor.execute(sql,(None,bed_number))
    connection.commit()
    click.echo(click.style("patient discharged and bed number {} is free now for admit another patient",fg="green"))



if __name__ == "__main__":
    cli()

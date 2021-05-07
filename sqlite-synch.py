#!/usr/bin/python
# https://stackoverflow.com/questions/80801/how-can-i-merge-many-sqlite-databases

import sys, sqlite3

def getTables(master):
    db = sqlite3.connect(master)
    tables = []
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    for table in cursor.fetchall():
        tables.append(table[0])
    cursor.close()
    return tables

def merge_table(master, slave, table_name):
    db_a = sqlite3.connect(master)
    db_b = sqlite3.connect(slave)
    cursor_a = db_a.cursor()
    cursor_b = db_a.cursor()
    
    new_table_name = table_name + "_new"
    
    non_null = lambda x: "" if x is None else x
    
    try:
        cursor_a.execute(f"CREATE TABLE IF NOT EXISTS {new_table_name} AS SELECT * FROM {table_name}")
        for row in cursor_b.execute(f"SELECT * FROM {table_name}"):
            
            ls = map(non_null,row)   
            row1 = tuple(ls)
            cursor_a.execute("INSERT INTO " + new_table_name + " VALUES" + str(row1) +";")

        cursor_a.execute("DROP TABLE IF EXISTS " + table_name);
        cursor_a.execute("ALTER TABLE " + new_table_name + " RENAME TO " + table_name);
        db_a.commit()

        print(f"\n\nTable:{table_name} Merged Successfully!\n")

    except sqlite3.OperationalError:
        print(sqlite3.OperationalError.__cause__)
        print("ERROR!: Merge Failed")
        cursor_a.execute("DROP TABLE IF EXISTS " + new_table_name);

    finally:
        cursor_a.close()
        cursor_b.close()

    return

def mergeAll(master, slave):
    tables = getTables(master)
    #for table in tables:
    #   merge_table(master,slave,table)
    merge_table(master,slave,'CUSTOMER')
    

if __name__ == '__main__':
    
    '''
    if(len(sys.argv)!=3)
        return
    master = sys.argv[1]
    slave = sys.argv[2]
    '''
    master = 'C:/DB/1.db'
    slave  = 'C:/DB/2.db'
    mergeAll(master,slave)

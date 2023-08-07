from connectors import Connector

conector = Connector("""test""")

"""connection = conector.sqlserver_connect()"""

"""cs = connection.sqlite_connect("C:/Users/lakhdar.belkharroubi/Desktop/sqlite.db")

cs.execute("select * fcurom Users")

l = cs.fetchall()

for r in l:
    print(r)"""

"""cs = connection.sqlserver_connect(
    driver="ODBC Driver 17 for SQL Server",
    server="10.92.1.18\MSSQLSERVERI03",
    database="ProsesKontrolNMT",
    user="sa",
    password="Tos2014hiba",
    )

l = cs.execute("select * from auth_user").fetchall()
for r in l:
    print(r) """


"""connection = connection.mysql_mariadb_connect("localhost", "testdb", "root",  "Lakhdar8301450", 3310)
print(connection)
cs = connection.cursor()

cs.execute("select * from playersc")

l = cs.fetchall()

for r in l:
    print(r)"""


"""cs =  connection.postgresql_connect("127.0.0.1", "postdb", "postgres", "khadero94")

cs.execute("select * from users")
l= cs.fetchall()

for r in l:

    print(r)"""
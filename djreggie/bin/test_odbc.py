from djzbar.settings import MSSQL_EARL
import pyodbc

cnxn = pyodbc.connect(MSSQL_EARL)
jenzabarUserID=""
userID = jenzabarUserID.encode("utf-8")
sql = "SELECT * FROM fwk_user WHERE id='%s'" % userID
print sql
cursor = cnxn.cursor()
cursor.execute(sql)
row = cursor.fetchone()
print row

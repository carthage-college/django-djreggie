from djzbar.settings import MSSQL_EARL
import pyodbc
cnxn = pyodbc.connect(MSSQL_EARL)
jenzabarUserID="73CAB7B5-D774-4600-9941-851A9C3303CA"
userID = jenzabarUserID.encode("utf-8")
sql = "SELECT * FROM fwk_user WHERE id='%s'" % userID
print sql
cursor = cnxn.cursor()
cursor.execute(sql)
row = cursor.fetchone()
print row

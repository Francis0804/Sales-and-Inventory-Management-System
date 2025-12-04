"""Project package init.

Install pymysql as a MySQLdb shim so Django can use PyMySQL as the MySQL driver.
This keeps compatibility with code that expects MySQLdb.
"""
try:
	import pymysql
	pymysql.install_as_MySQLdb()
except Exception:
	# If pymysql is not available, importing will fail later when Django tries to connect.
	pass

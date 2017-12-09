import pymysql

def cursorConexao():
	connection = pymysql.connect(host='localhost',user='root',password='danilo11',db='justica_estadual',charset='utf8', autocommit = True)
	return connection.cursor()

if __name__ == '__main__':
	pass

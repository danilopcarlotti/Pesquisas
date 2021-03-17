import pymysql


def cursorConexao():
    connection = pymysql.connect(
        host="", user="", password="", db="", charset="utf8", autocommit=True
    )
    return connection.cursor()


if __name__ == "__main__":
    pass

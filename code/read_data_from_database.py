import pymysql
pymysql.install_as_MySQLdb()

# Database connection settings
mydb = pymysql.connect(
    host="localhost", user="tahir", password="Password123#@!", database="logistic"
)
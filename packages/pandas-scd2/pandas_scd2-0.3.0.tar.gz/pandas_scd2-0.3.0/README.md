# pandas_scd

  

executing slowly changing dimension type 2

supported databases: 
 - postgresql
 - mysql
 - mariadb
 - sqlite
 - mssql



## Installation  
basic installtion :
 
    pip install pandas-scd2 

contain *'pandas', 'SQLAlchemy'*

for databases other than sqlite:

    pip install pandas-scd2['{database}']
database options:

*mysql
postgres
mariadb
mssql
all*

## Getting started
 

    from pandas_scd import SCD2
    from  sqlalchemy  import  create_engine
    
    source_table = 'my_source_table'
    dim_table = 'my_dim_table'
    key = 'id'
    columns = ['first_name', 'last_name']
    engine = sqlalchemy.create_engine("mariadb+pymysql://user:pass@hostname/dbname")

    SCD2(source_table, dim_table, key, columns, engine)


**source_table:** name of the table with the new source

**dim_table:** name of the dim table to apply scd2

**key:** the key to identify a row in the dim/source (the column type in the database must be of type Int)

**tracked_columns:** list of columns to check is any update occurred

**connection:** sqlalchemy connection engine

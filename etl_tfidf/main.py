'''
description: This script is the main program to run the etl process,
                from mySQL to redis. 

'''

from ETL import ETL

def main():
    etl = ETL()
    etl.run()
    

if __name__ == '__main__':
    main()
    print( 'main ... end.' )

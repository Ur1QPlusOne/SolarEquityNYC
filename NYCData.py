import requests
import json
import sqlite3
import os

def dataConsolidator(cur, conn, zipList, zipTrue = False):
    '''
        pseudocode until we have specific values

        for every filter:
            que api for data
            load into dict
            run through dict and scrape property value, other columns, etc, put into tuple/dict/list
            add ^ to db and sort

    '''
    api = 'https://data.cityofnewyork.us/resource/8y4t-faws.json'
    cur.execute('''
                CREATE TABLE IF NOT EXISTS nycdata (
                    zip_code INTEGER,
                    avg_mv FLOAT,
                    avg_sqft FLOAT
                )
            ''')
    for zipp in zipList:
        r = requests.get(f"{api}?$limit=25&zip_code={str(zipp[0])}")
        dataList = r.json()
        
        avgMv = 0
        avgSqft = 0
        cnt = 0
        for i in dataList:
            parid = i['parid']
            zip_code = i['zip_code']
            b_class = i['bldg_class']
            sqrft = i['gross_sqft']
            marketValue = i['curmkttot']

            #print(f"[{parid}, {zip_code}, {marketValue}, {sqrft}, {b_class}]")
            cnt += 1
            avgMv += int(marketValue)
            avgSqft += int(sqrft)

        if cnt == 0:
            avgSqft = 0
            avgMv = 0
        else:
            avgSqft /= cnt
            avgMv /= cnt
        cur.execute(f'''
                    INSERT INTO nycdata (zip_code,avg_mv,avg_sqft)
                    VALUES ({zipp[0]},{avgMv},{avgSqft})
                    ''')
            
    return 'Done'
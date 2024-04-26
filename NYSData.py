import requests
import sqlite3
import json

def nys_dataConsolidator(zips, cur, conn):
    url = f"https://data.ny.gov/resource/3x8r-34rs.json"
    r = requests.get(url)
    data = r.json()
    
    zipList = []
    for code in zips:
            zipList.append(int(code[0]))
    
    inDict = {}
    for i in range(len(zipList)):
        url = f"https://data.ny.gov/resource/3x8r-34rs.json"
        r = requests.get(f"{url}?$limit=25&zip_code={zipList[i]}")
        data = r.json()
        inDict[zipList[i]] = []
        for item in data:
            if int(item['zip_code']) == zipList[i]:
                project_number = item['project_number']
                city = item['city']
                project_cost = item['project_cost']
                if 'total_nyserda_incentive' in item:
                    total_nyserda_incentive = item['total_nyserda_incentive']
                else:
                    total_nyserda_incentive = 0
                temp = [zipList[i], project_number,city,project_cost,total_nyserda_incentive]
                inDict[zipList[i]].append(temp)
        if inDict[zipList[i]] == []:
            inDict[zipList[i]] = [[zipList[i],'0','n/a','0','0']]
    return inDict

def add_to_database(inDict, cur, conn):
    ret = []
    cur.execute('''
                CREATE TABLE IF NOT EXISTS nys_avg (
                    zip_code INTEGER,
                    solar_projects FLOAT,
                    avg_cost FLOAT,
                    avg_incentive FLOAT
                )
            ''')
    for key,value in inDict.items():
        ret.append(value)
        cost = 0
        incentive = 0
        for i in range(len(value)):
            cost += float(value[i][3])
            incentive += float(value[i][4])
        avg_cost = cost/len(value)
        avg_incentive = incentive/len(value)
        rows = cur.execute('''SELECT COUNT(*) FROM nys_avg''')
        rows = rows.fetchall()[0][0]
        cur.execute(f'''INSERT INTO nys_avg (zip_code, solar_projects, avg_cost, avg_incentive)
                        VALUES({key}, {len(value)}, {avg_cost}, {avg_incentive})''')
    conn.commit()


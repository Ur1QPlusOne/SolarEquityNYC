import os
import sqlite3
import matplotlib.pyplot as plt

def plot_all_graphs_combined(cur, conn, inDict, bList):
    
    cur.execute('''
        SELECT nys_avg.zip_code, nys_avg.avg_cost, nys_avg.avg_incentive, nycdata.avg_mv
        FROM nys_avg 
        LEFT JOIN nycdata ON nys_avg.zip_code = nycdata.zip_code
        GROUP BY nys_avg.zip_code
        ORDER BY nycdata.avg_mv DESC
    ''')
    result = cur.fetchall()

    # Fetch data
    value_data = []
    cost_data = []
    incentive_data = []
    for i in result:
        value_data.append((i[0],i[3]))
        cost_data.append((i[0],i[1]))
        incentive_data.append((i[0],i[2]))

    # Create one figure with three subplots
    plt.figure(figsize=(10, 2))

    # Plot Average Property Value
    plt.subplot(1, 3, 1)  # 3 rows, 1 column, subplot 1
    for row in value_data:
        if int(row[0]) in bList:
            plt.barh(str(row[0]), row[1])
    plt.xlabel('Average Property Value')
    plt.ylabel('Zip Code')
    plt.title('Average Property Value by Zip Code')
    plt.xticks(rotation=45, fontsize = 7)

    # Plot Average Project Cost
    plt.subplot(1, 3, 2)  # 3 rows, 1 column, subplot 2
    for row in cost_data:
        if int(row[0]) in bList:
            plt.barh(str(row[0]), row[1])
    plt.xlabel('Average Project Cost')
    plt.ylabel('Zip Code')
    plt.title('Average Project Cost by Zip Code')
    plt.xticks(rotation=45, fontsize = 7)

    # Plot Average NYSERDA Incentive
    plt.subplot(1, 3, 3)  # 3 rows, 1 column, subplot 3
    for row in incentive_data:
        if int(row[0]) in bList:
            plt.barh(str(row[0]), row[1])
    plt.xlabel('Average NYSERDA Incentive Value')
    plt.ylabel('Zip Code')
    plt.title('Average NYSERDA Incentive by Zip Code')
    plt.xticks(rotation=45, fontsize = 7) 

    for key,value in inDict.items():
        cost = 0
        incentive = 0
        for i in value:
            cost += float(i[3])
            incentive += float(i[4])
        with open(f"NYC_Data.txt", "a") as file:
            file.write(f"In {key}, out of {len(value)} projects:\n")
            file.write(f"    {cost} was the total cost and the total incentives were {incentive}.\n")
            file.write(f"    So, the average cost is {cost/len(value)} and the average incentive is {incentive/len(value)}.\n\n\n")
            
    # Adjust layout and show plot
    plt.tight_layout()
    plt.show()
import GoogleMaps as g
import NYCData as c
import NYSData as s
import Visualize as v


''' —— Run File 5 Times —— '''
# If it's giving a zip list error, delete the NYC_Data.db and timesran.txt
# The code works but every time you run the file it selects a borough (hence run 5 times)
# So if you run it a 6th, then it returns nothing since each borough was already iterated through


''' ————  GMaps Data  ———— '''
# Make SQL database
dbTup = g.make_database('NYC_Data')
# Check how many times file has been run to select a new borough
codes = g.getZips()
# Selecting zip codes and pulling coordinates
temp = g.convertZip(codes, dbTup[0],dbTup[1])

print("GMaps data done")

''' ————  City Data  ———— '''
# Inputs average property value and square footage for each of the zip codes into database
c.dataConsolidator(dbTup[0],dbTup[1], temp)

print("City data done")

''' ————  State Data  ———— '''
# Pulls 25 project's solar cost and incentive per zip code
temp1 = s.nys_dataConsolidator(temp, dbTup[0],dbTup[1])
# Inserts into database
s.add_to_database(temp1, dbTup[0],dbTup[1])

print("State data done")

''' ————  Visualization  ———— '''
# Makes a subplot with three graphs for the borough being ran this iteration (also writes calculation)
v.plot_all_graphs_combined(dbTup[0],dbTup[1], temp1, codes)

print("Completed")
import pandas as pd
import math
import csv
import numpy as np

#data = "C:/ST/Analysis/sensordata/sensortile/2023-04-16 08_48_02stile.csv"
data ="C:/Users/mahak/Desktop/BTP-2/Working/rawdata/IIIT_trail1_sun/sensordata/sensortile/2023-04-16 08_48_02stile.csv"
import pandas as pd

# Define the expected number of columns in the CSV file
expected_columns = 12

# Initialize an empty list to store valid lines
lines = []

# Open the CSV file and read each line
with open(data) as f:
    for i, line in enumerate(f):
        # Skip the first row (header)
        if i == 0:
            continue
        # Split the line into fields
        fields = line.strip().split(',')
        # Check if the line has the expected number of fields
        if len(fields) == expected_columns:
            # Append the line to the list of valid lines
            lines.append(fields)
        elif len(fields) > expected_columns:
            # If there are too many fields, take the first n fields and skip the rest
            lines.append(fields[:expected_columns])
        else:
            # If there are too few fields, skip the line
            continue

# Read the CSV file using pandas
data = pd.DataFrame(lines, columns=['time', 'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z', 'mag_x', 'mag_y', 'mag_z', 'pressure', 'label'])
data = data[:5051]
# set window size and initialize variables
window_size = 50
current_label = 0
current_rows = []


print(data.shape)


i=0
j=0

#print(data[['accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z', 'mag_x', 'mag_y', 'mag_z']])

#exit()
#main_np = np.empty((0,9*window_size), int)
main_np = np.empty((0, 9*window_size))
#print(len(main_np[0]))
while i < len(data)-window_size:
    row=data.iloc[i]
    current_label = row['label']
    for j in range(i,i+window_size):
        #print(j)
        if data.loc[j, 'label'] != current_label:
            print("mismatch of labels at ",i," and ",j," for label ",current_label)
            i=j
            break
    print(i,"/",len(data))
    if i != j:
        temp_df=data[i:i+window_size]
        temp_np=temp_df[['accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z', 'mag_x', 'mag_y', 'mag_z']].values
        #print(temp_np)
        temp_np=np.reshape(temp_np, 9*window_size, order='F')
        print("----------------------------------------------------------")
        #print(temp_np)
        temp_np=np.append(temp_np,[current_label])
        if len(main_np)==0:
            #print("hit")
            main_np=temp_np
        else:
            print(main_np)
            print(main_np.shape)
            print(temp_np.shape)
            main_np = np.vstack([main_np, temp_np])
        i=i+window_size
print(main_np)
#print(type(main_np))
print(main_np.shape)
#main_np.tofile('resized_data.csv', sep=',')

with open('resized_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for row in main_np:
        writer.writerow(row)
exit()
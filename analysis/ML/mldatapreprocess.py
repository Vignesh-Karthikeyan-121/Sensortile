import pandas as pd
import math
import csv
import numpy as np

#data = "C:/ST/Analysis/sensordata/sensortile/2023-04-16 08_48_02stile.csv"

import pandas as pd
data = pd.read_csv("ML_Data_with_Timestamps (1).csv")

i=1
j=1
len_data = len(data)
window_size=50
#print(data[['accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z', 'mag_x', 'mag_y', 'mag_z']])

#exit()
# main_np = []
# print(type(main_np))
import numpy as np
main_np = np.empty((0,9*window_size), int)
count = 0
while i < len_data - window_size:
    row = data.iloc[i]
    current_label = row['labels']
    current_stamp = row['Timestamp']

    for j in range(i,i+window_size):
        #print(j)
        if data.loc[j, 'labels'] != current_label:
            print("mismatch of labels at ", i , " and ", j , " for label ", current_label)
            count = count + 1
            i=j
            break
    # print(i,"/",len(data))
    if i != j: # i.e. if the window sized block all entries have the same labels.
        temp_df = data[i:i+window_size]
        temp_np = temp_df[['acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'mag_x', 'mag_y', 'mag_z']].values
        #print(temp_np)
        temp_np = np.reshape(temp_np, 9*window_size, order='F')
        # print("----------------------------------------------------------")
        #print(temp_np)
        temp_np = np.append([current_stamp],temp_np)

        temp_np = np.append(temp_np,[current_label])
        final_time_row=data.iloc[j]
        temp_np = np.append(temp_np,final_time_row['Timestamp'])

        if len(main_np)==0:
            #print("hit")
            main_np = temp_np
        else:
            # print(main_np)
            # print(main_np.shape)
            # print(temp_np.shape)
            main_np = np.vstack([main_np, temp_np])
        i=i+window_size
print(count)
print(type(main_np))
#print(type(main_np))
print(main_np.shape)
#main_np.tofile('resized_data.csv', sep=',')

with open('ML_data_with_450features_with_Timestamps.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for row in main_np:
        writer.writerow(row)
exit()
from os import walk, path
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas
from mpl_toolkits.mplot3d import Axes3D


# This plots data from CISS

matplotlib.use('TkAgg')

filter_window_size = 25
filter_standard_deviation = 5



directory = "/Users/thomasgarry/Downloads/sesame-0000000000000003/Measurements/Spectrometer-0"
average_over = 100

existing = []
for (dirpath, dirnames, filenames) in walk(directory):
    existing.extend(filenames)
    break
existing = [x for x in existing if (".JSON" in x)]


existing_names = [int(file[-18: -5]) for file in existing]
number_name = list(zip(existing_names, existing))
number_name.sort()
#
# newFile = open("export.csv", "w")

# export_parameter_list = [
#             "year",
#             "month",
#             "day",
#             "day_of_week",
#             "hour",
#             "minute",
#             "second",
#             "system_temp_hundredths",
#             "detector_temp_hundredths",
#             "humidity_hundredths",
# ]
y = {}
z = {}

print(number_name)

def smooth_plot(df):
    smooth = df.mean(axis=1).rolling(
        window=filter_window_size, win_type='gaussian', center=True
    ).mean(std=filter_standard_deviation)
    # print(smooth)
    return smooth

for count, i in enumerate(number_name):
    print(count)
    with open(path.join(directory,(i[1])), "r") as this_file:
        this_json = json.loads(this_file.read())

        if count%average_over == 0:
            z[int(count/average_over)] = ([int(len) for len in this_json["intensity"][0:this_json["length"]]])
            y[int(count/average_over)] = ([int(len) for len in this_json["wavelength"][0:this_json["length"]]])
            # break
        else:
            for colcount, col in enumerate(z[int(count/average_over)]):
                z[int(count/average_over)][colcount] += this_json["intensity"][colcount]
    if count % average_over == average_over-1 or count == len(number_name)-1:
        z[int(count/average_over)] = smooth_plot(pandas.DataFrame(z[int(count/average_over)]))
        # print(z[int(count/average_over)])
print(y)
print(z)


fig = plt.figure()
ax = fig.add_subplot(111)
names = []
for i in z:
    Y = np.array(y[i])
    Z = np.array(z[i])
    ax.plot(Y, Z)
    names.append(i)

ax.legend(names)
plt.show()
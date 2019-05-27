from os import walk, path
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.mplot3d import Axes3D


# This plots data from CISS

matplotlib.use('TkAgg')

directory = "/Users/thomasgarry/Downloads/sesame-0000000000000003/Measurements/Spectrometer-0"
average_over = 500

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

sum_of_values = []
for count, i in enumerate(number_name):
    print(count)
    with open(path.join(directory,(i[1])), "r") as this_file:
        this_json = json.loads(this_file.read())


        sum_of_values.append(sum(this_json["intensity"]))


fig = plt.figure()
ax = fig.add_subplot(111)


Y = np.array(sum_of_values)
X = np.array(range(0,len(sum_of_values)))
ax.plot(X,Y)

# ax.legend(names)
plt.show()
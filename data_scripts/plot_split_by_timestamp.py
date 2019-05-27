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

# filter_window_size = 10
# filter_standard_deviation = 2

timestamps = [1558788490757, 1558794833457, 1558794854130, 1558794876402, 1558794897076, 1558794919334, 1558794941604, 1558794962266, 1558794984540, 1558795005220, 1558795027472, 1558795049740, 1558795070418, 1558795092685, 1558795113354, 1558795135621, 1558795157892, 1558795178575, 1558795200843, 1558795223108, 1558795243777, 1558795266042, 1558795286717, 1558795308978, 1558795331258, 1558795351921, 1558795374190, 1558795383735, 1558795412372, 1558795444181, 1558795480761, 1558795517347, 1558795549158, 1558795582559, 1558795617556, 1558795652543, 1558795689126, 1558795725709, 1558795765469, 1558795806833, 1558795860912, 1558795907036, 1558795962713, 1558796023155, 1558796093132, 1558796169482, 1558796247431, 1558796325373, 1558796401709, 1558796470082, 1558796543237, 1558796616383, 1558796689546, 1558796762724, 1558796834296, 1558796905874, 1558796967918, 1558797033132, 1558797095189, 1558797152445, 1558797217674, 1558797276524, 1558797329022, 1558797381515, 1558797432410, 1558797481715, 1558797535805, 1558797585120, 1558797632837, 1558797685337, 1558797737824, 1558797790315, 1558797836439, 1558797882555, 1558797927095, 1558797973216, 1558798022517, 1558798067052, 1558798111578, 1558798162473, 1558798211780, 1558798265854, 1558798316744, 1558798366037, 1558798415344, 1558798472605, 1558798536238, 1558798598257, 1558798661886, 1558798725498, 1558798790706, 1558798855926, 1558798927500, 1558798994286, 1558799059493, 1558799121512, 1558799178761, 1558799232839, 1558799280552, 1558799331462, 1558799380766, 1558799423711, 1558799471429, 1558799509604, 1558799546189, 1558799582770, 1558799622535, 1558799660708, 1558799694116, 1558799738655, 1558799781608, 1558799819793, 1558799857961, 1558799899311, 1558799935889, 1558799970877, 1558800005863, 1558800056755, 1558800091730, 1558800125123, 1558800158521, 1558800196697, 1558800228506, 1558800263486, 1558800293713, 1558800323946, 1558800365300, 1558800403468, 1558800425728, 1558800446392, 1558800467053, 1558800489320, 1558800509986, 1558800532253, 1558800552919, 1558800573583, 1558800595842, 1558800616517, 1558800637179, 1558800659436, 1558800680115, 1558800700782, 1558800723045, 1558800743715, 1558800764387, 1558800786651, 1558800807324]


directory = "/Users/thomasgarry/Documents/University/Project_Work/results_and_readings/sesame-0000000000000004/Measurements/Spectrometer-0"

existing = []
for (dirpath, dirnames, filenames) in walk(directory):
    existing.extend(filenames)
    break
existing = [x for x in existing if (".JSON" in x)]


existing_names = [int(file[-18: -5]) for file in existing]
number_name = list(zip(existing_names, existing))
number_name.sort()

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

for count1, stamp in enumerate(timestamps):
    print(count1)
    if stamp == timestamps[-1]:
        break
    turn = False
    mean_count = 0
    for count, i in enumerate(number_name):
        if i[0] > stamp and i[0] < timestamps[count1+1]:
            with open(path.join(directory,(i[1])), "r") as this_file:
                this_json = json.loads(this_file.read())
                if turn == False:
                    turn = True
                    z[stamp] = ([int(len) for len in this_json["intensity"][0:this_json["length"]]])
                    y[stamp] = ([int(len) for len in this_json["wavelength"][0:this_json["length"]]])
                    mean_count+=1
                    # break
                else:
                    mean_count += 1
                    for colcount, col in enumerate(z[stamp]):
                        z[stamp][colcount] += this_json["intensity"][colcount]


    z[stamp] = smooth_plot(pandas.DataFrame(z[stamp]))
    z[stamp] = z[stamp] / mean_count
                # print(z[int(count/average_over)])
print(y)
print(z)


fig = plt.figure(figsize=(10,6))
ax = fig.add_subplot(111)
names = []

fig.suptitle("\nMean Spectra Per Layer, for 'Print 2'", fontsize=16)

ax.set_ylabel("Sample Mean Reading")
ax.set_xlabel("Wavelength / nm")


index_list = [0, 52, 53, 54, 55, 100, 101, 102]

for count, i in enumerate(z):
    if count not in index_list:
        continue
    Y = np.array(y[i])
    Z = np.array(z[i])
    ax.plot(Y, Z)
    names.append("Mean spectrum for Layer {} \nat timestamp: {}".format(count, i))

ax.legend(names)
plt.show()
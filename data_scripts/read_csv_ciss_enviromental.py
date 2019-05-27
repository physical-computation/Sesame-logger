import pandas
import matplotlib
import matplotlib.pyplot as plt
import datetime
from os import walk, path
import matplotlib.dates as mdates
from scipy.stats import mode
import numpy


# This plots the enviromental data from ciss for an entire folder, and removes noise from the readings.  This has
# only been tested with data from the sesame-004 repo (private).

# TODO  This is extremely messy, needs some parts breaking out into fucntions (but it works)

matplotlib.use('TkAgg')


filter_window_size = 200
filter_standard_deviation = 20



def smooth_plot(series):
    smooth = series.rolling(
        window=filter_window_size, win_type='gaussian', center=True
    ).mean(std=filter_standard_deviation)
    return smooth


# directory = "/Users/thomasgarry/Downloads/sesame-0000000000000003/Measurements/CISS-0"
directory = "/Users/thomasgarry/Documents/University/Project_Work/results_and_readings/sesame-0000000000000004/Measurements/CISS-0"

existing = []
for (dirpath, dirnames, filenames) in walk(directory):
    existing.extend(filenames)
    break
existing = [x for x in existing if (".csv" in x)]


frames = []
for file in existing:
    frames.append(
        pandas.read_csv(
            path.join(directory, file),
            skiprows=1, usecols=[1, 2, 3, 4, 11, 12, 13], names=["timestamp", "ax", "ay", "az", "temp", "pres", "humi"]
        )
    )

df = pandas.concat(frames)

# df['time'] = pandas.to_datetime(df['timestamp'], unit="ms")

df['time'] = pandas.to_datetime(df['timestamp'].astype(int),unit="ms")








# directory = "/Users/thomasgarry/Downloads/sesame-0000000000000003/Measurements/CISS-0"
directory2 = "/Users/thomasgarry/Documents/University/Project_Work/results_and_readings/sesame-0000000000000004/Measurements/CISS-1"

existing2 = []
for (dirpath, dirnames, filenames) in walk(directory2):
    existing2.extend(filenames)
    break
existing2 = [x for x in existing2 if (".csv" in x)]


frames2 = []
for file in existing2:
    frames2.append(
        pandas.read_csv(
            path.join(directory2, file),
            skiprows=1, usecols=[1, 2, 3, 4, 11, 12, 13], names=["timestamp", "ax", "ay", "az", "temp", "pres", "humi"]
        )
    )

df2 = pandas.concat(frames2)

# df['time'] = pandas.to_datetime(df['timestamp'], unit="ms")

df2['time'] = pandas.to_datetime(df2['timestamp'].astype(int),unit="ms")








# df['time_from_start'] = pandas.to_timedelta(
#     [n - df['timestamp'][1] for n in df['timestamp']],
#     unit="ms"
# )

# time_from_start = datetime.timedelta(milliseconds=(timestamp - t0))

# matplotlib.use('MacOSX')

# df["ax"] = df["ax"].astype(int)
# df["ay"] = df["ay"].astype(int)
# df["az"] = df["az"].astype(int)


# ax = plt.gca()
tfig, tax = plt.subplots(3,sharex=True, figsize=(10,6))

tfig.autofmt_xdate()

tax[0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
tax[0].set_ylabel("Temperature \n/ Degrees C")

tax[1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
tax[1].set_ylabel("Pressure / mbar")

tax[2].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
tax[2].set_ylabel("Humidity / %")

tfig.suptitle('Enviromental Readings During Print', fontsize=16)



# df.plot(x="time", y="ax", ax=tax)
# df.plot(x="time", y="ay", ax=tax)
# df.plot(x="time", y="az", ax=tax)
# df.plot(x="time", y="temp", ax=tax)


df_temp = df.dropna(subset=['temp'])
df_pres = df.dropna(subset=['pres'])
df_humi = df.dropna(subset=['humi'])

print(df_temp)
print(df_pres)
print(df_humi)

df_temp = df_temp[numpy.abs(df_temp.temp - df_temp.temp.mean())<=(0.5*df_temp.temp.std())]

df_pres = df_pres[numpy.abs(df_pres.pres - df_pres.pres.mean())<=(0.5*df_pres.pres.std())]

df_humi = df_humi[df_humi.humi > 15]
df_humi = df_humi[(numpy.abs(df_humi.humi - df_humi.humi.mean())<=(2*df_humi.humi.std()))]
df_humi = df.dropna(subset=['humi'])
df_humi = df_humi.reset_index(drop=True)






df_humi = df_humi.sort_values('timestamp')
df_humi = df_humi.reset_index(drop=True)
going = True
i = 0
indices = []
while (going):
    length = len(df_humi)
    start = i * 40
    end = i * 40 + 39
    if end > len(df_humi):
        going = False
        end = int(len(df_humi))

    series = df_humi.loc[start:end]
    series.humi = series.humi.apply(lambda x: int(x))
    series = series.humi[series.humi != series.humi.mode()[0]]

    indices.extend(series.index.values.tolist())
    i = i + 1

df_humi = df_humi.drop(indices[:-2])

df_humi = df_humi[df_humi.humi > 10]


df_pres = df_pres.sort_values('timestamp')
df_pres.pres = smooth_plot(df_pres.pres)


df_temp.plot(x="time", y="temp", ax=tax[0])
df_pres.plot(x="time", y="pres", ax=tax[1])
df_humi.plot(x="time", y="humi", ax=tax[2])



df2_temp = df2.dropna(subset=['temp'])
df2_pres = df2.dropna(subset=['pres'])
df2_humi = df2.dropna(subset=['humi'])

print(df2_temp)
print(df2_pres)
print(df2_humi)

df2_temp = df2_temp[numpy.abs(df2_temp.temp - df2_temp.temp.mean())<=(0.5*df2_temp.temp.std())]

df2_pres = df2_pres[numpy.abs(df2_pres.pres - df2_pres.pres.mean())<=(0.5*df2_pres.pres.std())]

df2_humi = df2_humi[df2_humi.humi > 15]
df2_humi = df2_humi[(numpy.abs(df2_humi.humi - df2_humi.humi.mean())<=(2*df2_humi.humi.std()))]
df2_humi = df2.dropna(subset=['humi'])


df2_humi = df2_humi.sort_values('timestamp')
df2_humi = df2_humi.reset_index(drop=True)
going = True
i=0
indices = []
while(going):
    length = len(df2_humi)
    start = i * 40
    end = i * 40 + 39
    if end > len(df2_humi):
        going = False
        end = int(len(df2_humi))

    series = df2_humi.loc[start:end]
    series.humi = series.humi.apply(lambda x: int(x))
    series = series.humi[series.humi != series.humi.mode()[0]]

    indices.extend(series.index.values.tolist())
    i = i + 1

df2_humi = df2_humi.drop(indices[:-2])

df2_humi = df2_humi[df2_humi.humi > 10]


df2_pres = df2_pres.sort_values('timestamp')
df2_pres.pres = smooth_plot(df2_pres.pres)

df2_temp.plot(x="time", y="temp", ax=tax[0])
df2_pres.plot(x="time", y="pres", ax=tax[1])
df2_humi.plot(x="time", y="humi", ax=tax[2])

tax[0].set_xlabel("Time")
tax[1].set_xlabel("Time")
tax[2].set_xlabel("Time")

# tax[0].get_legend().remove()
# tax[1].get_legend().remove()
# tax[2].get_legend().remove()


tax[0].legend(["Intake", 'Exhaust'])
tax[1].legend(["Intake", 'Exhaust'])
tax[2].legend(["Intake", 'Exhaust'])

# df.plot(x="time", y="pres", ax=tax, marker='o')







# df.plot(x="time", y="axg2", ax=ax)
# df.plot(x="time", y="axg4", ax=ax)

# df.plot(x="timestamp", y="pres", ax=ax, marker='o')
# df.plot(x="timestamp", y="ay")

# df.plot(x="timestamp", y="humi", ax=ax, marker='o')

plt.show()

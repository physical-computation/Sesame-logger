import pandas
import matplotlib
import matplotlib.pyplot as plt
import datetime
from os import walk, path
import matplotlib.dates as mdates
from scipy.stats import mode


matplotlib.use('TkAgg')


filter_window_size = 50
filter_standard_deviation = 5

# directory = "/Users/thomasgarry/Documents/University/Project_Work/results_and_readings/sesame-0000000000000004/Measurements/CISS-1"
directory = "/Users/thomasgarry/Downloads/sesame-0000000000000003/Measurements/CISS-0"

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
tax[0].set_ylabel("X Acceleration / g")

tax[1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
tax[1].set_ylabel("Y Acceleration / g")

tax[2].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
tax[2].set_ylabel("Z Acceleration / g")

tfig.suptitle('Accelerometer Readings During Print', fontsize=16)



# df.plot(x="time", y="ax", ax=tax)
# df.plot(x="time", y="ay", ax=tax)
# df.plot(x="time", y="az", ax=tax)
# df.plot(x="time", y="temp", ax=tax)


df = df.dropna(subset=['ax'])


df.plot(x="time", y="ax", ax=tax[0])
df.plot(x="time", y="ay", ax=tax[1])
df.plot(x="time", y="az", ax=tax[2])

tax[0].set_xlabel("Time")
tax[1].set_xlabel("Time")
tax[2].set_xlabel("Time")

tax[0].get_legend().remove()
tax[1].get_legend().remove()
tax[2].get_legend().remove()
# df.plot(x="time", y="pres", ax=tax, marker='o')







# df.plot(x="time", y="axg2", ax=ax)
# df.plot(x="time", y="axg4", ax=ax)

# df.plot(x="timestamp", y="pres", ax=ax, marker='o')
# df.plot(x="timestamp", y="ay")

# df.plot(x="timestamp", y="humi", ax=ax, marker='o')

plt.show()

print(df)
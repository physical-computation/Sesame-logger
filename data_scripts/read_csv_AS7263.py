import pandas
import matplotlib
import matplotlib.pyplot as plt
import datetime
from os import walk, path
import matplotlib.dates as mdates
from scipy.stats import mode


matplotlib.use('TkAgg')


# filter_window_size = 50
# filter_standard_deviation = 5

directory = "/Users/thomasgarry/Documents/University/Project_Work/results_and_readings/sesame-0000000000000004/Measurements/Warp-0"

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
            skiprows=0, usecols=[0, 1, 2, 3, 4, 5, 6], names=["timestamp", "1", "2", "3", "4", "5", "6"]
        )
    )

df = pandas.concat(frames)

# df['time'] = pandas.to_datetime(df['timestamp'], unit="ms")

df['time'] = pandas.to_datetime(df['timestamp'].astype(int),unit="ms")

df['sum'] = df["1"] + df["2"] + df["3"] + df["4"] + df["5"] + df["6"]



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
tfig, tax = plt.subplots(1, figsize=(10,6))

tfig.autofmt_xdate()

tax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
tax.set_ylabel("Cumulative sum")

tfig.suptitle('AS7263 Sum of all channels', fontsize=16)



# df.plot(x="time", y="ax", ax=tax)
# df.plot(x="time", y="ay", ax=tax)
# df.plot(x="time", y="az", ax=tax)
# df.plot(x="time", y="temp", ax=tax)


# df = df.dropna(subset=['ax'])


df.plot(x="time", y="sum", ax=tax)
# df.plot(x="time", y="ay", ax=tax[1])
# df.plot(x="time", y="az", ax=tax[2])

tax.set_xlabel("Time")
# tax[1].set_xlabel("Time")
# tax[2].set_xlabel("Time")

# df.plot(x="time", y="pres", ax=tax, marker='o')







# df.plot(x="time", y="axg2", ax=ax)
# df.plot(x="time", y="axg4", ax=ax)

# df.plot(x="timestamp", y="pres", ax=ax, marker='o')
# df.plot(x="timestamp", y="ay")

# df.plot(x="timestamp", y="humi", ax=ax, marker='o')

plt.show()

print(df)
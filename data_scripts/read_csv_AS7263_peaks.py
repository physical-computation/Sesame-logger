import pandas
import matplotlib
import matplotlib.pyplot as plt
import datetime
from os import walk, path
import matplotlib.dates as mdates
from scipy.stats import mode
from scipy.signal import find_peaks

# This reads data from the AS7263 / AS7262 spectrometers, (recorded by sesame_logger) with headings:
# "timestamp", "1", "2", "3", "4", "5", "6"
# This then sums the readings from each sample, and plots the results, along with peaks which are found using a
# combination of a gaussian smoothing operation, and the Scipy find_peaks function

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
df = df.sort_values(by=['timestamp'])
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
tfig, tax = plt.subplots(2, figsize=(10,6), sharex=True)

tfig.autofmt_xdate()

tax[0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
tax[1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
tax[0].set_ylabel("Cumulative sum")
tax[1].set_ylabel("Time Between Layers / s")

tfig.suptitle('AS7263 Sum of all channels', fontsize=16)



# df.plot(x="time", y="ax", ax=tax)
# df.plot(x="time", y="ay", ax=tax)
# df.plot(x="time", y="az", ax=tax)
# df.plot(x="time", y="temp", ax=tax)


# df = df.dropna(subset=['ax'])

filter_window_size = 5
filter_standard_deviation = 1



def smooth_plot(series):
    smooth = series.rolling(
        window=filter_window_size, win_type='gaussian', center=True
    ).mean(std=filter_standard_deviation)
    return smooth

df['smooth_sum'] = smooth_plot(df['sum'])

# peaks, _ = find_peaks(df['sum'], distance=10, prominence=9, threshold=3)
peaks, _ = find_peaks(df['smooth_sum'], distance=6, prominence=7, height=140)

# print(peaks)

df_peaks = df.iloc[peaks]


df.plot(x="time", y="sum", ax=tax[0])
df_peaks.plot(x="time", y="sum", ax=tax[0], alpha=1, marker='x', linewidth=0, markeredgecolor='black')

for count, peak in df_peaks.iterrows():
    print(peak['timestamp'])

print([peak['timestamp'] for count, peak in df_peaks.iterrows()])
# df.plot(x="time", y="smooth_sum", ax=tax[0])

time_diffs = [0]
for count, row in enumerate(df_peaks.iterrows()):
    if count+1 == len(peaks):
        break
    time_difference = df_peaks.iloc[count+1]['timestamp'] - df_peaks.iloc[count]['timestamp']
    time_difference = time_difference/1000
    time_diffs.append(time_difference)

# for i in time_diffs:
    # print(i)

df_peaks['time_diffs'] = time_diffs

# print(df_peaks)

df_peaks.plot(x="time", y="time_diffs", ax=tax[1], alpha=1)

# df.plot(x="time", y="ay", ax=tax[1])
# df.plot(x="time", y="az", ax=tax[2])

tax[0].set_xlabel("Time")
tax[1].set_xlabel("Time")
# tax[2].set_xlabel("Time")

tax[0].legend(["Cumulative Sum", "Peaks"])

tax[1].get_legend().remove()

# df.plot(x="time", y="pres", ax=tax, marker='o')







# df.plot(x="time", y="axg2", ax=ax)
# df.plot(x="time", y="axg4", ax=ax)

# df.plot(x="timestamp", y="pres", ax=ax, marker='o')
# df.plot(x="timestamp", y="ay")

# df.plot(x="timestamp", y="humi", ax=ax, marker='o')

plt.show()

# print(df)
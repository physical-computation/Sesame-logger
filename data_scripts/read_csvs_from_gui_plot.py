import pandas
import matplotlib
import matplotlib.pyplot as plt
import os

# This program takes a set of CSVs, and normalises them by the first in the list

# The first of these readings is the reference reading

matplotlib.use('TkAgg')
plt.style.use('seaborn-whitegrid')

files = [
    "/Users/thomasgarry/Documents/University/Project_Work/results_and_readings/60_samples_normal_window_test/paper.csv",
    # "/Users/thomasgarry/Documents/University/Project_Work/results_and_readings/60_samples_normal_window_test/foil.csv",
    "/Users/thomasgarry/Documents/University/Project_Work/results_and_readings/60_samples_normal_window_test/nylonpowder.csv",
    "/Users/thomasgarry/Documents/University/Project_Work/results_and_readings/60_samples_normal_window_test/pla.csv",
]

names = [
    "Paper",
    # "Foil",
    "Nylon Powder",
    "PLA"
]

filter_window_size = 10
filter_standard_deviation = 2
# filter_window_size = 1
# filter_standard_deviation = 2
output_to_csv = True

def read_file(file):
    df = pandas.read_csv(
        file,
        # skiprows=22, names=["wavelength", "sample"]
        skiprows=22, names=["wavelength", "absorbance", "reference", "sample"],
        usecols=["wavelength", "sample", "reference", "absorbance"]
    )

    df = df.set_index('wavelength')
    df['sample'] = df['sample'] / df['reference'].mean()

    df = df['sample'].to_frame()
    # df = df['absorbance'].to_frame()

    return df

def smooth_plot(df):
    # return df
    smooth = df.mean(axis=1).rolling(
        window=filter_window_size, win_type='gaussian', center=True
    ).mean(std=filter_standard_deviation)
    return smooth

# df.mean(axis=1).reset_index().plot(x='wavelength', y=0, ax=tax)

tfig, tax = plt.subplots(2, sharex=True, figsize=(10,6))

smoothed_data = []
for count, file in enumerate(files):
    print("here")
    df = read_file(file)
    smooth = smooth_plot(df)
    smooth.plot(ax=tax[0])
    smoothed_data.append(smooth)
tax[0].legend(names)

print(df)


names_normalised = []
for count, folder in enumerate(files):
    print(count)
    normalised = smoothed_data[count].div(smoothed_data[0])
    normalised.plot(ax=tax[1])
    names_normalised.append(
        "{} normalised by {} reading".format(names[count], names[0])
    )
tax[1].legend(names_normalised)


tax[0].set_ylabel("Direct Sample Reading")

tax[1].set_xlabel("wavelength / nm")
tax[1].set_ylabel("Reflectance (normalised with paper)")

print("here")

plt.show()
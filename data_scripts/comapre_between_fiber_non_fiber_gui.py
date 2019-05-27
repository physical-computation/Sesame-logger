import pandas
import matplotlib
import matplotlib.pyplot as plt
import os
import numpy

# This program takes the data from a bunch os CSVs as outputted by the NIRScan GUI
# and sums the readings (sample column) to obtain a smoother output.

# The first of these readings is the reference reading

matplotlib.use('TkAgg')
plt.style.use('seaborn-whitegrid')

enable_sd_normalise = True
enable_mean_normalise = True



folders = [
    "/Users/thomasgarry/Documents/University/Project_Work/results_and_readings/Initital_fiber_with_external_illumination_test/thick_feed_thin_reciever_printer_off_60_per_reading_paper_12v",
    # "/Users/thomasgarry/Documents/University/Project_Work/results_and_readings/Initital_fiber_with_external_illumination_test/thick_feed_thin_reciever_printer_off_60_per_reading_aluminium_foil_12v",
    "/Users/thomasgarry/Documents/University/Project_Work/results_and_readings/Initital_fiber_with_external_illumination_test/thick_feed_thin_reciever_printer_off_60_per_reading_nylon_12v",
    "/Users/thomasgarry/Documents/University/Project_Work/results_and_readings/Initital_fiber_with_external_illumination_test/thick_feed_thin_reciever_printer_off_60_per_reading_pla_12v",
]

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
csv_output_name = "combined_data.csv"

def average_folders(folder):
    files_in_folder = []
    for (dirpath, dirnames, filenames) in os.walk(os.path.join(folder)):
        files_in_folder.extend((filenames))
        # This doesn't include files in subfolders

    csv_files_in_folder = [x for x in files_in_folder if x.endswith(".csv") and not x==csv_output_name]

    pandas_data = []
    for file in csv_files_in_folder:
        csv_data = pandas.read_csv(
                os.path.join(folder, file),
                # skiprows=22, names=["wavelength", "sample"]
                skiprows=22, names=["wavelength", "absorbance", "reference", "sample"],
                usecols=["wavelength", "reference", "sample"]
            )
        csv_data
        csv_data['sample'] = csv_data['sample']/csv_data['reference'].mean()
        pandas_data.append((
            file,
            csv_data
        ))

    df = pandas_data[0][1].copy()
    df = df.set_index('wavelength')
    df = df['sample'].to_frame()
    for count, data in enumerate(pandas_data[1:]):
        df = df.join(data[1].set_index('wavelength')['sample'].to_frame(), rsuffix=str(count))
    return df

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
    smooth = df.mean(axis=1).rolling(
        window=filter_window_size, win_type='gaussian', center=True
    ).mean(std=filter_standard_deviation)
    smooth = smooth[numpy.logical_not(numpy.isnan(smooth))]
    return smooth

def normalise_plot(df):
    if enable_mean_normalise:
        df = (df - df.mean())
    if enable_sd_normalise:
        df = df / df.std()
    # df = (df - df.mean()) / df.std()
    return df

# df.mean(axis=1).reset_index().plot(x='wavelength', y=0, ax=tax)

tfig, tax = plt.subplots(1, sharex=True, figsize=(10,6))





smoothed_data = []
for count, file in enumerate(files):
    print("here")
    df = read_file(file)
    smooth = smooth_plot(df)
    # smooth.plot(ax=tax[0])
    smoothed_data.append(smooth)
# tax[0].legend(names)

stds = []
means = []
names_normalised = []
file_data = []
for count, folder in enumerate(files[1:]):
    count+=1
    print(count)
    normalised = smoothed_data[count].div(smoothed_data[0])
    # normalised = normalise_plot(normalised)
    stds.append(normalised.std())
    means.append(normalised.mean())
    normalised.plot(ax=tax)
    names_normalised.append(
        "Normalised {} direct reading".format(names[count], names[0])
    )
    file_data.append(normalised)
legend = []
legend.extend(names_normalised)







smoothed_data = []
for count, folder in enumerate(folders):
    print("here")
    df = average_folders(folder)
    smooth = smooth_plot(df)
    # smooth.plot(ax=tax[0])
    smoothed_data.append(smooth)
# tax[0].legend(names)

folder_data = []
names_normalised = []
for count, folder in enumerate(folders[1:]):
    count+=1
    print(count)
    normalised = smoothed_data[count].div(smoothed_data[0])
    # normalised = normalise_plot(normalised)
    if enable_sd_normalise:
        normalised = (normalised/normalised.std())*stds[count-1]
    if enable_mean_normalise:
        normalised = (normalised - normalised.mean()) + means[count - 1]

    normalised.plot(ax=tax)
    names_normalised.append(
        "Normalised {} fiber optic reading".format(names[count], names[0])
    )
    folder_data.append(normalised)
legend.extend(names_normalised)
tax.legend(legend)

print(file_data[0])
print(numpy.corrcoef(file_data[0],folder_data[0]))
print(numpy.corrcoef(file_data[1],folder_data[1]))



print("here")

tax.set_ylabel("Direct Sample Reading")

tax.set_xlabel("wavelength / nm")
tax.set_ylabel("Reflectance (normalised with paper)")

tax.set_title("Comparison of normalised data through the fiber optic transmission and illumination \nsystem, and a direct measurement from the spectrometer.")

plt.show()










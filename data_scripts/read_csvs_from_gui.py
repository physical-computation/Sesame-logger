import pandas
import matplotlib
import matplotlib.pyplot as plt
import os

# This program takes the data from multiple CSVs as outputted by the NIRScan GUI
# and sums the readings (sample column) to obtain a smoother output.


folder = "/Users/thomasgarry/Documents/University/Project_Work/results_and_readings/Initital_fiber_with_external_illumination_test/thick_feed_thin_reciever_printer_off_60_per_reading_aluminium_foil_12v"
filter_window_size = 25
filter_standard_deviation = 5
output_to_csv = True
csv_output_name = "combined_data.csv"


files_in_folder = []
for (dirpath, dirnames, filenames) in os.walk(os.path.join(folder)):
    files_in_folder.extend((filenames))
    # This doesn't include files in subfolders

csv_files_in_folder = [x for x in files_in_folder if x.endswith(".csv") and not x==csv_output_name]

pandas_data = []
for file in csv_files_in_folder:
    pandas_data.append((
        file,
        pandas.read_csv(
            os.path.join(folder, file),
            # skiprows=22, names=["wavelength", "sample"]
            skiprows=22, names=["wavelength", "absorbance", "reference", "sample"],
            usecols=["wavelength", "sample"]
        )
    ))


tfig, tax = plt.subplots(1)

if output_to_csv:
    output_csv_df = pandas_data[0][1].copy()
    output_csv_df = output_csv_df.set_index('wavelength')
    for count, data in enumerate(pandas_data):
        output_csv_df = output_csv_df.join(data[1].set_index('wavelength'), rsuffix=str(count))
    output_csv_df.to_csv(os.path.join(folder, csv_output_name))


df = pandas_data[0][1].copy()
df = df.set_index('wavelength')
for count, data in enumerate(pandas_data[1:]):
    df = df.join(data[1].set_index('wavelength'), rsuffix=str(count))
print(df.mean(axis=1))


# df.mean(axis=1).reset_index().plot(x='wavelength', y=0, ax=tax)


smooth = df.mean(axis=1).rolling(
    window=filter_window_size, win_type='gaussian', center=True
).mean(std=filter_standard_deviation)

smooth.plot()
plt.show()
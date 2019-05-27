import pandas
import matplotlib
import matplotlib.pyplot as plt
import os

# This program uses linear least squares to find the percentage of each Nylon and Talc, based on the input waveform.
# The first of these readings are the reference readings

matplotlib.use('TkAgg')
plt.style.use('seaborn-whitegrid')

pure_materials = {
    "100% Nylon": "/Users/thomasgarry/Documents/University/Project_Work/results_and_readings/impurities_spectrometer_readings/100p.csv",
    "100% Talc": "/Users/thomasgarry/Documents/University/Project_Work/results_and_readings/impurities_spectrometer_readings/100talc.csv",
}

mixtures = {
    "20% Nylon": "/Users/thomasgarry/Documents/University/Project_Work/results_and_readings/impurities_spectrometer_readings/20p.csv",
    "40% Nylon": "/Users/thomasgarry/Documents/University/Project_Work/results_and_readings/impurities_spectrometer_readings/40p.csv",
    "60% Nylon": "/Users/thomasgarry/Documents/University/Project_Work/results_and_readings/impurities_spectrometer_readings/60p.csv",
    "80% Nylon": "/Users/thomasgarry/Documents/University/Project_Work/results_and_readings/impurities_spectrometer_readings/80p.csv",
    "90% Nylon": "/Users/thomasgarry/Documents/University/Project_Work/results_and_readings/impurities_spectrometer_readings/90p.csv",
    "95% Nylon": "/Users/thomasgarry/Documents/University/Project_Work/results_and_readings/impurities_spectrometer_readings/95p.csv",
}

title = "Normalised Direct Sample Reading for Different Concentrations of Nylon12 and Talc Powder"
xlabel = "Wavelength / nm"
ylabel = "Normalised Sample"

enable_sd_normalise = True
enable_mean_normalise = False
enable_smoothing = False

accuracy = 10
subset_s = None
subset_e = None

filter_window_size = 25
filter_standard_deviation = 5
# filter_window_size = 5
# filter_standard_deviation = 1

def read_file(file):
    df = pandas.read_csv(
        file,
        # skiprows=22, names=["wavelength", "sample"]
        skiprows=22, names=["wavelength", "absorbance", "reference", "sample"],
        usecols=["wavelength", "absorbance", "reference", "sample"]
    )

    df = df.set_index('wavelength')

    # df['reflectance'] = df['sample']/df['reference']
    # df = (df['reflectance']).to_frame()

    df = (df['sample']).to_frame()

    # df = df.loc[1370:1420]
    # df = df.loc[1300:1420]
    return df

def smooth_plot(df):
    if not enable_smoothing:
        return df
    smooth = df.mean(axis=1).rolling(
        window=filter_window_size, win_type='gaussian', center=True
    ).mean(std=filter_standard_deviation)
    return smooth.to_frame()

def normalise_plot(df):
    if enable_mean_normalise:
        df = (df - df.mean())
    if enable_sd_normalise:
        df = df / df.std()
    # df = (df - df.mean()) / df.std()
    return df

# df.mean(axis=1).reset_index().plot(x='wavelength', y=0, ax=tax)

tfig, tax = plt.subplots(1, figsize=(10,6))
# print(tfig.figsize())

pure_materials_dfs = {}
for count, (name, file) in enumerate(pure_materials.items()):
    print(count, name, file)
    df = read_file(file)
    df_normalised = normalise_plot(df)
    smooth = smooth_plot(df_normalised)
    # smooth.plot(ax=tax)
    pure_materials_dfs[name] = smooth

percentage_list = []
for count, (name, file) in enumerate(dict(mixtures,**pure_materials).items()):
    # print(count, name, file)
    df = read_file(file)
    df_normalised = normalise_plot(df)
    smooth = smooth_plot(df_normalised)
    smooth.plot(ax=tax)
    # smoothed_data.append(smooth)
    difference = []
    for i in range(0,accuracy+1):
        percentage = (i) * pure_materials_dfs['100% Nylon'][subset_s:subset_e] + (accuracy-i) * pure_materials_dfs['100% Talc'][subset_s:subset_e]
        squares = (((smooth[subset_s:subset_e]*accuracy) - percentage) ** 2).sum()[0]
        difference.append(squares)
    percentage_calc = difference.index(min(difference))/(accuracy/100.0)
    print(name, "- Linear estimated concentration of nylon: {}%".format(percentage_calc))
    percentage_list.append(percentage_calc)
tax.legend([name for name in dict(mixtures,**pure_materials)])

tax.set_title(title)
tax.set_xlabel(xlabel)
tax.set_ylabel(ylabel)

print(percentage_list)

# names_normalised = []
# for count, folder in enumerate(files):
#     print(count)
#     normalised = smoothed_data[count].div(smoothed_data[0])
#     normalised.plot(ax=tax[1])
#     names_normalised.append(
#         "{} normalised by {} reading".format(names[count], names[0])
#     )
# tax[1].legend(names_normalised)

plt.show()
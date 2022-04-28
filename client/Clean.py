import glob
import pandas as pd
import warnings

warnings.simplefilter("ignore")

path = "/Users/timurmalik/Desktop/Tern/Tern"

file_list = glob.glob(path + "/*.xlsx")

excl_list = []

for file in file_list:
    excl_list.append(pd.read_excel(file))

excl_merged = pd.concat(excl_list, ignore_index=True)

excl_merged.to_excel('Merged Canadian Prices.xlsx', index=False)



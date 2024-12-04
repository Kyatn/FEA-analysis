import pandas as pd
import zipfile


def zip_read_withDate(folder, desired_date):
    df_list = []
    name_list = []
    with zipfile.ZipFile(folder) as zf:
        #desired_date = '06-Jun-2024'
        txt_files = zf.namelist()
        #txt_files = [info.filename for info in zf.infolist() if info.filename.endswith('.txt')]
        filtered_files = [k for k in txt_files if desired_date in k]
        name_list = filtered_files
        # Iterate over each text file
        #print(zf.filename)
        for filenames in filtered_files:
        # Open the text file
            with zf.open(filenames) as file:
                #dataframes.append([])
                # Read the file content into a pandas DataFrame
                df = pd.read_csv(file, encoding='latin-1', usecols=[0,1], skiprows=2) # this depends highly in the data we are dealing with
                new_column_names = df.iloc[1] 
                df.columns = new_column_names 
                df_list.append(df)
    return df_list, name_list

def zip_read(folder, cols):
    df_list = []
    name_list = []
    with zipfile.ZipFile(folder) as zf:
        txt_files = zf.namelist()
        #txt_files = [info.filename for info in zf.infolist() if info.filename.endswith('.txt')]
        name_list = txt_files
        # Iterate over each text file
        #print(zf.filename)
        for filenames in txt_files:
        # Open the text file
            with zf.open(filenames) as file:
                #dataframes.append([])
                # Read the file content into a pandas DataFrame
                df = pd.read_csv(file, sep=',', usecols = cols) #['timestamp','ch', 'VMON','IMON']) # this depends highly in the data we are dealing with
                new_column_names = df.iloc[1] 
                df.columns = new_column_names 
                df_list.append(df)
    return df_list, name_list
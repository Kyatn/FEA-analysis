from datetime import datetime
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import shutil
import pandas as pd


def org_file(folder, num_partitions):
    all_files = os.listdir(folder)
    sorted_files = sorted(all_files)
    partition_size = len(sorted_files) // num_partitions

    #divide = int(len(sorted_files)/num_partitions) # C1, C2, C3

    partitions = []
    for i in range(num_partitions):
        start_index = i * partition_size
        # Ensure the last partition gets any remaining files
        if i == num_partitions - 1:
            end_index = len(sorted_files)
        else:
            end_index = start_index + partition_size
        partitions.append(sorted_files[start_index:end_index])

    return partitions

def rename_file(folder, new_folder, new_path, file, format):
    for i in range(len(file)):
        new_folder_path = new_path + f'C{i+1}_{new_folder}'
        if os.path.exists(new_folder_path):  
            shutil.rmtree(new_folder_path)
            os.makedirs(new_folder_path)
        else:
            os.makedirs(new_folder_path)
        for filename in file[i]:
            df = pd.read_csv(os.path.join(folder,filename), sep=',', encoding='latin-1', usecols=[0,1], skiprows=2)
            new_column_names = df.iloc[1]
            df.columns = new_column_names
            string_time = str(df.iloc[0, 1])
            date_format = '%d-%b-%Y %H:%M:%S'
            date_time = datetime.strptime(string_time, date_format)
            if date_time.year == 2009:
                date_adj = date_time + relativedelta(years=15, months=3, days=16, hours=-2)
                date_str = date_adj.strftime('%Y-%m-%d_%H-%M-%S')
            else:
                date_str = date_time.strftime('%Y-%m-%d_%H-%M-%S')
            # Full path to the file
            file_path = os.path.join(folder, filename)
            #print(file_path)
        
            # Get the modification time of the file and convert it to a date format
            #mod_time = os.path.getmtime(file_path)
            #original_date = datetime.fromtimestamp(mod_time) + relativedelta(years=15, months=3, days=16, hours=-2)
            #date_str = original_date.strftime('%Y-%m-%d-%H-%M-%S.%f')
            #date_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d-%H-%M-%S.%f')
        
            # Create a new filename with the date
            new_filename = f"{date_str}{format}"  # Assuming the files are txt
        
            # Full path to the new file
            new_file_path = os.path.join(new_folder_path, new_filename)
            #print(new_file_path)

            # Rename the file
            shutil.copy(file_path, new_file_path) 
            #os.rename(file_path, new_file_path)
            #print(f"Renamed '{filename}' to '{new_filename}'")

        shutil.make_archive(new_folder_path, 'zip', new_folder_path)
        shutil.rmtree(new_folder_path)

        print("new folder is " + new_folder_path)


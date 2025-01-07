import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import schedule 
import time 
import os
import shutil
from zipfile import ZipFile

print("format of file name: <date>_<#FEAs><single/21x21>FEA_<vac/lxe> (e.g 231121_4singleTipFEA_vac)")
destination_folder = input("type the name of the directory to save the data in Xegpu and deepbox01: ")

folder_path1 = '/home/xenon/slowcontrol/datalogs/'
zip_path1 = '/home/xenon/slowcontrol/dataZip/datalogsZip'
folder_to_send1 = zip_path1 + ".zip"

folder_path2 = '/home/xenon/slowcontrol/datascope/'
zip_path2 = '/home/xenon/slowcontrol/dataZip/datascopeZip'
folder_to_send2 = zip_path2 + ".zip"

folder_path3 = '/home/xenon/slowcontrol/logs/'
zip_path3 = '/home/xenon/slowcontrol/dataZip/logsZip'
folder_to_send3 = zip_path3 + ".zip"


def sync():
    # Create a ZipFile Object
    #with ZipFile(zip_path, 'w') as zip_object:
    # Adding files that need to be zipped
    #    to_be_zipped = os.listdir(folder_path)
    #    for file in to_be_zipped:
    #        zip_object.write(folder_path + '/' + file)
    shutil.make_archive(zip_path1, format='zip', root_dir=folder_path1)
    shutil.make_archive(zip_path2, format='zip', root_dir=folder_path2)
    shutil.make_archive(zip_path3, format='zip', root_dir=folder_path3)

    os.system(f"rsync -Puav {folder_to_send1} xenon@xegpu:/mnt/xedisk02/FEA/{destination_folder}/")
    os.system(f"rsync -Puav {folder_to_send2} xenon@xegpu:/mnt/xedisk02/FEA/{destination_folder}/")
    os.system(f"rsync -Puav {folder_to_send3} xenon@xegpu:/mnt/xedisk02/FEA/{destination_folder}/")
    
    os.system(f"rsync -Puav {folder_to_send1} lxe_user@deepbox01:/raid0/FEA/FEA_data/{destination_folder}/")
    os.system(f"rsync -Puav {folder_to_send2} lxe_user@deepbox01:/raid0/FEA/FEA_data/{destination_folder}/")
    os.system(f"rsync -Puav {folder_to_send3} lxe_user@deepbox01:/raid0/FEA/FEA_data/{destination_folder}/")
    
    time_now = datetime.datetime.now()
    print(f"last time updated: {time_now}\n the path fot the folder is:\n deepbox01:/raid0/FEA/{destination_folder}\n xegpu:/mnt/xedisk02/FEA/{destination_folder}")

sync()
schedule.every(3).hours.do(sync)

while True:
    schedule.run_pending()
    time.sleep(1)


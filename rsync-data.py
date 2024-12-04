import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import schedule 
import time 
import os
import shutil
from zipfile import ZipFile

folder_path1 = '/home/xenon/slowcontrol/datalogs/'
zip_path1 = '/home/xenon/slowcontrol/dataZip/datalogsZip'

folder_path2 = '/home/xenon/slowcontrol/datascope/'
zip_path2 = '/home/xenon/slowcontrol/dataZip/datascopeZip'

folder_path3 = '/home/xenon/slowcontrol/logs/'
zip_path3 = '/home/xenon/slowcontrol/dataZip/logsZip'

def func():
    # Create a ZipFile Object
    #with ZipFile(zip_path, 'w') as zip_object:
    # Adding files that need to be zipped
    #    to_be_zipped = os.listdir(folder_path)
    #    for file in to_be_zipped:
    #        zip_object.write(folder_path + '/' + file)
    shutil.make_archive(zip_path1, format='zip', root_dir=folder_path1)
    shutil.make_archive(zip_path2, format='zip', root_dir=folder_path2)
    shutil.make_archive(zip_path3, format='zip', root_dir=folder_path3)
    os.system(f"rsync -Puav  {zip_path1} xenon@xegpu:/mnt/xedisk02/FEA/240827_4FEA_vac/")
    os.system(f"rsync -Puav {zip_path2} xenon@xegpu:/mnt/xedisk02/FEA/240827_4FEA_vac/")
    os.system(f"rsync -Puav {zip_path3} xenon@xegpu:/mnt/xedisk02/FEA/240827_4FEA_vac/")
    
    os.system(f"rsync -Puav  {zip_path1} caio@deepbox01:/raid0/caio/240827_4FEA_vac/")
    os.system(f"rsync -Puav {zip_path2} caio@deepbox01:/raid0/caio/240827_4FEA_vac/")
    os.system(f"rsync -Puav {zip_path3} caio@deepbox01:/raid0/caio/240827_4FEA_vac/")
    
    print(datetime.datetime.now())

func()
schedule.every(8).hours.do(func)

while True:
    schedule.run_pending()
    time.sleep(1)


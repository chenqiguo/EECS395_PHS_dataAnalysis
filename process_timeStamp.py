"""convert the unix time stamp to time, by Chenqi"""

import csv
import datetime

with open('rr_dataset_time.csv', 'w') as csvfile_w:
    csv_writer = csv.writer(csvfile_w)
    header_flag = True
    with open('rr_dataset.csv') as csvfile_r:
        csv_reader = csv.reader(csvfile_r)
        for row in csv_reader:
            if header_flag:
                csv_writer.writerow(row)
                header_flag = False
            else:
                [id,unix_timestamp,bpm,rr] = row
                time = str(datetime.datetime.fromtimestamp(int(unix_timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
                newRow = [id,time,bpm,rr]
                csv_writer.writerow(newRow)
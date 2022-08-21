import os
import csv

class Logger():
    def __init__(self,loss_list,log_dir,loss_plot_path):
        self.loss_plot_path=loss_plot_path
        try:
            os.mkdir(log_dir)
        except FileExistsError:
            pass
        try:
            os.mkdir(log_dir+"/model")
        except FileExistsError:
            pass
        self.loss_list = loss_list
        with open(loss_plot_path,'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file,fieldnames=loss_list)
            csv_writer.writeheader()
    def lossLog(self,loss_list):
        with open(self.loss_plot_path,'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file,fieldnames=self.loss_list)
            csv_writer.writerow(loss_list)
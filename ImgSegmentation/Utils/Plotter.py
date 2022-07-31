import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
class Plotter():
    def __init__(self,outputdir,loss_log_path,loss_plot_path,validation_output_path,outputcmap):
        try:
            os.mkdir(outputdir)
        except FileExistsError:
            pass
        self.outputdir=outputdir
        self.loss_log_path=loss_log_path
        self.loss_plot_path=loss_plot_path
        self.validation_output_path=validation_output_path
        self.outputcmap=outputcmap

    def loss_plotter(self):
        data =pd.read_csv(self.loss_log_path)
        plt.figure(figsize=(10,5))
        plt.title("Loss")
        for losses in list(data.columns.values.tolist()):
            plt.plot(data[losses],label=str(losses))
        plt.xlabel("iterations")
        plt.ylabel("Loss")
        plt.legend()  
        plt.savefig(self.loss_plot_path)
    def loss_live_plotter(self):
        def _animation(i):
            data=pd.read_csv(self.loss_log_path)
            plt.cla()
            plt.title("Loss")
            for losses in list(data.columns.values.tolist()):
                plt.plot(data[losses],label=str(losses))
            plt.xlabel("iterations")
            plt.ylabel("Loss")
            plt.legend()
        ani=FuncAnimation(plt.gcf(),_animation)
        plt.show()
    def im_live_plotter(self):
        def _animation(i):
            image=plt.imread(self.validation_output_path)
            plt.cla()
            plt.imshow(image) 
            plt.axis('off')
        ani=FuncAnimation(plt.gcf(),_animation)
        plt.show()
    def im_plot(self,image,val=True):
        plt.imshow(image,cmap=self.outputcmap)
        plt.axis('off')
        if val:
            plt.savefig(self.validation_output_path)
        else :
            plt.savefig(self.outputdir+"/Test_"+str(time.time())+".jpg")
if __name__ == "__main__":
    pl=Plotter("../outputs","../logs/log_loss.csv","../logs/loss_plot.png","../outputs/validation.jpg","gray")
    pl.loss_live_plotter()
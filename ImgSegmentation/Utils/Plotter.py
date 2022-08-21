import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
from torchvision.utils import save_image
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
        plt.clf()
    def loss_live_plotter(self):
        def _animation(i):
            data=pd.read_csv(self.loss_log_path)
            plt.cla()
            plt.title("Loss")
            for losses in list(data.columns.values.tolist()):
                plt.plot(data[losses][len(data[losses])-100:],label=str(losses))
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
    def im_plot(self,image,image2,val=True):
        plt.figure(figsize=(10,5))
        plt.subplot(1,2,1)
        plt.imshow(image.permute(1,2,0).cpu().detach().numpy(),cmap=self.outputcmap)
        plt.subplot(1,2,2)
        plt.imshow(image2.permute(1,2,0).cpu().detach().numpy(),cmap=self.outputcmap)
        plt.axis('off')
        t=time.time()
        if val:
            plt.savefig(self.validation_output_path+"_"+str(t)+".jpg")
        else :
            plt.savefig(self.outputdir+"/Test_P"+str(t)+".jpg")
        plt.clf()
        if val:
            save_image(image,self.validation_output_path)
        else :
            save_image(image,self.outputdir+"/Test_"+str(t)+".jpg")
if __name__ == "__main__":
    pl=Plotter("../../../outputs","../../../logs/log_loss.csv","../../../logs/loss_plot.png","../../../outputs/validation.jpg","gray")
    pl.loss_live_plotter()
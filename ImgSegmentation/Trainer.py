from Utils import DataLoader,Logger,Plotter
from Models import SegModel
import config
import torch
from tqdm import tqdm


def train():
    dataloader = DataLoader.dataloader(config.DATASET, config.IMG_DIR,config.MASK_DIR,config.BATCHSIZE,config.SHUFFLE,config.NUM_WORKERS)
    valdataloader = DataLoader.dataloader(config.DATASET,config.IMG_DIR,config.MASK_DIR,config.BATCHSIZE,config.SHUFFLE,config.NUM_WORKERS)
    model = SegModel.SegModel(config.IMCHANNELS,config.OUTCHANNELS,config.FILTERBASE,config.LOSS,config.OPTIMIZER,config.LR).to(config.DEVICE)
    logger=Logger.Logger(['Recon_loss', 'accuracy'],config.LOGDIR,config.LOG_LOSS_PATH)
    plotter=Plotter.Plotter(config.OUTPUTDIR,config.LOG_LOSS_PATH,config.LOSS_PLOT_PATH,config.VALIDATION_OUTPUT_PATH,config.OUTPUT_COLORMAP)
    if config.LOAD_MODEL != "":
        model.load_state_dict(torch.load(config.MODEL_LOG_PATH+'/'+config.LOAD_MODEL))
    model.train()

    try:
        epoch_last_loss=0
        tqdm_epoch =tqdm(range(config.EPOCHS))
        for epoch in tqdm_epoch :
            tqdm_minibatch = tqdm(dataloader)
            for i, (images, masks) in enumerate(tqdm_minibatch):
                model.train()
                model.zero_grad()
                outputs = model(images.to(config.DEVICE))
                loss = model.loss(outputs, masks.to(config.DEVICE))
                loss.backward()
                model.optimizer.step()
                log_dict={
                        'Recon_loss':loss.item(),
                        }
                logger.lossLog(log_dict)
                if i % config.SAMPLE_EVERY == 0:
                    sample=next(iter(valdataloader))
                    # print(sample[0].shape)
                    sample_output=model.test(sample[0].to(config.DEVICE))
                    # print(sample_output[0].squeeze(0).shape)
                    plotter.im_plot(sample_output[0].permute(1,2,0).cpu().detach().numpy())
                tqdm_minibatch.set_description(f'Iter: {i} Loss: {loss.item()}')
                epoch_last_loss=loss.item()
            tqdm_epoch.set_description(f'Epoch:{epoch} Loss:{epoch_last_loss}')
            if epoch % config.SAVE_EVERY == 0:
                torch.save(model.state_dict(),config.MODEL_LOG_PATH+ "/model_{}.pth".format(epoch))
                sample=next(iter(valdataloader))
                accuracy = 0
                for image, mask in sample[:50]:
                    model.eval()
                    accuracy += torch.sum(model.test(image.to(config.DEVICE))-mask.to(config.DEVICE), dim=1).item() * 100 / mask.shape[1]
                accuracy/=50
                log_dict={
                        'accuracy':accuracy,
                        }
                sample_output=model.test(sample[0].to(config.DEVICE))
                plotter.im_plot(sample_output[0].permute(1,2,0).cpu().detach().numpy(),False)
                plotter.loss_plotter()
    except KeyboardInterrupt:
        print("Epoch: {}, Iteration: {}, Loss: {}".format(epoch, i, loss.item()))
        torch.save(model.state_dict(),config.MODEL_LOG_PATH+ "/model_{}.pth".format(epoch))
if __name__ == '__main__':
    train()
    


        





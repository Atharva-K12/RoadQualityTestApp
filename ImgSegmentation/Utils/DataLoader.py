from . import Dataset
import torch 


def dataloader(datasetname,rtk_image_dir,rtk_mask_dir,batchsize,shuffle,num_workers):
    if datasetname == "RTK":
        dataset = Dataset.RTKDataset(rtk_image_dir, rtk_mask_dir)
    else:
        raise ValueError("Unknown dataset name: {}".format(datasetname))
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=batchsize, shuffle=shuffle, num_workers=num_workers)
    return dataloader

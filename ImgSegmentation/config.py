import torch.cuda as cuda
import torch

DEVICE=torch.device("cuda:0" if cuda.is_available() else "cpu")



IMG_DIR = "../../RTK_SemanticSegmentationGT_originalFrames"
# MASK_DIR = "../../RTK_SemanticSegmentationGT_NoColorMapMasks/RTK_SemanticSegmentationGT_NoColorMapMasks"
MASK_DIR= "../../RTK_SemanticSegmentationGT_coloredMasks"
DATASET='RTK'


# UNet
# NestedUNet
# R2U_Net
# AttU_Net
# R2AttU_Net          
        
MODEL = "R2U_Net"

BATCHSIZE=5
SHUFFLE=True
NUM_WORKERS=3

EPOCHS=5
SAVE_EVERY=1
SAMPLE_EVERY=10
LR=0.0001

OPTIMIZER='Adam'
LOSS='MSE'

LOAD_MODEL=""

FILTERBASE=64
IMGSIZE=64
IMCHANNELS=3
OUTCHANNELS=1
OUTPUT_COLORMAP="gist_rainbow"
VALIDATION_OUTPUT_PATH="../../outputs/validation.jpg"
LOGDIR='../../logs'
LOG_LOSS_PATH='../../logs/log_loss.csv'
LOSS_PLOT_PATH='../../logs/loss_plot.png'
OUTPUTDIR='../../outputs'
MODEL_LOG_PATH='../../logs/model'
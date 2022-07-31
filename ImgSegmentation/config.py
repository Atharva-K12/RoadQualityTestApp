import torch.cuda as cuda
import torch

DEVICE=torch.device("cuda:0" if cuda.is_available() else "cpu")



IMG_DIR = "../../RTK_SemanticSegmentationGT_originalFrames"
MASK_DIR = "../../RTK_SemanticSegmentationGT_NoColorMapMasks/RTK_SemanticSegmentationGT_NoColorMapMasks"

DATASET='RTK'

BATCHSIZE=1
SHUFFLE=True
NUM_WORKERS=0

EPOCHS=1
PRINT_EVERY=1
SAVE_EVERY=1
SAMPLE_EVERY=1
LR=0.001

OPTIMIZER='Adam'
LOSS='MSE'



FILTERBASE=32
IMGSIZE=256
IMCHANNELS=3
OUTCHANNELS=1
OUTPUT_COLORMAP="gray"
VALIDATION_OUTPUT_PATH="./outputs/validation.jpg"
LOGDIR='./logs'
LOG_LOSS_PATH='./logs/log_loss.csv'
LOSS_PLOT_PATH='./logs/loss_plot.png'
OUTPUTDIR='./outputs'
MODEL_LOG_PATH='./logs/model'
import torch.nn.functional as F
import torch.optim as optim
import torch.nn as nn
import torch

class conv_block(nn.Module):

    def __init__(self, in_ch, out_ch):
        super(conv_block, self).__init__()
        
        self.conv = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, kernel_size=3, stride=1, padding=1, bias=True),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_ch, out_ch, kernel_size=3, stride=1, padding=1, bias=True),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True))

    def forward(self, x):

        x = self.conv(x)
        return x


class up_conv(nn.Module):
    def __init__(self, in_ch, out_ch):
        super(up_conv, self).__init__()
        self.up = nn.Sequential(
            nn.Upsample(scale_factor=2),
            nn.Conv2d(in_ch, out_ch, kernel_size=3, stride=1, padding=1, bias=True),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True)
        )

    def forward(self, x):
        x = self.up(x)
        return x

class UNET(nn.Module):
    def __init__(self, in_ch=3, out_ch=1, filter_base=32):
        super(UNET, self).__init__()

        
        filters = [filter_base, filter_base * 2,filter_base* 4, filter_base * 8,filter_base* 16]
        
        self.Maxpool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.Maxpool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.Maxpool3 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.Maxpool4 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.Conv1 = conv_block(in_ch, filters[0])
        self.Conv2 = conv_block(filters[0], filters[1])
        self.Conv3 = conv_block(filters[1], filters[2])
        self.Conv4 = conv_block(filters[2], filters[3])
        self.Conv5 = conv_block(filters[3], filters[4])

        self.Up5 = up_conv(filters[4], filters[3])
        self.Up_conv5 = conv_block(filters[4], filters[3])

        self.Up4 = up_conv(filters[3], filters[2])
        self.Up_conv4 = conv_block(filters[3], filters[2])

        self.Up3 = up_conv(filters[2], filters[1])
        self.Up_conv3 = conv_block(filters[2], filters[1])

        self.Up2 = up_conv(filters[1], filters[0])
        self.Up_conv2 = conv_block(filters[1], filters[0])

        self.Conv = nn.Conv2d(filters[0], out_ch, kernel_size=1, stride=1, padding=0)


    def forward(self, x):

        e1 = self.Conv1(x)

        e2 = self.Maxpool1(e1)
        e2 = self.Conv2(e2)

        e3 = self.Maxpool2(e2)
        e3 = self.Conv3(e3)

        e4 = self.Maxpool3(e3)
        e4 = self.Conv4(e4)

        e5 = self.Maxpool4(e4)
        e5 = self.Conv5(e5)

        d5 = self.Up5(e5)
        d5 = torch.cat((e4, d5), dim=1)

        d5 = self.Up_conv5(d5)

        d4 = self.Up4(d5)
        d4 = torch.cat((e3, d4), dim=1)
        d4 = self.Up_conv4(d4)
        d3 = self.Up3(d4)
        d3 = torch.cat((e2, d3), dim=1)
        d3 = self.Up_conv3(d3)
        d2 = self.Up2(d3)
        d2 = torch.cat((e1, d2), dim=1)
        d2 = self.Up_conv2(d2)
        out = self.Conv(d2)
        return out

class SegModel(nn.Module):
    def __init__(self,in_ch=3, out_ch=1, filter_base=32,loss="MSE",optimizer="Adam",lr=0.001):
        super(SegModel, self).__init__()
        self.optimizer=optimizer
        self.select_loss=loss
        self.lr=lr
        self.unet = UNET(in_ch,out_ch,filter_base)
        self.optimizer = self.select_optimizer()
    def forward(self, x):
        return self.unet(x)
    def test(self,x):
        self.unet.eval()
        with torch.no_grad():
            out = self.unet(x)
        return out
    def loss(self, x, y):
        if self.select_loss == "MSE":
            return F.mse_loss(x, y)
        elif self.select_loss == "BCE":
            return F.binary_cross_entropy(x, y)
        elif self.select_loss == "BCEWithLogits":
            return F.binary_cross_entropy_with_logits(x, y)
        else :
            raise ValueError("Unknown loss: {}".format(self.loss))
    def select_optimizer(self):
        if self.optimizer == "Adam":
            return optim.Adam(self.unet.parameters(), lr=self.lr)
        elif self.optimizer == "SGD":
            return optim.SGD(self.unet.parameters(), lr=self.lr)
        else:
            raise ValueError("Unknown optimizer: {}".format(self.optimizer))
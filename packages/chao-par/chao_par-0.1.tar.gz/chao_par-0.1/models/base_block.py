import math

import torch
import torch.nn as nn
import torch.nn.init as init

import torch.nn.functional as F
from torch.nn.modules.batchnorm import _BatchNorm

from models.registry import CLASSIFIER


class BaseClassifier(nn.Module):

    def fresh_params(self, bn_wd):
        if bn_wd:
            return self.parameters()
        else:
            return self.named_parameters()

@CLASSIFIER.register("linear")
class LinearClassifier(BaseClassifier):
    def __init__(self, nattr, c_in, bn=False, pool='avg', scale=1):
        super().__init__()

        self.pool = pool
        if pool == 'avg':
            self.pool = nn.AdaptiveAvgPool2d(1)
        elif pool == 'max':
            self.pool = nn.AdaptiveMaxPool2d(1)

        self.logits = nn.Sequential(
            nn.Linear(c_in, nattr),
            nn.BatchNorm1d(nattr) if bn else nn.Identity()
        )


    def forward(self, feature, label=None):

        if len(feature.shape) > 2:  # for vit (bt, nattr, c)
            if len(feature.shape) == 3:
                bt, hw, c = feature.shape
                # NOTE ONLY USED FOR INPUT SIZE (256, 192)
                h = 16
                w = 12
                feature = feature.reshape(bt, h, w, c).permute(0, 3, 1, 2)

            feat = self.pool(feature).view(feature.size(0), -1)
        else:
            feat = feature

        x = self.logits(feat)
        return [x], feature



@CLASSIFIER.register("cosine")
class NormClassifier(BaseClassifier):
    def __init__(self, nattr, c_in, bn=False, pool='avg', scale=30):
        super().__init__()

        self.logits = nn.Parameter(torch.FloatTensor(nattr, c_in))

        stdv = 1. / math.sqrt(self.logits.data.size(1))
        self.logits.data.uniform_(-stdv, stdv)

        self.pool = pool
        if pool == 'avg':
            self.pool = nn.AdaptiveAvgPool2d(1)
        elif pool == 'max':
            self.pool = nn.AdaptiveMaxPool2d(1)

    def forward(self, feature, label=None):
        if len(feature.shape) > 2:
            feat = self.pool(feature).view(feature.size(0), -1)
        else:
            feat = feature

        feat_n = F.normalize(feat, dim=1)
        weight_n = F.normalize(self.logits, dim=1)
        x = torch.matmul(feat_n, weight_n.t())
        return [x], feat_n


def initialize_weights(module):
    for m in module.children():
        if isinstance(m, nn.Conv2d):
            n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
            m.weight.data.normal_(0, math.sqrt(2. / n))
        elif isinstance(m, _BatchNorm):
            m.weight.data.fill_(1)
            if m.bias is not None:
                m.bias.data.zero_()
        elif isinstance(m, nn.Linear):
            stdv = 1. / math.sqrt(m.weight.size(1))
            m.weight.data.uniform_(-stdv, stdv)


class FeatClassifier(nn.Module):

    def __init__(self, backbone, classifier, bn_wd=True):
        super(FeatClassifier, self).__init__()

        self.backbone = backbone
        self.classifier = classifier
        self.bn_wd = bn_wd

    def fresh_params(self):
        return self.classifier.fresh_params(self.bn_wd)

    def finetune_params(self):

        if self.bn_wd:
            return self.backbone.parameters()
        else:
            return self.backbone.named_parameters()

    def forward(self, x, label=None):
        feat_map = self.backbone(x)
        # for DeiT
        if isinstance(feat_map, tuple):
            # If it is, we keep both elements of the tuple
            class_feat_map = feat_map[0]
            dist_feat_map = feat_map[1]
            class_logits, class_feat = self.classifier(class_feat_map, label)
            dist_logits, dist_feat = self.classifier(dist_feat_map, label)
            # return the average of class_logits[0] and dist_logits[0],
            # and the concatenation of class_feat and dist_feat
            return [(class_logits[0] + dist_logits[0]) / 2], torch.cat([class_feat, dist_feat], dim=-1)
        else:
            logits, feat = self.classifier(feat_map, label)
            return logits, feat


'''这段代码定义了几个分类器类，这些分类器可以应用于各种深度学习任务，如行人属性识别。主要有以下几个类：

BaseClassifier：一个基础分类器类，继承自nn.Module，提供了一个用于获取参数的fresh_params方法。其它分类器可以继承该类以获得一些基本功能。

LinearClassifier：一个线性分类器，继承自BaseClassifier。这个分类器首先对输入特征进行池化操作（平均池化或最大池化），然后将池化后的特征通过一个线性层进行分类。
如果需要，可以在线性层之后添加一个批量归一化（Batch Normalization）层。

NormClassifier：一个基于余弦相似度的分类器，也继承自BaseClassifier。这个分类器首先对输入特征进行池化操作（平均池化或最大池化），然后对池化后的特征和分类器权重进行归一化。
最后，计算归一化后的特征和权重之间的点积作为分类结果。

initialize_weights：一个用于初始化权重的函数，适用于卷积层、批量归一化层和线性层。

FeatClassifier：一个特征分类器，继承自nn.Module。这个分类器接收一个预训练的backbone（用于特征提取）和一个分类器（如LinearClassifier或NormClassifier）。
在前向传播时，首先使用backbone提取输入图像的特征，然后将特征传递给分类器进行分类。这个类还提供了用于获取待优化参数的fresh_params和finetune_params方法。

这些类可以用于行人属性识别任务。你可以使用预训练的backbone（例如ResNet、VGG等）提取输入图像的特征，然后使用LinearClassifier或NormClassifier对特征进行分类。
通过组合这些类，可以构建一个端到端的行人属性识别模型。'''

'''这段代码定义了一个用于分类的神经网络模型，主要包含以下几个模块：

BaseClassifier：是所有分类器的基类，定义了一个方法fresh_params，用于返回模型参数。如果bn_wd为True，返回所有参数，否则返回带有名称的参数。

LinearClassifier：线性分类器，继承自BaseClassifier。它首先使用AdaptiveAvgPool2d或AdaptiveMaxPool2d对输入进行池化，然后通过一个线性层和一个可选的批量归一化层得到输出。

NormClassifier：归一化分类器，继承自BaseClassifier。它首先对输入进行池化，然后对池化后的特征和权重进行归一化，最后通过矩阵乘法得到输出。

FeatClassifier：特征分类器，包含一个骨干网络（backbone）和一个分类器（classifier）。它首先通过骨干网络对输入进行特征提取，然后将得到的特征输入到分类器中得到输出。此外，它定义了两个方法fresh_params和finetune_params，用于返回分类器和骨干网络的参数。

在这段代码中，LinearClassifier和NormClassifier都是行人属性分类器的候选模型，而FeatClassifier则是整合特征提取和分类两个步骤的完整模型。'''
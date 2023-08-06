import torch.nn as nn
import torch
import torch.nn.functional as F


class RDropLoss(nn.Module):
    '''R-Drop的Loss实现，官方项目：https://github.com/dropreg/R-Drop
    '''
    def __init__(self, ce_loss, alpha):
        super().__init__()
        self.alpha = alpha
        self.loss_sup = ce_loss
        self.loss_rdrop = nn.KLDivLoss(reduction='none')

    def forward(self, input: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        pred1, pred2 = input
        loss_sup = self.loss_sup(pred1, target) + self.loss_sup(pred2, target)

        loss_rdrop1 = self.loss_rdrop(F.log_softmax(pred1, dim=-1), F.softmax(pred2, dim=-1))
        loss_rdrop2 = self.loss_rdrop(F.log_softmax(pred2, dim=-1), F.softmax(pred1, dim=-1))
        return loss_sup + (torch.mean(loss_rdrop1 + loss_rdrop2) / 4) * self.alpha
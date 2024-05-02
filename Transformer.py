import os
import numpy as np
import torch
import torch.nn as nn
import tqdm
import matplotlib.pyplot as plt

from HelperFunction import _extractVideoFrames
from TransformerModel import TransformerModel
from VideoDataSetForModel import VideoDataSetForModel


# Train
def get_lr(optimizer):
    for param_group in optimizer.param_groups:
        return param_group['lr']


def run_epoch(model, dataloader, optim, device):
    total = 0.
    n = 0
    loss_hist = []

    model.train(True)
    print("Learning rate:", get_lr(optim))

    weighting = torch.tensor([1., 5., 5.]).to(device)
    loss_fct1 = nn.CrossEntropyLoss(weight=weighting, reduction='mean')

    with tqdm.tqdm(total=len(dataloader)) as pbar:
        for (frames, label) in dataloader:
            nB, nF, nC, nH, nW = frames.shape

            # Merge batch and frames dimension
            frames = frames.view(nB * nF, nC, nH, nW)
            frames = frames.to(device, dtype=torch.float32)

            # (F*B) X C x W X H
            class_vec = model(frames, nF)

            label = label.to(device, dtype=torch.long)

            loss1 = loss_fct1(class_vec.view(-1, 3), label.view(-1))
            loss = loss1

            # Take gradient step if training
            optim.zero_grad()
            loss.backward()
            optim.step()

            # Accumulate losses and compute baselines
            total += loss.item()
            n += 1
            loss_hist.append(loss.item())

            avg = np.mean(loss_hist[max(-len(loss_hist), -10):])

            # Show info on process bar
            pbar.set_postfix_str("{:.4f} / {:.4f} / {:.4f}".format(total / n, loss1.item(), avg))
            pbar.update()
    loss_hist = np.array(loss_hist)

    return (total / 1), loss_hist


def trainTransformer(train_dataSet, num_epochs, batch_size, parallel):
    np.random.seed(0)
    torch.manual_seed(0)

    # Device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if type(device) == type(list()):
        os.environ["CUDA_VISIBLE_DEVICES"] = ','.join(str(x) for x in device)
        device = "cuda"

    device = torch.device(device)
    print("Using device:", device)

    # Model
    model = TransformerModel(embedding_dim=1024, num_hidden_layers=16, attention_heads=16, intermediate_size=8192,
                             input_shape=(128, 128, 3))

    pytorch_total_params = sum(p.numel() for p in model.parameters())
    print('model name', model.__class__.__name__, "contains", pytorch_total_params, "parameters.")

    if parallel:
        model = nn.DataParallel(model)

    model.to(device)

    # DATA SETUP
    train_dataSet = VideoDataSetForModel(dataSet=train_dataSet, fullVideo=False)

    train_dataloader = torch.utils.data.DataLoader(train_dataSet, batch_size=batch_size, num_workers=0,
                                                   shuffle=True,
                                                   pin_memory=(device.type == "cuda"),
                                                   drop_last=True)

    dataloaders = {'train': train_dataloader}
    # len(dataloaders['train'])

    # Set up optimizer
    lr = 1e-5
    optim = torch.optim.AdamW(model.parameters(), lr=lr)
    lr_step_period = 1
    scheduler = torch.optim.lr_scheduler.StepLR(optim, lr_step_period)

    bestLoss = float("inf")

    for epoch in range(1, num_epochs + 1):
        print("Epoch {} / {}".format(epoch, num_epochs), flush=True)
        for phase in ['train']:  # , 'val']:
            print("Running on", phase)
            loss, _ = run_epoch(model, dataloaders[phase], optim, device)
            print('Loss =', loss)
            print()
        scheduler.step()

        # Save checkpoint
        save = {
            'epoch': epoch,
            'state_dict': model.state_dict(),
            'best_loss': bestLoss,
            'loss': loss,
            'opt_dict': optim.state_dict(),
            'scheduler_dict': scheduler.state_dict(),
        }
        if loss < bestLoss:
            print('new Best Version')
            torch.save(save, "best.pt")
            bestLoss = loss
        else:
            torch.save(save, "checkpoint_" + str(epoch) + ".pt")


# Test
def show_graph(label, predict):
    predict = predict.copy() + 0.5
    plt.plot(predict, label='predict')
    plt.plot(label, label='Label')
    plt.legend()
    plt.show()


def smooth(vec, window=5, rep=1):
    weight = torch.ones((1, 1, window)) / window
    for _ in range(rep):
        pad = int((window - 1) / 2)
        vec = vec.unsqueeze(0).unsqueeze(0)
        vec = torch.nn.functional.conv1d(vec, weight, bias=None, stride=1, padding=pad, dilation=1, groups=1).squeeze()
    return vec


def loadTransformerModel(path):
    best = torch.load(path, map_location="cpu")
    model = TransformerModel(embedding_dim=1024, num_hidden_layers=16, attention_heads=16, intermediate_size=8192,
                             input_shape=(128, 128, 3))
    model = torch.nn.DataParallel(model)
    model.load_state_dict(best['state_dict'])
    model.eval()
    return model


def GetLengthOfEachBet(predict, deleteLastHalfBet=False):
    lengthBet = []
    firstFrames = []
    lastFrames = []
    check = True

    for i in range(len(predict)):
        if predict[i] != 0:
            if check:
                firstFrames.append(i)
                check = False
            else:
                lastFrames.append(i)
                check = True

    if deleteLastHalfBet:
        # Delete the last half Bet
        if len(firstFrames) > len(lastFrames):
            predict[firstFrames[-1]] = 0
            firstFrames.pop()
        elif len(firstFrames) < len(lastFrames):
            predict[lastFrames[-1]] = 0
            lastFrames.pop()

    for i in range(len(firstFrames)):
        lengthBet.append(lastFrames[i] - firstFrames[i])

    return lengthBet, firstFrames, lastFrames


def testForOneVideo(model, frames, device):
    nB, nF, nC, nH, nW = frames.shape
    frames = torch.cat(([frames[i] for i in range(frames.size(0))]), dim=0)
    frames = frames.to(device, dtype=torch.float)

    class_vec = model(frames, nF).squeeze()

    class_diff = class_vec[:, 2] - class_vec[:, 1]

    smooth_vec = smooth(class_diff, window=5, rep=3).detach().numpy()

    # Get Peaks
    predict = np.zeros((len(smooth_vec)), np.int8)
    for i in range(len(smooth_vec)):
        if i == 0 or i == len(smooth_vec) - 1:
            continue
        if smooth_vec[i] < smooth_vec[i + 1] and smooth_vec[i] < smooth_vec[i - 1]:
            predict[i] = 1
        if smooth_vec[i] > smooth_vec[i + 1] and smooth_vec[i] > smooth_vec[i - 1]:
            predict[i] = 2

    # Get length of each bet
    lengthBet, firstFrames, lastFrames = GetLengthOfEachBet(predict, True)

    # Apply Threshold
    thr = max(lengthBet) * 0.35
    for i in range(len(lengthBet)):
        if thr > lengthBet[i]:
            predict[firstFrames[i]] = 0
            predict[lastFrames[i]] = 0

    return predict


def testTransformer(transformer_path, dataSet):
    device = 'cpu'
    device = torch.device(device)
    model = loadTransformerModel(transformer_path)

    dataSet = VideoDataSetForModel(dataSet=dataSet, fullVideo=True)
    dataloader = torch.utils.data.DataLoader(dataSet, batch_size=1, shuffle=False)
    trueFrames = 0
    trueTransitionFrames = 0
    trueESFrames = 0
    trueEDFrames = 0
    totalFrames = 0
    trueFrames2 = 0
    with tqdm.tqdm(total=len(dataloader)) as pbar:
        for frames, label in dataloader:
            predict = testForOneVideo(model, frames, device)
            label = label.squeeze().detach().numpy()

            totalFrames += len(label)
            for i in range(len(label)):
                if predict[i] == label[i]:
                    trueFrames += 1
                if predict[i] == 0 and label[i] == 0:
                    trueTransitionFrames += 1
                elif predict[i] == 1 and label[i] == 1:
                    trueEDFrames += 1
                elif predict[i] == 2 and label[i] == 2:
                    trueESFrames += 1

                if label[i] != 0:
                    if predict[i] == label[i]:
                        trueFrames2 += 1

            pbar.update()

    accuracy = (trueFrames / totalFrames) * 100
    print('Accuracy: ', accuracy)

    accuracy2 = (trueFrames2 / (2 * len(dataloader))) * 100
    print('Accuracy ES & ED: ', accuracy2)

    accuracyED = (trueEDFrames / len(dataloader)) * 100
    print('Accuracy ED: ', accuracyED)

    accuracyES = (trueESFrames / len(dataloader)) * 100
    print('Accuracy ES: ', accuracyES)

    accuracyTransition = (trueTransitionFrames / (totalFrames - len(dataloader) * 2)) * 100
    print('Accuracy Transition: ', accuracyTransition)


# Detect ES & ED Frame
def Detect_ESED_Frame(video_path, transformerModel, labels=None):
    device = 'cpu'
    device = torch.device(device)
    # Prepare Video
    frames = _extractVideoFrames(video_path)
    if frames is None:
        return None,None
    # (F,W,H,C) > F C W H
    frames = frames.transpose((3, 0, 1, 2))
    # Load video into np.array
    frames = frames.astype(np.float32)
    # Scale pixel values from 0-255 to 0-1
    frames /= 255.0

    frames = np.moveaxis(frames, 0, 1)
    p = 8
    frames = np.pad(frames, ((0, 0), (0, 0), (p, p), (p, p)), mode='constant', constant_values=0)

    frames = torch.from_numpy(frames)
    frames = frames.unsqueeze(0)

    predict = testForOneVideo(transformerModel, frames, device)

    lengthBet, firstFrames, lastFrames = GetLengthOfEachBet(predict, False)

    maxIDX = 0
    for i in range(1, len(lengthBet)):
        if lengthBet[maxIDX] <= lengthBet[i]:
            maxIDX = i

    frames = frames.squeeze()
    if predict[firstFrames[maxIDX]] == 1:
        ES_Frame_IMG = np.transpose(frames[firstFrames[maxIDX]], (1, 2, 0))
        ED_Frame_IMG = np.transpose(frames[lastFrames[maxIDX]], (1, 2, 0))
    else:
        ED_Frame_IMG = np.transpose(frames[firstFrames[maxIDX]], (1, 2, 0))
        ES_Frame_IMG = np.transpose(frames[lastFrames[maxIDX]], (1, 2, 0))

    # Show 4 Frames
    if labels is not None:
        print(firstFrames[maxIDX], lastFrames[maxIDX])
        TrueES_Frame = 0
        TrueED_Frame = 0
        for i in range(len(labels)):
            if labels[i] == 1:
                TrueES_Frame = np.transpose(frames[i], (1, 2, 0))
            elif labels[i] == 2:
                TrueED_Frame = np.transpose(frames[i], (1, 2, 0))

            fig, axes = plt.subplots(2, 2)

            axes[0][0].imshow(ES_Frame_IMG)
            axes[0][0].set_title('ES Pred')
            axes[0][0].axis('off')

            axes[0][1].imshow(TrueES_Frame)
            axes[0][1].set_title('ES True')
            axes[0][1].axis('off')

            axes[1][0].imshow(ED_Frame_IMG)
            axes[1][0].set_title('ED Pred')
            axes[1][0].axis('off')

            axes[1][1].imshow(TrueED_Frame)
            axes[1][1].set_title('ED True')
            axes[1][1].axis('off')

            plt.show()

    # Crop the padding added in train
    ES_Frame_IMG = ES_Frame_IMG.numpy()[8:-8, 8:-8, :]
    ED_Frame_IMG = ED_Frame_IMG.numpy()[8:-8, 8:-8, :]

    return ES_Frame_IMG, ED_Frame_IMG

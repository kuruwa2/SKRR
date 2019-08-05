import numpy as np
import os
import cv2
#import pandas as pd
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import random

def get_files(filename, num=50):
    X = np.array([])
    with open(filename) as f:
        f.readline()
        f.readline()
        b = f.readline()
        b = [float(x) for x in b.split(',')]
        l = len(b)
        X = np.append(X, b)
        for line in f:
            if line[0] == '0':
                a = [float(x) for x in line.split(',')]
                if len(a) == l:
                    X = np.append(X, a)
    X = X.reshape((np.shape(X)[0] // l, l))
    f.close()
    #X_outliers = np.random.uniform(low=0, high=0.2, size=(10, 14))
    if num != 50:
        X = X[np.random.choice(len(X), size=num, replace=False)]
    return X#, X_outliers

def OneClassSVM_train(data1, data2, ii):
    from sklearn import svm
    from sklearn import preprocessing

    len1 = len(data1)
    len2 = len(data2)
    trainSet = np.concatenate((data1, data2), axis=0)
    trainSet = preprocessing.scale(trainSet, axis=1)
    # print(trainSet)
    nus = np.linspace(0.01, 0.5, 50)
    gammas = np.linspace(0.05, 0.95, 19)
    error = 100
    for nui in nus:
        for gammai in gammas:
            clf = svm.OneClassSVM(nu=nui, kernel='rbf', gamma=gammai)
            clf.fit(trainSet)
            y_pred_train = clf.predict(trainSet)
            my_y = y_pred_train[:len1]
            ab_y = y_pred_train[len1:]
            #print(my_y)
            #print(ab_y)
            normal = trainSet[y_pred_train == 1]
            abnormal = trainSet[y_pred_train == -1]
            my_abnormal = len(my_y[my_y == -1])
            ab_normal = len(ab_y[ab_y == 1])
            #print(normal)
            #print(abnormal)
            #print(normal.shape)
            #print(abnormal.shape)
            #print("False Alarm:", my_abnormal / len(my_y))
            #print("False Positive:", ab_normal / len(ab_y))
            if my_abnormal / len(my_y) + ab_normal / len(ab_y) < error:
                error = my_abnormal / len(my_y) + ab_normal / len(ab_y)
                bestnu = nui
                bestgamma = gammai
                #print(nui, gammai)
    clf = svm.OneClassSVM(nu=bestnu, kernel='rbf', gamma=bestgamma, verbose=True)
    clf.fit(trainSet)
    y_pred_train = clf.predict(trainSet)
    my_y = y_pred_train[:len1]
    ab_y = y_pred_train[len1:]
    normal = trainSet[y_pred_train == 1]
    abnormal = trainSet[y_pred_train == -1]
    my_abnormal = len(my_y[my_y == -1])
    ab_normal = len(ab_y[ab_y == 1])
    #print(normal.shape)
    #print(abnormal.shape)
    print("False Alarm:", my_abnormal / len(my_y))
    print("False Positive:", ab_normal / len(ab_y))

    #plt.plot(normal[:, 1], normal[:, 2], 'bx')
    #plt.plot(abnormal[:, 1], abnormal[:, 2], 'ro')
    #plt.show()
    tsne = TSNE(n_components=2, init='pca', random_state=501)
    X_tsne = tsne.fit_transform(trainSet)
    x_min, x_max = X_tsne.min(0), X_tsne.max(0)
    X_norm = (X_tsne - x_min) / (x_max - x_min)
    plt.figure(figsize=(10, 10))
    for i in range(X_norm.shape[0]):
        if y_pred_train[i] == 1:
            plt.plot(X_norm[i, 0], X_norm[i, 1], 'bx')
        else:
            plt.plot(X_norm[i, 0], X_norm[i, 1], 'ro')
    plt.xticks([])
    plt.yticks([])
    plt.show()
    
    import pickle
    with open('save/Kuruwa'+str(ii)+'.pickle', 'wb') as f:
        pickle.dump(clf, f)


if __name__ == '__main__':
    train_dir = './account/Kuruwa'
    data = get_files(train_dir)
    adata = get_files('./ais3/notkuruwa.bin', 5)
    adata = np.concatenate((adata, get_files('./ais3/notKuruwa.txt', 5)), axis=0)
    adata = np.concatenate((adata, get_files('./ais3/notkuruwa2.bin', 5)), axis=0)
    OneClassSVM_train(data, adata, 0)
    '''for i in [6,8,10,12]:
        train_dir = './account/Kuruwa'+str(i)
        data = get_files(train_dir)
        l = len(data[0])
        #adata = np.random.uniform(low=0, high=0.2, size=(10, l))
        adata = get_files('./account/'+str(i), 4)
        adata = np.concatenate((adata, get_files('./account/yuan'+str(i), 4)), axis=0)
        adata = np.concatenate((adata, get_files('./account/skps2010'+str(i), 4)), axis=0)
        OneClassSVM_train(data, adata, i)'''

from train2 import get_files
import pickle
from sklearn import preprocessing
import numpy as np

from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import random

show = 2
def read_model(filename):
    with open(filename, 'rb') as f:
        clf2 = pickle.load(f)
    return clf2
clf2 = read_model('./save/Kuruwa.pickle')

trainSet = get_files('./account/Kuruwa')
len1 = len(trainSet)
l = len(trainSet[0])
adata = np.random.uniform(low=0, high=0.2, size=(12, l))

#adata = get_files('./account/6', 4)
#adata = np.concatenate((adata, get_files('./account/yuan6', 6)), axis=0)
#adata = np.concatenate((adata, get_files('./account/skps20106', 6)), axis=0)
trainSet = np.concatenate((trainSet, adata), axis=0)
trainSet = preprocessing.scale(trainSet, axis=1)
y_pred_train = clf2.predict(trainSet)
my_y = y_pred_train[:len1]
ab_y = y_pred_train[len1:]
normal = trainSet[y_pred_train == 1]
abnormal = trainSet[y_pred_train == -1]
my_abnormal = len(my_y[my_y == -1])
ab_normal = len(ab_y[ab_y == 1])
my_abnormal = len(my_y[my_y == -1])
ab_normal = len(ab_y[ab_y == 1])
print("False Alarm:", my_abnormal / len(my_y))
print("False Positive:", ab_normal / len(ab_y))

if show <= 1:
    user = ['Others', 'Me']
    array = [my_abnormal, len(
        my_y)-my_abnormal] if show == 1 else [len(my_y)-ab_normal, ab_normal]
    plt.pie(array, labels=[user[show]+'Failed Login',
                            user[show]+'Success Login'], autopct='%1.1f%%')
    plt.show()

if show == 2:
    my_s = trainSet[:len1][y_pred_train[:len1] == 1]
    my_f = trainSet[:len1][y_pred_train[:len1] == -1]
    ot_s = trainSet[len1:][y_pred_train[len1:] == 1]
    ot_f = trainSet[len1:][y_pred_train[len1:] == -1]

    tsne = TSNE(n_components=2).fit_transform(
        np.concatenate((my_s, my_f, ot_s, ot_f)))
    print(tsne.shape)

    ll1 = my_s.shape[0]
    ll2 = ll1+my_f.shape[0]
    ll3 = ll2+ot_s.shape[0]

    l1 = plt.scatter(tsne[:ll1, 0], tsne[:ll1, 1],
                        marker='o', color='g', label='Me (Success)')
    l2 = plt.scatter(tsne[ll1:ll2, 0], tsne[ll1:ll2, 1],
                        marker='o', color='r', label='Me (Failed)')
    l3 = plt.scatter(tsne[ll2:ll3, 0], tsne[ll2:ll3, 1],
                        marker='x', color='g', label='Others (Success)')
    l4 = plt.scatter(tsne[ll3:, 0], tsne[ll3:, 1],
                        marker='x', color='r', label='Others (Failed)')
    plt.legend(handles=[l1, l2, l3, l4])
    plt.show()

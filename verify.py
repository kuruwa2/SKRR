from train2 import get_files
import pickle
from sklearn import preprocessing

model_path='save/clf.pickle'

def read_model(filename):
    with open(filename, 'rb') as f:
        clf2 = pickle.load(f)
    return clf2

def verify(timestamps, account):
    model_path = f'save/{account}.pickle'
    n = [timestamps]
    n = preprocessing.scale(n, axis=1)
    print(n)
    svm = read_model(model_path)
    try:
        return svm.predict(n)
    except:
        return -1

if __name__ == '__main__':
    clf2 = read_model(model_path)
    #print(clf2)
    train_dir = './ais3/Noyou.txt'
    X = get_files(train_dir)
    #print(X)
    X = preprocessing.scale(X, axis=1)
    #print(X)
    print(clf2.predict(X))
    #print(verify('0.         ,0.06745252 ,0.06155861 ,0.16568435 ,0.03863785 ,0.04780616,0.06614276 ,0.12115259 ,0.05108055 ,0.05370007 ,0.05631958 ,0.1453831,0.06090373 ,0.06417813'))

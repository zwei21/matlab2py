import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

# Utils #
def concatenate(data):
    cdata = data[0]
    for i in range(1, len(data)):
        cdata = np.concatenate((cdata, data[i]), axis=1)
    return cdata

def clssifier(data, tail_size, eps=0.5, visual_flag=True):
    '''
    The data input should follow the Structure:
    data[index_of_traj][index_of_coord][index_of_point]
    '''
    # First Step: Take the data input, should consider the tail points
    data_tail = data[:,:,-tail_size:]
    X = concatenate(data_tail)
    # Second Step: apply DBSCAN and label all points
    clustering = DBSCAN(eps=eps, min_samples=2).fit(X.T)

    # Third Step: Assign label of points to its corresponding trajctory
    label=[]
    for i in range(1,len(X.T),tail_size): # This should be modified wrt length of lables and length of assigned dataset in DBSCAN
        label.append(clustering.labels_[i])
    counts = [label.count(i) for i in set(label)]
    print(set(label))
    print(counts)
    lgd_idx = [label.index(i) for i in set(label)]
    # Optional: Plot of the result
    if visual_flag:
        for i in lgd_idx:
            plt.plot(data[i][0],data[i][1], color="C{}".format(label[i]), label=str(label[i]))
            plt.legend()
        for i in range(len(data)):
            plt.plot(data[i][0], data[i][1], color="C{}".format(label[i]), alpha=0.2)
            
    return label


def pickOut(data, labels, cnum=2):
    '''
    data: data of generated trajs to be precocessed, containing the outliners
    labels: label of traj data, in num of trajs
    cnum: number of class to be saved in the output
        default=2
    return
    pData: picked data without outliners, only have the labels and data which is meaningful for next process
    pLabels: correspond labels of picked data
    '''
    assert len(data) == len(labels), "Data and Labels shoud have same dimension at axis 0"
    cls = list(set(labels)) # Given category of labels, defined as class of trajs
    pData = []
    pLabels = []
    for idc in range(cnum):
        for idx in range(len(labels)):
            if labels[idx] == idc:
                pData.append(data[idx])
                pLabels.append(labels[idx])
            else:
                continue
    #Debug
    print(len(pData), len(pLabels))
    return pData, pLabels


class Projector:
    def __init__(self, n_features, seeding_flag = True):
        self.iter_time = n_features
        self.coefficients = self.generator2()
        self.seeding_flag = seeding_flag

    def generator(self):
        a = np.random.uniform(-1,1) # [0,1) // a*cons1 + b*const2 a+b !~ uniform
        b = np.random.uniform(-1,1) # [0,1) * 2 -> [0,2) - 1 -> [-1,1)
        return a, b
    
    def generator2(self):
        random_seq = np.random.uniform(-1,1,2*self.iter_time)
        para_tuples = []
        for i in range(0, len(random_seq), 2):
            para_tuples.append([random_seq[i], random_seq[i+1]])
        return para_tuples
        

    def projection(self, X, Y, plotting=True):
        assert len(X) == len(Y), "X and Y should be in same shape"
        data = np.zeros((self.iter_time, len(X)))
        for i in range(self.iter_time):
            p1, p2 = self.generator() # Generate paramters each prjection
            temp_data = p1 * np.array(X) + p2 * np.array(Y)
            self.coefficients[i][0] = p1
            self.coefficients[i][1] = p2
            #print(temp_data)
            data[i] = temp_data

        if self.seeding_flag:
            data[-1] = np.array(X) # Replace the last one to seeds on X
            self.coefficients[-1] = [1,0]

        if plotting == True:
            x = np.arange(-1,1,0.1)

            for i in range(self.iter_time):
                y = (-1 * self.coefficients[i][1]/self.coefficients[i][0]) * x
                plt.xlim(-1,1)
                plt.ylim(-1,1)
                plt.plot(x, y)

        return data
            
    def projection2(self, X, Y, plotting=True):
        assert len(X) == len(Y), "X and Y should be in same shape"
        data = np.zeros((self.iter_time, len(X)))
        for i in range(self.iter_time):
            p1, p2 = self.coefficients[i][0], self.coefficients[i][1]
            temp_data = p1 * np.array(X) + p2 * np.array(Y)
            #print(temp_data)
            data[i] = temp_data

        if self.seeding_flag:
            data[-1] = np.array(X) # Replace the last one to seeds on X
            self.coefficients[-1] = [1,0]

        if plotting == True:
            x = np.arange(-1,1,0.1)

            for i in range(self.iter_time):
                y = (-1 * self.coefficients[i][1]/self.coefficients[i][0]) * x
                plt.xlim(-1,1)
                plt.ylim(-1,1)
                plt.plot(x, y)

        return data
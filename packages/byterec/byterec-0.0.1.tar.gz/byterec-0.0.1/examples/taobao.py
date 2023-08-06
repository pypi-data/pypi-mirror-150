
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from torch.utils.data import Dataset
import torch

class TaobaoDataset(Dataset):
    """
    Criteo Display Advertising Challenge Dataset

    :param dataset_path: criteo train.csv path.
    Reference:
        https://labs.criteo.com/2014/02/kaggle-display-advertising-challenge-dataset
        https://www.csie.ntu.edu.tw/~r01922136/kaggle-2014-criteo.pdf
    """

    def __init__(self, data_path="./taobao_train.csv"):
        data = pd.read_csv(data_path) #sequence特征已padding 对齐长度50
        self.max_len = 50
        n_users = 864915 
        n_items = 4027558 
        n_cates = 9377
        sparse_features = ["user_id", "hist_len","user_count","item_count"]
        sequence_features = ["hist_item_id","hist_cate_id"]
        candidate_features = ["item_id","cate_id"]

        for fea in sparse_features:
            if fea!="user_id": #原始数据 user_id 已经encode
                le = LabelEncoder()
                data[fea] = le.fit_transform(data[fea])
        sparse_field_dims = np.zeros(len(sparse_features), dtype=np.int32)
        for i, fea in enumerate(sparse_features):
           n_unique = data[fea].nunique()
           print("feature: %s n_unique: %d"%(fea, n_unique))
           sparse_field_dims[i] = n_unique

        sequence_field_dims = np.zeros(len(sequence_features), dtype=np.int32)
        #sequence特征与它对应的candidate特征的embedding词表大小一致
        sequence_field_dims[0] = n_items
        sequence_field_dims[1] = n_cates
        
        self.sparse_field_dims = sparse_field_dims #每个sparse特征的unique值个数 list
        self.sequence_field_dims = sequence_field_dims
        self.length = data.shape[0]
        
        self.x_sequence = np.zeros((self.length, len(sequence_features),self.max_len),dtype=np.int32)

        for i in range(len(sequence_features)): #str->list
            seq_list = data[sequence_features[i]].apply(lambda x:eval(x))
            self.x_sequence[:,i,:] = np.array(seq_list.to_list(),dtype=np.int32)
            #(batch_size, num_seq_fields, seq_length)
 
        self.x_sparse = data[sparse_features].values 
        self.x_candidate = data[candidate_features].values 
        self.y = data["label"].values

    def __getitem__(self, index):
        return torch.LongTensor(self.x_sequence[index]), torch.LongTensor(self.x_candidate[index]), torch.LongTensor(self.x_sparse[index]), self.y[index]

    def __len__(self):
        return self.length


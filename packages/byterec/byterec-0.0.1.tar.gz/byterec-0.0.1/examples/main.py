import sys
sys.path.append('/home/wlsh/ssd/lmc/torch-ctr')

import torch
import tqdm
from sklearn.metrics import roc_auc_score
from torch.utils.data import DataLoader
from torch_ctr.models import WideAndDeep, DeepFM, DIN

from taobao import TaobaoDataset
from criteo import CriteoDataset
from amazon import AmazonDataset

class EarlyStopper(object):

    def __init__(self, num_trials, save_path):
        self.num_trials = num_trials
        self.trial_counter = 0
        self.best_accuracy = 0
        self.save_path = save_path

    def is_continuable(self, model, accuracy):
        if accuracy > self.best_accuracy:
            self.best_accuracy = accuracy
            self.trial_counter = 0
            torch.save(model, self.save_path)
            return True
        elif self.trial_counter + 1 < self.num_trials:
            self.trial_counter += 1
            return True
        else:
            return False


def train(model, optimizer, scheduler, data_loader, criterion, device, log_interval=100):
    print("Current lr : {}".format(optimizer.state_dict()['param_groups'][0]['lr']))
    model.train()
    total_loss = 0
    tk0 = tqdm.tqdm(data_loader, smoothing=0, mininterval=1.0)
    #for i, (dense_fields, sparse_fields, target) in enumerate(tk0):
    #    dense_fields, sparse_fields, target = dense_fields.to(device), sparse_fields.to(device), target.to(device)
    for i, (sequence_fields, candidate_fields, sparse_fields, target) in enumerate(tk0):
        sequence_fields, candidate_fields, sparse_fields, target = \
            sequence_fields.to(device), candidate_fields.to(device),sparse_fields.to(device), target.to(device)
        #y = model(dense_fields, sparse_fields)
        y = model(sequence_fields, candidate_fields, sparse_fields)
        loss = criterion(y, target.float())
        model.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        if (i + 1) % log_interval == 0:
            tk0.set_postfix(loss=total_loss / log_interval)
            total_loss = 0
    scheduler.step()

    

def test(model, data_loader, device):
    model.eval()
    targets, predicts = list(), list()
    with torch.no_grad():
        tk0 = tqdm.tqdm(data_loader, smoothing=0, mininterval=1.0)
        for i, (sequence_fields, candidate_fields, sparse_fields, target) in enumerate(tk0):
            sequence_fields, candidate_fields, sparse_fields, target = \
                sequence_fields.to(device), candidate_fields.to(device),sparse_fields.to(device), target.to(device)
            y = model(sequence_fields, candidate_fields, sparse_fields)
            targets.extend(target.tolist())
            predicts.extend(y.tolist())
    return roc_auc_score(targets, predicts)


def main(dataset_name,
         dataset_path,
         dataset_mode,
         model_name,
         epoch,
         learning_rate,
         batch_size,
         emb_dim,
         weight_decay,
         device,
         save_dir, 
         seed):
    torch.manual_seed(seed)
    device = torch.device(device)
    if dataset_name == "criteo":
        dataset = CriteoDataset(dataset_mode, dataset_path)
        model = get_model(model_name, dataset, emb_dim)

    elif dataset_name == "taobao":
        dataset = TaobaoDataset(dataset_path)
        model = DIN(dataset.sequence_field_dims, dataset.sparse_field_dims, embed_dim=emb_dim, mlp_dims=[256, 128], dropout=0.2)
    elif dataset_name == "amazon":
        dataset = AmazonDataset(dataset_path)
        model = DIN(dataset.sequence_field_dims, dataset.sparse_field_dims, embed_dim=emb_dim, mlp_dims=[256, 128], dropout=0.2)

    train_length = int(len(dataset) * 0.8)
    valid_length = int(len(dataset) * 0.1)
    test_length = len(dataset) - train_length - valid_length
    train_dataset, valid_dataset, test_dataset = torch.utils.data.random_split(
        dataset, (train_length, valid_length, test_length))
    
    train_data_loader = DataLoader(train_dataset, batch_size=batch_size, num_workers=8)
    valid_data_loader = DataLoader(valid_dataset, batch_size=batch_size, num_workers=8)
    test_data_loader = DataLoader(test_dataset, batch_size=batch_size, num_workers=8)
    
    model.to(device)
    criterion = torch.nn.BCELoss()
    optimizer = torch.optim.Adam(params=model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=40, gamma=0.1)
    #scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.1)

    early_stopper = EarlyStopper(num_trials=50, save_path=f'{save_dir}/{model_name}.pth')
    print("train %s"%model_name)
    for epoch_i in range(epoch):
        train(model, optimizer, scheduler, train_data_loader, criterion, device)
        auc = test(model, valid_data_loader, device)
        print('epoch:', epoch_i, 'validation: auc:', auc)
        if not early_stopper.is_continuable(model, auc):
            print(f'validation: best auc: {early_stopper.best_accuracy}')
            break
    model = torch.load(f'{save_dir}/{model_name}.pth') #load best model
    auc = test(model, test_data_loader, device)
    print(f'test auc: {auc}')


def get_model(model_name, dataset, emb_dim):
    if model_name == "widedeep":
        model = WideAndDeep(dataset.dense_field_nums, dataset.sparse_field_dims, embed_dim=emb_dim, mlp_dims=(256, 128), dropout=0.2)
    elif model_name == "deepfm":
        model = DeepFM(dataset.dense_field_nums, dataset.sparse_field_dims, embed_dim=emb_dim, mlp_dims=(256, 128), dropout=0.2)
    return model

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_name', default='criteo')
    parser.add_argument('--dataset_path', default='./criteo/data/criteo_sample_50w.csv')
    parser.add_argument('--dataset_mode', default='mini')
    parser.add_argument('--model_name', default='din')
    parser.add_argument('--epoch', type=int, default=100)
    parser.add_argument('--learning_rate', type=float, default=5e-3)
    parser.add_argument('--batch_size', type=int, default=4096)
    parser.add_argument('--emb_dim', type=int, default=8)
    parser.add_argument('--weight_decay', type=float, default=1e-3)
    parser.add_argument('--device', default='cuda:0')
    parser.add_argument('--save_dir', default='chkpt')
    parser.add_argument('--seed', type=int, default=2022)

    args = parser.parse_args()
    main(args.dataset_name,
         args.dataset_path,
         args.dataset_mode,
         args.model_name,
         args.epoch,
         args.learning_rate,
         args.batch_size,
         args.emb_dim,
         args.weight_decay,
         args.device,
         args.save_dir,
         args.seed)
import os
import pickle
import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader
from models.dkt import DKT

class DKTDataset(Dataset):
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        q_seq, r_seq = self.data[idx]
        # q_seq and r_seq are already length 200, padded with -1 at the front
        # We need q (0 to n-1), r (0 to n-1), qshft (1 to n), rshft (1 to n)
        q = q_seq[:-1]
        r = r_seq[:-1]
        qshft = q_seq[1:]
        rshft = r_seq[1:]
        
        # Mask where padded (-1)
        m = (q != -1) & (qshft != -1)
        
        # Replace -1 with 0 for embedding (mask handles ignoring these later)
        q = np.where(q == -1, 0, q)
        r = np.where(r == -1, 0, r)
        qshft = np.where(qshft == -1, 0, qshft)
        rshft = np.where(rshft == -1, 0, rshft)

        return (
            torch.FloatTensor(q),
            torch.FloatTensor(r),
            torch.FloatTensor(qshft),
            torch.FloatTensor(rshft),
            torch.BoolTensor(m)
        )

def main():
    data_path = os.path.join(os.path.dirname(__file__), "../data/assistments_processed.pkl")
    ckpt_dir = os.path.join(os.path.dirname(__file__), "../checkpoints")
    os.makedirs(ckpt_dir, exist_ok=True)
    
    with open(data_path, 'rb') as f:
        data = pickle.load(f)
        
    train_data = data['train']
    val_data = data['val']
    num_skills = data['num_skills']
    
    train_dataset = DKTDataset(train_data)
    val_dataset = DKTDataset(val_data)
    
    # We use batch_size 64
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=64, shuffle=False)
    
    # Init model
    emb_size = 100
    hidden_size = 100
    model = DKT(num_skills, emb_size, hidden_size)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    opt = torch.optim.Adam(model.parameters(), lr=0.001)
    
    print("Starting training...")
    model.train_model(
        train_loader=train_loader,
        test_loader=val_loader,
        num_epochs=50,
        opt=opt,
        ckpt_path=ckpt_dir,
        device=device
    )
    print("Training finished. Checkpoint saved to checkpoints/dkt_best.pt")

if __name__ == "__main__":
    main()

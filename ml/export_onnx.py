import os
import pickle
import torch
from models.dkt import DKT

def export_to_onnx():
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, "../data/assistments_processed.pkl")
    ckpt_path = os.path.join(base_dir, "../checkpoints/dkt_best.pt")
    out_dir = os.path.join(base_dir, "../model_store/dkt/1")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "model.onnx")

    with open(data_path, 'rb') as f:
        data = pickle.load(f)
    num_skills = data['num_skills']
    
    emb_size = 100
    hidden_size = 100
    model = DKT(num_skills, emb_size, hidden_size)
    
    device = torch.device("cpu")
    model.load_state_dict(torch.load(ckpt_path, map_location=device))
    model.eval()

    # Create dummy inputs
    dummy_q = torch.zeros((1, 200), dtype=torch.long)
    dummy_r = torch.zeros((1, 200), dtype=torch.long)

    print("Exporting model to ONNX...")
    torch.onnx.export(
        model,
        (dummy_q, dummy_r),
        out_path,
        export_params=True,
        opset_version=14,
        do_constant_folding=True,
        input_names=['q', 'r'],
        output_names=['output'],
        dynamic_axes={
            'q': {0: 'batch_size'},
            'r': {0: 'batch_size'},
            'output': {0: 'batch_size'}
        }
    )
    print(f"Model exported successfully to {out_path}")

if __name__ == "__main__":
    export_to_onnx()

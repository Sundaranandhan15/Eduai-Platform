import numpy as np
import tritonclient.grpc as grpcclient

class TritonDKTClient:
    def __init__(self, url="localhost:8001"):
        self.url = url
        self.client = grpcclient.InferenceServerClient(url=self.url)
        self.model_name = "dkt"
        self.seq_len = 200

    def predict(self, skill_seq: list, correct_seq: list) -> np.ndarray:
        """
        Takes a sequence of skill interactions and predicts the mastery probability array.
        skill_seq: list of skill IDs
        correct_seq: list of 1s and 0s (correctness)
        Returns a numpy array of shape (seq_len, num_skills)
        """
        # Ensure sequences are no longer than max seq_len
        if len(skill_seq) > self.seq_len:
            skill_seq = skill_seq[-self.seq_len:]
            correct_seq = correct_seq[-self.seq_len:]

        # Pad sequences to match expected input size (batch_size, seq_len)
        pad_len = self.seq_len - len(skill_seq)
        
        # We pad with -1, then replace with 0. But for inference, we only care about the latest step.
        q = np.pad(skill_seq, (pad_len, 0), 'constant', constant_values=0).astype(np.int64)
        r = np.pad(correct_seq, (pad_len, 0), 'constant', constant_values=0).astype(np.int64)

        # Batch dimension
        q = np.expand_dims(q, axis=0)
        r = np.expand_dims(r, axis=0)

        # Create inputs
        inputs = [
            grpcclient.InferInput("q", q.shape, "INT64"),
            grpcclient.InferInput("r", r.shape, "INT64")
        ]
        
        inputs[0].set_data_from_numpy(q)
        inputs[1].set_data_from_numpy(r)

        # Create output
        outputs = [grpcclient.InferRequestedOutput("output")]

        # Run inference
        result = self.client.infer(
            model_name=self.model_name,
            inputs=inputs,
            outputs=outputs
        )

        output_data = result.as_numpy("output")
        # output_data has shape (1, 200, 198). We want the probabilities for the current (latest) step
        # which is the last valid interaction. Since we padded at the beginning, the last element is the latest.
        # But let's just return the whole (seq_len, num_skills) for the single batch
        return output_data[0]

if __name__ == "__main__":
    # Test
    client = TritonDKTClient()
    # Mock data
    skills = [1, 5, 2, 1]
    corrects = [1, 0, 1, 1]
    try:
        preds = client.predict(skills, corrects)
        print("Prediction shape:", preds.shape)
        print("Latest step predictions:", preds[-1])
    except Exception as e:
        print("Error during inference (is Triton server running?):", e)

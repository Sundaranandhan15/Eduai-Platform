import pandas as pd
import numpy as np
import pickle
import os

def preprocess_assistments(input_file, output_file, max_seq_len=200):
    print(f"Loading data from {input_file}...")
    # Load dataset (using low_memory=False to avoid DtypeWarnings, or specify types)
    cols_to_use = ['user_id', 'skill', 'correct', 'problem_id']
    
    # Check what columns exist in the file
    df_sample = pd.read_csv(input_file, nrows=10)
    print("Columns in file:", df_sample.columns.tolist())
    
    # Some ASSISTments datasets use different column names
    col_mapping = {}
    if 'user_id' not in df_sample.columns and 'student_id' in df_sample.columns:
        col_mapping['student_id'] = 'user_id'
    
    actual_cols = df_sample.columns.tolist()
    usecols = [c for c in cols_to_use if c in actual_cols]
    
    df = pd.read_csv(input_file, usecols=usecols, engine='c')
    df.rename(columns=col_mapping, inplace=True)
    
    # Drop rows with missing values in essential columns
    df.dropna(subset=['user_id', 'skill', 'correct', 'problem_id'], inplace=True)
    
    # Convert types
    df['correct'] = df['correct'].astype(int)
    
    print(f"Total rows after dropping NaNs: {len(df)}")
    
    # Encode skill and problem_id
    df['skill_id'] = df['skill'].astype('category').cat.codes
    df['problem_id'] = df['problem_id'].astype('category').cat.codes
    
    print(f"Number of unique skills: {df['skill_id'].nunique()}")
    print(f"Number of unique problems: {df['problem_id'].nunique()}")
    
    # Group by user_id to form sequences
    print("Grouping by user_id to form sequences...")
    sequences = []
    
    # Group and build sequences
    for _, user_df in df.groupby('user_id'):
        skill_seq = user_df['skill_id'].values
        correct_seq = user_df['correct'].values
        
        # Pad or truncate
        if len(skill_seq) > max_seq_len:
            skill_seq = skill_seq[-max_seq_len:]
            correct_seq = correct_seq[-max_seq_len:]
        else:
            pad_len = max_seq_len - len(skill_seq)
            skill_seq = np.pad(skill_seq, (pad_len, 0), 'constant', constant_values=-1)
            correct_seq = np.pad(correct_seq, (pad_len, 0), 'constant', constant_values=-1)
            
        sequences.append((skill_seq, correct_seq))
        
    print(f"Total sequences (users): {len(sequences)}")
    
    # Split 80/10/10
    n = len(sequences)
    train_end = int(0.8 * n)
    val_end = int(0.9 * n)
    
    np.random.seed(42)
    np.random.shuffle(sequences)
    
    train_data = sequences[:train_end]
    val_data = sequences[train_end:val_end]
    test_data = sequences[val_end:]
    
    print(f"Train size: {len(train_data)}")
    print(f"Val size: {len(val_data)}")
    print(f"Test size: {len(test_data)}")
    
    # Save processed data
    print(f"Saving to {output_file}...")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'wb') as f:
        pickle.dump({
            'train': train_data,
            'val': val_data,
            'test': test_data,
            'num_skills': df['skill_id'].nunique(),
            'max_seq_len': max_seq_len
        }, f)
        
    print("Preprocessing complete!")

if __name__ == "__main__":
    input_csv = r"C:\Users\dhars\.cache\kagglehub\datasets\nicolaswattiez\skillbuilder-data-2009-2010\versions\4\2012-2013-data-with-predictions-4-final.csv"
    output_pkl = r"D:\EduAI - Adaptive Knowledge Tracing & AI Tutoring Platform\eduai-platform\data\assistments_processed.pkl"
    preprocess_assistments(input_csv, output_pkl)

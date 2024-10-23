import pandas as pd

df = pd.read_csv('names.csv')

chunk_size = 1000
num_chunks = len(df) // chunk_size + (1 if len(df) % chunk_size != 0 else 0)

for i in range(num_chunks):
    start = i * chunk_size
    end = start + chunk_size
    chunk = df[start:end]
    chunk.to_csv(f'names-{i+1}.csv', index=False)

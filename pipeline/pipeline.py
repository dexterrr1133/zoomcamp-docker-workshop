import sys
import pandas as pd

print('Arguments:', sys.argv)

month = int(sys.argv[1])

print('Hello Pipeline')

df = pd.DataFrame({'Day': [1, 2, 3], 'Passengers': [4, 5, 6]})
df['month'] = month
print(df.head())

df.to_parquet(f'output{month}.parquet', index=False)

print('Month:', month)
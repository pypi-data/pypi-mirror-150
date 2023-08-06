import pandas

import ictiopy
df = pandas.DataFrame()

df = ictiopy.load_zipdb('test/Ictio_Basic_20220401.zip')
df.to_csv('parsed_data.csv')
print(df.head())


import pandas as pd
from users import dfToDict, RFID0Corrector

df = pd.read_csv('admin.csv', encoding='latin1')

password_to_admin = dfToDict(df)

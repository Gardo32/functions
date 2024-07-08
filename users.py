import pandas as pd

def RFID0Corrector(dct):
    keys_to_update = list(dct.keys())
    for key in keys_to_update:
        new_key = key
        while len(new_key) < 10:
            new_key = '0' + new_key
        if new_key != key:
            dct[new_key] = dct.pop(key)


df = pd.read_csv('Users.csv', encoding='latin1')

password_to_user = {str(row[1]): row[0] for _, row in df.iterrows()}



import pandas as pd
import os

def load_votes_df():
    votes_file = 'votes.csv'
    if os.path.exists(votes_file):
        return pd.read_csv(votes_file)
    else:
        return pd.DataFrame(columns=['user_id', 'choice'])

votes_df = load_votes_df()

def record_vote(user_id, choice):
    global votes_df
    votes_df = load_votes_df()
    new_vote = pd.DataFrame({'user_id': [user_id], 'choice': [choice]})
    votes_df = pd.concat([votes_df, new_vote], ignore_index=True)
    votes_df.to_csv('votes.csv', index=False)

def has_voted(user_id):
    global votes_df
    votes_df = load_votes_df()
    return user_id in votes_df['user_id'].values

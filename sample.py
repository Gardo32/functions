import pandas as pd

# Sample data for demonstration
votes_df = {
    'user_id': ['User1', 'User2', 'User3', 'User4', 'User5'],
    'choice': ['Option A', 'Option B', 'Option A', 'Option C', 'Option B']
}

# Create DataFrame
view_df = pd.DataFrame(votes_df)

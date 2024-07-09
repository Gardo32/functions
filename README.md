# Voting App

## Getting Started

1. **Install Dependencies**

   Download all required dependencies by running:
   ```bash
   pip install -r "requirements.txt"
   ```

2. **Upload CSV Files**

   Upload two CSV files named `admin.csv` and `Users.csv`. Ensure they follow this format (use the RFID card ID for physical login if applicable):
   
   For `admin.csv`:
   ```csv
   username,password
   Admin 1,1234566
   ```

   For `Users.csv`:
   ```csv
   username,password
   User 2,09876545
   User 3,1234567
   ```

3. **RFID Card Configuration**

   If you are using RFID cards, skip this step. Otherwise, remove the following lines from `main.py`:
   ```python
   RFID0Corrector(password_to_user) # Remove if not using NFC reader
   RFID0Corrector(password_to_admin) # Remove if not using NFC reader
   ```

4. **Launch the Web App**

   Start the web application by running:
   ```bash
   python main.py
   ```

## How to Use

1. **Logging In**

   - **Admins**: Admins can log in using the credentials provided in the `admin.csv` file. Admins have access to view voting results and manage the votes.
   - **Users**: Users can log in using the credentials provided in the `Users.csv` file. Users can vote once using their unique credentials.

2. **Voting**

   - After logging in, users will be redirected to the voting page where they can cast their vote by selecting one of the available choices.
   - Users can only vote once. If they attempt to vote again, they will receive a message indicating that they have already voted.

3. **Viewing Results**

   - Admins can view the voting results by navigating to the results page after logging in.
   - The results page displays a table with all the votes, including user IDs and their choices.
   - A summary of the vote counts for each choice is also displayed below the vote logs.

4. **Managing Votes**

   - **Downloading CSV**: Admins can download the current vote data as a CSV file by clicking the "Download CSV" button on the results page.
   - **Deleting CSV**: Admins can delete the `votes.csv` file by clicking the "Delete CSV" button on the results page. A confirmation prompt will appear to ensure that the admin wants to proceed with the deletion.

## Notes

- Ensure the CSV files are correctly formatted and located in the same directory as `main.py`.
- The `votes.csv` file will be created and updated automatically as users cast their votes.
- Admins should handle the deletion of the `votes.csv` file with care as this action cannot be undone.

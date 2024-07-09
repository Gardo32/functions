# Multi-Pass Login Page

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

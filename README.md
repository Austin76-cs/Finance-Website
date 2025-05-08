# Personal Finance App

## Source Code

The source code for this project is available in this repository.

To run this project locally:

1.  **Backend (Flask, SQLite, PLAID API):**
    *   Ensure you have the required Python packages installed (see [`requirements.txt`]. You might need to create a virtual environment and run `pip install -r requirements.txt`.
    *   Run the Flask dev server:
        ```bash
        python run.py
        ```
    *   The backend API will be running at `http://127.0.0.1:5000/`.
    *   Note that since the API Keys are not in the project you will not see any info displayed for transactions
    *   All API calls are through PLAID to connect to banks and get user information to store in the database
    *   With Plaid API access you would see this : ![image](https://github.com/user-attachments/assets/813a4c42-686c-4b09-9a67-5fe8e0195c08)
    *   


2.  **Frontend (HTML, CSS, Javascript):**



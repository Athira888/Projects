# Automated Email Sender

This is a simple Python script designed to send personalized emails to a list of recipients from a CSV file. It's built for efficiency and ease of use, making it ideal for sending bulk notifications, newsletters, or personalized messages.

### Features

**Personalized Emails**: Automatically inserts the recipient's name from the CSV file into the email body, making each message unique and  yespersonal.
**CSV-Based Recipient Management**: Manages recipient lists in a straightforward, human-readable format (`.csv`), which can be easily edited using any spreadsheet program.
**Secure SMTP Connection**: Utilizes SSL encryption to ensure a secure connection to Google's SMTP server for safe and reliable email delivery.
**Minimal Dependencies**: Uses only Python's built-in libraries (`csv`, `smtplib`, `ssl`), so no extra packages need to be installed.

### Prerequisites

To run this script, you will need:

* **Python 3.x**: The script is written in Python 3.
* **A Gmail Account with an App Password**: For security reasons, you cannot use your regular Gmail password. You must enable **2-Step Verification** on your Google Account and generate a specific **App Password** for this script.

### How to Set Up and Run

1.  **Clone the Repository**:
    If you're using Git, clone this repository to your local machine.

    ```bash
    git clone [repository_url]
    cd automated-email-sender
    ```

    Alternatively, you can download the project files (`main.py`, `list.csv`, `README.md`) directly into a single folder.

2.  **Prepare the Recipient List**:
    Create a file named `list.csv` in the same directory as the `main.py` script. This file **must** have two columns with the exact headers `name` and `email`.

    **Example `list.csv`:**
    ```csv
    name,email
    John Doe,johndoe@example.com
    Jane Smith,janesmith@anotherdomain.com
    Mark Wilson,markwilson@emailprovider.net
    ```

3.  **Generate a Gmail App Password**:
    This is the most critical step. Your regular Gmail password will not work.

    * Ensure **2-Step Verification** is enabled for your Google Account.
    * Navigate to your Google Account settings and go to **Security > App Passwords**. You can also use this direct link: [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).
    * From the "Select app" dropdown, choose `Mail`.
    * From the "Select device" dropdown, choose `Other (Custom name)`.
    * Give it a memorable name, like "Python Email Sender," and click **Generate**.
    * A 16-character password will be displayed. **Copy this password immediately** and save it somewhere secure, as you will not be able to see it again. This is the "passkey" you will use when prompted by the script.

4.  **Run the Script**:
    Open a terminal or command prompt, navigate to the project directory, and execute the Python script.

    ```bash
    python main.py
    ```

    The script will ask you for your Gmail address and the App Password you just generated. After you enter the credentials, it will begin sending emails to the recipients listed in `list.csv`.

### Customizing the Email

You can easily modify the email's subject and body within the `main.py` file. Locate the `message` variable and edit the content. Remember to keep the `f-string` formatting (`f"..."`) if you want to include personalized variables like `{row['name']}`.

```python
    message = f"""Subject: Hello {row['name']}

Hello {row['name']}!,

I hope this message finds you well.

This is a personalized email from the automated email system.

Best regards,
Athira Denny

"""

#Security Note
Never hardcode your email address or password directly into the script. By prompting for input, the current version of the script ensures your credentials are not saved within the file itself. For more advanced projects, consider using environment variables or a .env file to manage sensitive information.

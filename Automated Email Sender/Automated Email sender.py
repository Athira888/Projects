import csv,smtplib,ssl
sendername = input("Enter your Gmail: ")
password = input("Enter passkey (dw i wont steal it): ")
server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context())
server.login(sendername, password)
for row in csv.DictReader(open("list.csv")):
    message = f"""Subject: Hello {row['name']}

HALLLOOOO {row['name']}!!!,

Wassup lil dumbass, this is a test email to check if this shi works.

Best Regards,
Athira The Great <3
"""
    server.sendmail(sendername, row["email"], message)
    print("Email Sent to", row["name"])

server.quit()

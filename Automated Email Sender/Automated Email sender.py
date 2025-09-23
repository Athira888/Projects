import csv,smtplib,ssl
sendername = input("Enter your Gmail: ")
password = input("Enter passkey : ")
server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context())
server.login(sendername, password)
for row in csv.DictReader(open("list.csv")):
    message = f"""Subject: Hello {row['name']}

Hello {row['name']}!,

I hope this message finds you well.

This is a test email to verify that the automatic email system is functioning correctly.

Best regards,
Athira Denny

"""
    server.sendmail(sendername, row["email"], message)
    print("Email Sent to", row["name"])

server.quit()

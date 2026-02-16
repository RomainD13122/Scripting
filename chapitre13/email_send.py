#chapitre 13

import smtplib
import getpass

def prompt(title):
    return input(title).strip()

from_addr = prompt("From (Outlook): ")
password = getpass.getpass("Password (App password if 2FA enabled): ")
to_addrs = prompt("To: ").split()

lines = [f"From: {from_addr}", f"To: {', '.join(to_addrs)}", ""]
print("Enter message body (Ctrl+D to finish):")
while True:
    try:
        line = input()
    except (EOFError, KeyboardInterrupt):
        break
    else:
        lines.append(line)

msg = "\r\n".join(lines)
print("Message length is", len(msg))

server = smtplib.SMTP('smtp-mail.outlook.com', 587)
server.starttls()
server.login(from_addr, password)
server.sendmail(from_addr, to_addrs, msg)
server.quit()
print("Email sent successfully!")
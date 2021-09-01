import smtplib
from email.message import EmailMessage

def email_alert(to, subject, body):
    # create an Email Message
    msg = EmailMessage()
    # Set the Body of the Email
    msg.set_content(body)
    # Set the Subject for the Email
    msg['subject'] = subject
    # Set the address for the Email to be sent
    msg['to'] = to
    
    # Define the Sending Email Address
    user = "pi.airmonitor@gmail.com"
    msg['from'] = user
    # App password for the sending Email Account
    password = "ccswmxzevkgvbfid"
    
    # gmails smtp server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    
    server.quit()
    
# Stops code from running when just imported into another program    
if __name__ == '__main__':
    #testing email alert function
    email_alert("rick_mcmanus@hotmail.com", "Email Notification Test", "Particle Matter to high")   

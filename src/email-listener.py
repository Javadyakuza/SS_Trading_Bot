import email_listener
import logging
from config import RECEIVER_EMAIL
from config import APP_PASSWORD
# Set your email, password, what folder you want to listen to, and where to save attachments
email = RECEIVER_EMAIL
app_password = APP_PASSWORD
folder = "Inbox"
attachment_dir = "./inboxes"
el = email_listener.EmailListener(email, app_password, folder, attachment_dir)

# Log into the IMAP server
el.login()

# Get the emails currently unread in the inbox
messages = el.scrape()
print(messages)


# Start listening to the inbox and timeout after an hour
timeout = 525600


def run():
    try:
        # Log into the IMAP server
        el.login()
        el.listen(timeout)
    except Exception as e:
        logging.warning(e)
        logging.warning("setting thing's up again waiting ...")
        run_runner()


def run_runner():
    run()


run()

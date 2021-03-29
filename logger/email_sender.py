import toml
import os
from datetime import date
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, COMMASPACE
import notify2


class EmailSender:
    LOG_FILE_PATH = "logger/data/logs/daily_log_"
    BOT_EMAIL_FILE_PATH = "logger/data/bot_email.toml"
    USER_EMAILS_FILE_PATH = "logger/data/user_emails.toml"
    LOG_DESCRIPTION_FILE_PATH = "logger/data/log_description.txt"
    LOG_SUBJECT = "Daily Log - "

    _bot_address = ""
    _bot_pass = ""

    def __init__(self):
        self._load_bot_email_configuration(self.BOT_EMAIL_FILE_PATH)

    def send_log(self):
        user_addresses = self._load_user_addresses_configuration(self.USER_EMAILS_FILE_PATH)
        if len(user_addresses) > 0:
            daily_log_mail = MIMEMultipart()
            daily_log_mail["From"] = self._bot_address
            daily_log_mail["To"] = COMMASPACE.join(user_addresses)
            daily_log_mail["Date"] = formatdate(localtime=True)
            daily_log_mail["Subject"] = self.LOG_SUBJECT + date.today().strftime("%d/%m/%Y")
            with open(self.LOG_DESCRIPTION_FILE_PATH, 'r') as log_description_file:
                daily_log_description = log_description_file.read()
                log_description_file.close()
            daily_log_mail.attach(MIMEText(daily_log_description))

            daily_log_path = self.LOG_FILE_PATH + date.today().strftime("%d_%m_%Y") + ".pdf"
            with open(daily_log_path, "rb") as daily_log:
                part = MIMEApplication(daily_log.read(), Name=os.path.basename(daily_log_path))
            part["Content-Disposition"] = 'attachment; filename="%s"' % os.path.basename(daily_log_path)
            daily_log_mail.attach(part)

            try:
                server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
                server_ssl.ehlo()
                server_ssl.login(self._bot_address, self._bot_pass)
                does_not_get_email = server_ssl.sendmail(self._bot_address, list(user_addresses), daily_log_mail.as_string())
                server_ssl.close()
                if len(does_not_get_email) == 0:
                    self._notify_user("Email Sent!", "Your daily log was sent successfully", "success.png")
                else:
                    self._notify_user("Email Error!", f"Your daily log wasn't sent successfully to the following users: "
                                                      f"{str(does_not_get_email)}", "warning_sign.png")
            except smtplib.SMTPRecipientsRefused:
                self._notify_user("Email Error", "Couldn't deliver emails to the recipients because they refused", "warning_sign.png")
            except smtplib.SMTPAuthenticationError:
                self._notify_user("Email Error", "Couldn't authenticate to the waf waf gmail account", "warning_sign.png")
            except smtplib.SMTPException:
                self._notify_user("Email Error", "Couldn't send emails properly", "warning_sign.png")

    def _load_bot_email_configuration(self, bot_email_file_path):
        if os.path.exists(bot_email_file_path):
            bot_email = toml.load(bot_email_file_path)
            self._bot_address = bot_email["address"]
            self._bot_pass = bot_email["pass"]
        else:
            raise FileNotFoundError

    def _load_user_addresses_configuration(self, user_emails_file_path):
        user_emails = dict()
        if os.path.exists(user_emails_file_path):
            user_emails = toml.load(user_emails_file_path).get("emails", {})

        user_addresses = set()
        for address in user_emails.values():
            user_addresses.add(address)
        return user_addresses

    def _notify_user(self, title, content, image_name):
        notify2.init("WAF WAF")
        picture_path = os.getcwd() + "/misc/" + image_name
        notifier = notify2.Notification(title, content, picture_path)
        notifier.set_timeout(5000)
        notifier.show()

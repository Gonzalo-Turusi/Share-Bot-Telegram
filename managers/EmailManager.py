import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from configuration.ConfigEnv import configEnv
from datetime import datetime, timedelta

class EmailManager:
    def __init__(self):
        self.server = configEnv.get('SMTP_SERVER')
        self.port = configEnv.get('SMTP_PORT')
        self.user = configEnv.get('EMAIL_SENDER')
        self.password = configEnv.get('EMAIL_PASSWORD')
        self.log_file_path = configEnv.get('RESOURCES_PATH') + 'HourEmailSended.txt'

    def _read_log(self):
        try:
            with open(self.log_file_path, 'r') as file:
                lines = file.readlines()
            return {line.split(' - ')[1].strip(): datetime.strptime(line.split(' - ')[0].strip(), "%Y-%m-%d %H:%M:%S") for line in lines}
        except FileNotFoundError:
            with open(self.log_file_path, 'w') as file:
                pass
            return {}

    def _update_log(self, subject):
        try:
            updated = False

            # Leer todas las líneas del archivo
            with open(self.log_file_path, 'r') as file:
                lines = file.readlines()

            # Abrir el archivo para sobrescribir
            with open(self.log_file_path, 'w') as file:
                for line in lines:
                    if line.split(' - ')[1].strip() == subject:
                        file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {subject}\n")
                        updated = True
                    else:
                        file.write(line)

                # Si el subject no estaba en el archivo, agregarlo
                if not updated:
                    file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {subject}\n")
        except Exception as e:
            print(f"Error al actualizar el archivo de log: {e}")
            logging.error("Error al actualizar el archivo de log: %s", e, exc_info=True)
            raise

    def send_email_if_needed(self, subject, body, recipients, attachments=None) -> bool:
        logs = self._read_log()
        now = datetime.now()
        
        if logs:
            last_sent = logs.get(subject)
            if last_sent and now - last_sent < timedelta(hours=configEnv.get('INTERVAL_FOR_SEND', default=1)):
                logging.info("El correo con el asunto %s ya fue enviado hace menos de una hora.", subject)
                print(f"El correo con el asunto '{subject}' ya fue enviado hace menos de una hora.")
                return False
        
        result = self.send_email(subject, body, recipients, attachments)
        if result:
            self._update_log(subject)
        
        return result

    def send_email(self, subject, body, recipients, attachments=None) -> bool:
        msg = MIMEMultipart()
        msg['From'] = self.user
        msg['Subject'] = subject
        msg['To'] = recipients

        msg.attach(MIMEText(body, 'plain'))

        if attachments:
            for file in attachments:
                try:
                    part = MIMEBase('application', 'octet-stream')
                    with open(file, 'rb') as attachment:
                        part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename={file}',
                    )
                    msg.attach(part)
                except Exception as e:
                    print(f"Failed to attach file {file}: {e}")
                    logging.error("Error al adjuntar el archivo %s: %s", file, e, exc_info=True)

        try:
            server = smtplib.SMTP(self.server, self.port)
            server.starttls()
            server.login(self.user, self.password)
            server.send_message(msg)
            server.quit()
            print(f"Se envió el mail exitosamente a los siguientes correos: {recipients}")
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            logging.error("Error al enviar el correo: %s. ", e, exc_info=True)
            return False
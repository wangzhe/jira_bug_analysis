import configparser
import getpass
import smtplib
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from module.analysis_util import debug_log_console
from module.storage_util import write_html_to_file
from module.sys_invariant import config_path


class JbaEmail:
    class __JbaEmail:
        def __init__(self, arg):
            config = configparser.ConfigParser()
            try:
                config.read(config_path + arg + '.local')
                self.smtp_host = config['EMAIL']['SMTP_HOST']
            except KeyError as e:
                config.read(config_path + 'default.local')
                self.smtp_host = config['EMAIL']['SMTP_HOST']
            self.smtp_port = config['EMAIL']['SMTP_PORT']
            self.smtp_timeout = config['EMAIL']['SMTP_TIMEOUT']
            self.smtp_user = config['EMAIL']['SMTP_USER']
            self.smtp_pass = config['EMAIL']['SMTP_PASS']
            self.charset = config['EMAIL']['CHARSET']
            self.from_addr = config['EMAIL']['FROM_ADDR']
            self.to_addrs = config['EMAIL']['TO_ADDR']
            self.receivers = self.to_addrs.split(",")
            self.debug_mode = config['EMAIL'].getboolean('DEBUG_MODE')

        def is_debug(self):
            return self.debug_mode

        def compose_email_body(self, graphics, online_bug_source):
            msg_content = MIMEMultipart('related')
            msg_content['From'] = "{}".format(self.from_addr)
            msg_content['To'] = ",".join(self.receivers)
            msg_content['Subject'] = '[Tech Index] online bug report'

            msg_template = self.generate_msg_template_according_to_graphics(graphics)

            msg_content = self.fill_content_into_template(graphics, msg_content, msg_template)
            msg_content = self.attach_binary_csv_into_content(online_bug_source, msg_content)
            return msg_content

        def send_email(self, msg_content):
            print(self.from_addr)
            print(self.smtp_pass)
            smtp = None
            try:
                smtp = smtplib.SMTP_SSL(
                    host=self.smtp_host,
                    port=self.smtp_port,
                    timeout=int(self.smtp_timeout),
                )
                smtp.connect(host=self.smtp_host, port=self.smtp_port)
                smtp.login(self.smtp_user, self.smtp_pass)
                smtp.sendmail(self.from_addr, self.receivers, msg_content)
                smtp.close()
                debug_log_console(str(self.from_addr))
                debug_log_console(str(self.receivers))
                debug_log_console('mail send finished.')

            except (Exception,) as e:
                send_err = str(e)
                print(send_err)
            finally:
                if smtp is not None:
                    print("smtp close")
                    smtp.close()

        @staticmethod
        def attach_binary_csv_into_content(online_bug_source, msg_content):
            msg_content.attach(MIMEText("source.csv"))
            part = MIMEApplication(online_bug_source, Name="source.csv")
            part['Content-Disposition'] = 'attachment; filename="%s"' % "source.csv"
            msg_content.attach(part)
            return msg_content

        @staticmethod
        def fill_content_into_template(graphics, msg_content, msg_template):
            msg_content.attach(msg_template)
            index = 0
            for graphic in graphics:
                if graphic is None:
                    continue
                msg_image = MIMEImage(graphic)
                msg_image.add_header('Content-ID', '<' + str(index) + '>')
                index += 1
                msg_content.attach(msg_image)
            return msg_content

        @staticmethod
        def generate_msg_template_according_to_graphics(graphics):
            content = '<p>Hello guys,</p><br/> ' \
                      'This is one of the tech team index: <b>online bug summary</b>. ' \
                      + str(len(graphics)) + ' analysis graphics as followed<br/><p>' \
                                             '<table border="1">'
            for index in range(len(graphics)):
                content += '<tr><td><img src="cid:' + str(index) + '"><br><p></td></tr>'
            content += "</table>"
            return MIMEText(content, 'html', 'utf-8')

    instance = None

    def __init__(self):
        if not JbaEmail.instance:
            JbaEmail.instance = JbaEmail.__JbaEmail(getpass.getuser())


def send_email_from_graphics(graphs_full_path, online_bug_source):
    jba_email = JbaEmail().instance
    email_body = jba_email.compose_email_body(graphs_full_path, online_bug_source)
    write_html_to_file("test.eml", email_body.as_string())
    jba_email.send_email(email_body.as_string())

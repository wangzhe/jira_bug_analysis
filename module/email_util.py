import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from module.sys_invariant import smtpserver, sender, receiver


def compose_email_body(graphics):
    msg_content = MIMEMultipart('related')
    msg_content['Subject'] = '[Tech Index] online bug report'

    msg_template = generate_msg_template_according_to_graphics(graphics)
    msg_content = fill_content_into_template(graphics, msg_content, msg_template)
    return msg_content


def fill_content_into_template(graphics, msg_content, msg_template):
    msg_content.attach(msg_template)
    index = 0
    for file in graphics:
        fp = open(file, 'rb')
        msg_image = MIMEImage(fp.read())
        fp.close()
        msg_image.add_header('Content-ID', '<' + str(index) + '>')
        index += 1
        msg_content.attach(msg_image)
    return msg_content


def generate_msg_template_according_to_graphics(graphics):
    content = '<p>Hello guys,</p><br/> ' \
              'This is one of the tech team index: <b>online bug summary</b>. ' \
              + str(len(graphics)) + ' analysis graphics as followed<br/><p>'
    for index in range(len(graphics)):
        if index % 2 == 0:
            content += '<img src="cid:' + str(index) + '"><br>'
        else:
            content += '<img src="cid:' + str(index) + '">'
    return MIMEText(content, 'html', 'utf-8')


def send_email(msg_content):
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.sendmail(sender, receiver, msg_content.as_string())
    smtp.quit()

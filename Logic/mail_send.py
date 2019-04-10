# coding=utf-8
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
import sys
sys.path.append('E:\MyProgram\InterfaceTestFrame\Config')
from Config.read_config import DealCommonCfg


# 接口超时预警邮件,发送文本格式的邮件
class MailSend:
    dcc = DealCommonCfg()
    mylist = dcc.read_config('email_qq')                                                # 获得配置文件中的信息内容
    mydic = {}                                                                          # 将获得的内容转换为字典类型
    for i in mylist:
        mydic[i[0].encode('UTF-8')] = i[1].encode('UTF-8')
    smtp_server = mydic['smtp_server']                                                  # QQ的SMTP服务器地址
    sender_qq_adr = mydic['sender_qq_adr']                                              # 发送人的邮箱地址
    password = mydic['password']                                                        # QQ邮箱的授权码
    receiver_qq_adr = mydic['receiver_qq_adr']                                          # 收件人的邮箱地址
    mail_to_copy = mydic['mail_to_copy']                                                        # 抄送人的邮箱地址

    def overtime_warn(self,mail_title):
        mail_content = 'warn,interface request overtime,please look out!!'  # 邮件的正文内容
        mail_title = mail_title  # 邮件标题

        smtp = SMTP_SSL(self.smtp_server)  # SSL登录
        smtp.set_debuglevel(1)  # 用来调试的，1为开启调试模式，可以在控制台打印出和SMTP服务器交互的所有信息
        smtp.ehlo(self.smtp_server)  # what't mean
        smtp.login(self.sender_qq_adr, self.password)  # 登录SMTP服务器

    # 邮件主题、如何显示发件人、收件人等信息并不是通过SMTP协议发给MTA,而是包含在发给MTA的文本中的
        msg = MIMEText(mail_content, 'plain', 'utf-8')  # 构造MIMEText对象
        msg['Subject'] = Header(mail_title, 'utf-8')
        msg['From'] = self.sender_qq_adr                 # 将邮件主题、发件人和收件人添加到MIMEText中
        msg['To'] = self.receiver_qq_adr
        # 邮件正文是一个str，所以需要将MIMEText对象变成str类型，这一个特别注意，是将对象转换成字符串类型的方法
        smtp.sendmail(self.sender_qq_adr, self.receiver_qq_adr,
                    msg.as_string())
        print('send ok')

        smtp.quit()

    # 接口请求测试完成后的通知邮件,发送html格式的邮件
    def send_mail(self,text):
        subject = '[AutomantionTest]接口自动化测试报告通知'  # 邮件标题
        username = '893026750'  # 用户邮箱的账号

        msg = MIMEText(text, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = self.sender_qq_adr
        msg['To'] = ';'.join([self.receiver_qq_adr])
        msg['Cc'] = ';'.join([self.mail_to_copy])
        smtp = SMTP_SSL(self.smtp_server)
        smtp.connect(self.smtp_server)
        smtp.login(username, self.password)
        smtp.sendmail(self.sender_qq_adr, [self.receiver_qq_adr] + [self.mail_to_copy], msg.as_string())
        smtp.quit()

from __future__ import print_function
from mailer import Mailer


def main():
    mail_settings = {'subject': "Test mail",
                     'to': ["recepient@gmail.com"],
                     'from': "recepient@gmail.com",
                     'smtp_server': "smtp.gmail.com",
                     'smtp_user': "recepient@gmail.com",
                     'smtp_password': "abcdefghijkl",
                     'smtp_port': "465"
                     }

    text = "\t\t\tMy Mail\n" \
           "================================\n" \
           "Hello World!\n" \
           "Good bye!"

    print ("Going to send email")
    m = Mailer()
    res = m.mail(text, "my_docs", mail_settings)
    if res:
        print ("Send succeeded")
    else:
        print("Send failed")


if __name__ == '__main__':
    main()

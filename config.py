# Configurations for CertificateChecker
class Config:
    # directory for log files
    LOG_DIR = "./logs"
    # filename of the input file
    FILENAME = "ServerList.txt"
    # link to input file both in raw for download and normal view for users
    URL_RAW = "https://github.wdf.sap.corp/raw/Certificatechecker/CertificateChecker/master/{}".format(FILENAME)
    URL_USER = "https://github.wdf.sap.corp/Certificatechecker/CertificateChecker/blob/master/{}".format(FILENAME)
    # link to repository
    URL_REPOSITORY = "https://github.wdf.sap.corp/Certificatechecker/CertificateChecker"
    # determines where to send error messages if errors occur 
    ADMIN_MAILS = ["kunal.suresh@sap.com"]
    # details for sending out mails
    SMTP_SERVER = "mail.sap.corp:587"
    MAIL_SUBJECT = "Certificate Checker"
    MAIL_SENDER = "noreply+it-tools-certcheck@sap.corp" 
    # set the max time before terminating the script in seconds
    MAX_TIME = 7200

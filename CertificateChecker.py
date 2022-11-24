#!/usr/bin/env python3
import datetime
import fileinput
import logging
import os
import socket
import ssl
import time
import sys
import urllib.request

from multiprocessing import Process
from ssl_expiry import ssl_expiry_datetime
from mail import sendMail
from config import Config

def certificateChecker(smtppw):
    # create a directory for logs 
    logDir = Config.LOG_DIR
    if not os.path.isdir(logDir):
        os.makedirs(logDir)
    # initialize logger
    now = datetime.datetime.today().strftime('%Y-%m-%d')
    logging.basicConfig(filename='logs/{}.CertificateChecker.log'.format(now), format='%(asctime)s %(levelname)s: %(message)s', filemode='w', level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info("Start CertificateChecker")
    # determines where to send crash reports
    adminMails = Config.ADMIN_MAILS

    # Download the most recent version of the server list file
    filename = Config.FILENAME
    urlRaw = Config.URL_RAW
    urlUser = Config.URL_USER
    urlRepo = Config.URL_REPOSITORY

   # try:
    #    filename, headers = urllib.request.urlretrieve(urlRaw, filename=filename)
    #    textbody = "Downloaded '{}' from git.".format(filename)
    #    logging.info(textbody)
  #  except Exception as e:
  #      textbody = ("Error when trying to download input file from '{}'."
   #                 "\n \t {}"
   #                 "\n \t Program will abort further execution.").format(urlUser, e)
   #     logging.error(textbody)
    #    sendMail(adminMails,textbody)
    #    sys.exit(1)

    # Read in the Certificate input file (kind of redundant now)
    if not os.path.isfile(filename):
        logging.error("{} not found. Please make sure it is in the same directory".format(filename))
        sys.exit(1)

    with open(filename, encoding='utf-8-sig') as f:
        lines = (line.strip() for line in f)
        # ignore blank lines and comments, inline comments are still an issue
        lines = (line for line in lines if line and not line.startswith("#")) 
        # remove the https from the urls
        lines = (line.replace("https://","") for line in lines)
        # create list element out of the generator 
        lines = list(lines)

    for line in lines:
        # make sure the input format is correct
        try:
            lineList = line.split(';')
            logging.info("Start to check Certificate for {}".format(lineList[0]))
            # get port number if necessary
            if ':' in lineList[0]:
                hostname,port = lineList[0].split(':')
                port = int(port)
            else:
                hostname = lineList[0]
                port = 443

            daysFile = int(lineList[1])
            # ignore SAP-exernal mails, ensure treatmet of several mail addresses
            mailRecipient = [mail for mail in lineList[2:] if "sap.corp" in mail or "sap.com" in mail or "corp.sap" in mail]
        except:
            textbody = "Erroneous input format in the following line: \n \t {}".format(line)
            sendMail(adminMails,textbody,smtppw)
            logging.error(textbody)
            continue
        
        # if no valid email was found, send mail to admins and continue
        if not mailRecipient:
            textbody = ("No or invalid (SAP-external) email address in the following line: \n \t {}"
                        "\n \t Certificate will not be checked!").format(line)
            logging.warning(textbody)
            sendMail(adminMails,textbody,smtppw)
            continue

        # check ssl certificate and send mail if error occurs
        try:
            logging.debug("Connecting to url '{}'".format(hostname))
            date = ssl_expiry_datetime(hostname, port)
            logging.debug("Successfully read certificate info for url '{}'".format(hostname))
            # determine the remainig days
            rem_days = int((date - datetime.datetime.utcnow()).days)
        except Exception as e:
            textbody = ("Error for url '{}': \n \t {}. \n \t Please maintain the correct format in '{}' as described in the instructions."
                        "\n \t For more information as to why you receive this mail, please read the description in the gitbub repository: {}"
                        "\n \t Address questions with regards to this automatic warning to {}").format(lineList[0], e, urlUser, urlRepo, adminMails)
            logging.error(textbody)
            sendMail(mailRecipient, textbody,smtppw)
            logging.info("Sent mail to '{}'".format(mailRecipient))
            # directly continue since comparison is unnecessary in case of error 
            continue
            
        # compare days and send email if expiration date stated in input file is smaller than the actual
        if rem_days < daysFile: 
            textbody = ("Warning for url '{}': \n \t Certificate will expire in {} days.\n \t Date of expiration: {}"
                        "\n \t PLEASE RENEW THE CERTIFICATE !"
                        "\n \t Warning for expiration check is set to {} days."
                        "\n \t For more information as to why you receive this mail, read the description in the gitbub repository: {}"
                        "\n \t In case of questions with regards to Certificate Checker please contact {}.").format(lineList[0], rem_days, date, daysFile, urlRepo, adminMails)
            logging.warning(textbody)
            sendMail(mailRecipient, textbody,smtppw)
            logging.info("Sent mail to '{}'".format(mailRecipient))
        else:
            logging.info("No mail sent because certificate won't expire within {} days. Certificate is valid until {}".format(daysFile, date))
        
    logging.info("End CertificateChecker")

if __name__ == '__main__':
    smtppw = sys.argv[1]
    # introduce a timeout for the whole checking process 
    process = Process(target=certificateChecker, args=(smtppw,))
    # start the checking routine and block for certain time span
    process.start()
    process.join(timeout=Config.MAX_TIME)
    # terminate the process if it's still running 
    if process.is_alive():
        process.terminate()
        print("CertificateChecker exceeded its time limit ({} seconds) and was terminated!".format(Config.MAX_TIME))



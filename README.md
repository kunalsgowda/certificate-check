# CertificateChecker

CertificateChecker is a program that periodically checks on ssl certificates and informs you per email when the remaining valid days 
fall below a certain threshold. Please manage your entries by yourself by changing *ServerList.txt* via pull request. 

## Usage 

If you want a url to be checked, you can add it to *ServerList.txt* via **pull request** using the following scheme:
```
<url>;<threshold>;<your_Mail1>;[another_Mail];...
```
**Example**:
```
https://hcp-deploy.mo.sap.corp:8443;30;myMail@sap.com;secondMail@sap.com
```
In this example, the CertificateChecker will send out a mail to both email addresses, if the remaining valid days of the ssl Certificate for
the url drop below 30 days. 

### Features and Limitations

* SAP external email addresses will be ignored!
* At least one email address must be stated, but several are supported. 
* Empty lines or line comments can be used to improve readability.
* Inline comments are not supported!

Here is another more **extensive example**:
```
# nwdi test landscape:
https://dtr8800.wdf.sap.corp:50001;25;firstMail@exchange.sap.corp;secondMail@sap.com;thirdMail@sap.com
https://sldinternal.wdf.sap.corp:53601;50;d051256@exchange.sap.corp

# perforce infrastructure:
https://pie.wdf.sap.corp:443;30;d051256@exchange.sap.corp
https://pietest.wdf.sap.corp:443;40;d051256@exchange.sap.corp
```


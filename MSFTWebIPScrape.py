from urllib import urlopen
from re import search, match
from socket import gethostbyname
from time import strftime
from sys import exc_info
from email.mime.text import MIMEText
import smtplib


# The below function connects to an arbitrary webpage (defined in a
# configuration file) and looks for IP addresses in that webpage, and
# then writes the corresponding CIDR notation of those IP addresses
# to a file.
def GetMSFTWebIPs(URL):
    """ Retrieve IPs that are listed on a webapge."""
    IPs = []
    temp_data = []
    data_page = URL
    IP_Rgx = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    CIDR_Rgx = r'(.*?)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{2})'
    try:
        for a in urlopen(data_page):
            if search(IP_Rgx, a):
                for b in a.split(','):
                    temp_data.append(b)
    except IOError:
        print exc_info()[:2]
        print 'Unable to make connection to ', data_page
        exit(1)
    for c in temp_data:
        if match(CIDR_Rgx, c):
            p_holder = match(CIDR_Rgx, c)
            IPs.append(p_holder.group(2))
    return IPs


# The below function is a simple mailer.
def MailSend(mail_sender, mail_recipients, mail_server, mail_body):
    """Simple function to send mail."""
    msg = MIMEText(mail_body)
    msg['Subject'] = 'MSFT IP Scrape'
    msg['From'] = mail_sender
    msg['To'] = mail_recipients
    s = smtplib.SMTP(gethostbyname(mail_server), '25')
    s.sendmail(mail_sender, mail_recipients, msg.as_string())


# Defining the location of the configuration and reading its contents
# to obtain the necessary configurations.
conf_File = 'WebIPs.conf'
conf = open(conf_File, 'r+b')
URLs = []
for line in conf:
    if search(r'^web_page.*?=', line):
        urls = search(r'(?<=^web_page = )\S+', line)
        URLs.append(urls.group(0))
    elif search(r'^results_file.*?=', line):
        rf = search(r'(?<=^results_file = )\S+', line)
        results_file = open(rf.group(0), 'w')
    elif search(r'^smtp_server.*?=', line):
        s_server = search(r'(?<=^smtp_server = )\S+', line)
        server = s_server.group(0)
    elif search(r'^email.*?=', line):
        recip = search(r'(?<=^email = )\S+', line)
        rcpts = recip.group(0)
    elif search(r'^from_addr.*?=', line):
        sndr = search(r'(?<=^from_addr = )\S+', line)
        sender = sndr.group(0)

# Executing the function to get IPs.
IP_List = []
for url in URLs:
    print 'Retrieving data from ' + url + '\n'
    IP_List = GetMSFTWebIPs(url)

# Writing the IPs to a file.
for ip in IP_List:
    results_file.write(ip + '\n')

# Emailing a report and wrapping up the script.
c_time = strftime('%H:%M:%S')
IP_tally = len(IP_List)
body = ('The webscrape for IPs completed at %s.  A total of %d IPs ' +
        'have been written to %s.  If you notitce any errors, please ' +
        'contact IT Security.') % (c_time, IP_tally, rf.group(0))
try:
    MailSend(sender, rcpts, server, body)
except NameError:
    print exc_info()[:2]
    print ('Undefined variable encounterd in mailing the report.')
    exit(1)
finally:
    conf.close()
    results_file.close()

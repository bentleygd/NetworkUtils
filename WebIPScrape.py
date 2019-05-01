from urllib import urlopen
from re import search, match


def GetWebIPs(URL):
    """ Retrieve IPs that are listed on a webapge."""
    IPs = []
    temp_data = []
    matched_data = []
    data_page = URL
    IP_Rgx = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    CIDR_Rgx = r'(.*?)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{2})'
    for a in urlopen(data_page):
        if search(IP_Rgx, a):
            temp_data.append(a.split(',')
    for b in temp_data:
        p_holder = match(CIDR_Rgx, b)
        
    return IPs


Conf_File = 'WebIPs.conf'
Conf = open(Conf_File, 'r+b')
URLs = []
for line in Conf:
    if search('^web_page =', line):
        urls = search('(?<=^web_page = )\S+', line)
        URLs.append(urls.group(0))
    elif search('^results_file =', line):
        rf = search('(?<=^results_file = )\S+', line)
        results_file = open(rf.group(0), 'w+b')

IP_List = []
for url in URLs:
    print 'Retrieving data from ', url
    IP_List = GetWebIPs(url)

for ip in IP_List:
    results_file.write(str(ip))

Conf.close()
results_file.close()

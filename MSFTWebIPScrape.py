from urllib import urlopen
from re import search, match


# The below function connects to an arbitrary webpage defined in a
# configuration file and looks for IP addresses in that webpage, and
# then writes the corresponding CIDR notation of those IP addresses
# to a file.
def GetMSFTWebIPs(URL):
    """ Retrieve IPs that are listed on a webapge."""
    IPs = []
    temp_data = []
    data_page = URL
    IP_Rgx = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    CIDR_Rgx = r'(.*?)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{2})'
    for a in urlopen(data_page):
        if search(IP_Rgx, a):
            for b in a.split(','):
                temp_data.append(b)
    for c in temp_data:
        if match(CIDR_Rgx, c):
            p_holder = match(CIDR_Rgx, c)
            IPs.append(p_holder.group(2))
    return IPs


# Defining the location of the configuration and reading its contents
# to obtain the necessary configurations.
Conf_File = 'WebIPs.conf'
Conf = open(Conf_File, 'r+b')
URLs = []
for line in Conf:
    if search(r'^web_page =', line):
        urls = search(r'(?<=^web_page = )\S+', line)
        URLs.append(urls.group(0))
    elif search(r'^results_file =', line):
        rf = search(r'(?<=^results_file = )\S+', line)
        results_file = open(rf.group(0), 'w')

# Executing the function to get IPs.
IP_List = []
for url in URLs:
    print 'Retrieving data from ', url
    IP_List = GetMSFTWebIPs(url)

# Writing the IPs to a file.
for ip in IP_List:
    results_file.write(ip + '\n')

Conf.close()
results_file.close()

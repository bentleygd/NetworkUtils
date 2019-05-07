# NetworkUtils
Python scripts to automate network administration related tasks.

MSFTWebIPScrape.py
This Python utility scrapes a web page and writes the results to a file.  The below configuration tags must be present in WebIP.conf configuration file.
An example configuration is also included below.

"results_file = "
This tag is for the location where the script will write the results.

"web_page = "
This tag indicates which URLs to scrape for IPs.

"smtp_server = "
The SMTP server that will send the notification that the script completed.

"email = "
The recipient address for the notification.

"from_addr = "
The email address that will appear to send the email.

EXAMPLE CONFIGURATION:

results_file = Results.txt

web_page = https://www.example.com

smtp_server = smtp_server.example.com

email = dudefella@domain.com

from_addr = pythonbot@domain.com
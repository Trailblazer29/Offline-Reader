import http.client
import re
import os
import urllib.request

#Downloading webpage

print("Website: ")
website = input()
print("URL: ")
URL = input()

HTTPConnect = None

if URL.startswith("https:"):
    HTTPConnect = http.client.HTTPSConnection(website)
else:
    HTTPConnect = http.client.HTTPConnection(website)
    
HTTPConnect.request("GET", URL)

response = HTTPConnect.getresponse()

result_file = open("index.html","wb")

received = response.read(1024)

while len(received)!=0:
    result_file.write(received)
    received = response.read(1024)
    
result_file.close()

#Downloading resources

folder_name = URL.split('/')[-1].split('.')[0]
os.mkdir(folder_name)
os.chdir(folder_name)
main_file = open("../index.html","rb")
file_content = ""
for line in main_file:
    file_content+=line.decode("unicode_escape")
main_file.close()
resources = re.findall('"[^"]+\.css"|"[^"]+\.js"|"[^"]+\.png"|"[^"]+\.jpeg"|"[^"]+\.xss"|"[^"]+\.ico"',file_content,re.M)

with open('../index.html', 'rb') as old_webpage:
    data = old_webpage.read().decode("unicode_escape")
    
for result in resources:
    URL = result.replace('"','')
    file_name = URL.split('/')[-1]
    data = re.sub(result,'"'+folder_name+'/'+file_name+'"',data) 
    if URL.startswith("//"):
        URL = "https:" + URL
    elif URL.startswith('/'):
        URL = "https://" + website + URL
    print(URL)
    try:
        urllib.request.urlretrieve(URL, file_name)
    except: 
        continue

#New webpage (local resources)
with open("../local_index.html", "wb") as new_webpage:
    new_webpage.write(data.encode())

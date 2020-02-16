#REF: https://ip-api.com/docs/api:json

import multiprocessing as mp
import requests
import json
import csv
import traceback

base_url = 'http://ip-api.com/json/{0}?fields=status,message,country,regionName,city,lat,lon,isp,org,mobile,query'
print("CPUs: {0}".format(mp.cpu_count()))

def scraper(url):
  try:
    api_response = requests.get(url, timeout=5)
    print(api_response.status_code)
    if api_response.status_code == 200:
      content = api_response.text
      obj = json.loads(content)
      print(obj)
      with open('networks.csv','a+') as new_file:
        csv_writer = csv.writer(new_file, delimiter=',',lineterminator='\n')
        csv_writer.writerow([obj])
  except Exception:
    traceback.print_exc()

if __name__ == '__main__':
  with mp.Pool(mp.cpu_count()) as pool:
    with open('ips.csv', 'r', encoding="utf8") as csv_file:
      csv_reader = csv.reader(csv_file)
      urls = [base_url.format(line[0]) for line in csv_reader]
      pool.map(scraper, urls)


print("FINISHED!")

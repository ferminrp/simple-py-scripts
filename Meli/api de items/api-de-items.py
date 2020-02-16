import multiprocessing as mp
import requests
import json
import csv
import traceback

base_url = 'https://api.mercadolibre.com/items?ids=MLA{0}'
print("CPUs: {0}".format(mp.cpu_count()))

def scraper(url):
  try:
    api_response = requests.get(url, timeout=5)
    if api_response.status_code == 200:
      content = api_response.text
      obj = json.loads(content)
      #title = obj["title"]
      #price = obj["price"]
      #base_price = obj["base_price"]
      #original_price = obj["original_price"]
      #item_url = obj["permalink"]
      #free_shipping = obj["shipping"]["free_shipping"]
      #thumbnail = obj[0]["body"]["thumbnail"]
      #category = obj["category_id"]
      #product = obj["catalog_product_id"]
      status = obj[0]["body"]["status"]
      item_id = url.replace('https://api.mercadolibre.com/items?ids=MLA','')
      with open('results.csv','a+') as new_file:
        csv_writer = csv.writer(new_file, delimiter=',',lineterminator='\n')
        csv_writer.writerow([item_id,status])
  except Exception:
    traceback.print_exc()



if __name__ == '__main__':
  with mp.Pool(mp.cpu_count()) as pool:
    with open('data.csv', 'r', encoding="utf8") as csv_file:
      csv_reader = csv.reader(csv_file)
      urls = [base_url.format(line[0]) for line in csv_reader]
      pool.map(scraper, urls)




print("FINISHED!")
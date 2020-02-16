import multiprocessing as mp
import requests
import json
import csv
import traceback

base_url = 'https://www.instagram.com/{0}/?__a=1'
print("CPUs: {0}".format(mp.cpu_count()))

def scraper(url):
  try:
    # Only runs process if the endpoint returns 200 response
    api_response = requests.get(url, timeout=5)
    print(api_response.status_code)
    if api_response.status_code == 200:
      #parses api content as json
      content = api_response.text
      obj = json.loads(content)
      #extracts username and profile image from json
      username = obj["graphql"]["user"]["username"]
      print(username)
      profile_img = obj["graphql"]["user"]["profile_pic_url_hd"]
      #appends data to new image.csv file.
      with open('images.csv','a+') as new_file:
        csv_writer = csv.writer(new_file, delimiter=',',lineterminator='\n')
        csv_writer.writerow([username,profile_img])
  except Exception:
    traceback.print_exc()


# Opens accounts.csv file and starts scrapping those accounts.
if __name__ == '__main__':
  with mp.Pool(mp.cpu_count()) as pool:
    with open('accounts.csv', 'r', encoding="utf8") as csv_file:
      csv_reader = csv.reader(csv_file)
      urls = [base_url.format(line[0]) for line in csv_reader]
      pool.map(scraper, urls)


print("FINISHED!")

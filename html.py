from bs4 import BeautifulSoup as BS
import pycurl, cStringIO
import os

all_recipes_choc_chips = 'http://allrecipes.com/search/default.aspx?wt=chocolate%20chip%20cookies'

# go to beautifulsoup and return page listed above
def fetch_page(url):
	buf = cStringIO.StringIO()
	c = pycurl.Curl()
	c.setopt(c.URL, str(url))
	c.setopt(c.WRITEFUNCTION, buf.write)
	c.perform()
	data = BS(buf.getvalue())
	buf.close()
	return data

def write_page(url, filepath):
	data = fetch_page(url)
	f = open(filepath,'w')
	f.write(str(data))

folder_path = 'downloaded_recipes'
if os.path.isdir(folder_path):
	files = os.listdir(folder_path)
	for f in files:
		os.remove(os.path.join(folder_path,f))
else: 
	os.mkdir(folder_path)


def download_page_results(url, file_counter):
	search_results_soup = fetch_page(url)
	search_tags = search_results_soup.findAll('div','searchImg_result')

	recipe_links = [result.a['href'] for result in search_tags]

	# fetch and save each link to a file
	for recipe in recipe_links:
		file_counter += 1
		print recipe
		write_page(recipe, os.path.join(folder_path,str(file_counter) + '.txt'))
	return len(recipe_links)

# go get next page on search results. ITERATE ABOVE
page_counter = 1
file_counter = 0
url = all_recipes_choc_chips + '&Page=' + str(page_counter)
while download_page_results(url, file_counter) > 0:
	page_counter+=1
	file_counter += 20
	url = all_recipes_choc_chips + '&Page=' + str(page_counter)

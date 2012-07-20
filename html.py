from bs4 import BeautifulSoup as BS
import pycurl, cStringIO
import os
from threading import Lock, Thread
from Queue import Queue

all_recipes_choc_chips = 'http://allrecipes.com/search/default.aspx?wt=chocolate%20chip%20cookies'

class FileSteward:
	def __init__(self, folder_path):
		self.folder = folder_path
		self.lock = Lock()
		self.file_counter = 0
	def get_next(self):
		self.lock.acquire()
		self.file_counter += 1
		counter = self.file_counter
		self.lock.release()
		file_name = os.path.join(self.folder, str(counter)+'.txt')
		return file_name

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

def write_page_queue(data, filepath):
	f = open(filepath, 'w')
	f.write(str(data))

folder_path = 'downloaded_recipes'
file_daemon = FileSteward(folder_path)
if os.path.isdir(folder_path):
	files = os.listdir(folder_path)
	for f in files:
		os.remove(os.path.join(folder_path,f))
else: 
	os.mkdir(folder_path)

def page_fetch_worker():
	while True:
		page = url_queue.get()
		data = fetch_page(page)
		print "page fetched for %s" % (page)
		write_queue.put(data)
		url_queue.task_done()
		if url_queue.empty():
			break

def page_write_worker():
	while True:
		page = write_queue.get()
		filename = file_daemon.get_next()
		print("Writing data to %s" % filename)
		write_page_queue(page, filename)
		write_queue.task_done()

def download_page_results(url):
	search_results_soup = fetch_page(url)
	search_tags = search_results_soup.findAll('div','searchImg_result')
	return [result.a['href'] for result in search_tags]

page_counter = 1
num_worker_threads = 5
url_queue = Queue()
write_queue = Queue()
url = all_recipes_choc_chips + '&Page=' + str(page_counter)

# initialize threads
for i in range(num_worker_threads):
	w = Thread(target=page_write_worker)
	u = Thread(target=page_fetch_worker)
	w.daemon = True
	u.daemon = True
	w.start()
	u.start()

recipe_links = download_page_results(url)
while len(recipe_links) > 0:
	for recipe_link in recipe_links:
		url_queue.put(recipe_link)
	page_counter+=1
	url = all_recipes_choc_chips + '&Page=' + str(page_counter)
	recipe_links = download_page_results(url)

url_queue.join()
write_queue.join()

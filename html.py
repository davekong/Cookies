from bs4 import BeautifulSoup as BS
import pycurl, cStringIO
import os
from threading import Lock, Thread
from Queue import Queue

# FileSteward class (used to increment file numbers)
class FileSteward:
	instance = None
	@staticmethod
	def shared():
		if FileSteward.instance is None:
			FileSteward.instance = FileSteward()
		return FileSteward.instance
	def __init__(self):
		self.lock = Lock()
		self.file_counter = 0
	def set_path(self, folder_path):
		self.folder = folder_path
	def get_next(self):
		self.lock.acquire()
		self.file_counter += 1
		counter = self.file_counter
		self.lock.release()
		file_name = os.path.join(self.folder, str(counter)+'.txt')
		return file_name

# Constants
all_recipes_choc_chips = 'http://allrecipes.com/search/default.aspx?wt=chocolate%20chip%20cookies%s'
all_recipes_url_string = '&Page=' 
all_recipes_page_increment = 1
all_recipes_html = 'div'
all_recipes_html_class = 'searchImg_result'

cooks_url = 'http://www.cooks.com'
cooks_choc_chips = 'http://www.cooks.com/rec/doc/0,1-%s,chocolate_chip_cookie,FF.html'
cooks_page_increment = 10
cooks_html = 'div'
cooks_html_class = 'regular'

file_daemon = FileSteward.shared() 
num_worker_threads = 5
url_queue = Queue()
write_queue = Queue()

# go to beautifulsoup and return page listed above
def fetch_page(url):
	print "fetching page %s" % str(url)
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


def page_fetch_worker():
	while True:
		page = url_queue.get()
		data = fetch_page(page)
		print "page fetched for %s" % (page)
		write_queue.put(data)
		url_queue.task_done()

def page_write_worker():
	while True:
		page = write_queue.get()
		filename = file_daemon.get_next()
		print("Writing data to %s" % filename)
		write_page_queue(page, filename)
		write_queue.task_done()

def download_page_results(url):
	search_results_soup = fetch_page(url)
	#search_tags = search_results_soup.findAll('div','searchImg_result')
	search_tags = search_results_soup.findAll(cooks_html, cooks_html_class)
	return [result.a['href'] for result in search_tags]

def download_from_sites(download_path):
	page_counter = 1
	url = cooks_choc_chips % (str(page_counter))
	#url = all_recipes_choc_chips % (all_recipes_url_string +  str(page_counter))
	file_daemon.set_path(download_path)
	
	if os.path.isdir(download_path):
		raise Exception("Folder %s already exists." % download_path)
	else: 
		os.mkdir(download_path)
	
	# initialize threads
	for i in range(num_worker_threads):
		for target in [page_write_worker, page_fetch_worker]:
			t = Thread(target=target)
			t.daemon = True
			t.start()


	recipe_links = download_page_results(url)
	while len(recipe_links) > 0:
		for recipe_link in recipe_links:
			url = cooks_url + recipe_link
			url_queue.put(cooks_url + recipe_link)
		page_counter+= cooks_page_increment
		url = cooks_choc_chips % (str(page_counter))
		recipe_links = download_page_results(url)

	url_queue.join()
	write_queue.join()

	return download_path 

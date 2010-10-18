# !/usr/bin/env python
import sys, thread # kudos to Nicholas Herriot (see comments)
import gtk
import webkit
#import warnings
 
#warnings.filterwarnings('ignore')
 
class WebView(webkit.WebView):
	def get_html(self):
		self.execute_script('oldtitle=document.title;document.title=document.documentElement.innerHTML;')
		html = self.get_main_frame().get_title()
		self.execute_script('document.title=oldtitle;')
		return html
 
class CrawlerJS(gtk.Window):
	def __init__(self, url):
		gtk.gdk.threads_init() # suggested by Nicholas Herriot for Ubuntu Koala
		gtk.Window.__init__(self)
		self._url = url
 
	def crawl(self):
		view = WebView()
		view.open(self._url)
		view.connect('load-finished', self._finished_loading)
		self.add(view)
		gtk.main()
 
	def _finished_loading(self, view, frame):
	#	with open(self._file, 'w') as f:
	#		f.write(view.get_html())
                sys.stdout.write(view.get_html())
		gtk.main_quit()
 
 
#if __name__ == '__main__':
	#main()


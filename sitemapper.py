#!/usr/bin/env python
import sys
import re
import urllib
import urllib2
#import urllib.parse
#import urllib.error


class SiteMapper:
	url        = None
	domain     = None
	verbose    = False
	user_agent = "SiteMapper/0.4  manvscode.com"
	visited    = []

	def __init__( self, url, verbose = False ):
		self.url     = url.strip( )
		self.verbose = verbose
		self.domain  = urllib2.Request( url ).get_host( )


	def map( self ):
		return self._map( self.url )	

	def _map( self, url ):
		if self.verbose:
			print url + " is_outside=" + str(self.is_outside_url(url)) + " is_path=" + str(self.is_path(url))

		if url in self.visited or self.is_outside_url( url ):
			return


		try:	
			request  = urllib2.Request( url )
			request.add_header( 'User-Agent', self.user_agent )
			response = urllib2.urlopen( request )
			the_page = response.read( )
			new_urls = self.extract_urls( the_page )
		except ValueError:
			return
		finally:
			self.visited.append( url )


		for url in self.extract_urls( the_page ):
			self._map( url )
		return	

	def is_outside_url( self, url ):
		T = re.match( self.domain, url )
		if T != None or self.is_path( url ):
			return False
		else:
			return True

	def write( self, filename ):
		self.visited.sort( )
		out = open( filename, 'w' )
		for url in self.visited:
			out.write( url + "\n" )
		out.close()
	
	def is_path( self, url ):
		return (re.match( '^/(\S*)', url ) != None or re.match( '^(\S+)(/*)', url ) != None) and re.match('http://(\S+)/', url ) == None

	def extract_urls( self, page ):
		urls = []
		matches = re.findall( '(src|href)(\s*)=(\s*)(\'|\")(\S+)(\'|\")', page, re.I | re.M )
		for match in matches:
			urls.append( match[ 4 ] )
		return urls


#------------------------------------------------------------#

if len(sys.argv) <= 1:
	print "Need to know the URL\n"
	sys.exit( )
else:
	myurl = sys.argv[ 1 ].strip( )
	mapper = SiteMapper( myurl, True )
	mapper.map( )
	mapper.write( "urls.txt" )

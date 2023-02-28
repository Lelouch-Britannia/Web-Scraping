from bs4 import BeautifulSoup 
import requests 
import os
import csv
import argparse


def Parser():
	# create a new ArgumentParser object
	parser = argparse.ArgumentParser(
	    prog="Web Scraping", # name of the program
	    description="Program to scrape <p> tag from website", # program description
	    epilog="Thank you for using it!!", # text displayed at the end of help output
	    argument_default=argparse.SUPPRESS, # don't show default values in help output
	    allow_abbrev=True, # allow abbreviations for long options
	    fromfile_prefix_chars="@" # support reading options and arguments from a file
	)

	# add a positional argument for the URL of the website to be scraped
	parser.add_argument("url")

	# add an optional argument for the URL of the website to be scraped
	parser.add_argument(
	    "-u", "--url", # option flags for the argument
	    action="store_true", # specify that the argument does not take a value
	    required=True, # make this argument required
	    help="URL to Website" # help message displayed in the help output
	)

	# parse the command-line arguments and return the value of the "url" argument
	args = parser.parse_args()
	return args.url





def Web_Scraper_main():

	# get the URL of the website to be scraped from the command-line arguments
	url = Parser()

	# send a GET request to the website
	response = requests.get(url)

	# check if the response status code is 200 (OK)
	if response.status_code != 200:
		# if not, print an error message and exit the program
		raise SystemExit(f"Cannot connect to URL")

	# get the header and metadata from the response
	# response.headers is a dictionary containing the HTTP headers of the response
	date = response.headers["date"]
	content_type = response.headers["content-type"]

	# print the header and metadata to the console
	print(f"url  : {response.url}")
	print(f"Date : {date}")
	print(f"Date : {content_type}")

	# parse the HTML content of the page using BeautifulSoup
	soup = BeautifulSoup(response.content, "lxml")

	# extract the page title from the HTML using the find() method of BeautifulSoup
	# find() returns the first element in the HTML that matches the specified tag and attributes
	Pagetitle = soup.find("h1").text

	# create a directory to store the results of the web scraping
	# get the current working directory using os.getcwd()
	cwd = os.getcwd()

	# specify the name of the directory to create
	dirname = "Raw Data"

	# get the full path of the directory to create by joining the current working directory and the directory name
	dirpath = os.path.join(cwd, dirname)

	# check if the directory already exists
	if not os.path.exists(dirpath):
		# if not, create it using os.makedirs()
		try:
			os.makedirs(dirpath)
		except OSError:
		# if there was an error creating the directory, print an error message and exit the program
			raise SystemExit(f"Directory don't exsits: {dirpath}")

	# create a new CSV file to store the extracted text
	# specify the name of the file based on the page title and the directory name
	path = os.path.join(dirname, f"{Pagetitle}.csv")

	count = 0
	#Open the file in Write Mode
	with open(path, "w") as f:


		#Columns of CSV files
		fieldnames = ["Paragraph"]

		#Writer Object 
		csv_writer  = csv.DictWriter(f, fieldnames=fieldnames, delimiter=",")
		csv_writer.writeheader()


		#Find all the paragraphs
		for p in soup.find_all("p"):
			count += 1
			csv_writer.writerow({"Paragraph": p.text})

	print(f"No. of Paragraphs Successfully Writen : {count}")


if __name__ == "__main__":
	Web_Scraper_main()
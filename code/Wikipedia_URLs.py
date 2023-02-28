import wikipedia 
import os
import csv
import argparse


def Parser():

	# Create an ArgumentParser object and define its attributes
	parser = argparse.ArgumentParser(prog="Wikipedia URL",
		description="This is Wrapper function for Web Scraper",
		epilog="Thank you for using!",
		argument_default=argparse.SUPPRESS,
		allow_abbrev=True,
		fromfile_prefix_chars="@")

	# Add positional arguments to the parser
	parser.add_argument("dataset_location")
	parser.add_argument("url_file_path")
	parser.add_argument("no_of_results")

	# Add optional arguments to the parser
	parser.add_argument("-d", "--data", action="store_true", required=True, help="Location of dataset")
	parser.add_argument("-f", "--file", action="store_true", required=True, help="Location to store URLs")
	parser.add_argument("-r", "--results", action="store_true", help="Results required for each query")

	# Parse the arguments and return the parsed arguments as a tuple
	args = parser.parse_args()
	return args.dataset_location, args.url_file_path, args.no_of_results


def pageUrl(query, no_of_results):
	"""
	Searches for the given query on Wikipedia and returns a list of URLs
	for the top `no_of_results` search results.

	Parameters:
	query (str): The search query for Wikipedia.
	no_of_results (int): The number of search results to return.

	Returns:
	List[str]: A list of URLs for the top search results on Wikipedia.
	"""

	# Search Wikipedia for the given query
	titles = wikipedia.search(query, results=no_of_results)

	# Initialize an empty list to store the URLs for each search result
	url_list = []

	# Iterate over each search result
	for title in titles:

		# Check if the title contains "(disambiguation)", which usually indicates
		# that it's a disambiguation page with multiple possible meanings for the search query
		if "(disambiguation)" in title:
			# Skip this search result and move on to the next one
			continue

		# Construct the URL for the Wikipedia page based on the search result title
		url = f"https://en.wikipedia.org/wiki/{title}"

		# Add the URL to the list of URLs
		url_list.append(url)

	# Return the list of URLs for the search results
	return url_list



def main_wiki_url():
	"""
	Reads a dataset file containing words, searches for each word on Wikipedia,
	and writes a list of URLs for the top search results to a CSV file.
	"""

	# Parse the command line arguments to get the input and output file paths and the number of search results to return
	dataset_location, url_file, no_of_results = Parser()

	# Check if the input dataset file exists
	if not os.path.exists(dataset_location):
		# If the file doesn't exist, exit the program with an error message
		raise SystemExit(f"Dataset don't exsits")

	# Initialize an empty list to store the words from the dataset file
	word_db = []

	# Open the dataset file for reading
	with open(dataset_location, "r") as f:

		# Iterate over each line in the file
		for line in f:
			# Remove any leading or trailing whitespace from the line
			line = line.strip()

			# Split the line into a list of words
			word_list = line.split(" ")

			# Add the words from the line to the list of words
			word_db.extend(word_list)

	# Remove duplicates from the list of words
	word_db = list(set(word_db))

	# Convert all words to lowercase
	word_db = [word.lower() for word in word_db if len(word) != 0]

	# Sort the list of words by the first letter of each word
	word_db = sorted(word_db, key=lambda x : x[0])

	# Initialize an empty list to store the URLs for the search results
	url_list = []

	# Search Wikipedia for each word in the list of words from the dataset
	for word in word_db:
		# Get the top `no_of_results` search results for the word on Wikipedia
		url_list.extend(pageUrl(word, no_of_results))

	# Write the list of URLs to a CSV file
	with open(url_file, "w") as f:

		# Define the field names for the CSV file
		fieldnames = ["URL"]

		# Create a CSV writer object with the field names and write the header row
		writer = csv.DictWriter(f, fieldnames=fieldnames)
		writer.writeheader()

		# Write each URL to a row in the CSV file
		for url in url_list:
			writer.writerow({"URL" : url})



if __name__ == "__main__":
	main_wiki_url()
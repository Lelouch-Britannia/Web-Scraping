import argparse
import os
import csv
import sys
from Web_Scraper import Web_Scraper_main


def Parser():
    # Define an ArgumentParser object
    parser = argparse.ArgumentParser(prog="Wikipedia Scraper",
                                     description="For scraping all the wiki URLs in the url.csv",
                                     epilog="Thank you for using it!",
                                     argument_default=argparse.SUPPRESS,
                                     allow_abbrev=True,
                                     fromfile_prefix_chars="@")

    # Add a positional argument for the URL file path
    parser.add_argument("url_file_path")

    # Add an optional argument for specifying that the input is a file
    parser.add_argument("-f", "--file", action="store_true", required=True, help="Location of dataset")

    # Parse the command-line arguments and return the URL file path
    args = parser.parse_args()
    return args.url_file_path


def main():
    # Read the URLs from url.csv
    url_file_path = Parser()

    # Open the URL file in read mode
    with open(url_file_path, "r") as f:
        reader = csv.DictReader(f)

        # Arguments to pass to the Web_Scraper_main function
        u = "--url"

        # Iterate over each row in the URL file
        for line in reader:
            # Get the URL from the current row
            url = line["URL"]

            # Request and scrape the data for the current URL
            # Modify sys.argv before calling Web_Scraper_main to pass in the URL as an argument
            sys.argv = [sys.argv[0], u, url]
            Web_Scraper_main()




if __name__ == "__main__":
	main()
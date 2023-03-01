import neattext as nt
import neattext.functions as nfx
import contractions
import argparse
import os
import csv
import re


def Parser():

	parser = argparse.ArgumentParser(prog="Text Cleaning",
		description="For cleaning of text",
		epilog="Thank you for using!",
		allow_abbrev=True,
		argument_default=argparse.SUPPRESS,
		fromfile_prefix_chars="@")

	parser.add_argument("raw_data_dir")


	parser.add_argument("-r", "--raw",  action="store_true", required=True, help="Location of dataset")

	args = parser.parse_args()

	return args.raw_data_dir


def textPP(data):

	#Remove paranthesis
	data = re.sub(r'\([^)]*\)', '', data)

	#Get rid of Ref nos
	data = re.sub(r"\[\d+\]", "", data)

	#Better to get rid of numbers
	data= re.sub(r'\d+(\.\d+)?', '', data)

	#Fix Contractions
	data = contractions.fix(data)

	data = re.sub(r'\bi\.e\.', "that is", data)
	data = re.sub(r'\be\.g\.', "for example", data)

	#Remove hypens
	data= re.sub(r"-", " ", data)

	#Remove remaining paranthesis
	data =  re.sub(r'[()]', '', data)

	#Remove specail Characters
	data = re.sub(r'[^A-Za-z0-9\s]+', '', data)

	return data


def text_processing_main(raw_data_dir):
	

	#Directory name
	dirname = os.path.dirname(raw_data_dir)

	clean_data_dir = os.path.join(dirname, "Data")

	if not os.path.exists(clean_data_dir):
		try:
			os.makedirs(clean_data_dir)
		except OSError:
			raise SystemExit(f"Directory don't exsits")

	#Get files 
	filenames = os.listdir(raw_data_dir)

	for filename in filenames:

		#File Location
		file_loc = os.path.join(raw_data_dir, filename)

		#Clean file Location
		clean_file_loc = os.path.join(clean_data_dir, filename)

		#Open raw data file
		with open(file_loc, "r") as f:
			reader = csv.DictReader(f)

			with open(clean_file_loc, "w") as f_prime:

				fieldnames = ["Unclean", "Clean", "Noise_Pre_Processing","Training_Data", "Noise_Post_Processing", "Query"]
				writer = csv.DictWriter(f_prime, fieldnames=fieldnames)
				writer.writeheader()

				for row in reader:

					data = row["Paragraph"].lower()
					try:
						query = row["Query"]
					except KeyError:
						continue
						print(f"No query found")


					data = textPP(data)

					lines = data.split(".")
					for line in lines:

					  #Remove empty string and word
					  if len(line) < 2:
					    continue

					  unclean_string = line

					  #Noise Pre
					  noise_pre = nt.TextFrame(line).noise_scan()["text_noise"]
					  noise_pre = f"{noise_pre:.2f}"

					  # 1. Remove Special Characters
					  line = nfx.remove_special_characters(line)

					  # 2. Remove multiple whitespaces
					  line = nfx.remove_multiple_spaces(line)

					  # 3. Remove stop words
					  line = nfx.remove_stopwords(line)

					  # 4. Remove punctuations
					  line = nfx.remove_puncts(line)

					  clean_string = line

					  #Noise post
					  noise_post = nt.TextFrame(line).noise_scan()["text_noise"]
					  noise_post = f"{noise_post:.2f}"

					  #Tokenization
					  training_data = line.split(" ")

					  #Keeping only those sentences that has query(Training word instance)
					  if query in training_data:

						  training_data = ",".join(training_data)
						  writer.writerow({"Unclean": unclean_string, "Noise_Pre_Processing" : noise_pre,"Clean" : clean_string, "Training_Data" : training_data, "Noise_Post_Processing": noise_post, "Query": query})



if __name__ == "__main__":

	raw_data_dir = Parser()
	text_processing_main(raw_data_dir)
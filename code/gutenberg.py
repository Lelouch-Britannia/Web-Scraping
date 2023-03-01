import neattext as nt
import neattext.functions as nfx
import nltk
from nltk.corpus import gutenberg
from Text_Processing import textPreProcessing
import csv
import os
import argparse

def Parser():

	parser = argparse.ArgumentParser(prog="Gutenberg",
		description="Cleaning Gutenberg dataset",
		epilog="Thank you for using!",
		allow_abbrev=True,
		argument_default=argparse.SUPPRESS,
		fromfile_prefix_chars="@")

	parser.add_argument("data_dir")

	parser.add_argument("-d", "--data", action="store_true", required=True, help="Location for dataset")

	args = parser.parse_args()

	return args.data_dir


def main():

	data_dir = Parser()

	if not os.path.exists(data_dir):
		try:
			os.makedirs(data_dir)
		except OSError:
			raise SystemExit(f"Directory don't exsits!")
	
	filename = "readme"
	dirname = os.getcwd()

	file_loc = os.path.join(dirname, f"{filename}.txt")

	with open(file_loc, "a") as f:

		fieldnames = ["Title", "No_of_lines"]
		writer1 = csv.DictWriter(f, fieldnames=fieldnames)
		writer1.writeheader()

		files = gutenberg.fileids()

		for file in files:

			data = gutenberg.sents(file)
			filename = file.split(".")[0]

			clean_file_loc = os.path.join(data_dir, f"{filename}.csv")

			n = 0

			with open(clean_file_loc, "w") as f_prime:



				fieldnames = ["Unclean", "Clean", "Noise_Pre_Processing","Training_Data", "Noise_Post_Processing", "Query"]
				writer2 = csv.DictWriter(f_prime, fieldnames=fieldnames)
				writer2.writeheader()

				# #Lets Prepare the data
				for word_list in data[3:]:

					n += 1

					line = " ".join(word_list)
					# f_prime.write(line)
					# f_prime.write("\n")
					line = textPreProcessing(line)

					#Remove empty string and word
					# if n > 1314 and n<1317:
					# 	print(f"{line} : {len(line)}")

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

					if len(training_data) < 3:
						continue
					training_data = ",".join(training_data)

					writer2.writerow({"Unclean": unclean_string, "Noise_Pre_Processing" : noise_pre,"Clean" : clean_string, "Training_Data" : training_data, "Noise_Post_Processing": noise_post})

			print(f"{file} : {n}")
			writer1.writerow({"Title": file, "No_of_lines":n})



if __name__ == "__main__":
	main()
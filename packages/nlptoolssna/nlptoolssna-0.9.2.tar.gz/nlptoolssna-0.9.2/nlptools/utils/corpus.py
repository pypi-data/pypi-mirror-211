# Version: Ver1 (2021-09-09)
# By Wasim Khatib
# This program take file (contain all file names) and Tokenize corpus by using  tokenizer.py that was implemented previosly to
# return one CSV file that contains all words from all files.
# The first column in the file is a row_id (serial number).
# The second column is the docs_sentence_word_id: concatenation of the filename, sentence number, and word position in this sentence.
# The third column is word.

import os
from typing import Counter
from nlptools.utils.tokenizer import simple_word_tokenize
import sys
import pandas
def Tokenize_Corpus(path_of_the_names):
    # This function take the path_of_the_names of the files.txt then for each file in files.txt, split the corpus into lins then split these lines by using
    # function called simple_word_tokenize, after that its generate  these three columns row_id,docs_sentence_word_id,word, and store the results into csv file (corpus.csv)

    corpus_list= list()

    # Read the all file names form the input file
    #file_names = open(path_of_the_names, "r")
    file_names =open((os.path.join(sys.path[0] + '/'+  path_of_the_names)), mode='r')

    row_id = 1
    try:

        for file in file_names:
            file_path = file.split("\n")[0]
            #f = open(file_path, "r")
            f=open((os.path.join(sys.path[0] + '/wojood_dataset_test/'+  file_path)), mode='r', encoding='utf-8')
            sentance_id = 1

            # split the name of the file, because we need to add file name in the docs_sentence_word_id
            slash_split = f.name.split("\\")
            f_name = slash_split[len(slash_split) - 1].split(".")[0]



            # For each line in file, tokenized using simple_word_tokenize and generate row_id,docs_sentence_word_id for each word in the line
            for line in f:
                words = simple_word_tokenize(line)

                # Check if the line is empty or not, if yes then will be add to the previous line.
                if len(words) == 0:
                    # # Generate docs_sentence_word_id which is file name, sentance_id and word position
                    # #docs_sentence_word_id = f_name + "_" + str(sentance_id-1) + "_" + str(word_position)
                    # corpus_list.append([row_id, f_name,sentance_id,word_position, "x" ,'x'])
                    # #corpus_list.append([row_id, docs_sentence_word_id, ""])
                    # word_position += 1
                    # row_id += 1  # auto increment
                    continue


                word_position = 1

                # This loop go to each word and save it in corpus list (row_id,docs_sentence_word_id,word)
                for word in words:
                    #docs_sentence_word_id = f_name+"_"+str(sentance_id)+"_"+str(word_position)
                    #corpus_list.append([row_id,docs_sentence_word_id,word])
                    corpus_list.append([row_id, f_name,sentance_id,word_position, word ,'O'])
                    word_position += 1
                    row_id += 1

                # At the end of each sentance add new line.
                #docs_sentence_word_id = f_name + "_" + str(sentance_id) + "_" + str(word_position)
                
                # corpus_list.append([row_id, f_name,sentance_id,word_position, 'x' ,'x'])
                # #corpus_list.append([row_id, docs_sentence_word_id, ""])
                
                word_position += 1
                row_id += 1
                sentance_id += 1
    except UnicodeDecodeError:
        print(f"UnicodeDecodeError: Skipping file {file_path} due to decoding error.")

    column_names = ["row_id", "f_name","sentance_id","word_position", "word","label"]
    df = pandas.DataFrame(columns=column_names, data= corpus_list )
    json_object = df.to_json(orient='records')
    return json_object




def extract_filename_from_path(file_path):
    # Split the file path into directory and file name
    directory, file_name = os.path.split(file_path)
    return file_name

def read_arabic_text_file(file_path):
    # with open(file_path, 'r', encoding='utf-8') as file:
    #     for line in file:
    #         # Remove leading/trailing whitespaces and print the line
    #         line = line.strip()
    #         print(line)
    filename =file_path.split('\\')[-1]
    with open(file_path, 'r', encoding='UTF-8') as file:
        line = file.readline()
        print(line)




##################### Main #####################
#read_arabic_text_file(r'wojood_dataset_test\Agriculture\ag1.txt')
print(Tokenize_Corpus("output_relative.txt"))







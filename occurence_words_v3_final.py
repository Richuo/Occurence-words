import numpy as np
import re
import sys
from collections import Counter
from tkinter import Tk
from tkinter.filedialog import askopenfilename

class Wordscounter:

    def __init__(self):
        self.filename = ''
        self.user_nb = 0
        self.nb_best = 0


    def customize_searching(self):
        while True:
            try:
                self.user_nb = int(input("Words detection : ",))
                if self.user_nb > 0:
                    break;
            except ValueError:
                print("Please enter a strictly positive number")
                pass;

        while True:
            try:
                self.nb_best = int(input("Number of results : ",))
                if self.nb_best > 0:
                    break;
            except ValueError:
                print("Please enter a strictly positive number")
                pass;


    def list_2_string(self,liste):
        result = ''
        for i in liste:
            if isinstance(i, str):
                result += i
        return(result)


    def characters_filter(self,liste): #Can be improved
        L_split = [x.lower() for x in re.split('; |, |-|\n|\s|"|', liste)]
        banned_letters = [',', ';', '.', '?', '!', ':', '(', ')', '-', '\n'] 
        banned_words = [''] #Can be implemented as a config.ini file
        filtered_list =[]
        for i in range(len(L_split)):
            mot = L_split[i]
            for j in range(len(mot)):
                try:
                    letter = mot[j]
                    double_letters = mot[j:j+1]
                    if letter in banned_letters or double_letters in banned_letters: #Filter the unwanted letters
                        mot = self.list_2_string([x for x in mot if x != letter and x != double_letters])
                except:
                    pass;
            if mot not in banned_words:
                filtered_list.append(mot)
        return(filtered_list)


    def regroup_words(self,liste,nb):
        if nb > 1:
            result_list = []
            while len(liste) > nb-1:
                expression = ''
                for i in range(nb):
                    if i != nb-1:
                        expression += liste.pop(0) + ' '
                    else:
                        expression += liste[0]
                result_list.append(expression)
            return(result_list)
        else:
            return(liste)
    

    def best_of(self,liste,nb):
        best_words = liste[:nb]
        print('best : ', best_words)
        result = ''
        for i in range(nb):
            mot = best_words[i][0]
            nb_mot = str(best_words[i][1])
            result += ('"%s" which appeared %s times' % (mot,nb_mot)) + '\n'
        print('\n Here are the most reccurent words : \n\n' + result)


if __name__ == '__main__':

    wc = Wordscounter()

    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    wc.filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    if wc.filename[-4:] == '.txt' :
        print('"%s" file selected.' % wc.filename)
        wc.customize_searching()
    else:
        print("Please select a .txt file, program stopped.")
        sys.exit()

    file = open(wc.filename, 'r', encoding="utf8")
    datalist = file.read()
    lenght_datalist = len(datalist)

    print('Starting the filtering...')
    L_filtered = wc.characters_filter(datalist)
    print('  Filtering completed. \nStarting the words grouping...')
    L_regrouped = wc.regroup_words(L_filtered,wc.user_nb)
    print('  Regrouping words completed. \nStarting the words counter...')
    L_counted_fast = list(Counter(L_regrouped).items()) #collections.Counter() O(n) faster than list.count() O(n^2)
    print('  Counting completed. \nStarting the sorting...')
    L_sorted = sorted(L_counted_fast, key=lambda tup: tup[1], reverse=True)
    print('  Sorting finished \nGiving the results...')
    wc.best_of(L_sorted,wc.nb_best)
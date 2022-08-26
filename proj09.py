##########################################################################
#    Computer Project #9
#    Algorithm
#        >9 functions defined.        
#        >Main function starts with calling functions used to opening
#         both JSON and text files and reading them. It then asks for 
#         options and calls or quit functions based on user input.
#         It ends by printing thank you message.  
##########################################################################

import json,string

STOP_WORDS = ['a','an','the','in','on','of','is','was','am','I','me','you','and','or','not','this','that','to','with','his','hers','out','it','as','by','are','he','her','at','its']

MENU = '''
    Select from the menu:
        c: display categories
        f: find images by category
        i: find max instances of categories
        m: find max number of images of categories
        w: display the top ten words in captions
        q: quit
        
    Choice: '''


def get_option():
   '''
   Prompts for input until it is valid.
   Parameter: None
   Returns: str
   Prints: prmopts and error messages
   '''
   ans = True
   while ans:
      option = input(MENU)
      if option.lower() not in "cfimwq":
         #invalid input so loop continues 
         print("Incorrect choice.  Please try again.")
      else:
         #valid input so loo breaks
         ans = False
         return option.lower()

    
def open_file(s):
   '''
   Prompts for a file name until a file is correctly opened.
   Parameters: str
   Returns: file pointer
   Displays: prmpts and error messages
   '''
   ans = True
   while ans:
      filename = input("Enter a {} file name: ".format(s))
      try:
         #works if filename is valid
         fp = open(filename)
         ans = False
         return fp
      except:
         #filename invalid so loop continues 
         print("File not found.  Try again.")

        
def read_annot_file(fp1):
   '''
   Reades JSON file.
   Parameters: file pointer
   Returns: dictionary of dictionaries
   '''
   data = json.load(fp1)    #reads data from json file
   return data


def read_category_file(fp2):
   '''
   Reads a text file and stores the data in a dictionary.
   Parameters: file pointer
   Returns: dictionary
   '''
   data = fp2.readlines()   #creates list of data
   dict1 = dict()
   list1 = []
   for line in data:
      line = line.replace("\n", "")    #to remove new line character
      list2 = line.split(" ")    #creates list
      list1.append(list2)
   for i in list1:
      dict1[int(i[0])] = i[1]   #assigns value to dictionary
   return dict1


def collect_catogory_set(D_annot,D_cat):
   '''
   Creates a set of the categories used in dictionary.
   Parameters: dictionary of dictionaries, dictionary
   Returns: set of strings
   '''
   list1 = []
   list2 = []
   set1 = set()
   for key in D_annot:
       #category numbers
       value = D_annot[key]["bbox_category_label"]
       list1.append(value)
   for i in list1:
       for j in i:
           if j not in list2:
               list2.append(j)
           else:
               continue
   for num in list2:
       val = D_cat[num]
       set1.add(val)   #set means all values are different 
   return set1

    
def collect_img_list_for_categories(D_annot,D_cat,cat_set):
   '''
   Creates a mapping of each category to the list of images that has an 
   instance of that category.
   Parameters: dictionary of dictionaries, dictionary, set of strings
   Returns: dictionary of sorted lists
   '''
   dict1 = dict()
   for i in cat_set:
       dict1[i] = []    #initializes dictionary
   for key in D_annot:
       value = D_annot[key]["bbox_category_label"]
       for num in value:
           dict1[D_cat[num]].append(key)    #assigns value to dictionary
   for j in dict1:
       dict1[j].sort()    #sorts dictionary from lowest to highest
   return dict1      
         
   
def max_instances_for_item(D_image):
   ''' 
   Finds the most occurrences of a category across all images.
   Parameters: dictionary of sorted lists
   Returns: tuple
   '''
   max1 = 0    #setting max to lowest possible number
   for key in D_image:
       if len(D_image[key]) > max1:
           #replaces max1 and category values
           max1 = len(D_image[key])
           category = key
   return (max1, category)    #returns value in a tuple

def max_images_for_item(D_image):
   ''' 
   Finds the most images that a category appears in.
   Parameters: dictionary of sorted lists
   Returns: tuple
   '''
   max1 = 0    #setting max to lowest possible number
   for key in D_image:
       length = len(set(D_image[key]))
       if length > max1:
           #replaces max1 and category values
           max1 = length
           category = key
   return (max1, category)    #returns value in a tuple
       

def count_words(D_annot):
   ''' 
   Counts the occurrences of words in captions and stores in a list.
   Parameters: dictionary of dictionaries
   Returns: list of tuples
   '''
   captions_list = []
   dict1 = dict()
   final_list = []
   for key in D_annot:
       captions = D_annot[key]["cap_list"]
       #used extend to have a 1D list and not a 2D list.
       captions_list.extend(captions)    
   for captions in captions_list:
       words = captions.split(" ")    #creates a list
       for word in words:
           word = word.strip(string.punctuation)    #replaces punctuation 
           if word in STOP_WORDS or word.isdigit():
               #skips invalid words or number
               continue
           if not word.isalpha():
               #skips empty space
               continue
           #adds key to list if not present otherwise increments value
           if word not in dict1:
               dict1[word] = 1
           else:
               dict1[word] += 1
   for key in dict1:
       value = (dict1[key], key)    #tuple
       final_list.append(value)    #list of tuples
   final_list.sort(reverse = True)   #sorts from highest to lowest 
   return final_list

def main():    
    print("Images\n")
    #initializing files and calling required functions
    fp1 = open_file("JSON image")   
    D_annot = read_annot_file(fp1)
    fp2 = open_file("category")
    D_cat = read_category_file(fp2)
    cat_set = collect_catogory_set(D_annot, D_cat)
    D_image = collect_img_list_for_categories(D_annot, D_cat, cat_set)
    option = get_option() 
    while option != "q":
        
        if option == "c":
            cat_list = list(cat_set)
            cat_list.sort()
            print("\nCategories:")
            for i in range(len(cat_list)-1):
                print(cat_list[i], end = ", ")
            print(cat_list[-1])
                
        elif option == "f":
            cat_list = list(cat_set)
            cat_list.sort()
            print("\nCategories:")
            for i in range(len(cat_list)-1):
                print(cat_list[i], end = ", ")
            print(cat_list[-1])
            cat = input("Choose a category from the list above: ")
            #invalid choice so takes user input again
            while cat not in cat_list:
                print("Incorrect category choice.")
                cat = input("Choose a category from the list above: ")
            print("\nThe category {} appears in the following images:".format(cat))
            images = D_image[cat]
            for i in range(len(images)):
                images[i] = int(images[i])
            #sorts then converts to set to remove duplicate values then
            #converts back to list and sorts
            images.sort()
            images = set(images)
            images = list(images)
            images.sort()
            for image in range(len(images)-1):
                print(images[image], end = ", ")
            print(images[-1])
                
        elif option == "i":
            max1, category = max_instances_for_item(D_image)
            print("\nMax instances: the category {} appears {} times in images.".format(category, max1))
        
        elif option == "m":
            max1, category = max_images_for_item(D_image)
            print("\nMax images: the category {} appears in {} images.".format(category, max1))
        
        elif option == "w":
            num = int(input("\nEnter number of desired words: "))
            while num <= 0:
                #invalid input so loop continues
                print("Error: input must be a positive integer: ")
                num = int(input("\nEnter number of desired words: "))
            print("\nTop {} words in captions.".format(num))
            print("{:<14s}{:>6s}".format("word","count"))
            words_list = count_words(D_annot)
            for i in range(num):
                count, word = words_list[i]
                print("{:<14s}{:>6d}".format(word, count))

        option = get_option() 
    print("\nThank you for running my code.") 
    
# Calls main() if this modules is called by name
if __name__ == "__main__":
    main()     

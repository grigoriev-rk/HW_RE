from pprint import pprint
import csv
import re
import operator
import itertools
import os


def correct_numbers(read_file, write_file):             # Read and write correct numbers function
    with open(read_file, encoding="utf8") as f:         # Open file for read
        text = f.read()
    pattern_phone = r'(\+7|8)?\s*\(?(\d{3})\)?[\s*-]?(\d{3})[\s*-]?(\d{2})[\s*-]?(\d{2})(\s*)\(?(доб\.?)?\s*(\d*)?\)?'  # Using regular expression
    correct_numbers = re.sub(pattern_phone, r'+7(\2)\3-\4-\5\6\7\8', text)
    with open(write_file, 'w+', encoding="utf8") as f:  # Write new file with correct numbers 
        text = f.write(correct_numbers)


def create_dict(file_name):                             # Create dict from CSV phonebook function
    contacts_dict = []
    with open(file_name, encoding="utf8") as f:         # Open file for read
        reader = csv.reader(f, delimiter=",")
        contacts_list = list(reader)
        keys = contacts_list[0]                         # Create dict from contacts_list
        values = contacts_list[1:]
        for num, vals in enumerate(values):
            contacts_dict.append({})
            for key, val in zip(keys, vals):
                contacts_dict[num].update({key: val})
        return contacts_dict


def correct_initials(read_file):                         # Correct initials function
    contacts_dict = create_dict(read_file)               # Call the create dict function 
    for ln_ in contacts_dict:                            # Check for initials len and placing items on their places 
        split_ = ln_['lastname'].split(' ')                 
        if len(split_) > 1:
            ln_['lastname'] = split_[0]
            ln_['firstname'] = split_[1]
            if len(split_) > 2:
                ln_['surname'] = split_[2]
        split_ = ln_['firstname'].split(' ')
        if len(split_) > 1:
            ln_['firstname'] = split_[0]
            ln_['surname'] = split_[1]
    return contacts_dict


def merge_initials(contacts):                                   # Merge initials function 
    keys_ = set(contacts[0].keys())
    list_ = ['firstname', 'lastname']                
    group = operator.itemgetter(*list_)                         # Return data from group_list (by firstname and lastname)
    cols = operator.itemgetter(*(keys_ ^ set(list_)))           # Build an unordered collections of unique elements 
    contacts.sort(key=group)                                    # Sorting by lastname
    grouped = itertools.groupby(contacts, group)                # Grouping entries in a phonebook
    merge_data = []                     
    for (firstname, lastname), g in grouped:                    # Merging elements in string
        merge_data.append({'lastname': lastname, 'firstname': firstname})
        for g1 in g:
            g2 = merge_data[-1]
            for i, j in g1.items():
                if i not in g2 or g2[i] == '':
                    g2[i] = j
    return merge_data


def write_dict(file_name, dicts):                      # Write CSV file function
    keys = list(dicts[0].keys())
    with open(file_name, "w", encoding="utf8") as f:   # Write values without keys 
        writer = csv.writer(f, delimiter=',')
        writer.writerow(keys)
        for d in dicts:
            writer.writerow(d.values())


def main():   
    correct_numbers(read_file="phonebook_raw.csv", write_file="correct_phones.csv")        # Correct phone numbers
    corrected_initials = correct_initials(read_file="correct_phones.csv")                  # Correct initials
    os.remove("correct_phones.csv")                                                        # Remove intermediate work file  
    merged_initials = merge_initials(corrected_initials)                                   # Merge initial info
    write_dict("phonebook.csv", merged_initials)                                           # Write data in CSV file


if __name__ == '__main__':
    main()

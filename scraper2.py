import pandas as pd
import json

df = pd.read_csv("C://Users//josep//urop//CEPT_ListeningItems_2021 - Sheet1.csv", encoding='latin-1')

def flatten_list(_2d_list):
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list

id_list = []
diff_list = []
cefr_list = []
soundfile_list = []
q_text_list = []
options_list = []
key_list = []

for i in range(0, len(df)):

    id = df['itemID'][i]
    id_list.append(id)

    diff = df['difficulty'][i]
    diff_list.append(diff)

    cefr = df['CEFR'][i]
    cefr_list.append(cefr)

    soundfile = df['soundfile'][i]
    soundfile_list.append(soundfile)

    q_text = df['questionText'][i]
    q_text_list.append(q_text)

    if df["numberOfOptions"][i] == 3:
        options = [df["optionA"][i], df["optionB"][i], df["optionC"][i]]
    else:
        options = [df["optionA"][i], df["optionB"][i], df["optionC"][i], df["optionD"][i]]
    options_list.append(options)

    key = df['key'][i]
    key_list.append(key)

#to find the repeated question ids
repeat_ids = []
for elem in id_list:
    if id_list.count(elem) > 1:
        if elem not in repeat_ids:
            repeat_ids.append(elem)
        else:
            pass

#returns lists of indices where the id is the same (i.e. clumps of 5 questions)
def list_duplicates_of(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs

#returns a dict with the id as key and the indices where the id repeats as the value
repeat_dict = {}
for elem in repeat_ids:
    x = list_duplicates_of(id_list, elem)
    repeat_dict[elem] = x

for x in repeat_dict.values():
    my_sound = []
    my_text = []
    my_options = []
    my_keys = []
    for i in x:
        my_sound.append(soundfile_list[i])
        my_text.append(q_text_list[i])
        my_options.append(options_list[i])
        my_keys.append(key_list[i])

    for i in x:
        soundfile_list[i] = my_sound
        q_text_list[i] = my_text
        options_list[i] = my_options
        key_list[i] = my_keys

#returns a list of indices to extract
initial_indices = []
for elem in repeat_dict.values():
    initial_indices.append(elem[0])

all_indices = list(range(0, 112))
for elem in repeat_dict.values():
    for sub_elem in elem:
        all_indices.remove(sub_elem)

safe_indices = sorted(all_indices + initial_indices)

#given a list it will return a new list with no repeated values
def crop(input_list):
    x = []
    for i in safe_indices:
        x.append(input_list[i])
    return x


#id list will now have zero repeats
id_list = crop(id_list)
diff_list = crop(diff_list)
cefr_list = crop(cefr_list)
soundfile_list = crop(soundfile_list)
q_text_list = crop(q_text_list)
options_list = crop(options_list)
key_list = crop(key_list)

soundfile_list_ids = []
for elem in soundfile_list:
    if type(elem) == list:
        sub_list = []
        for item in elem:
            x = str(item[32:len(item)-17])
            new_item = "http://docs.google.com/uc?export=open&id=" + x
            sub_list.append(new_item)
        soundfile_list_ids.append(sub_list)
    else:
        x = str(elem[32:len(elem)-17])
        elem = "http://docs.google.com/uc?export=open&id=" + x
        soundfile_list_ids.append(elem)

for list_of_3 in options_list:
    for index, answer in enumerate(list_of_3):
        if answer[:5] == "https":
            x = str(answer[32:len(answer)-17])
            list_of_3[index] = "https://drive.google.com/uc?export=view&id=" + x
            
combo_list = [id_list, diff_list, cefr_list, soundfile_list_ids, q_text_list, options_list, key_list]

def splitter(d, diff, combo):
    d_num = list(enumerate(d))
    indices  =[]
    for elem in d_num:
        if diff in elem[1]:
            indices.append(elem[0])
    
    mod_id = []
    mod_diff = []
    mod_cefr = []
    mod_soundfile = []
    mod_q_text = []
    mod_options = []
    mod_key = []

    for i in indices:
        mod_id.append(combo[0][i])
        mod_diff.append(combo[1][i])
        mod_cefr.append(combo[2][i])
        mod_soundfile.append(combo[3][i])
        mod_q_text.append(combo[4][i])
        mod_options.append(combo[5][i])
        mod_key.append(combo[6][i])
    return [mod_id, mod_diff, mod_cefr, mod_soundfile, mod_q_text, mod_options, mod_key]

b1_list = splitter(combo_list[2], "B1", combo_list)
b2_list = splitter(combo_list[2], "B2", combo_list)
c1_list = splitter(combo_list[2], "C1", combo_list)
c2_list = splitter(combo_list[2], "C2", combo_list)

#converts the list of lists into a js question array full of dictionaries
def js(myl):
    js_list = []
    for i in range(len(myl[0])):
        js = {}
        js['id'] = myl[0][i]
        js['question'] = myl[4][i]
        js['audio'] = myl[3][i]
        #assigns question type
        if type(myl[5][i][0]) == list:
            js['qtype'] = "block"
        elif "drive.google.com" in myl[5][i][0]:
            js['qtype'] = "image"
        else:
            js['qtype'] = "text"
        #checks if soundfile has multiple questions
        if type(myl[5][i][0]) == list:
            #make a sub dict and then add as the val of another dict
            #j will index the 5 sets of answers
            answer_list = []
            for elem in myl[5][i]:
                answer_dict = {}
                answer_dict['A'] = elem[0]
                answer_dict['B'] = elem[1]
                answer_dict['C'] = elem[2]
                answer_list.append(answer_dict)
            js['answers'] = answer_list
        else:
            answer_dict = {}
            answer_dict['A'] = myl[5][i][0]
            answer_dict['B'] = myl[5][i][1]
            answer_dict['C'] = myl[5][i][2]
            js['answers'] = answer_dict

        js['correctAnswer'] = myl[6][i]

        js_list.append(js)
    return js_list

b1_js = js(b1_list)
#b2_js = js(b2_list)

##c1_dict = js_array(c1_list)
##c2_dict = js_array(c2_list)
print(b1_js)
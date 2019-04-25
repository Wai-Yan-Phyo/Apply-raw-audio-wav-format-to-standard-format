def apply_raw_voice_to_standard_all_file ():
    
    import numpy as np
    import glob
    import os
    import sys
    from tqdm import tqdm
    import time
    import json
    start_time = time.time()
    
    file_location = './Brainstorm'
 
    voice = []
    read_path2_list = []
    sr = []
    list1 = []
    fname = []
    check_folder_lis = []
    length_list = []
    ch_len_list = []
    all_sub_folder = []
    all_sub_folder_len =[]
    final_wav_with_complete_loc = []
    For_duration = []
    audio_ID_for_json = []
    len_of_all_file = []
    not_match_list = []
    
    Dict_for_json = {}
    Second_Dict = {}
    user_dict = {}
    
    #Read Path 
    read_path = os.listdir(file_location)
    #print("read_path:",read_path)


    for i in read_path:
        suffix = 'S'
        if suffix in i:
            all_user_folder = i
            
            ###Create all Folder in one list (given path)
            check_folder_lis.append(all_user_folder)
            
        #print("check_folder_lis:",check_folder_lis)
        
    ###To reach Final main sub folder
    #loop for above created list to get Final sub folder Location 
    for j in check_folder_lis:
        read_path2 = os.listdir(file_location+'/'+j)
        read_path2_list.append(read_path2)
    #print("read_path2_list:",read_path2_list)
             
    
    ###Get Information 
    #
    count = 0
    c = 0
    for idi, pp in enumerate(read_path2_list):
        #print("pp:",pp)
        for idx, final_sub_folder in enumerate(pp):
            #print("final_sub_folder:",final_sub_folder)
            reformat_for_name = final_sub_folder.replace('(',' ').replace(')',' ').replace('_',' ')
            reformat_new = reformat_for_name.split(' ')
            #print("reformat_new:",reformat_new)

            middle_loc = reformat_new[0]
            #unique = middle_loc
            #print("unique:",unique)
            new_path = file_location+'/'+middle_loc+'/'+final_sub_folder+'/*.wav'
            #print("new_path:",new_path)
            new_path1 = file_location+'/'+middle_loc+'/'+final_sub_folder
            #print("new_path1:",new_path1)
            list_file_location = new_path1.split('/')
            #print("list_file_location:",list_file_location)

            len_of_output_file_loc = len(list_file_location)-1
            #print("len_of_output_file_loc:",len_of_output_file_loc)
            ch_len = os.listdir(new_path1)
            #print("ch_len:",ch_len)
            #print("len of ch_len:",len(ch_len))
            ch_len_list.append(len(ch_len))
            #print("ch_len_list:",ch_len_list)
            #print("length_list:",length_list)
            reformat = final_sub_folder.replace('(',' ').replace(')',' ').replace('_',' ')
            reformat1 = reformat.split(' ')
            #print("reformat1:",reformat1)

            no1 = reformat1[1]
            no2 = reformat1[2]

            gg1 = int(no1)
            gg2 = int(no2)

            length = gg2 - gg1
            length = length + 1
            length_list.append(length)
            #print("length_list:",length_list)
            count = 1 * c
            c = c + 1 
            

            if len(ch_len) == length_list[count]: 
                
                #print("Processing:....................................")
                for filename in glob.glob(new_path):
                    fname.append(filename)
                    fname.sort()
                

                    
                    rename = filename.split('/')
                    
                    for_output_file_loc = rename[len_of_output_file_loc]
                    
                    
                    include_name = (rename[len_of_output_file_loc].replace('(',' ').replace(')',' ').replace('_',' ')).split(' ')
                    #take start point from file name ...eg: S1(1000_1100) take 1000 for start point
                    start_point = include_name[1]
                   
                    #take user name only ..eg:S1 for match user information that in user_dict.value
                    for_check_dict = include_name[0]
                   
                    audio_ID = int(start_point)

                if for_check_dict in user_dict.keys():

                    user_info_af_dict = user_dict[for_check_dict]
                    First_step_for_json = user_info_af_dict.split("-")

                    user_S = for_check_dict
                    Org_json = First_step_for_json[0]
                    Name_json = First_step_for_json[1]
                    Gender_json = First_step_for_json[2]
                    Age_json = First_step_for_json[3]
                    Language_json = First_step_for_json[4]
                       
                for ii in fname:
                    
                    audio_ID_for_json.append(audio_ID)
                    
                    audio_ID = audio_ID+1

                #print("Audio IDs:",audio_ID_for_json)
                len_of_all_file.append(len(audio_ID_for_json))
                #print("len_of_all_file:",len_of_all_file)
                fname = []
                list1 = []
                voice = []
                sr = []
                audio_ID_for_json = []

            else:
                
                #print(len(ch_len),length_list[count])
                print("Length not match Folder in :",new_path1)
                len_not_match = "Length not match Folder in : %s \n"%(new_path1)
                
                not_match_list.append(len_not_match)
                with open('not_match_list_file.txt', 'a') as g:
                    g.write(len_not_match)
    sum_of_all_file = sum(len_of_all_file)
    #print("sum_of_all_file:",sum_of_all_file)
    #print("Type sum_of_all_file:",type(sum_of_all_file))
    output_sum_of_all_file = "The Sum of overall wav file number is : %s : for this processing"%(sum_of_all_file)
    with open('TEst_output_sum_of_all_file.txt', 'w') as f:
         f.write(output_sum_of_all_file)
if __name__ == "__main__":
    apply_raw_voice_to_standard_all_file()
            

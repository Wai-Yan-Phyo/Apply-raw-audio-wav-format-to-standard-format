def apply_raw_voice_to_standard_all_file ():
    
    #### Function Information -------------------------------
    #For Standard Wave length Format with Speaker Information
    #For Speaker Information Database with JSON format
    #For Sum of over all wav file number for processing
    #Calculation for each Speaker Duration 
    #--------------------------------------------------------
    
    ##Import Lib---------------------------------------------
    import numpy as np
    import librosa
    import glob
    import os
    import sys
    from tqdm import tqdm
    import time
    import json
    ##--------------------------------------------------------
    
    start_time = time.time()
    
    ### Munual Mode --------------------------------------------------------------------------
    ##--------------Remove '#' When you want to run with input information manually-----------
    
    #file_location = input('Type Your File location Path : \n eg: /notebook/myG2P/Audio_test:')
    #onesec_location = input('Type Your Onesec location Path :')
    #output = input("Output Location: dont end with / :")
    #arr = input('Enter file location of user information Dict:')
    arr = (input('Enter file name & user information: \n eg: S1:bit-WaiYanMyintMyat-m-23-burmese: \n You can write multi user with comma:').split(','))
    
    ##-----------------------------------------------------------------------------------------

    ### Fix Mode -------------------------------------------------------------------------------
    ##----------- Close with '#' When you don't want to run automatically
    file_location = './new1'
    onesec_location = './onesecond.wav'
    output = './output1'
    #arr = './Speaker_Information.clean'
    nnn = input("Input Folder name for outputs txt:")

    #--------------------------------------------------------------------------------------------
    
    
    #Code for created Speaker Information Dict----------------------------------------------------
    #read_arr = open("%s"%(arr))
    #line = read_arr.readlines()
           
    keys = [i.split(':')[0] for i in arr]
    value = [i.split(':')[1] for i in arr]
    
    '''   
    for i in line:
        for_key = i.replace('\n','').split(":")[0]
        for_values = i.replace('\n','').replace(',','').split(":")[1]
        keys.append(for_key)
        value.append(for_values)
    '''
    #-----------------------------------------------------------------------------------------------
    
    #Create list for whole function-------------------------------------------------------------------
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
    #-------------------------------------------------------------------------------------------------
    
    #Create Dict for whole function--------------------------------------------------------------------
    Dict_for_json = {}
    Second_Dict = {}
    Speaker_info1 = {}
    Speaker_info2 = {}
    user_dict = {}
    
    #Read Path 
    read_path = os.listdir(file_location)
    print("read_path:",read_path)

    #Loop for User Information Dict
    for jjj in range(len(keys)):
       
        user_dict[keys[jjj]] = value[jjj]

    for name, info in user_dict.items():
        print('Folder name: {}, user information: {}'.format(name, info))
    
    #First Step To Find Folder under given path*** 
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
    print("read_path2_list:",read_path2_list)
             
    
    ###Get Information for Folder
    
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
            
            ch_len_list.append(len(ch_len))
            #print("ch_len_list:",ch_len_list)
            
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
            
            #### Process stage for if len of given folder name and number of wav file under its folder

            if len(ch_len) == length_list[count]: 

                for filename in glob.glob(new_path):
                    fname.append(filename)
                    fname.sort()

                    rename = filename.split('/')
                    #print('rename:',rename)
                    
                    for_output_file_loc = rename[len_of_output_file_loc]
                    #print("for_output_file_loc:",for_output_file_loc)
                    
                    #take user name file information ...eg: S1(1000_1100)
                    include_name = (rename[len_of_output_file_loc].replace('(',' ').replace(')',' ').replace('_',' ')).split(' ')
                    
                    #take start point from file name ...eg: S1(1000_1100) take 1000 for start point
                    start_point = include_name[1]
                    #print("start_point:",start_point)
                    
                    #take user name only ..eg:S1 for match user information that in user_dict.value
                    for_check_dict = include_name[0]
                    #print("for_check_dict:",for_check_dict)
                    
                    audio_ID = int(start_point)
                    
                #If Speaker Information Dict's key is in Folder name ,take value from Speaker Information Dict
                #Ta kal lo Folder name ka Speaker Information htae mhar pr ml so yin Speaker Information Dic yae Values tan po ko yu
                if for_check_dict in user_dict.keys():

                    user_info_af_dict = user_dict[for_check_dict]
                    First_step_for_json = user_info_af_dict.split("-")

                    user_S = for_check_dict
                    Org_json = First_step_for_json[0]
                    Name_json = First_step_for_json[1]
                    Gender_json = First_step_for_json[2]
                    Age_json = First_step_for_json[3]
                    Language_json = First_step_for_json[4]
                    print("Testing for Dict")
                    #print(user_S)
                    print(Org_json,Name_json,Gender_json,Age_json,Language_json)
                
                #Audio Processing Stage with Librosa ---------------------------------------------
                #Load 
                for ii in fname:
                    x_val , sr_val = librosa.load(ii)
                    voice.append(x_val)
                    sr.append(sr_val)
                    Duration = len(x_val)/sr_val
                    For_duration.append(Duration)
                #print("For_duration:",For_duration)
                
                sum_duration = sum(For_duration)
                #print(sum_duration) 
                    
                Second_Dict[user_info_af_dict] = {"Name":Name_json,
                                                  "Duration":sum_duration,
                                                  "Folder name":for_output_file_loc}
                                                  
                #print("Second_Dict:",Second_Dict)
                
                for name,info in Second_Dict.items():
                    
                    with open('%s_Speaker_Dict_with_sec.txt'%(nnn), 'a') as f:
                        f.write("{%s:%s,\n"%(name,info))
                print("Overall Duration For Under Speaker Folder: %s s"%(sum_duration))
               

                
                if sum_duration >= 3600:
                
                    Hour = sum_duration/3600
                    Hour_str = str(Hour)
                    print('This Speaker total Duration is : %d : Hours'%(Hour))
                
       
                    Speaker_info1[user_info_af_dict] = {"Name":Name_json,
                                                      "Duration":Hour,
                                                      "Folder name":for_output_file_loc}
                    print("Speaker_info1:",Speaker_info1)
                
                    for name1, info1 in Speaker_info1.items():
                    

                        print('Speaker name: {}, Duration: {}'.format(name1, info1))
                    with open('%s_Speaker_Dict_with_Hour.txt'%(nnn), 'a') as f:
                        f.write("{%s:%s,\n"%(name1,info1))
                   
                elif sum_duration >= 60:
                
                    Minute = float(sum_duration/60)
                    #print("Minute:",Minute)
                    Min_str = str(Minute)
                    #print("Min_str:",Min_str)
                    print('This Speaker total Duration is : %d : min'%(Minute))
                
                
                    Speaker_info2[user_info_af_dict] = {"Name":Name_json,
                                                      "Duration":Minute,
                                                      "Folder name":for_output_file_loc}
                    print("Speaker_info2:",Speaker_info2)
                
                    for name, info in Speaker_info2.items():
                
                        print('Speaker name: {}, Duration: {}'.format(name, info))
                    with open('%s_Speaker_Dict_with_min.txt'%(nnn), 'a') as f:
                        f.write("{%s:%s,\n"%(name,info))
                
                #Remove silence value 
                for j in voice:
                    afc , ind = librosa.effects.trim(j,ref=3)
                    list1.append(afc)

                #read one second wav file 
                one_sec_read , ssr = librosa.load('%s'%(onesec_location))
                
                #create output file location
                final_location = output+'/'+for_output_file_loc
                os.mkdir(final_location)
                
                #Add non silence wave to original wav front and back
                for i in list1:
                    front_onesec = np.append(one_sec_read,i)
                    back_onesec = np.append(front_onesec,one_sec_read)
                    
                    #write audio output under its associated user file 
                    librosa.output.write_wav('%s/%s-%d.wav'%(final_location,user_info_af_dict,audio_ID), back_onesec, sr_val)
                    
                    audio_ID_for_json.append(audio_ID)
                    #print("Audio IDs:",audio_ID_for_json)
                    audio_ID = audio_ID+1
                    
                len_of_all_file.append(len(audio_ID_for_json))
                
                ##For Speaker Information Database with Json
                if user_S in Dict_for_json.keys():

                    Dict_for_json[user_S]["Recorded_sentence"] = Dict_for_json[user_S]["Recorded_sentence"]+audio_ID_for_json
                    (Dict_for_json[user_S]["Recorded_sentence"]).sort()
                    print("if loop:")
                    
                else:
                    Dict_for_json[user_S]= {"Name":Name_json,
                                                      "Organization":Org_json,
                                                      "Gender":Gender_json,
                                                      "Age":Age_json,
                                                      "Native_Language":Language_json,
                                                      "Recorded_sentence":audio_ID_for_json}
                    print("else loop:")
                    
                #print("Dict_for_json.keys():",Dict_for_json.keys())
                
                #Reset for this below list
                fname = []
                list1 = []
                voice = []
                sr = []
                audio_ID_for_json = []
                Second_Dict = {}
                Speaker_info1 = {}
                Speaker_info2 = {}

            else:
                
                #Write Length not match folder with Txt format
                print("Length not match Folder in :",new_path1)
                len_not_match = "Length not match Folder in : %s \n"%(new_path1)
                with open('%s_length_not_match_list_file.txt'%(nnn), 'a') as g:
                    g.write(len_not_match)
    
    #For getting number of wav file for all Folder
    sum_of_all_file = sum(len_of_all_file)
    print("sum_of_all_file:",sum_of_all_file)
    #print("Type sum_of_all_file:",type(sum_of_all_file))
    output_sum_of_all_file = "The number of wav file for all Folder are : %s : for this processing"%(sum_of_all_file)
    with open('%s_output_sum_of_all_file.txt'%(nnn), 'w') as f:
         f.write(output_sum_of_all_file)
            
    #Write for Speaker Information Database with JSON       
    current_path = os.getcwd()
    print(current_path)
    
    exist = os.path.isfile(current_path+'/%s_Json_output_new.txt'%(nnn))
    print('file exists')
    print(exist)
    if not exist:
        with open("%s_Json_output_new.txt"%(nnn),"w+") as writefile:
            writefile.write(json.dumps(Dict_for_json))
    else:
        with open("%s_Json_output_new.txt"%(nnn), "r+") as readfile:
            readfile.seek(-1, os.SEEK_END)
            readfile.truncate()
        with open("%s_Json_output_new.txt"%(nnn),"a") as outfile:
##	    json.dump(Dict_for_json,"J.txt")
            outfile.write(','+json.dumps(Dict_for_json)[1:])
    
    print("---Yay %s seconds Yay---" % (time.time() - start_time))

if __name__ == "__main__":
    apply_raw_voice_to_standard_all_file()
            

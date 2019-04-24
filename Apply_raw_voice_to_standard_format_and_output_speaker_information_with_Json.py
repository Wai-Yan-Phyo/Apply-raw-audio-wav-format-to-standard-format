#!/usr/bin/env python
# coding: utf-8

# In[2]:


def apply_raw_voice_to_standard_all_file ():
    
    import numpy as np
    import librosa
    import glob
    import os
    import sys
    from tqdm import tqdm
    import time
    import json
    start_time = time.time()
    
    
    ###    Munual Mode --------------------------------------------------------------------------
    #file_location = input('Type Your File location Path : \n eg: /notebook/myG2P/Audio_test:')
    #onesec_location = input('Type Your Onesec location Path :')
    #user_name = input('Input Your Audio name,like bit-WaiYanMyintMyat-m-23-burmese :')
    #audio_ID = int(input('Audio ID :'))
    #output = input("Output Location: dont end with / :")
    #arr = input('Enter file location of user information Dict:')
    
    
    ###    Fix Mode --------------------------------------------------------------------------
    file_location = './Test_for_/S4'
    onesec_location = './onesecond.wav'
    output = './Test'
    #arr = 'S23:bit-WaiYanMyintMyat-m-23-burmese,S2:bit-Wai-m-23-burmese,S3:bit-Myat-m-23-burmese,S4:bit-Wait-m-23-burmese'.split(',')
    arr = './Speaker_Information.clean'
    #keys = [i.split(':')[0] for i in arr]
    #value = [i.split(':')[1] for i in arr]
    
    #  ------------------------------------------------------------------------------------------
    read_arr = open("%s"%(arr))
    line = read_arr.readlines()
           
    keys = []
    value = []
           
    for i in line:
        for_key = i.replace('\n','').split(":")[0]
        for_values = i.replace('\n','').replace(',','').split(":")[1]
        keys.append(for_key)
        value.append(for_values)
        
    voice = []
    sr = []
    list1 = []
    fname = []
    check_folder_lis = []
    length_list = []
    audio_ID_for_json = []
    test_json = []
    
    read_path = os.listdir(file_location)
        
    user_dict = {}
    
    for jjj in range(len(keys)):
       
        user_dict[keys[jjj]] = value[jjj]

    for name, info in user_dict.items():
        print('Folder name: {}, user information: {}'.format(name, info))
        
    for i in read_path:
        suffix = 'S'
        if suffix in i:
            rr = i
            check_folder_lis.append(rr)
    #check length for each folder,example: S1(1000_1200)>> 1200 - 1000 = 200 so length is 200        
    for jj in check_folder_lis:
 
        reformat = jj.replace('(',' ').replace(')',' ').replace('_',' ')
        reformat1 = reformat.split(' ')
	print("reformat1:",reformat1)

        no1 = reformat1[1]
        no2 = reformat1[2]

        gg1 = int(no1)
        gg2 = int(no2)

        length = gg2 - gg1
        length = length + 1
        length_list.append(length)

    #reformat folder name and set new path for read wave file in each sub folder
    #keep folder name length and number of wav file under each sub folder 
    #folder name length for insert in rename[len_of_output_file_loc] to get S23(1000_1004)
    Dict_for_json={}
    for idx, next_step in enumerate(check_folder_lis):
        
        new_path = file_location+'/'+next_step+'/*.wav'
        new_path1 = file_location+'/'+next_step
        
        list_file_location = file_location.split('/')

        len_of_output_file_loc = len(list_file_location)
  
        ch_len = os.listdir(new_path1)

        #processing only for file name length and number of wav file under sub folder are same...  
        if len(ch_len) == length_list[idx]:
            for_check_dict =''
            
            #read wav file under sub file with glob
            for filename in glob.glob(new_path):
                fname.append(filename)
                fname.sort()
 
                #split with '/' file name
                rename = filename.split('/')
                #print('rename:',rename)
                for_output_file_loc = rename[len_of_output_file_loc]
                
                #take user name file information ...eg: S1(1000_1100)
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
                    #print("Testing for Dict")
                    #print(user_S)
                    #print(Org_json,Name_json,Gender_json,Age_json,Language_json)

            #load each wav file with librosa library
            for ii in fname:
                x_val , sr_val = librosa.load(ii)
                voice.append(x_val)
                sr.append(sr_val)

            #cut only positive value in each wav file array 
            #take only speech spectrogram
            for j in voice:
                afc , ind = librosa.effects.trim(j,ref=3)
                list1.append(afc)
            #read one second wav file 
            one_sec_read , ssr = librosa.load('%s'%(onesec_location))
            #create output file location
            final_location = output+'/'+for_output_file_loc
            os.mkdir(final_location)
            
            #add one sec front and back in original wav file 
	    
            for i in list1:

                front_onesec = np.append(one_sec_read,i)
                back_onesec = np.append(front_onesec,one_sec_read)
                #write audio output under its associated user file 
                #librosa.output.write_wav('%s/%s-%d.wav'%(final_location,user_info_af_dict,audio_ID), back_onesec, sr_val)
		audio_ID_for_json.append(audio_ID)
		#print("Audio IDs:",audio_ID_for_json)
                audio_ID = audio_ID+1
		    
	        #audio_ID_for_json.append(audio_ID)
                #Dict_for_json = {}
		#if user_S in Dict_for_json.keys():
		   #for i in audio_ID_for_json:
		      # Dict_for_json[user_S]["Recorded_sentence"].append(i)
                #Dict_for_json[user_S] = []
	    #print("Dict_for_json.keys():",Dict_for_json.keys())
	    print("user_S:",user_S)
            if user_S in Dict_for_json.keys():
		    #Dict_for_json[user_S]["Recorded_sentence"]=Dict_for_json[user_S]["Recorded_sentence"]+audio_ID_for_json
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
	    print("Dict_for_json.keys():",Dict_for_json.keys())
            #new_Dic_for_json = Dict_for_json
	    #print("new_Dict_for_json: before",new_Dic_for_json)
	    #if user_S in Dict_for_json.keys():
	     #  for i in audio_ID_for_json:
	#	   new_Dict_for_json[user_S]["Recorded_sentence"].append(i)
	    #print("new_Dict_for_json: after",new_Dict_for_json)
            #check_user_and_recorded_sen = [user_S]+audio_ID_for_json
	    #test_json.append(check_user_and_recorded_sen)
	    #print("check_user_and_recorded_sen:",check_user_and_recorded_sen)
	    #print("Test json:",test_json)
	    #for i in test_json:
		#print("i:",i)
            #print("user_S:",user_S)
                #print(Dict_for_json)
		#test_json.append(Dict_for_json)
		#print("Test Json List:")
		#print(test_json)
		     

            fname = []
            list1 = []
            voice = []
            sr = []
	    audio_ID_for_json = []
	    #test_json = []
            #test_json.append(Dict_for_json)
	    #print("Test Json List")
	    #print(test_json)
	    #Dict_for_json[user_S]["Recorded_sentence"]=set(Dict_for_json[user_S]["Recorded_sentence"])


#            current_path = os.getcwd()
#            print(current_path)
#            exist = os.path.isfile(current_path+'/Json_output.txt')
#            print('file exists')
#            print(exist)
#            if not exist:
#            	with open("Json_output.txt","w+") as writefile:
#	            writefile.write(json.dumps(Dict_for_json))
#            else:
#                with open("Json_output.txt", "r+") as readfile:
#                    readfile.seek(-1, os.SEEK_END)
#                    readfile.truncate()
#    	        with open("Json_output.txt","a") as outfile:
##	    json.dump(Dict_for_json,"J.txt")
#	            outfile.write(','+json.dumps(Dict_for_json)[1:])

        else:
            print("Length not match Folder in :",new_path1)
    current_path = os.getcwd()
    print(current_path)
    exist = os.path.isfile(current_path+'/Json_output.txt')
    print('file exists')
    print(exist)
    if not exist:
       with open("Json_output.txt","w+") as writefile:
	   writefile.write(json.dumps(Dict_for_json))
    else:
       with open("Json_output.txt", "r+") as readfile:
            readfile.seek(-1, os.SEEK_END)
            readfile.truncate()
       with open("Json_output.txt","a") as outfile:
##	    json.dump(Dict_for_json,"J.txt")
	   outfile.write(','+json.dumps(Dict_for_json)[1:])
    print("---Yay %s seconds Yay---" % (time.time() - start_time))
if __name__ == "__main__":
    apply_raw_voice_to_standard_all_file()


# In[ ]:





def apply_raw_voice_to_standard_all_file ():
    
    import numpy as np
    import librosa
    import glob
    import os
    import sys
    from tqdm import tqdm
    import time
    start_time = time.time()
    
    
    ##       Manual Mode ----------------------------------------------------------------------------------------------------------
    file_location = input('Type Your File location Path : \n eg: /notebook/myG2P/Audio_test:')
    onesec_location = input('Type Your Onesec location Path :')
    output = input("Output Location: dont end with / :")
    arr = (input('Enter file name & user information: \n eg: S1:bit-WaiYanMyintMyat-m-23-burmese: \n You can write multi user with comma:').split(','))

    ##       Fix Mode --------------------------------------------------------------------------------------------------------------
    #file_location = '/notebook/myG2P/Audio_test'
    #onesec_location = './onesecond.wav'
    #output = './output'
    #arr = 'S23:bit-WaiYanMyintMyat-m-23-burmese,S2:bit-Wai-m-23-burmese,S3:bit-Myat-m-23-burmese,S4:bit-Wait-m-23-burmese'.split(',')

    ## -----------------------------------------------------------------------------------------------------------------------------
    list3 = [i.split(':')[0] for i in arr]
    list2 = [i.split(':')[1] for i in arr]
    #print('list3',list3)
    #print('list2',list2)
    voice = []
    sr = []
    list1 = []
    fname = []
    check_folder_lis = []
    length_list = []
    read_path = os.listdir(file_location)
    user_dict = {}
    for jjj in range(len(list3)):
       
        user_dict[list3[jjj]] = list2[jjj]

    for name, info in user_dict.items():
        print('Floder name: {}, user information: {}'.format(name, info))
        
    for i in read_path:
        suffix = 'S'
        if suffix in i:
            rr = i
            check_folder_lis.append(rr)
            
    for jj in check_folder_lis:
        #print("jj:",jj)
        reformat = jj.replace('(',' ').replace(')',' ').replace('_',' ')
        reformat1 = reformat.split(' ')
        print('reformat:',reformat1)
        #print('type:',type(reformat1))
        #no1 = reformat[8:12]
        #no2 = reformat[3:7]
        no1 = reformat1[1]
        no2 = reformat1[2]
        #print('no1:',no1)
        #print('no2:',no2)
        gg1 = int(no1)
        gg2 = int(no2)
        #print('gg1:',gg1)
        #print('gg2:',gg2)
        length = gg2 - gg1
	length = length + 1
        length_list.append(length)
        #print('length:',length)
        #print('length_list:',length_list)
        
    for idx, next_step in enumerate(check_folder_lis):
        new_path = file_location+'/'+next_step+'/*.wav'
        new_path1 = file_location+'/'+next_step
	list_file_location = file_location.split('/')
        #print('list_file_location:',list_file_location)
        len_of_output_file_loc = len(list_file_location)
        #print('len_of_output_file_loc:',len_of_output_file_loc)
        #print('new_path1:',new_path1)
        #print('new_path:',new_path)
        
        ch_len = os.listdir(new_path1)
        #print('total wav files:',len(ch_len))
            
        if len(ch_len) == length_list[idx]:
            for_check_dict =''
            
            for filename in glob.glob(new_path):
                fname.append(filename)
                fname.sort()
                #print("complete floder:",fname)
               
                rename = filename.split('/')
                for_output_file_loc = rename[len_of_output_file_loc]
                 
                include_name = (rename[len_of_output_file_loc].replace('(',' ').replace(')',' ').replace('_',' ')).split(' ')
                start_point = include_name[1]
                for_check_dict = include_name[0]
                audio_ID = int(start_point)
                #user_info_af_dict = [user_dict[keys]  for keys,value in user_dict.items() if keys in for_check_dict]
                #print("user_info_af_dict:",user_info_af_dict)
                #print("type user_info_af_dict:",type(user_info_af_dict))

                if for_check_dict in user_dict.keys():
                    #print('keys:',keys)
                    user_info_af_dict = user_dict[for_check_dict]
                    #print("user_info_af_dict:",user_info_af_dict)
                    #print("type user_info_af_dict:",type(user_info_af_dict))
                #print("for_check_dict:",for_check_dict)
                #print("include_name:",include_name)
                #print("start_point:",start_point)
                #print("for_output_file_loc:",for_output_file_loc)

            for ii in fname:
                x_val , sr_val = librosa.load(ii)
                voice.append(x_val)
                sr.append(sr_val)
                #print('done')
                
            for j in voice:
                afc , ind = librosa.effects.trim(j,ref=3)
                list1.append(afc)
                #print('len list1:',len(list1))
            one_sec_read , ssr = librosa.load('%s'%(onesec_location))
            final_location = output+'/'+for_output_file_loc
            os.mkdir(final_location)
            for i in list1:
                #list1.set_description("Processing %s" % i)
                front_onesec = np.append(one_sec_read,i)
                back_onesec = np.append(front_onesec,one_sec_read)
                librosa.output.write_wav('%s/%s-%d.wav'%(final_location,user_info_af_dict,audio_ID), back_onesec, sr_val)
                audio_ID = audio_ID+1
            fname = []
            list1 = []
            voice = []
            sr = []
        else:
            print("Length not match Folder in :",new_path1)
    print("---Yay %s seconds Yay---" % (time.time() - start_time))
if __name__ == "__main__":
    apply_raw_voice_to_standard_all_file()

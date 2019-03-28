def only_rename_raw_file ():
    
    import numpy as np
    import librosa
    import glob
    import os
    import sys
    from tqdm import tqdm
    import time
    start_time = time.time()
    
    
    ###    Munual Mode --------------------------------------------------------------------------
    file_location = input('Type Your File location Path : \n eg: /notebook/myG2P/Audio_test:')
    #onesec_location = input('Type Your Onesec location Path :')
    #user_name = input('Input Your Audio name,like bit-WaiYanMyintMyat-m-23-burmese :')
    #audio_ID = int(input('Audio ID :'))
    output = input("Output Location: dont end with / :")
    arr = (input('Enter file name & user information: \n eg: S1:bit-WaiYanMyintMyat-m-23-burmese \n You can write multi user with comma:').split(','))
    
    
    ###    Fix Mode --------------------------------------------------------------------------
    #file_location = '/notebook/myG2P/Audio_test/S1'
    #onesec_location = './onesecond.wav'
    #output = './output'
    #arr = 'S23:bit-WaiYanMyintMyat-m-23-burmese,S2:bit-Wai-m-23-burmese,S3:bit-Myat-m-23-burmese,S4:bit-Wait-m-23-burmese'.split(',')
    keys = [i.split(':')[0] for i in arr]
    value = [i.split(':')[1] for i in arr]
    
    #  ------------------------------------------------------------------------------------------
    voice = []
    sr = []
    list1 = []
    fname = []
    check_folder_lis = []
    length_list = []
    
    read_path = os.listdir(file_location)
        
    user_dict = {}
    for jjj in range(len(keys)):
       
        user_dict[keys[jjj]] = value[jjj]

    for name, info in user_dict.items():
        print('Floder name: {}, user information: {}'.format(name, info))
        
    for i in read_path:
        suffix = 'S'
        if suffix in i:
            rr = i
            check_folder_lis.append(rr)
    #check length for each folder,example: S1(1000_1200)>> 1200 - 1000 = 200 so length is 200        
    for jj in check_folder_lis:
 
        reformat = jj.replace('(',' ').replace(')',' ').replace('_',' ')
        reformat1 = reformat.split(' ')

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
                #print("fname:",fname)
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
                   # print('user_info_af_dict:',user_info_af_dict)
            final_location = output+'/'+for_output_file_loc
            #print('final_location:',final_location)
            os.mkdir(final_location)    
            
            for ii in fname:
               # print('ii:',ii)
                os.rename(ii,'%s/%s-%d.wav'%(final_location,user_info_af_dict,audio_ID))
                audio_ID = audio_ID+1
            fname = []
        else:
            print("Length not match Folder in :",new_path1)
    print("---Yay %s seconds Yay---" % (time.time() - start_time))
if __name__ == "__main__":
   only_rename_raw_file ()

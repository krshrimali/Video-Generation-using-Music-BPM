'''
Video Generation using Music BPM

Author: @krshrimali
Date: 25/6/2019
'''

# Steps
# 1. Read Data
# 2. Know BPM
# 3. Fast forward video based on the BPM


import cv2
import os
import sys
import moviepy.editor as mpe
import process_music as pm

class Dataset:
    def __init__(self, data_dir="data"):
        '''
        Parameters
        :data_dir: (str) data path, no '/' at the end. Default=data
        '''
        self.data = data_dir
        # TODO: Check if data_dir exists
        # Read Data
        self.list_images = os.listdir(self.data)
        print("Total Images: ", len(self.list_images))
        base_path = data_dir + "/"

        self.images = []
        for index, image_path in enumerate(self.list_images):
            print("Reading: {}/{}".format(index+1, len(self.list_images)))
            image_path = base_path + image_path
            self.images.append(cv2.imread(image_path, 1))
            
        # self.images is a vector containing all the images
    
    def __len__(self):
        '''
        Returns the count of images
        '''
        return len(self.images)

    def __getitem__(self, idx):
        '''
        Returns idx(th) image
        Parameters
        =====================
        :idx: (int)
        '''
        return self.images[idx]
    
    def get(self, idx):
        """
        Returns path of idx(th) image
        """
        return self.list_images[idx]

    def get_list(self):
        return self.images

    def show(self, idx):
        '''
        Displays idx(th) image
        '''
        cv2.imshow("Index: " + str(idx), self.images[idx])
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
if __name__ == "__main__":
    beats = pm.main()
    ds = Dataset()
    bps = 1 # This is the beats per second
    # BPM = 86
    '''
    video_details = {
        name: 'video.avi',
        height: ds[0].shape[0],
        width: ds[0].shape[1],
        layers: 3
    }
    '''

    print("len(beats): ", len(beats))

    name = 'video.avi'
    width = ds[0].shape[1]
    height = ds[0].shape[0]

    # Combine all the images
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    video = cv2.VideoWriter(name, 0, 1, (width, height), True)
    images = ds.get_list()
    print("This length is: ", len(images))

    for count, img in enumerate(images):
        print("Writing: ", count)
        print(ds.get(count))
        temp = cv2.imread("data/" + ds.get(count), 1)
        temp = cv2.resize(temp, (width, height), cv2.INTER_CUBIC)
        blur_amount = 50 * beats[count]
        if(blur_amount < 1):
            blur_amount = 5
        temp = cv2.blur(temp, (int(blur_amount), int(blur_amount)))
        video.write(temp)
    
    # cv2.destroyAllWindows()
    video.release()
    
    my_clip = mpe.VideoFileClip('video.avi')
    audio_background = mpe.AudioFileClip('never-ever.mp3')

    print("All read")

    final_audio = mpe.CompositeAudioClip([audio_background])
    final_clip = my_clip.set_audio(final_audio)
    final_clip.write_videofile("video-output.mp4")
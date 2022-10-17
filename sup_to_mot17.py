import os
import cv2
import configparser
import json




#make directory for images
def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)



# video.mp4 is a video of 9 seconds
rawVideoPath = "gtvideos"
motTrainPath = "mot/train/"
motTestPath = "mot/test/"

#make directory for images

make_dir(motTrainPath)
make_dir(motTestPath)




# iterate over files in
# that directory
for filename in os.listdir(rawVideoPath):
    f = os.path.join(rawVideoPath, filename)
    # checking if it is a file
    if os.path.isfile(f):
        #print filename without extension
        # print(os.path.splitext(filename)[0])
        vidFolderPath = motTrainPath + os.path.splitext(filename)[0]
        print(vidFolderPath)
        os.mkdir(vidFolderPath)
        os.mkdir(vidFolderPath + "/img1/")
        os.mkdir(vidFolderPath + "/gt/")
        os.mkdir(vidFolderPath + "/det/")

        # det.txt
        detFile = open(vidFolderPath + "/det/det.txt", "w")
        detFile.close()


        



        # gt.txt
        gtFile = open(vidFolderPath + "/gt/gt.txt", "w")

        # fill annotation file
        with open('annotations/' + filename + '.json') as f:
            data = json.load(f)

            # object Ids dict
            objIds = {}

            # object Ids
            i = 1;
            for obj in data['objects']:
                objIds[obj['key']] = i;
                i += 1;

            # number of top iterations
            topIterations = len(objIds)
            
            # iterate over frames
            for  ii in range(topIterations):
                for frame in data['frames']:
                    # iterate over figures
                    for figure in frame['figures']:
                        fish_id = objIds[figure['objectKey']]
                        xStart = figure['geometry']['points']['exterior'][0][0]
                        yStart = figure['geometry']['points']['exterior'][0][1]
                        xEnd = figure['geometry']['points']['exterior'][1][0]
                        yEnd = figure['geometry']['points']['exterior'][1][1]
                        xWidth = xEnd - xStart
                        yWidth = yEnd - yStart
                        if fish_id == ii + 1:
                            finalEntry = f"{frame['index'] + 1},{fish_id},{xStart},{yStart},{xWidth},{yWidth},1,-1,-1,-1"
                        
                            # if not last line
                            if(ii != topIterations - 1 or frame['index'] != len(data['frames']) - 1):
                                #write line at newline 
                                gtFile.write(finalEntry + "\n")
                            else:
                                #write line without newline
                                gtFile.write(finalEntry)


        gtFile.close()

      
        # Opens the Video file
        cap= cv2.VideoCapture(rawVideoPath + "/" + filename)
        i=1

        print("Converting %s" %rawVideoPath + "/" + filename)
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == False:
                break
            cv2.imwrite(vidFolderPath  + "/img1/%06d.jpg" % i,frame)
            i+=1

        # seqinfo.ini
        config = configparser.ConfigParser()
        config.read(vidFolderPath + "/seqinfo.ini")

        try:
            config.add_section("Sequence")
        except configparser.DuplicateSectionError:
            pass
            
        config.set("Sequence", "name", os.path.splitext(filename)[0])
        config.set("Sequence", "imDir", "img1")
        config.set("Sequence", "frameRate", "30")
        config.set("Sequence", "seqLength", str(i-1))
        config.set("Sequence", "imWidth", "1920")
        config.set("Sequence", "imHeight", "1080")
        config.set("Sequence", "imExt", ".jpg")


        with open(vidFolderPath + "/seqinfo.ini", "w") as config_file:
            config.write(config_file)
        

        


        cap.release()
    cv2.destroyAllWindows()
        


                
        






# Writing Data to ini file
config = configparser.ConfigParser()




# # Opens the Video file
# cap= cv2.VideoCapture(filename)
# i=1

# print("Converting %s" %filename)
# while(cap.isOpened()):
#     ret, frame = cap.read()
#     if ret == False:
#         break
    
#     cv2.imwrite('ds0/img1/%06d.jpg' % i,frame)
#     i+=1

# cap.release()
# cv2.destroyAllWindows()
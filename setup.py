import os

def convertVideo(inputVideo):
    command = """ffmpeg -i input_videos/'{inputVideo}' \
    -c copy temp_videos/temp1.mkv""".format(inputVideo=inputVideo)

    os.system(command)

def addOverlay(class_type,text,extention):
    if extention == "webm":
        command = '''ffmpeg -i class_type_videos/{class_type}.mkv -vf drawtext="text={text} \
        :fontcolor=black :fontsize=34: box=1: boxcolor=white@1.0: boxborderw=10: x=(w-text_w)/2: y=(h-text_h)-100" \
        -vcodec libvpx -acodec libopus temp_videos/class_type_video.mkv'''.format(class_type=class_type,text=text)
    else:
        command = '''ffmpeg -i class_type_videos/{class_type}.mkv -vf drawtext="text={text} \
        :fontcolor=black :fontsize=34: box=1: boxcolor=white@1.0: boxborderw=10: x=(w-text_w)/2: y=(h-text_h)-100" \
        -c:a copy temp_videos/class_type_video.mkv'''.format(class_type=class_type,text=text)

    os.system(command)

def conacatnateVideos(finalVideoName):
    print("*" * 100)
    print(finalVideoName)
    print("*" * 100)

    with open('input.txt','w') as file:
        file.write("file 'temp_videos/class_type_video.mkv'\n")
        file.write("file 'temp_videos/temp1.mkv'\n")

    command = """ffmpeg -f concat -i input.txt \
    -c copy output_videos/{finalVideoName}""".format(finalVideoName=finalVideoName)
    os.system(command)

def deleteTempVideo():
    os.remove("temp_videos/temp1.mkv")
    os.remove("temp_videos/class_type_video.mkv")


def setup():
    for video_file in os.listdir('input_videos/'):
        if(video_file != ".DS_Store"):
            videodetails = video_file.strip().split('_')
            curriculum_type = videodetails[0]
            curriculum_lesson_code = videodetails[1].split('.')[0]
            video_extention = videodetails[1].split('.')[1]
            text = curriculum_type + " " + videodetails[1].split('.')[0]

            final_video_name = curriculum_type + "_" + videodetails[1].split('.')[0] + ".mkv"
            convertVideo(video_file)
            addOverlay(curriculum_type, text, video_extention)
            conacatnateVideos(final_video_name)
            deleteTempVideo()

setup()

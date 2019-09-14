import os
import csv
import re

sessionId = None
classId = None
teacherName = None
cutTimings = ''

def splitVideo(cutTimings,filename,sessionId):
    for i in range(len(cutTimings)):
        startTime = cutTimings[i][0]
        endTime = cutTimings[i][1]
        tempVideo = "temp" + str(i+1)
        command_1 = """ffmpeg -i inputVideos/'{filename}' -ss {startTime} -to {endTime} \
        -c copy tempVideos/{tempVideo}.webm\
        """.format(filename=filename,startTime=startTime,endTime=endTime,tempVideo=tempVideo)

        command_2 = """ffmpeg -i inputVideos/'{filename}' -ss {startTime} -c copy \
        tempVideos/{tempVideo}.webm""".format(filename=filename,startTime=startTime,tempVideo=tempVideo)

        if cutTimings[i][1] == "end":
            os.system(command_2)
        else:
            os.system(command_1)

def addOverlay(details):
    classId = details[0][:3].lower()
    text = "     ".join(details[0:3])
    command = '''ffmpeg -i classTypeVideos/{classId}.webm -vf drawtext="text={text} \
    :fontcolor=black :fontsize=24: box=1: boxcolor=white@1.0: boxborderw=10: x=(w-text_w)/2: y=(h-text_h)-100" \
    -c:v libvpx tempVideos/classType.webm'''.format(classId=classId,text=text)

    os.system(command)

def concatenateVideos(cutTimings,sessionId):
    with open('input.txt','w') as inputFile:
        inputFile.write("file 'tempVideos/classType.webm'\n")
        for i in range(len(cutTimings)):
            inputFile.write("file 'tempVideos/temp" +str(i+1) +".webm'\n")

    command = "ffmpeg -f concat -i input.txt -c copy finalVideos/{sessionId}.mkv".format(sessionId=sessionId)
    os.system(command)


# def convertVideo(sessionId):
#     command = """ffmpeg -fflags +genpts -r 25 -i output.mkv \
#     -c copy finalVideos/{sessionId}.mov""".format(sessionId=sessionId)
#     os.system(command)


def deleteTempVideo(cutTimings):
    for i in range(len(cutTimings)):
        tempVideo = "temp" + str(i+1) +".webm"
        command = "tempVideos/{tempVideo}".format(tempVideo=tempVideo)
        os.remove(command)
    os.remove("tempVideos/classType.webm")


def setup():
    for filename in os.listdir('inputVideos/'):
        videodetails = filename.strip('-').split('-')
        sessionId = videodetails[0].strip()
        # classId = videodetails[1].strip()
        with open('allCsv/videoDetails.csv') as details:
            data = csv.reader(details)
            for row in data:
                if(row[2] == sessionId):
                    cutTimings = re.split("-|;",row[4].strip())
                    cutTimings.insert(0,"00:00:00")
                    cutTimings.append("end")
                    cutTimings = list(zip(cutTimings[::2], cutTimings[1::2]))
                    splitVideo(cutTimings,filename,sessionId)
                    addOverlay(row)
                    concatenateVideos(cutTimings,sessionId)
                    # convertVideo(sessionId)
                    deleteTempVideo(cutTimings)

setup()

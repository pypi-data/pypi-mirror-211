"""
                Video faceparser usage
"""
import glob
from innerverz import Video_FaceParser
VF = Video_FaceParser()

image_path_list = sorted(glob.glob('./assets/*.*'))

VF(image_path_list, './result')


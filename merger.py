import os

def get_segments_list(path):
    segments_list=[file for file in os.listdir(path)]
    segments_list = sorted(segments_list,key=lambda x: int(x.replace('.ts','')))
    segments_list = [os.path.join(path,each) for each in segments_list]
    return segments_list



def concatenate(segments_list,name):
    os.system(f"""ffmpeg -i "concat:{'|'.join(segments_list)}" -c copy {name}""")


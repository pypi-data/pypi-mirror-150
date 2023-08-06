import requests
import os, json
import tempfile
import base64
import uuid,math,shutil
from gbackup import *
import numpy as np
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import textwrap
from moviepy.editor import *
def upload_file(email, path):
    drh = DriverHelper()
    conf = drh.create_driver_config(email)
    file_name = os.path.basename(path)
    return Client(conf, "upload", path, "").upload_file(file_name,path, "ROOT_FOLDER")
def download_gdrive(id,email, path):
    drh = DriverHelper()
    conf = drh.create_driver_config(email)
    Client(conf, "download", path, "").download_file(id,path)

def create_vid_text_img(img_bg, img_text, root_path):
    final_path = f"{root_path}/txt-on-img-vid-{str(uuid.uuid4())}.avi"
    cmd=f'ffmpeg -y -loop 1 -i {img_bg} -t 10 -r 1 -loop 1 -i {img_text} -filter_complex " scale=w=3*1280:h=3*720, zoompan=z=min(max(zoom\,pzoom)+0.0008\,1.5):d=250:s=1280x720, setsar=1 [bg]; [bg][1:v]overlay=0:500:shortest=1,format=yuv420p[v1];[v1] fade=in:0:30[v] " -map "[v]" -c:v h264 -crf 18 -preset veryfast {final_path}'
    os.system(cmd)
    return final_path
def create_arr_vid_text(arr_img, arr_text, root_path):
    i=0
    arr_input = []
    while i < len(arr_text):
        arr_input.append(create_vid_text_img(arr_img[i], arr_text[i], root_path))
        i += 1
    final_path= concat_video(arr_input, root_path)
    for item in arr_input:
        os.remove(item)
    for item in arr_img:
        os.remove(item)
    for item in arr_text:
        os.remove(item)
    return final_path
def make_image_hd(img_path, root_dir,direct=3,w=1280,h=720):
    out=f"{root_dir}/{str(uuid.uuid4())}.jpg"
    arr_direct=[-6,-9,-18,180,18,9,6]
    direct_rs=arr_direct[direct]
    rotate_code=f",rotate=PI/{direct_rs}:c=none:ow=rotw(PI/{direct_rs}):oh=roth(PI/{direct_rs})"
    if direct==3:
        rotate_code=""
    cmd=f'ffmpeg -i "{img_path}" -filter_complex "[0:v] split=2 [video0-1][video0-2];[video0-1] ' \
        f'scale=w={w}:h={h},boxblur=luma_radius=min(h\,w)/20:luma_power=1:chroma_radius=min(cw\,h)/20:chroma_power=1,' \
        f'setsar=1 [bg0];[video0-2] scale=w=min(iw\,min(iw*{h}/ih\,{w})):h=min(ih\,min(ih*{w}/iw\,{h})),' \
        f'setsar=1{rotate_code} [video0-2-scaled];[bg0][video0-2-scaled] overlay=x=(W-w)/2:y=(H-h)/2 [video0]" -map "[video0]" "{out}"'
    cmd_bigger = f'ffmpeg -i "{img_path}" -filter_complex "[0:v] split=2 [video0-1][video0-2];[video0-1] ' \
          f'scale=w={w}:h={h},boxblur=luma_radius=min(h\,w)/20:luma_power=1:chroma_radius=min(cw\,h)/20:chroma_power=1,' \
          f'setsar=1 [bg0];[video0-2] scale=w=min(iw*{h}/ih\,{w}):h=min(ih*{w}/iw\,{h}),' \
          f'setsar=1{rotate_code} [video0-2-scaled];[bg0][video0-2-scaled] overlay=x=(W-w)/2:y=(H-h)/2 [video0]" -map "[video0]" "{out}"'
    #print(cmd_bigger)
    os.popen(cmd_bigger).read()
    return out
def create_loop(clip_path, loop_duration, root_path):
    try:
        clip = VideoFileClip(clip_path)
        clip_duration = clip.duration
        clip.close()
        if clip_duration > loop_duration:
            return clip_path
        tmp_clip_path =f'{root_path}/{str(uuid.uuid4())}-{os.path.basename(clip_path)}'
        shutil.copyfile(clip_path, tmp_clip_path)

        times = int(math.ceil(loop_duration / clip_duration))
        file_merg_path =f'{root_path}/{str(uuid.uuid4())}'
        final_clip_path =f'{root_path}/{str(uuid.uuid4())}-final-{os.path.basename(clip_path)}'
        file_merg = open(file_merg_path, "a")
        for i in range(times):
            file_merg.write("file '%s'\n" % os.path.basename(tmp_clip_path))
        file_merg.close()
        cmd = "ffmpeg -y -f concat -safe 0 -i \"%s\" -codec copy \"%s\"" % (file_merg_path, final_clip_path)
        os.system(cmd)
        os.remove(tmp_clip_path)
        os.remove(file_merg_path)
        clip = VideoFileClip(final_clip_path)
        clip_duration = clip.duration
        clip.close()
        if clip_duration < loop_duration:
            return None
        return final_clip_path
    except:
        return None
def concat_video(inputs, root_path):
    try:
        arr_tmp=[]
        file_merg_path = f'{root_path}/{str(uuid.uuid4())}'
        file_merg = open(file_merg_path, "a")
        for input in inputs:
            tmp_clip_path = f'{root_path}/{str(uuid.uuid4())}-{os.path.basename(input)}'
            arr_tmp.append(tmp_clip_path)
            shutil.copyfile(input, tmp_clip_path)
            file_merg.write("file '%s'\n" % os.path.basename(tmp_clip_path))
        final_clip_path = f'{root_path}/{str(uuid.uuid4())}-final-{os.path.basename(input)}'
        file_merg.close()
        cmd = "ffmpeg -y -f concat -safe 0 -i \"%s\" -codec copy \"%s\"" % (file_merg_path, final_clip_path)
        os.system(cmd)
        for tmp_p in arr_tmp:
            os.remove(tmp_p)
        os.remove(file_merg_path)
        return final_clip_path
    except:
        return None
def download_file(url, root_dir=None, ext= None):
    rs = None
    try:
        if ext:
            file_name = str(uuid.uuid4()) + "." + ext
        else:
            file_name = os.path.basename(url)
        if not root_dir:
            rs = get_dir('download') + file_name
        else:
            rs = root_dir + "/" + file_name
        if "gdrive" in url:
            download_gdrive(url.split(";;")[-1],url.split(";;")[-2],rs)
        else:
            r = requests.get(url)
            with open(rs, 'wb') as f:
                f.write(r.content)
    except:
        rs = None
        pass
    return rs

def cache_file(url):
    if not url:
        return None
    rs = None
    try:
        rs = get_dir('cached') + os.path.basename(url)
        if os.path.exists(rs):
            return rs #cached
        r = requests.get(url)
        with open(rs, 'wb') as f:
            f.write(r.content)
    except:
        rs = None
        pass
    return rs


def save_file(root,name,content,is_json=False):
    path=os.path.join(root,name)
    with open(path,"w", encoding='utf-8') as f:
        if is_json:
            json.dump(content, f)
        else:
            f.write(content)
    return path

def get_dir(dir):
    tmp_download_path = tempfile.gettempdir() + "/"+dir+"/"
    if not os.path.exists(tmp_download_path):
        os.makedirs(tmp_download_path)
    return tmp_download_path

def calsizeOfCharacter(font, text):
    avg_char_width = sum(font.getsize(char)[0] for char in text) / len(text)
    return int(avg_char_width)
def draw_text_img(text, font_path, bg_path, root_path, margin=50):
    final_path = f"{root_path}/txt-on-img-{str(uuid.uuid4())}.png"
    fontsize = 33
    max_char_count = 90
    font = ImageFont.truetype(font_path, fontsize)
    img = Image.open(bg_path)
    w , h= img.size
    draw = ImageDraw.Draw(img)
    while True:
        scaled_wrapped_text = textwrap.fill(text=text, width=max_char_count)
        x = draw.textsize(scaled_wrapped_text, font)
        if x[1] > h:
            fontsize -= 1
            font = ImageFont.truetype(font_path, fontsize)
            max_char_count = 90
            continue
        if x[0] > w-2*margin:
            bias = max(int((x[0] - (w-2*margin)) / calsizeOfCharacter(font, text)), 1)
            print(bias)
            max_char_count -= bias
            continue
        break
    draw.text((margin, 0), scaled_wrapped_text, (255, 255, 255), font=font)
    img.save(final_path)
    return final_path
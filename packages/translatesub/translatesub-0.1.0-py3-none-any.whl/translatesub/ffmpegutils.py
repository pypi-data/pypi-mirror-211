import os
import shutil
import subprocess
from translatesub.langutils import convert_639_1_to_2, convert_639_2_to_1

def ffmpeg_verify():
  return (shutil.which('ffmpeg') is not None) and (shutil.which('ffprobe') is not None)

def get_subtitle_list(mkv_file_path):
    ffprobe_cmd = [
        'ffprobe',
        '-loglevel', 'error',
        '-select_streams', 's',
        '-show_entries', 'stream=index:stream_tags=language',
        '-of', 'csv=p=0',
        mkv_file_path
    ]

    # Run ffmpeg command to extract each subtitle track separately
    ffprobe = subprocess.run(ffprobe_cmd, capture_output=True, text=True)
    if ffprobe.returncode == 0:
        return ffprobe.stdout.strip().split('\n')
    
    raise Exception(ffprobe.stderr.strip())

def extract_subtitles(mkv_file_path, from_sub):
    subs = get_subtitle_list(mkv_file_path)
    if from_sub >= len(subs):
        raise Exception(f"Index {from_sub} is greater than the number of indexes available ({len(subs)})")
    line = subs[from_sub]
    values = line.strip().split(',')
    if len(values) != 2:
        raise Exception(f"Index {from_sub} selected does not contains a valid ISO 639-2 language definition")
    sub_id = values[0]
    lang_source_639_2 = values[1]
    lang_source = convert_639_2_to_1(lang_source_639_2)
    if lang_source:
        # Get the subtitles as srt format in a variable and returns it to the caller.
        ffmpeg_cmd = [
            'ffmpeg',
            '-hide_banner',
            '-i', mkv_file_path,
            '-map', f'0:{sub_id}',
            '-c:s', 'srt',
            "-f", "srt",
            "-"
        ]
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout, lang_source
            #return result.stdout, "en"
    else:
        raise Exception(f"Index {from_sub} selected does not contains a valid ISO 639-2 language definition")
    return "", ""

def add_translated_subtitles(mkv_file_path, translated_subs_file_path, target_language):
    subs = get_subtitle_list(mkv_file_path)
    tmp_file = f"{os.path.splitext(mkv_file_path)[0]}_new.mkv"
    target_lang_639_2 = convert_639_1_to_2(target_language)
    if target_lang_639_2 == None:
        target_lang_639_2 = target_language

    ffmpeg_cmd = [
        'ffmpeg',
        '-i', mkv_file_path,
        '-i', translated_subs_file_path,
        '-c', 'copy',
        '-scodec', 'subrip',
        '-map', '0',
        '-map', '1',
        f"-metadata:s:s:{len(subs)}", f"language={target_lang_639_2}",
        "-y",
        tmp_file
    ]

    ffmpeg = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    if ffmpeg.returncode == 0:
        os.remove(mkv_file_path)
        os.rename(tmp_file, mkv_file_path)
        return True
    
    raise ffmpeg.stderr

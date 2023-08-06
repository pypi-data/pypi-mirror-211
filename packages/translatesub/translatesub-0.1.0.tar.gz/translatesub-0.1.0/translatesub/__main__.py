import sys
import os
import logging
from translatesub import AZURE_CONFIG_ERROR, ERRORS, FFMPEG_ERROR, azure, ffmpegutils

def main():
    usage = f"Usage: \n\tParameters: \n\t\t<mkv file> [<from index>] [<target_language=pt (use ISO 639-1 codes)>]\n\n\tExamples:\n\t\tpython -m translatesub\n\t\t\tShow this message.\n\n\t\tpython -m translatesub file.mkv\n\t\t\tShow this message and the available subtitles embeded in the file.mkv\n\n\t\tpython -m translatesub file.mkv 0\n\t\t\tGet the subtitle an index 0, translate it with azure translate to portuguese and embed it in the file.mkv as the last index of subtitles.\n\n\t\tpython -m translatesub file.mkv 0 es\n\t\t\tGet the subtitle an index 0, translate it with azure translate to spanish and embed it in the file.mkv as the last index of subtitles."
    if len(sys.argv) <= 1:
        print(usage)
        sys.exit(0)

    mkv_file_path = sys.argv[1]

    if not ffmpegutils.ffmpeg_verify():
       logging.fatal(ERRORS[FFMPEG_ERROR])
       sys.exit(FFMPEG_ERROR)

    if not azure.azure_verify():
       logging.fatal(ERRORS[AZURE_CONFIG_ERROR])
       sys.exit(AZURE_CONFIG_ERROR)


    if len(sys.argv) == 2:
        subs = ffmpegutils.get_subtitle_list(mkv_file_path=mkv_file_path)
        print(usage)
        print()
        print("Available subtitles:")
        print("Index -> subtitle")
        i = 0
        for sub in subs:
            print(f"{i} -> {sub}")
            i = i + 1
        sys.exit(0)

    target_language = "pt"
    if len(sys.argv) > 3:
        target_language = sys.argv[3]
    
    grab_translate_and_add_sub_to_mkv(mkv_file_path, target_language, int(sys.argv[2]))

def grab_translate_and_add_sub_to_mkv(mkv_file_path, target_language, from_sub):
  try:
    logging.info(f"Working on file {mkv_file_path}")

    # Extract subtitles from the MKV file
    logging.info(f"Extracting subtitles from index {from_sub}...")
    srt, source_lang = ffmpegutils.extract_subtitles(mkv_file_path, from_sub)
    
    # Translate the extracted subtitles
    logging.info("Translating...")
    pt_srt = azure.translate_subtitles(srt, target_lang=target_language, source_lang=source_lang)

    translated_subs_file_path = f"{os.path.splitext(mkv_file_path)[0]}_{target_language}.srt"
    logging.info(f"Saving translated srt file to {translated_subs_file_path}...")
    pt_srt.save(translated_subs_file_path)

    ## Add the translated subtitles to the original MKV file
    logging.info(f"Inserting {target_language} subtitle to {mkv_file_path}...")
    ffmpegutils.add_translated_subtitles(mkv_file_path, translated_subs_file_path, target_language)

    logging.info("Done.")
  except Exception as e:
    logging.exception("Exception: %s", e)

if __name__ == "__main__":
    main()
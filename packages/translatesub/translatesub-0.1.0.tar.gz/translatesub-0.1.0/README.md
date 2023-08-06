# translatesub

This project is a home made subtitles translation and embed for MKV files.

## Requirements

[Python](https://www.python.org/) > 3.9

[ffmpeg and ffprobe](https://ffmpeg.org/) must be on path

TRANSLATOR_TEXT_ENDPOINT, TRANSLATOR_TEXT_SUBSCRIPTION_KEY and TRANSLATOR_TEXT_REGION must be defined either on environment variables or in a .env file in current directory or home directory. This are for [azure translator API](https://github.com/MicrosoftTranslator/Text-Translation-API-V3-Python).

## Installing

Clone this repo, enter in the directory and with python enabled terminal, install it.

```
$ git clone https://github.com/Bigous/translatesub
$ cd translatesub
$ python -m pip install -e .
```

## Runing

In a python enabled terminal, after installing it, you can run it.

```
$ python -m translatesub
Usage:
        Parameters:
                <mkv file> [<from index>] [<target_language=pt (use ISO 639-1 codes)>]

        Examples:
                python -m translatesub
                        Show this message.

                python -m translatesub file.mkv
                        Show this message and the available subtitles embeded in the file.mkv

                python -m translatesub file.mkv 0
                        Get the subtitle an index 0, translate it with azure translate to portuguese and embed it in the file.mkv as the last index of subtitles.

                python -m translatesub file.mkv 0 es
                        Get the subtitle an index 0, translate it with azure translate to spanish and embed it in the file.mkv as the last index of subtitles.
```

Passing just the filename it lists all the subtitles with language information if available.

```
$ python -m translatesub tmp.mkv
Usage:
        Parameters:
                <mkv file> [<from index>] [<target_language=pt (use ISO 639-1 codes)>]

        Examples:
                python -m translatesub
                        Show this message.

                python -m translatesub file.mkv
                        Show this message and the available subtitles embeded in the file.mkv

                python -m translatesub file.mkv 0
                        Get the subtitle an index 0, translate it with azure translate to portuguese and embed it in the file.mkv as the last index of subtitles.

                python -m translatesub file.mkv 0 es
                        Get the subtitle an index 0, translate it with azure translate to spanish and embed it in the file.mkv as the last index of subtitles.

Available subtitles:
Index -> subtitle
0 -> 2,ara
1 -> 3,ger
2 -> 4,eng
3 -> 5,spa
4 -> 6,spa
5 -> 7,fre
6 -> 8,hin
7 -> 9,ita
8 -> 10,por
9 -> 11,rus
```

Passing the index, it does all the process targeting by default the portuguese language. In the following example it is translating from english to portuguese and inserting it in the end of the file. It leavs, in the same directory as the mkv file, the generated srt file.

```
$ python -m translatesub tmp.mkv 2
2023-05-31 17:01:45,519 - INFO - Working on file tmp.mkv
2023-05-31 17:01:45,519 - INFO - Extracting subtitles from index 2...
2023-05-31 17:01:46,096 - INFO - Translating...
2023-05-31 17:01:46,810 - INFO - Saving translated srt file to tmp_pt.srt...
2023-05-31 17:01:46,830 - INFO - Inserting pt subtitle to tmp.mkv...

$ lsd tmp*
 tmp.mkv   tmp_pt.srt

$ python -m translatesub tmp.mkv
Usage:
        Parameters:
                <mkv file> [<from index>] [<target_language=pt (use ISO 639-1 codes)>]

        Examples:
                python -m translatesub
                        Show this message.

                python -m translatesub file.mkv
                        Show this message and the available subtitles embeded in the file.mkv

                python -m translatesub file.mkv 0
                        Get the subtitle an index 0, translate it with azure translate to portuguese and embed it in the file.mkv as the last index of subtitles.

                python -m translatesub file.mkv 0 es
                        Get the subtitle an index 0, translate it with azure translate to spanish and embed it in the file.mkv as the last index of subtitles.

Available subtitles:
Index -> subtitle
0 -> 2,ara
1 -> 3,ger
2 -> 4,eng
3 -> 5,spa
4 -> 6,spa
5 -> 7,fre
6 -> 8,hin
7 -> 9,ita
8 -> 10,por
9 -> 11,rus
10 -> 12,por
```

The last parameter is the language to which you want it to translate to. It must be in [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) code and be [supported by azure](https://learn.microsoft.com/en-us/azure/cognitive-services/translator/language-support). I supports more than 100 languages, so, this will not be an issue.

## Common Issues

When you don't have azure variables seted (neither in environmen nor in .env file that can be in the current folder or home folder). Fix it following the [microsoft guide](https://learn.microsoft.com/pt-br/azure/cognitive-services/Translator/quickstart-translator-rest-api?tabs=csharp).

```
$ python -m translatesub .\tmp.mkv 0 es
2023-05-31 16:36:51,300 - CRITICAL - TRANSLATOR_TEXT_ENDPOINT, TRANSLATOR_TEXT_SUBSCRIPTION_KEY or TRANSLATOR_TEXT_REGION variables not defined
```

When you don't have `ffmpeg` or `ffprobe` in your path:

```
$ python -m translatesub .\tmp.mkv 0 es
2023-05-31 17:16:48,345 - CRITICAL - ffmpeg or ffprobe not found in path
```

Any other problem that rises an exception will thow the exception (for example out of memory, out of space).

One common case of problem can be an embeded subtitle in mkv with no language description or with an invalid language description (mkv files use ISO 639-2 language description). This will rise an exception informing that.

```
$ python -m translatesub tmp.mkv
Usage:
        Parameters:
                <mkv file> [<from index>] [<target_language=pt (use ISO 639-1 codes)>]

        Examples:
                python -m translatesub
                        Show this message.

                python -m translatesub file.mkv
                        Show this message and the available subtitles embeded in the file.mkv

                python -m translatesub file.mkv 0
                        Get the subtitle an index 0, translate it with azure translate to portuguese and embed it in the file.mkv as the last index of subtitles.

                python -m translatesub file.mkv 0 es
                        Get the subtitle an index 0, translate it with azure translate to spanish and embed it in the file.mkv as the last index of subtitles.

Available subtitles:
Index -> subtitle
0 -> 2

$ python -m translatesub tmp.mkv 0
2023-05-31 17:31:30,169 - INFO - Working on file tmp.mkv
2023-05-31 17:31:30,170 - INFO - Extracting subtitles from index 0...
2023-05-31 17:31:30,196 - ERROR - Exception: Index 0 selected does not contains a valid ISO 639-2 language definition
Traceback (most recent call last):
  File "R:\Richard\src\GitHub\Bigous\translatesub\translatesub\__main__.py", line 47, in grab_translate_and_add_sub_to_mkv
    srt, source_lang = ffmpegutils.extract_subtitles(mkv_file_path, from_sub)
  File "R:\Richard\src\GitHub\Bigous\translatesub\translatesub\ffmpegutils.py", line 33, in extract_subtitles
    raise Exception(f"Index {from_sub} selected does not contains a valid ISO 639-2 language definition")
Exception: Index 0 selected does not contains a valid ISO 639-2 language definition
```

In the above case, you can infer the language of the subtitle (watching the video) and setting it with ffmpeg before calling this tool to translate.

```
$ ffmpeg -i .\tmp.mkv -c copy -map 0 -metadata:s:s:0 language=por -y tmp2.mkv
```

And than try again in the new file

```
$ python -m translatesub tmp2.mkv 0
2023-05-31 17:37:34,114 - INFO - Working on file tmp2.mkv
2023-05-31 17:37:34,114 - INFO - Extracting subtitles from index 0...
2023-05-31 17:37:34,414 - INFO - Translating...
2023-05-31 17:37:34,762 - INFO - Saving translated srt file to tmp2_pt.srt...
2023-05-31 17:37:34,766 - INFO - Inserting pt subtitle to tmp2.mkv...
2023-05-31 17:37:36,225 - INFO - Done.
```
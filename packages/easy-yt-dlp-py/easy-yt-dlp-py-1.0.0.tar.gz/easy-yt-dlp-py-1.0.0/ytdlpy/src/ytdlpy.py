def ytdlpy(dir,filter2,filter3):
    import os

    cmd = 'cmd /C "cd '+dir+' & '
    
    filter3 = filter3 + '"'


    mp4 = 'yt-dlp -f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b" '

    webm = "yt-dlp "

    v3gp = "yt-dlp -f 3gp "

    mp3 = "yt-dlp -x --audio-format mp3 "

    ogg = "yt-dlp -x --audio-format ogg "

    m4a = "yt-dlp -x --audio-format m4a "

    aac = "yt-dlp -x --audio-format aac "

    opus = "yt-dlp -x --audio-format opus "


    if filter2 == "mp4":
         os.system(cmd+mp4+filter3)
    elif filter2 == "3gp":
        os.system(cmd+v3gp+filter3)
    elif filter2 == "webm":
        os.system(cmd+webm+filter3)
    elif filter2 == "mp3":
        os.system(cmd+mp3+filter3)
    elif filter2 == "ogg":
        os.system(cmd+ogg+filter3)
    elif filter2 == "m4a":
        os.system(cmd+m4a+filter3)
    elif filter2 == "aac":
        os.system(cmd+aac+filter3)
    elif filter2 == "opus":
        os.system(cmd+opus+filter3)
    else:
        print("Not a valid file type!")

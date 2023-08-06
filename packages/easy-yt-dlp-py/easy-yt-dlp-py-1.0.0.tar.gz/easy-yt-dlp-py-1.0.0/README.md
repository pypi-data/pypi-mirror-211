# REQUIRES YT-DLP THIS IS NOT A YT-DLP DISTRIBUTION
# How to use!  
import ytdlpy into your project  
then type "ytdlpy.ytdlpy()"  
then you will enter three arguments  
anything in quotations means you have to fill in what is supposed to be there  
***The file types are case sensitive!***  
`ytdlpy.ytdlpy(\"directory for yt-dlp","file type","video link")`  
## Example:  
```
import ytdlpy

link = input(please input link: )
filetype = input("please select file type: ")

ytdlpy.ytdlpy("\ytdl",filetype,link)
```  
> C:\ytdl is my yt-dlp folder  
> filetype is the file type you want to download in  
> link is the youtube link  
  
  
# Supported file types!  
#### Video file types are:  
`mp4`, `webm`, `3gp`  
#### Audio file types are:  
`mp3`, `ogg`, `m4a`, `aac`, `opus`
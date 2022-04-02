import os
import sys

os.system("cls")

print("使用前请准备ffmpeg及wget环境")
print("---------------------------")
text=input("钉钉m3u8内容(抓包获得):")
print("\n\n")
print("下载通道:\n1.https://dtliving-sz.dingtalk.com/live_hp/ (推荐)(最新)\n2.https://dtliving-sh.dingtalk.com/live_hp/\n3.https://dtliving-bj.dingtalk.com/live/\n4.自定义\n以上都是钉钉官方的API,钉钉会每隔一段时间换一个直播域名(很奇怪),所以要根据直播当时的时间选择\n(近期的直播可以选择1)")
print("---------------------------")
geturl=input("钉钉m3u8内容(抓包获得):")
if geturl=='1':
    dowurl='https://dtliving-sz.dingtalk.com/live_hp/'
else:
    if geturl=='2':
        dowurl='https://dtliving-sh.dingtalk.com/live_hp/'
    else:
        if geturl=='3':
            dowurl='https://dtliving-bj.dingtalk.com/live_hp/'
        else:
            if geturl=='4':
                dowurl=input("请输入自定义链接(结尾要加/):")
            else:
                print('选择无效')
                sys.exit()


notdot=text.replace(', ','.,.') #将", "替换为".,."防止将", "中的空格转换为换行
ntext=notdot.replace(' ','\n') #将" "转换为换行
stext=ntext.replace('.,.',', ') #将".,."转换回", "

# -------
# text        notdot          ntext       stext
# 原m3u8文本  替换, 后的文本   分行后文本    最终可用文本
# -------

list_text=stext.split("\n") #将m3u8内容按回车分割

list_line=int(len(list_text))-2 #ts文件行数

nowline=4 #当前读取到的行数,从4开始,跳过头文件

tss='' #临时存放ts URL(部分)的变量
tsurls='' #存储ts文件url
stop=0 #停止的次数 

while nowline<=list_line:
    
    nowtext=list_text[nowline]
    nowtext_list=nowtext.split(", ")

    if "#EXT-X-DISCONTINUITY" in nowtext:
        print("出现暂停")
        print(nowline)
        nowline=nowline+1
        stop=stop+1

    else:
        
        if "#EXT-X-ENDLIST" in nowtext:
            print("解析结束")
            break
        
        else:
            print(nowtext)
            tsurls=tsurls+dowurl+nowtext_list[1]+'\n'
            print("ok")
            nowline=nowline+1

print(tsurls)
# 至此 数据处理完毕
# ↓下载↓
urls=tsurls.split("\n")
urls_line=int(len(urls))-1-stop #ts URL数量
print("将下载 "+str(urls_line)+" 个分段")

nowts=0 #当前ts
tsstxt='' #ts文件目录树
os.system('mkdir tss') #创建用于存储ts文件的目录

while nowts<urls_line:

    os.system("wget "+urls[nowts]+" -O tss/"+str(nowts)+".ts")
    tsstxt=tsstxt+"file  'tss/"+str(nowts)+".ts'"+"\n"
    nowts=nowts+1

print(tsstxt)

with open('tss.txt','w') as f: #写目录树
    f.write(tsstxt)

os.system('ffmpeg -f concat -i tss.txt -c copy output.mp4') #利用ffmpeg合并视频文件
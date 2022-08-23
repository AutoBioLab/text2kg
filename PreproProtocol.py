import nltk
import os
import json
from nltk.tokenize import sent_tokenize
FileFolderPath='protocols'
FileNames=os.listdir(FileFolderPath)#['protocol_nprot-4523.json', 'protocol_nprot-2314.json', 'protocol_nprot-1889.json', 'protocol_nprot-2685.json',
for file in FileNames:
    if not os.path.isdir(file):#判断不是文件夹才打开
        f=open(FileFolderPath+'/'+file)
        a=json.load(f)

        #提取id
        id = a['identity']

        #提取标题
        title = a['title']

        #提取contents
        contents = a['content']

        #找到 procedures、intro,reagents,equipments
        for content in contents:

            # find intro
            if content['header']=="Introduction":
                Intro=content["content"]

            # find reagents
            if content['header'] == "Reagents":
                Reagents = content["content"]

            # find procedure
            if content['header'] == "Procedure":
                Procedure = content["content"]

            # find equipment
            if content['header'] == "Equipment":
                Equipment = content["content"]

#——————————提取文本完成————————————————

#开始预处理、分句
        ProcedureSentences=sent_tokenize(Procedure)


        
        break#删除即可处理所有的protocol
#coding:utf-8
import io
import sys
import pandas as pd
import codecs
import nltk
import os
import json
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from nltk import data
from nltk import pos_tag
from nltk import ne_chunk
sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

manipulate_sentence_list = []# for sentence and entitys

#读取数据
FileFolderPath='protocols'
FileNames=os.listdir(FileFolderPath)#['protocol_nprot-4523.json', 'protocol_nprot-2314.json', 'protocol_nprot-1889.json', 'protocol_nprot-2685.json',
for file_id, file in enumerate(FileNames):
    if not os.path.isdir(file):#判断不是文件夹才打开
        f=codecs.open(FileFolderPath+'/'+file,'r+',encoding='utf-8')
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

#——————————提取数据完成————————————————

#特殊操作词表
        manipulate_list = ["add", "agitate", "aliquot", "aspirate", "bake", "batch", "calibrate", "catalysis",
                           "catalyst", "centrifuge", "chop", "mince", "chromatograph", "clump", "coat", "collect",
                           "combine", "combustion", "concentrate", "condense", "crush", "decant", "dehydrate", "digest",
                           "dilute", "discard", "dissolution", "dissolve", "distill", "down", "droplet",
                           "electrophoresis", "electrotransformation", "elute", "equilibrate", "evaporate", "extract",
                           "fermentation", "filtrate", "filtration", "flow", "foster", "grind", "harvest", "homogenize",
                           "hydrolysis", "incubate", "inoculate", "lysate", "measure", "mix", "neutralize", "normalize",
                           "passage", "pellet", "perfusion", "pipette", "plate", "precipitate", "probe", "purify",
                           "quench", "remove", "replace", "resuspend", "rinse", "screen", "sediment", "shake", "slurry",
                           "spin", "sterilize", "suction", "supernatant", "thaw", "transfer", "transform", "turbid",
                           "ultrasonication", "ventilate", "viscous", "vortex","repeat"]

        #开始预处理、分句、分词、词性标注、命名实体识别

        if(Procedure):
            named_entity=[]

            def remove_newline(text):#去除\n\r
                return text.replace('\n', '').replace('\r', ' ')

            Procedure = remove_newline(Procedure)

            # 分句
            Procedure_sentences = sent_tokenizer.tokenize(Procedure)
            Procedure_sentences_list = []
            for sentence in Procedure_sentences:
                Procedure_sentences_list.append(sentence)

            #对每一个句子进行如下处理：

            for sentence_id,sentence in enumerate(Procedure_sentences_list):

                #1.分词
                sentence_words = word_tokenize(sentence)

                #2.词形归一化
                words_lemmatizer = []
                wordnet_lemmatizer = WordNetLemmatizer()
                sentence_words=[wordnet_lemmatizer.lemmatize(word) for word in sentence_words]

                #2.去除停用词
                stop_words = set(stopwords.words('english'))
                words_stop = [word for word in sentence_words if word not in stop_words]

                #3.去除标点符号
                aracter_punctuation = ['.', ',', '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '=', '+', '-', '*',
                                       '/', '%', '$', '&', '^', '@', '#', '`', '_', '|', '\\', '\'', '\"', ' ']
                words_stop_punctuation = [word for word in words_stop if
                                                     word not in aracter_punctuation]

                #4.词干提取
                lancaster_stemmer = LancasterStemmer()
                sentence_words_stem = [nltk.PorterStemmer().stem(word) for word in words_stop_punctuation]
                #对manipulate_list中的词进行词干提取
                manipulate_list = [nltk.PorterStemmer().stem(word) for word in manipulate_list]

                #5.单词变体还原
                wordnet_lemmatizer = WordNetLemmatizer()
                words_lemmatizer_stem = [wordnet_lemmatizer.lemmatize(word) for word in sentence_words_stem]
                #对manipulate_list中的词进行单词变体还原
                manipulate_list = [wordnet_lemmatizer.lemmatize(word) for word in manipulate_list]
                manipulate_list.extend(["times"])


                #6.词性标注
                words_tag = nltk.pos_tag(words_lemmatizer_stem)
                words_tag_list = [word for word, tag in words_tag]


                #7.命名实体识别
                words_chunk = nltk.ne_chunk(words_tag, binary=True)
                named_entity.append(words_chunk)



            #提取所有命名实体以及标注特殊操作的句子
            named_entity_list = []

            for sentence_id,tree in enumerate(named_entity):
                for leaf in tree:

                    if len(leaf) == 2:
                        entity_name = leaf[0]#提取命名实体名称
                        entity_type = leaf[1]#命名实体类型
                        named_entity_list.append((entity_name, entity_type))#提取命名实体名称和类型

                    #提取特殊操作词
                    if entity_name in manipulate_list:
                        infodict={"file_name":file,"sentence_id":sentence_id,"entity_name":entity_name,"entity_type":entity_type,"sentence":Procedure_sentences_list[sentence_id]}
                        manipulate_sentence_list.append(infodict)



            #         #实体名称去重
            #         named_entity_list=list(set(named_entity_list))
            # # 保存为表格形式
            # entity_frame = pd.DataFrame(named_entity_list, columns=['Entity Name', 'Entity Type'])
            #
            # print(entity_frame)





        print(file,file_id,"/",len(FileNames))

#将manipulate_sentence_list保存到json文件中
with open('manipulate_sentence_list.json', 'w') as f:
    json.dump(manipulate_sentence_list, f)


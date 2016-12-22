

#encoding=utf-8
import sys
sys.path.append("../")
import jieba
import jieba.analyse
import jieba.posseg as pseg

jieba.enable_parallel(4)


sentens = ['python,, 的正c++c#则表达式是好用的',
        'c++是世界上最好的语言',
        '导致 英文导致 英文24口交换机 xxx'
        ]

jieba.suggest_freq('24口交换机owri语言eeiw交换机', True)

allow=('n', 'nr', 'ns', 'nt', 'nz', 'vn', 'v', 'N', 'i', 'j', 'l', 'vn')
for i in sentens:
    ret = jieba.analyse.textrank(i, topK=20, withWeight=False, allowPOS=allow)
    for j in ret:
        print(j)
    print('--------------------------------------')

print('=======================================')
for i in sentens:
    ret = jieba.cut(i)
    for j in ret:
        print(j)
    print('--------------------------------------')
print('=======================================')

for i in sentens:
    ret = jieba.cut_for_search(i)
    for j in ret:
        print(j)
    print('--------------------------------------')
print('=======================================')

jieba.add_word('24口交换机')

for i in sentens:
    words = pseg.cut(i)
    for j in words:
        print(j)


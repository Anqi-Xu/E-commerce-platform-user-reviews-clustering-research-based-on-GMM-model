import pandas as pd
import re
#去超短评论和重复评论
df=pd.read_csv('Jd_comments.csv',encoding='gbk',header=0)
df_li=df.values.tolist () # 将 csv 数据转换为 python 列表
new_li=[]
comment_li=[]
for i in df_li:
    try:
        if len(i[0])>10:  #评论字数大于10
            if i[0] not in comment_li:  #去重复评论
                comment_li. append(i[0])
                new_li. append(i)
    except Exception as e:
            print('异常,跳转中...')
            continue
name_attribute = ['comment']
writerCSV=pd. DataFrame(columns=name_attribute, data=new_li)
writerCSV.to_csv('del_Jd_com.csv',encoding='gbk',index=False)

#定义五个电脑属性，通过正则表达式替换和规范化
txt= open('Jd_comments.txt', 'r', encoding='gbk')
xingjiabi=[]
kefu=[]
kaiji=[]
wuliu=[]
yunxing=[]
for line in txt:
    pattern1=re. compile(r'性价比. *?高')
    pattern2=re. compile (r'开机.*?快')
    pattern3=re. compile (r'客服.*?好')
    pattern4=re. compile(r'物流.*?快')
    pattern5=re. compile (r'运行.*?快')
    a=pattern1. findall(line)
    b=pattern2. findall(line)
    c=pattern3. findall(line)
    d=pattern4. findall(line)
    e=pattern5. findall(line)
    for i in a:
        if len(i)<=15:
            xingjiabi. append(i)
            xingjiabi=list(set (xingjiabi))
    for i in b:
        if len(i)<=15:
            kaiji. append(i)
            kaiji=list(set(kaiji))
    for i in c:
        if len(i)<=15:
            kefu. append (i)
            kefu=list(set(kefu))
    for i in d:
        if len(i)<=15:
            wuliu. append (i)
            wuliu=list(set(wuliu))
    for i in e:
        if len(i)<=15:
            yunxing. append(i)
            yunxing=list(set(yunxing))
txt. close ()
txt_new=open('Jd_comments.txt', 'r', encoding='gbk')
outputs=open('replace_Jd_com.txt','w')
for n in txt_new:
    for i in xingjiabi:
        n=n. replace (i,'性价比高')
    for i in kefu:
        n=n. replace (i,'客服不错')
    for i in kaiji:
        n=n. replace (i,'开机快')
    for i in wuliu:
        n=n. replace (i,'物流快')
    for i in yunxing:
        n=n. replace (i,'运行快')
    outputs.write(n)
txt_new.close ()
outputs.close ()
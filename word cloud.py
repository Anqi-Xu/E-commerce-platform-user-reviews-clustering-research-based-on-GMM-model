import jieba.analyse
from PIL import Image
import numpy as np
from wordcloud import WordCloud	#词云图
with open('C:\\Users\\ASUS\\Desktop\\京东\\replace_Jd_com.txt','r',encoding='gbk') as f:
    data = f.read ()
    keyword = jieba.analyse.extract_tags(data, topK=100, withWeight=False)
    wl=" ".join(keyword)
image =Image.open('C:\\Users\\ASUS\\Desktop\\京东\\image.PNG')
img = np.array(image)
wordcloud =WordCloud (background_color='white', max_words=100, max_font_size=80, font_path='C:\\Windows\\Fonts\\simhei.ttf'). generate(wl)
image =wordcloud.to_image()
image.show ()
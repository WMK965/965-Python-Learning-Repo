import jieba
import wordcloud
from PIL import Image
import numpy as np


raw_data = open("./resources/111.txt", encoding="gbk").read()
ls = jieba.lcut(raw_data)
text = ' '.join(ls)
open("./resources/111.txt", encoding="gbk").close()
mask = np.array(Image.open("./resources/mask.png"))
wc = wordcloud.WordCloud(font_path="msyh.ttc",
                         mask=mask,
                         background_color='white',
                         max_font_size=240,
                         stopwords={'王勃', '一'})
wc.generate(text)
wc.to_file("./results/111.png")
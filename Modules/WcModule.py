import jieba
import wordcloud
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

size = None  # 210
maxword = None  # 75
font = None  # "AdobeHeitiStd-Regular.otf"
file = None  # "../resources/111.txt"
mask = None  # "../resources/mask.png"


def generate(size, maxword, font, file, mask):
    raw_data = open(file, encoding="utf-8").read()
    ls = jieba.lcut(raw_data)
    text = ' '.join(ls)
    open(file, encoding="utf-8").close()
    mask = np.array(Image.open(mask))
    wc = wordcloud.WordCloud(font_path=font,
                             mask=mask,
                             background_color='white',
                             max_font_size=size,
                             max_words=maxword,
                             stopwords={'王勃', '一'})
    wc.generate(text)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()

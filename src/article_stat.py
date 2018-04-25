import ujson
from nltk import word_tokenize
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np


def write_to_file(dataset, filename):
    with open(filename, 'w', encoding='utf8') as f_out:
        for d in dataset.items():
            f_out.write('{}\t{}\n'.format(d[0], d[1]))


def plot(features, save_name, title_name):
    x = list(features.keys())
    y = list(features.values())
    elem_size = len(features)
    color_map = plt.cm.get_cmap('RdYlBu_r')
    colors = [color_map((i / elem_size)) for i in range(1, elem_size)]
    fig, ax = plt.subplots()
    fig.set_size_inches(16, 16)
    width = 0.75  # the width of the bars
    ind = np.arange(len(y))  # the x locations for the groups
    ax.barh(ind, y, width, color=colors)
    ax.set_yticks(ind)
    ax.set_yticklabels(x, minor=False)
    plt.title(title_name)
    for i, v in enumerate(y):
        ax.text(v, i, str(v), color='black', va='center')
    fig.savefig(save_name, dpi=100)
    plt.show()


# read data
with open('article.json', mode='r', encoding='utf8', errors='ignore') as f:
    data = ujson.load(f)

title_vocab = {}
title_len = {}
author_num = {}
author_vocab = {}
journal_name = {}
journal_vocab = {}
year_vocab = {}
pages_vocab = {}
index = 0
for record in data:
    title, author, year, journal, pages = record['title'], record['author'], record['year'], record['journal'], \
                                          record['pages']
    if len(title) == 0 or len(author) == 0 or len(year) == 0 or len(journal) == 0 or len(pages) == 0:
        continue
    index += 1
    if index % 100000 == 0:
        print('processed {} records'.format(index))
    # process title
    title_tokens = word_tokenize(title[0])
    title_len[len(title_tokens)] = title_len.get(len(title_tokens), 0) + 1
    for tok in title_tokens:
        title_vocab[tok] = title_vocab.get(tok, 0) + 1
    # process author
    author_num[len(author)] = author_num.get(len(author), 0) + 1
    for au in author:
        for tok in word_tokenize(au):
            author_vocab[tok] = author_vocab.get(tok, 0) + 1
    # process journal
    journal_name[journal[0]] = journal_name.get(journal[0], 0) + 1
    for tok in word_tokenize(journal[0]):
        journal_vocab[tok] = journal_vocab.get(tok, 0) + 1
    # process year
    year_vocab[year[0]] = year_vocab.get(year[0], 0) + 1
    # process pages
    pages_vocab[pages[0]] = pages_vocab.get(pages[0], 0) + 1

title_vocab = OrderedDict(sorted(title_vocab.items(), key=lambda t: t[1], reverse=True))
title_len = OrderedDict(sorted(title_len.items(), key=lambda t: t[1], reverse=True))
author_num = OrderedDict(sorted(author_num.items(), key=lambda t: t[1], reverse=True))
author_vocab = OrderedDict(sorted(author_vocab.items(), key=lambda t: t[1], reverse=True))
journal_name = OrderedDict(sorted(journal_name.items(), key=lambda t: t[1], reverse=True))
journal_vocab = OrderedDict(sorted(journal_vocab.items(), key=lambda t: t[1], reverse=True))
year_vocab = OrderedDict(sorted(year_vocab.items(), key=lambda t: t[0]))

pages_tmp = {}
for key, value in pages_vocab.items():
    key_ = abs(int(key))
    pages_tmp[key_] = pages_tmp.get(key_, 0) + value
pages_vocab = OrderedDict(sorted(pages_tmp.items(), key=lambda t: t[1], reverse=True))


write_to_file(title_vocab, 'title_vocab.txt')
write_to_file(author_vocab, 'author_vocab.txt')
write_to_file(author_num, 'author_number.txt')
write_to_file(journal_vocab, 'journal_vocab.txt')
write_to_file(journal_name, 'journal_name.txt')
write_to_file(year_vocab, 'year_vocab.txt')
write_to_file(pages_vocab, 'pages_vocab.txt')

plot(year_vocab, 'year.png', 'year')
plot(author_num, 'author_number.png', 'author number')
plot(pages_vocab, 'pages.png', 'pages')

numerator = 0
denominator = 0
for key, value in title_len.items():
    numerator += int(key) * value
    denominator += value
print('Average title length: {}'.format(float(numerator) / float(denominator)))
large_5 = 0
large_10 = 0
large_20 = 0
for key, value in title_vocab.items():
    if value > 20:
        large_5 += 1
        large_10 += 1
        large_20 += 1
    elif value > 10:
        large_5 += 1
        large_10 += 1
    elif value > 5:
        large_5 += 1
print('Total words in title: {}, large than 5: {}, large than 10: large than 20: {}'.format(len(title_vocab), large_5,
                                                                                            large_10, large_20))

numerator = 0
denominator = 0
for key, value in author_num.items():
    numerator += int(key) * value
    denominator += value
print('Average number of authors per article: {}'.format(float(numerator) / float(denominator)))
author_range = sorted([int(x) for x in list(author_num.keys())])
print('Author number range: {}~{}'.format(author_range[0], author_range[-1]))
large_5 = 0
large_10 = 0
large_20 = 0
for key, value in author_vocab.items():
    if value > 20:
        large_5 += 1
        large_10 += 1
        large_20 += 1
    elif value > 10:
        large_5 += 1
        large_10 += 1
    elif value > 5:
        large_5 += 1
print('Total words in author: {}, large than 5: {}, large than 10: large than 20: {}'
      .format(len(author_vocab), large_5, large_10, large_20))


year_range = sorted([int(x) for x in list(year_vocab.keys())])
print('Year range: {}~{}'.format(year_range[0], year_range[-1]))

print('Total numbers of journal: {}'.format(len(journal_name)))
large_100 = 0
large_200 = 0
large_300 = 0
for key, value in journal_vocab.items():
    if value > 300:
        large_100 += 1
        large_200 += 1
        large_300 += 1
    elif value > 200:
        large_100 += 1
        large_200 += 1
    elif value > 100:
        large_100 += 1
print('Total words in journal: {}, large than 100: {}, large than 200: large than 300: {}'
      .format(len(journal_vocab), large_100, large_200, large_300))

numerator = 0
denominator = 0
for key, value in pages_vocab.items():
    numerator += int(key) * value
    denominator += value
print('Average number of pages per article: {}'.format(float(numerator) / float(denominator)))



import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict

elements = {'article': 1796920, 'book': 15039, 'incollection': 46750, 'inproceedings': 2153167, 'mastersthesis': 10,
            'phdthesis': 64943, 'proceedings': 36625, 'www': 2066271}
elements = OrderedDict(sorted(elements.items(), key=lambda t: t[1], reverse=False))

entities = {'address': 3, 'author': 13959186, 'booktitle': 2237560, 'cdrom': 12967, 'chapter': 2, 'cite': 172724,
            'crossref': 2180669, 'editor': 88682, 'ee': 4446573, 'isbn': 56780, 'journal': 1796694, 'month': 10645,
            'note': 88768, 'number': 1433345, 'pages': 3694015, 'publisher': 56461, 'school': 67068, 'series': 23249,
            'title': 6179414, 'url': 4130609, 'volume': 1815623, 'year': 4113465}
entities = OrderedDict(sorted(entities.items(), key=lambda t: t[1], reverse=False))

features = {'title': 1796920, 'author': 1786539, 'year': 1796914, 'journal': 1796690, 'pages': 1576971}
features = OrderedDict(sorted(features.items(), key=lambda t: t[1], reverse=False))

x = list(elements.keys())
y = list(elements.values())
elem_size = len(elements)

color_map = plt.cm.get_cmap('RdYlBu_r')
colors = [color_map((i/elem_size)) for i in range(0, elem_size)]

fig, ax = plt.subplots()
fig.set_size_inches(15.5, 8.5)
width = 0.75  # the width of the bars
ind = np.arange(len(y))  # the x locations for the groups
ax.barh(ind, y, width, color=colors)
ax.set_yticks(ind)
ax.set_yticklabels(x, minor=False)
plt.title('Entity Count')
for i, v in enumerate(y):
    ax.text(v, i, str(v), color='black', va='center')
fig.savefig('elements.png', dpi=100)
plt.show()

from collections import Counter
import re
import boto

s3 = boto.connect_s3()
files = ["Tweet Day 2015-01-31.txt","Tweet Day 2015-02-01.txt","Tweet Day 2015-02-02.txt","Tweet Day 2015-02-03.txt",
         "Tweet Day 2015-02-04.txt","Tweet Day 2015-02-05.txt","Tweet Day 2015-02-06.txt"]
words = []

for file in files:
    print('Loading file ' + file + ' from S3')
    key = s3.get_bucket('com.christopherllop.w205assignment2').get_key(file)
    text = key.get_contents_as_string()

    print('Processing ' + file)
    for w in text.lower().split():
    #for w in re.split('; |, |\\\|\n|\s',text.lower()):
        w2 = w.strip('!,.?-=$%^&*()_+:\'/\\\"')
        if not(w2.startswith("http://") or w2.startswith("https://") or w2.count('/') > 1 or
                       w2.count('\\u') > 0 or w2 == '' or len(w2) > 30):
            words.append(w2)


print('Building histogram')

counter = Counter(words)

columns = 100
n_occurrences = len(counter)
to_plot = counter.most_common(n_occurrences)
preLabels, values = zip(*to_plot)
i = 0
labels = []
for l in preLabels:
    labels.append(preLabels[i] + " (" + str(values[i]) + ")")
    i += 1
label_width = max(map(len, labels))
data_width = columns - label_width - 1
plot_format = '{:%d}|{:%d}' % (label_width, data_width)
max_value = float(max(values))

print('Saving histogram')
for i in range(len(labels)):
    v = int(values[i]/max_value*data_width)
    str = (plot_format.format(labels[i], '*'*v))
    with open('histogram.txt', 'a') as outfile:
       outfile.write(str+'\n')
print('Save complete')


import sklearn.metrics as skm
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import csv
import numpy as np

def plot_confusion_matrix(cm, labels, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(labels))
    plt.xticks(tick_marks, labels, rotation=90)
    plt.yticks(tick_marks, labels)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

truths = []
preds = []

#models = ["logistic-regression","svm","decision-jungle","perceptron","rf100-30per","rf500-30per","rf1000-30per","rf1500-30per"]
models = ["top30-logistic-regression"]

for model in models:
	with open("/Users/jamarq_laptop/NIARA/Results/"+model) as infile:
		reader = csv.reader(infile)
		reader.next()

		for line in reader:
			truths.append(line[0])
			preds.append(line[1])

	metrics = skm.classification_report(truths,preds)
	#print metrics

	with open("/Users/jamarq_laptop/NIARA/Results/report-"+model, "wb") as outfile:
		outfile.write(metrics)
		outfile.write("\nAccuracy: " + str(skm.accuracy_score(truths,preds)))

'''
cm = confusion_matrix(truths, preds)
cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
plt.figure()
plot_confusion_matrix(cm_normalized, list(set(truths)), title='Normalized confusion matrix')
plt.show()
'''

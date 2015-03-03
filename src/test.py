from data_utils import load_linqs_data
from classifiers import LocalClassifier


from sklearn.cross_validation import KFold
from sklearn.metrics import accuracy_score, confusion_matrix
import numpy as np

if __name__ == '__main__':

    args = {
        'content_file': 'Z:/Data/CS_583_Project/citeseer/citeseer.content',
        'cites_file': 'Z:/Data/CS_583_Project/citeseer/citeseer.cites',
        'classifier': 'sklearn.linear_model.LogisticRegression',
        'num_folds': 10,
    }

    graph, domain_labels = load_linqs_data(args['content_file'], args['cites_file'])

    kf = KFold(n=len(graph.node_list), n_folds=args['num_folds'], shuffle=True, random_state=42)

    accuracies = []

    cm = None

    for train, test in kf:
        clf = LocalClassifier(args['classifier'])
        clf.fit(graph, train)
        y_pred = clf.predict(graph, test)
        y_true = [graph.node_list[t].label for t in test]
        accuracies.append(accuracy_score(y_true, y_pred))
        if cm is None:
            cm = confusion_matrix(y_true, y_pred, labels = domain_labels)
        else:
            cm += confusion_matrix(y_true, y_pred, labels = domain_labels)

    print accuracies
    print "Mean accuracy: %0.4f +- %0.4f" % (np.mean(accuracies), np.std(accuracies))
    print cm

import numpy as np
from sklearn import metrics

#multi_socre
#TP TN FP FN Accuracy Precision 

def scores(y_true:int, y_pred:float, show=False):
    """
    y_true:true label
    y_prob:pred label with probility

    multi scores of binnary class:
    (1) TP TN FP FN 
    (2) Accuracy    = (TP+TN)/(TP+TN+FP+FN)
    (3) precision   = TP/(TP+FP+1e-6)
    (4) recall      = TP/(TP+FN+1e-6)   
        sensitivity = TP/(TP+FN+1e-6)   
    (3) specificity = TN/(TN+FP+1e-6)
    (5) mcc = (TP*TN - FP*FN)/sqrt((TP+FP+1e-6)*(TP+FN+1e-6)*(TN+FP+1e-6)*(TN+FN+1e-6))
    (7) f1 = 2*(precision*recall)/(precision+recall+1e-6)
    (8) auc : Area under the curve of ROC(receipt operator curve) 
    (9) auprc:Area under the precision recall curve
    """

    if max(label) > 1 or min(label)< 0 :
        raise Exception("label not in range (0, 1)!")
    
    if max(y_prob) > 1 or min(y_prob) <0:
        raise Exception("y_prob value not in range (0, 1)!")

    y_true = np.array(y_true,float)
    y_pred = np.array(y_prob,float)

    y_true_label = np.round(y_ture)
    y_pred_label = np.round(y_pred)
    
    TP = sum((y_true >  0.5) & (y_prob >  0.5 ))
    TN = sum((y_true <= 0.5) & (y_prob <= 0.5 ))
    FP = sum((y_true <= 0.5) & (y_prob >  0.5 ))
    FN = sum((y_true >  0.5) & (y_prob <= 0.5 ))
    
    accuracy =      round(metrics.accuracy_score(       y_true_label, y_pred_label), 4)
    precision =     round(metrics.precision_score(      y_true_label, y_pred_label), 4)
    recall =        round(metrics.recall_score(         y_true_label, y_pred_label), 4)
    specificity =   recall

    average_precision, average_recall, thresholds = metrics.precision_recall_curve(y_true, y_prob)
    mcc =           round(metrics.matthews_corrcoef(    y_true, y_pred), 4)
    f1 =            round(metrics.f1_score(             y_true, y_pred), 4)
    auc =           round(metrics.roc_auc_score(        y_true, y_prob), 4)
    auprc =         round(metrics.auc(average_recall,average_precision), 4)
    
    if show:
        print("tp,tn,fp,fn,accuracy, precision, recall, specificity , mcc, f1, AUC, AuPRC")
        print(tp,tn,fp,fn, accuracy,precision,recall,specificity, mcc,f1,auc,auprc)
    return   (tp,tn,fp,fn, accuracy,precision,recall,specificity, mcc,f1,auc,auprc)


import json
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import logging

logger = logging.getLogger(__name__)

def evaluate_classification(y_true, y_pred, classes):
    acc = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average=None)
    macro_p, macro_r, macro_f1, _ = precision_recall_fscore_support(y_true, y_pred, average='macro')
    cm = confusion_matrix(y_true, y_pred)
    
    metrics = {
        "accuracy": acc,
        "macro_precision": macro_p,
        "macro_recall": macro_r,
        "macro_f1": macro_f1,
        "per_class": {
            classes[i]: {
                "precision": precision[i],
                "recall": recall[i],
                "f1": f1[i]
            } for i in range(len(classes))
        },
        "confusion_matrix": cm.tolist()
    }
    return metrics

def calculate_iou(pred_mask, true_mask, threshold=0.5):
    pred = (pred_mask > threshold).astype(bool)
    true = (true_mask > threshold).astype(bool)
    
    intersection = np.logical_and(pred, true).sum()
    union = np.logical_or(pred, true).sum()
    
    if union == 0:
        return 1.0 if intersection == 0 else 0.0
    return intersection / union

def calculate_dice(pred_mask, true_mask, threshold=0.5):
    pred = (pred_mask > threshold).astype(bool)
    true = (true_mask > threshold).astype(bool)
    
    intersection = np.logical_and(pred, true).sum()
    return (2. * intersection) / (pred.sum() + true.sum())

def save_metrics(metrics: dict, filepath: str):
    with open(filepath, 'w') as f:
        json.dump(metrics, f, indent=4)
    logger.info(f"Metrics saved to {filepath}")

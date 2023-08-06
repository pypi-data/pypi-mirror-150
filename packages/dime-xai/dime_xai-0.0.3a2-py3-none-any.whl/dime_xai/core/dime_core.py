import logging
from typing import Optional, List, Dict, Text, Union

import numpy as np
from sklearn.metrics import f1_score, accuracy_score

from dime_xai.shared.constants import Metrics, Smoothing
from dime_xai.shared.explanation import DIMEExplanation

logger = logging.getLogger(__name__)


def get_f1_score(
        model_output: List,
        average: Text = Metrics.AVG_WEIGHTED
) -> float:
    true_labels = [output['intent'] for output in model_output]
    predicted_labels = [output['predicted_intent'] for output in model_output]
    score = f1_score(
        y_true=true_labels,
        y_pred=predicted_labels,
        average=average
    )
    return score


def get_accuracy_score(
        model_output: List,
        normalize: bool = Metrics.AVG_WEIGHTED
) -> float:
    true_labels = [output['intent'] for output in model_output]
    predicted_labels = [output['predicted_intent'] for output in model_output]
    score = accuracy_score(
        y_true=true_labels,
        y_pred=predicted_labels,
        normalize=normalize
    )
    return score


def get_confidence_score(
        model_output: List,
        confidence_op: Text = Metrics.TOTAL_CONFIDENCE
) -> float:
    predicted_confidence = [output['intent_confidence'] for output in model_output]
    if confidence_op == Metrics.TOTAL_CONFIDENCE:
        total_predicted_confidence = sum(predicted_confidence)
        score = total_predicted_confidence
    elif confidence_op == Metrics.AVG_CONFIDENCE:
        average_predicted_confidence = sum(predicted_confidence) / len(predicted_confidence)
        score = average_predicted_confidence
    else:
        score = 0.0
    return score


def get_score(
        token: Text,
        init_model_output: List,
        token_model_output: List,
        scorer: Text = Metrics.DEFAULT,
        average: Text = Metrics.AVG_WEIGHTED,
        normalize: bool = Metrics.NORMALIZE,
        confidence_op: Text = Metrics.TOTAL_CONFIDENCE,
) -> Optional[float]:
    if scorer == Metrics.F1_SCORE:
        init_f1_score = get_f1_score(model_output=init_model_output, average=average)
        token_f1_score = get_f1_score(model_output=token_model_output, average=average)

        if init_f1_score < token_f1_score:
            logger.warning(f"F1-Score has boosted for the token '{token}")
        token_f1_score_diff = init_f1_score - token_f1_score
        return token_f1_score_diff

    elif scorer == Metrics.ACCURACY:
        init_accuracy = get_accuracy_score(model_output=init_model_output, normalize=normalize)
        token_accuracy = get_accuracy_score(model_output=token_model_output, normalize=normalize)

        if init_accuracy < token_accuracy:
            logger.info(f"Accuracy has boosted for the token '{token}")
        token_accuracy_diff = init_accuracy - token_accuracy
        return token_accuracy_diff

    elif scorer == Metrics.CONFIDENCE:
        init_confidence = get_confidence_score(model_output=init_model_output, confidence_op=confidence_op)
        token_confidence = get_confidence_score(model_output=token_model_output, confidence_op=confidence_op)

        if init_confidence < token_confidence:
            if confidence_op == Metrics.TOTAL_CONFIDENCE:
                logger.info(f"Total confidence has boosted for the token '{token}")
            if confidence_op == Metrics.AVG_CONFIDENCE:
                logger.info(f"Average confidence has boosted for the token '{token}")
        token_confidence_diff = init_confidence - token_confidence
        return token_confidence_diff


def softmax(
        vector: Union[List, Dict]
) -> Union[np.array, Dict]:
    if isinstance(vector, Dict):
        keys = list(vector.keys())
        values = list(vector.values())
        softmax_values = softmax(vector=values)
        return {keys[x]: softmax_values[x] for x in range(len(keys))}
    else:
        vector_copy = vector.copy()
        vector_np = np.array(vector_copy)
        return np.exp(vector_np) / np.exp(vector_np).sum()


def exp_norm_softmax(
        vector: Union[List, Dict]
) -> Union[np.array, Dict]:
    if isinstance(vector, Dict):
        keys = list(vector.keys())
        values = list(vector.values())
        softmax_values = softmax(vector=values)
        return {keys[x]: softmax_values[x] for x in range(len(keys))}
    else:
        vector_copy = vector.copy()
        vector_np = np.array(vector_copy)
        b = max(vector_np)
        return np.exp(vector_np - b) / np.exp(vector_np - b).sum()


def global_feature_importance(
        init_model_output: List,
        token_model_output: List,
        token: Text,
        scorer: Text = Metrics.F1_SCORE,
        average: Text = Metrics.AVG_WEIGHTED,
        normalize: bool = Metrics.NORMALIZE,
        confidence_op: Text = Metrics.TOTAL_CONFIDENCE,
) -> Optional[Dict]:
    score = get_score(
        init_model_output=init_model_output,
        token_model_output=token_model_output,
        scorer=scorer,
        average=average,
        normalize=normalize,
        confidence_op=confidence_op,
        token=token
    )
    return score


def local_feature_importance():
    # TODO :implement local
    pass


def apply_smoothing(
        vector: Union[List, Dict],
        smoothing_algorithm: Text = Smoothing.LAPLACE,
        smoothing_value: int = 1
) -> Union[List, Dict]:
    vector_copy = vector.copy()
    if isinstance(vector_copy, Dict):
        # TODO :implement
        return {}
    else:
        # TODO :refine
        return [value + smoothing_value for value in vector]


def load_explanation(explanation: Text) -> DIMEExplanation:
    dime_explanation = DIMEExplanation(explanation=explanation)
    return dime_explanation

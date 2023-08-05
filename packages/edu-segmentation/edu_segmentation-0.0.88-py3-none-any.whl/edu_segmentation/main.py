from .BARTTokenClassification.run_segbot_bart import run_segbot_bart
from .BERTTokenClassification.run_bert import run_segbot_bert_cased, run_segbot_bert_uncased
import warnings

def run_segbot(sent, granularity_level="default", model="bart", conjunctions=["and", "but", "however"]):
    warnings.filterwarnings('ignore')
    print(f"----------- EDU Segmentation with Segbot with {model} model at granularity level: {granularity_level}----------")
    results = []

    segbot_model = run_segbot_bart
    if model == "bert_uncased":
        segbot_model = run_segbot_bert_uncased
    elif model == "bert_cased":
        segbot_model = run_segbot_bert_cased

    if granularity_level == "conjunction_words":
        print("Conjunction words are removed from the sentence, then each segment is passed through the EDU-segmentation model.")
        segments = []
        current_segment = []
        words = sent.split()

        for word in words:
            if word.lower() in conjunctions:
                if current_segment:
                    segments.append(" ".join(current_segment))
                current_segment.clear()
            else:
                current_segment.append(word)

        if current_segment:
            segments.append(" ".join(current_segment))
        for word in segments:
            results.append(segbot_model(word))
    else:
        results.append(segbot_model(sent))
    return results


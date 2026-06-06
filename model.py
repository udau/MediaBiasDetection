from transformers import pipeline

_classifier = None

def get_classifier():
    global _classifier
    if _classifier is None:
        _classifier = pipeline(
            "text-classification",
            model="alxdev/echocheck-political-stance"
        )
    return _classifier

def predict_stance(text):
    classifier = get_classifier()
    result = classifier(text)
    return result

if __name__ == "__main__":
    # For testing purposes
    text = "trump is distroying america again"
    print(predict_stance(text))
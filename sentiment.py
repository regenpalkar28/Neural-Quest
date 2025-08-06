from transformers import pipeline

model_name = "distilbert-base-uncased-finetuned-sst-2-english"
classifier = pipeline("sentiment-analysis", model=model_name)


texts = [
    "I love making models!",
    "The weather today is terrible.",
    "I am bored today and have so much of work pending",
    "I love coding",
]


results = classifier(texts)

for text, result in zip(texts, results):
    print(f"Text: {text}")
    print(f"Label: {result['label']}, Score: {result['score']:.4f}\n")
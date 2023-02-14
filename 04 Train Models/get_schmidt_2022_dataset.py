import pandas as pd
def get_schmidt_2022_dataset():
    df1 = pd.read_csv("../Datasets/Schmidt2022/test.csv")
    df2 = pd.read_csv("../Datasets/Schmidt2022/train.csv")
    result = pd.concat([df1, df2], axis=0)
    result = result.rename(columns={'Embedded_text': 'text', 'majority_sentiment': 'sentiment_label'})
    result = result.rename(columns={'sentiment_label': 'sentiment'})
    result['sentiment'] = result['sentiment'].replace({3: 'neutral', 2: 'negative', 1: 'positive'})
    del result["Unnamed: 0"]
    result.reset_index()
    return result
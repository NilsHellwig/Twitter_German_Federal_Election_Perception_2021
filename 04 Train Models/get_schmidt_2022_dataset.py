import pandas as pd
def get_schmidt_2022_dataset():
    df1 = pd.read_csv("../Datasets/Schmidt2022/test.csv")
    df2 = pd.read_csv("../Datasets/Schmidt2022/train.csv")
    result = pd.concat([df1, df2], axis=0)
    result = result.rename(columns={'Embedded_text': 'text', 'majority_sentiment': 'sentiment_label'})
    del result["Unnamed: 0"]
    return result
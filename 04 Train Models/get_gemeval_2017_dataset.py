import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np

def get_gemeval_2017_dataset(paths: list = ["../Datasets/GermEval2017/train-2017-09-15.xml", "../Datasets/GermEval2017/dev-2017-09-15.xml", "../Datasets/GermEval2017/test_TIMESTAMP1.xml", "../Datasets/GermEval2017/test_TIMESTAMP2.xml"]):
    """
    Read the GemEval 2017 dataset from the given paths and return a Pandas DataFrame.
    """
    data_raw = []  # create an empty list to store the data
    for path in paths:
        # parse the xml file
        tree = ET.parse(path)

        # get the root element
        root = tree.getroot()

        # loop over the children of the root element
        for child in root:
            pair = []  # create an empty list to store the text and sentiment
            # loop over the grandchildren of the root element
            for child2 in child:
                # if the tag is "text", append the text to the pair list
                if child2.tag == 'text':
                    pair.append(child2.text)
                # if the tag is "sentiment", append the sentiment to the pair list
                if child2.tag == 'sentiment':
                    pair.append(child2.text)
            # append the pair as a numpy array to the data_raw list
            data_raw.append(np.array([pair]))

    # convert the data_raw list to a numpy array and reshape it to have 2 columns
    data_raw = np.array(data_raw).reshape(-1, 2)
    # swap the values in the first and second column
    data_raw[:, [1, 0]] = data_raw[:, [0, 1]]
    # create a Pandas DataFrame from the data_raw array and set the columns names
    df = pd.DataFrame(data_raw, columns=["text", "sentiment"])
    # return the DataFrame
    return df
import plotly.express as px
import pandas as pd
import json
import plotly.io as io
import sklearn
from sklearn import datasets

def getGraph():
    
    data = datasets.load_wine()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    fig = px.scatter(df, x="alcohol", y="malic_acid", title = "Bubble Plot")

    # fig.show()
    return io.to_json(fig)

dynamic_outputs = getGraph()

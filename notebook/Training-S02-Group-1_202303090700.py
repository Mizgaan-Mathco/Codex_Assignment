#!/usr/bin/env python
# coding: utf-8

# ## This is your Downloaded Blueprint Notebook ##

# In[ ]:


# tags to identify this iteration when submitted
# example: codex_tags = {'env': 'dev', 'region': 'USA', 'product_category': 'A'}

codex_tags = {
    'env': 'training_s02'
}

from codex_widget_factory import utils
results_json=[]


# In[ ]:





# In[ ]:





# In[ ]:





# ### Custom Plot
# 

# In[ ]:


#BEGIN CUSTOM CODE BELOW...

#put your output in this response param for connecting to downstream widgets
response_0 = """

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
"""
#END CUSTOM CODE


# In[ ]:





# In[ ]:


#BEGIN CUSTOM CODE BELOW...

#put your output in this response param for connecting to downstream widgets
response_1 = '''
import pandas as pd
import numpy as np
from pathlib import Path
from azure.storage.blob import BlockBlobService
from io import StringIO
import datetime
import plotly.express as px
import json
from itertools import chain
from plotly.io import to_json

sas_token = '?sv=2021-04-10&st=2022-12-22T08%3A12%3A47Z&se=2023-12-30T08%3A12%3A00Z&sr=c&sp=racwl&sig=fMeYkXsCvwK%2F0qVrCmj2j3NiMricQjOPWOkAEXekIPA%3D'
account_name = 'willbedeletedsoon'
container_name = 'codx-pede-s02'
blob_name = 'wine_I0896.csv'
def get_data_from_blob(sas_token, account_name, container_name, blob_name):
    block_blob_service = BlockBlobService(account_name=account_name, sas_token= sas_token)
    from_blob = block_blob_service.get_blob_to_text(container_name = container_name, blob_name=blob_name)
    return pd.read_csv(StringIO(from_blob.content))
df = get_data_from_blob(sas_token, account_name, container_name, blob_name)

def get_table(df, show_searchbar=False, multiple_tables=False):

    comp_dict = {}
    comp_dict['table_headers'] = df.columns.values.tolist()
    comp_dict['table_data'] = df.values.tolist()
    comp_dict['show_searchbar'] = show_searchbar
    comp_dict['multiple_tables'] = multiple_tables
    return comp_dict

container_dict = {}
container_dict = get_table(df, show_searchbar = True)
# container_dict

dynamic_outputs = json.dumps(container_dict)

'''

#END CUSTOM CODE


# In[ ]:





# In[ ]:


#BEGIN CUSTOM CODE BELOW...

#put your output in this response param for connecting to downstream widgets
response_2 = """
import pandas as pd
import numpy as np
from pathlib import Path
from azure.storage.blob import BlockBlobService
from io import StringIO
import datetime
import plotly.express as px
import json
from itertools import chain
from plotly.io import to_json

sas_token = '?sv=2021-04-10&st=2022-12-22T08%3A12%3A47Z&se=2023-12-30T08%3A12%3A00Z&sr=c&sp=racwl&sig=fMeYkXsCvwK%2F0qVrCmj2j3NiMricQjOPWOkAEXekIPA%3D'
account_name = 'willbedeletedsoon'
container_name = 'codx-pede-s02'
blob_name = 'wine_I0896.csv'
def get_data_from_blob(sas_token, account_name, container_name, blob_name):
    block_blob_service = BlockBlobService(account_name=account_name, sas_token= sas_token)
    from_blob = block_blob_service.get_blob_to_text(container_name = container_name, blob_name=blob_name)
    return pd.read_csv(StringIO(from_blob.content))
df = get_data_from_blob(sas_token, account_name, container_name, blob_name)
new_df = df.iloc[:, :5]

def get_grid_table(df,
                   col_props={},
                   grid_options={"tableSize": "small", "tableMaxHeight": "80vh"},
                   group_headers=[],
                   popups={},
                   popup_col=[],
                   popup_col_props={},
                   popup_grid_options={},
                   popup_group_headers={}
                   ):


    comp_dict = {}
    comp_dict['is_grid_table'] = True

    comp_props_dict = {}
    actual_columns = df.columns[~ ((df.columns.str.contains("_bgcolor")) | (df.columns.str.contains("_color")))]
    bg_color_columns = df.columns[df.columns.str.contains("_bgcolor")]
    color_columns = df.columns[df.columns.str.contains("_color")]

    values_dict = df[actual_columns].to_dict("records")

    row_props_list = []
    for index, row_values in enumerate(values_dict):
        row_props_dict = {}

        for col_name, row_value in row_values.items():
            row_props_dict[col_name] = row_value

            if (col_name in popup_col) or (col_name + '_bgcolor' in bg_color_columns) or (col_name + '_color' in color_columns):
                row_props_dict[col_name + '_params'] = {}
                if col_name in popup_col:
                    insights_grid_options = popup_grid_options.copy()
                    insights_grid_options.update({"tableTitle": row_value})

                    if isinstance(popups[col_name][row_value], pd.DataFrame):
                        row_props_dict[col_name + '_params'].update({"insights": {
                            "data": get_grid_table(popups[col_name][row_value], col_props=popup_col_props[col_name], grid_options=insights_grid_options[col_name],
                                                   group_headers=popup_group_headers[col_name])
                        }})
                    elif isinstance(popups[col_name][row_value], go.Figure):
                        row_props_dict[col_name + '_params'].update({"insights": {
                            "data": json.loads(to_json(popups[col_name][row_value]))
                        }})

                if col_name + '_bgcolor' in bg_color_columns:
                    row_props_dict[col_name + '_params'].update({'bgColor': df.iloc[index].to_dict()[col_name + '_bgcolor']})
                if col_name + '_color' in color_columns:
                    row_props_dict[col_name + '_params'].update({'color': df.iloc[index].to_dict()[col_name + '_color']})
        row_props_list.append(row_props_dict)

    col_props_list = []
    for col in actual_columns:
        col_props_dict = {}
        col_props_dict.update({"headerName": col, "field": col, 'cellParamsField': col + '_params'})
        if col in popup_col:
            col_props_dict.update({"enableCellInsights": True})

        if col in col_props:
            col_props_dict.update(col_props[col])
        col_props_list.append(col_props_dict)

    comp_props_dict['rowData'] = row_props_list
    comp_props_dict["coldef"] = col_props_list
    comp_props_dict["gridOptions"] = grid_options

    if group_headers:
        comp_props_dict['groupHeaders'] = group_headers

    comp_dict.update({"tableProps": comp_props_dict})

    return comp_dict

dropdowns = []
col_props = {
                "alcohol":{'cellEditor': "number", 'cellEditorParams' : {'options':dropdowns}, 'editable': True},
                "malic_acid":{'cellEditor': "number", 'editable':True},
                "ash":{'cellEditor': "number", 'editable':True},
                "alcalinity_of_ash":{'cellEditor': "number", 'editable':True},
                "magnesium":{'cellEditor': "number", 'editable':True}
            }

grid_options = {"enablePagination":True,
                "paginationSettings": {"rowsPerPageOptions": [10, 20, 30], "rowsPerPage": 10},
                "quickSearch": True,
                'editorMode': True
               }

group_headers =  []

popup_col = []

popups = {}

popup_col_props = {} 

popup_grid_options = { } 
                      
popup_group_headers = {}

new_df['alcohol_bgcolor'] = "#0000FF"
new_df['malic_acid_bgcolor'] = "#808080"
new_df['ash_bgcolor'] = "#008000"
new_df['alcalinity_of_ash_bgcolor'] = "#800080"
new_df['magnesium_bgcolor'] = new_df['magnesium'].apply(lambda x: "#e25241" if x < 100 else "#67ac5b")
# new_df

container_dict = {}
container_dict = get_grid_table(new_df,
                                col_props=col_props,
                                grid_options=grid_options,
                                group_headers=group_headers,
                                popups=popups,
                                popup_col=popup_col,
                                popup_col_props=popup_col_props,
                                popup_grid_options=popup_grid_options,
                                popup_group_headers=popup_group_headers,          
                                )
dynamic_outputs = json.dumps(container_dict)
    
    
"""

#END CUSTOM CODE


# In[ ]:





# In[ ]:


#BEGIN CUSTOM CODE BELOW...

#put your output in this response param for connecting to downstream widgets
response_3 = """

import plotly.express as px
import pandas as pd
import numpy as np
import json
import plotly.io as io
import sklearn
from sklearn import datasets
import plotly.graph_objects as go

def getGraph():
    
    x = np.linspace(1, 10, 11)
    y = x**2
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x,y=y, name= 'Line Plot', mode='lines'))
    # fig.show()
    return io.to_json(fig)

dynamic_outputs = getGraph()
"""

#END CUSTOM CODE


# In[ ]:





# In[ ]:





# In[ ]:


#BEGIN CUSTOM CODE BELOW...

#put your output in this response param for connecting to downstream widgets
response_4 = """
import pandas as pd
import numpy as np
from pathlib import Path
from azure.storage.blob import BlockBlobService
from io import StringIO
import datetime
import plotly.express as px
import json
from itertools import chain
from plotly.io import to_json
import plotly.graph_objects as go
import plotly.io as io

def getGraph():
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=[0, 1, 2, 3, 4, 5, 6, 7],y=[1.1, 1, 1.3, 0.7, 0.8, 0.9, 0.4, 0.1], name= 'Scatter Plot', mode='markers'))
    fig.add_trace(go.Scatter(x=[0, 1, 2, 3, 4, 5, 6, 7],y=[0.2, 1.2, 1.8, 0.8, 0.5, 1, 1.5, 1.2], name= 'Line Plot', mode='lines'))
    fig.add_trace(go.Bar(x=[0, 1, 2, 3, 4, 5, 6, 7], y=[1, 0.5, 0.7, 1.2, 0.3, 0.4, 1.5, 1.7], name = 'Bar Plot'))
    fig.add_trace(go.Pie(labels=['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen'],values=[1500,1200,1053,700], name = 'Pie Chart'))
    fig.add_trace(go.Scatter(x=[0, 1, 2, 3, 4, 5, 6, 7],y=[1.8, 2.2, 0.3, 1.7, 0.4, 0.7, 0.8, 1.1], name= 'Bubble Chart', mode='markers', marker_size=[10, 22, 12.5, 18.2, 5.3, 15.8, 29.8]))


    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(

                        label="Scatter",
                        args=[{"visible": [True, False, False, False, False]}, "chart_type", "Scatter"],
                        method="restyle"
                    ),
                    dict(

                        label="Line",
                        args=[{"visible": [False, True, False, False, False]}, "chart_type", "Line"],
                        method="restyle"
                    ),
                    dict(

                        label="Bar",
                        args=[{"visible": [False, False, True, False, False]}, "chart_type", "Bar"],
                        method="restyle"
                    ),
                    dict(

                        label="Pie",
                        args=[{"visible": [False, False, False, True, False]}, "chart_type", "Pie"],
                        method="restyle"
                    ),
                    dict(

                        label="Bubble",
                        args=[{"visible": [False, False, False, False, True]}, "chart_type", "Bubble"],
                        method="restyle"
                    )

                ]),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0,
                xanchor="left",
                y=1.2,
                yanchor="top"
            )
        ]
    )
    # fig.show()
    return io.to_json(fig)
   
dynamic_outputs = getGraph()

"""

#END CUSTOM CODE


# In[ ]:





# In[ ]:





# In[ ]:


dynamic_visual_reponse={
    "Plot": response_0,
    "Table": response_1,
    "Color_Table": response_2, 
    "Graph": response_3,
    "Multi_Trace": response_4
   
}

results_json.append({
    'type':'Dynamic_plot',
    'name': 'plot',
    'component':'plot',
    'dynamic_visual_results': dynamic_visual_reponse,
    'dynamic_code_filters':False,
    'dynamic_metrics_results':False,
    'metrics':False
           
})


# In[ ]:





# ### Please save and checkpoint notebook before submitting params

# In[ ]:



currentNotebook = 'Training-S02-Group-1_202303090700.ipynb'

get_ipython().system('jupyter nbconvert --to script {currentNotebook} ')


# In[ ]:



utils.submit_config_params(url='https://codex-api-stage.azurewebsites.net/codex-api/projects/upload-config-params/P9qhBIJpjtDtMXucWz0rXw', nb_name=currentNotebook, results=results_json, codex_tags=codex_tags, args={})


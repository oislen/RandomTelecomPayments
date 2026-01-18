import json
import numpy as np
import pandas as pd

class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        dtypes = (np.datetime64, pd.Timestamp)
        if isinstance(obj, dtypes):
            return str(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        return super(JsonEncoder, self).default(obj)
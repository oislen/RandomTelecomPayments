import json
import numpy as np
import pandas as pd

class JsonEncoder(json.JSONEncoder):
    """
    A custom JSON encoder for handling numpy and pandas data types.
    Extends the default JSONEncoder to convert numpy data types and pandas Timestamps
    to native Python data types for JSON serialization.
    
    Methods
    -------
    default(self, obj)
        Override the default method to handle specific data types.
    """
    def default(self, obj):
        """
        Convert numpy and pandas data types to native Python types.
        
        Parameters
        ----------
        obj : object
            The object to be converted.
        
        Returns
        -------
        object
            The converted object suitable for JSON serialization.
        """
        dtypes = (np.datetime64, pd.Timestamp)
        if isinstance(obj, dtypes):
            return str(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        return super(JsonEncoder, self).default(obj)
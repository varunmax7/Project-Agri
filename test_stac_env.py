import os
os.environ['AWS_NO_SIGN_REQUEST'] = 'YES'

import json
from datetime import datetime, timedelta
from scripts.stac_pipeline import get_stac_ndvi_time_series

dummy_polygon = [
    [75.8340, 30.9010],
    [75.8350, 30.9010],
    [75.8350, 30.9020],
    [75.8340, 30.9020],
    [75.8340, 30.9010]
]

end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=180)).strftime('%Y-%m-%d')

try:
    results = get_stac_ndvi_time_series(dummy_polygon, start_date, end_date)
    print("Results:", results)
except Exception as e:
    import traceback
    traceback.print_exc()

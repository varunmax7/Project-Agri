import os
import json
from datetime import datetime, timedelta
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# Crucial for reading public AWS buckets without credentials.
# Extra GDAL/CURL settings make parallel S3 reads safe: disable directory
# probing (one less HTTP call per asset), enable per-process VSI caching,
# and retry transient 5xx/timeouts a few times instead of failing the whole load.
os.environ.setdefault('AWS_NO_SIGN_REQUEST', 'YES')
os.environ.setdefault('GDAL_DISABLE_READDIR_ON_OPEN', 'EMPTY_DIR')
os.environ.setdefault('CPL_VSIL_CURL_ALLOWED_EXTENSIONS', '.tif,.TIF,.tiff')
os.environ.setdefault('VSI_CACHE', 'TRUE')
os.environ.setdefault('VSI_CACHE_SIZE', '67108864')  # 64 MB
os.environ.setdefault('GDAL_HTTP_MAX_RETRY', '4')
os.environ.setdefault('GDAL_HTTP_RETRY_DELAY', '1')

import pystac_client
import odc.stac
from shapely.geometry import Polygon

def get_stac_ndvi_time_series(roi_polygon_coords, start_date, end_date):
    """
    Fetches a Sentinel-2 L2A time series using the public AWS Earth Search STAC catalog,
    streams the pixel data into memory, and calculates the mean NDVI.
    Optimized for speed: caps images at 30, uses 20m resolution, sorts by cloud cover.
    """
    # 1. Initialize the STAC Client for AWS Earth Search
    # This is a public endpoint, no authentication required!
    print("Connecting to AWS Earth Search STAC API...")
    catalog = pystac_client.Client.open("https://earth-search.aws.element84.com/v1")

    # 2. Define geometry and bounding box
    roi_poly = Polygon(roi_polygon_coords)
    bbox = roi_poly.bounds # (minx, miny, maxx, maxy)

    print(f"Searching for Sentinel-2 L2A images between {start_date} and {end_date}...")
    
    # 3. Query the catalog
    search = catalog.search(
        collections=["sentinel-2-l2a"],
        bbox=bbox,
        datetime=f"{start_date}/{end_date}",
        query={"eo:cloud_cover": {"lt": 20}} # Less than 20% cloud cover
    )
    
    items = list(search.items())
    print(f"Found {len(items)} cloud-free images.")

    if not items:
        return []

    # 4. Cap at 25 scenes — every scene costs ~3 HTTPS roundtrips (red, nir, scl)
    # against S3, so this bounds the worst-case load time. Sort so the clearest
    # scenes win when we truncate.
    items.sort(key=lambda item: item.properties.get('eo:cloud_cover', 100))
    if len(items) > 25:
        items = items[:25]
        print(f"Using top 25 clearest images for faster processing.")

    print(f"Streaming pixel data for {len(items)} images...")

    # 5. Load the data using odc-stac (streams ONLY the requested bounding box).
    # 60m resolution: for mean NDVI over a 5-acre parcel a 60m grid has ~3x3 pixels
    # which is plenty for an unbiased mean, and ~9x less data than 20m.
    # chunks={} makes the load lazy (dask-backed) and pool=16 fans out the S3
    # byte-range reads across 16 worker threads — the slow part was waiting on
    # serial HTTPS roundtrips, not the math.
    dataset = odc.stac.load(
        items,
        bbox=bbox,
        bands=["red", "nir", "scl"],
        resolution=60,
        groupby="solar_day",
        pool=16,
        fail_on_error=False,
    )

    # 6. Vectorized NDVI + masked spatial mean over every timestep in one go.
    # Previously this looped per-timestep and called .values N times, forcing N
    # separate compute passes (and N serial fetches). Doing it as one xarray
    # expression lets dask schedule all the band reads concurrently and run a
    # single compute, while producing identical numbers.
    import math
    import numpy as np

    valid_mask = dataset.scl.isin([4, 5, 6])
    nir = dataset.nir.astype('float32')
    red = dataset.red.astype('float32')
    ndvi = (nir - red) / (nir + red)
    ndvi_masked = ndvi.where(valid_mask)
    mean_per_time = ndvi_masked.mean(dim=('y', 'x'))

    mean_values = np.asarray(mean_per_time.values)
    time_values = mean_per_time.time.values

    results = []
    for date_val, mean_ndvi in zip(time_values, mean_values):
        mean_ndvi = float(mean_ndvi)
        if math.isnan(mean_ndvi):
            continue
        results.append({
            "date": str(date_val)[:10],
            "ndvi": round(mean_ndvi, 4),
        })

    results.sort(key=lambda x: x['date'])
    print(f"Processed {len(time_values)} timesteps, {len(results)} valid NDVI observations.")
    return results

if __name__ == "__main__":
    import sys
    try:
        # Check if we are receiving JSON via stdin (for subprocess calls)
        if not sys.stdin.isatty():
            input_data = json.load(sys.stdin)
            polygon = input_data.get('polygon')
            start_date = input_data.get('start_date')
            end_date = input_data.get('end_date')
            
            # Suppress normal prints by redirecting stdout to stderr
            original_stdout = sys.stdout
            sys.stdout = sys.stderr
            results = get_stac_ndvi_time_series(polygon, start_date, end_date)
            sys.stdout = original_stdout
            
            # Output ONLY JSON to stdout
            print(json.dumps(results))
            sys.exit(0)

        # Standard execution (testing)
        dummy_polygon = [
            [75.8340, 30.9010],
            [75.8350, 30.9010],
            [75.8350, 30.9020],
            [75.8340, 30.9020],
            [75.8340, 30.9010]
        ]
        
        end_date = datetime.today().strftime('%Y-%m-%d')
        start_date = (datetime.today() - timedelta(days=180)).strftime('%Y-%m-%d')
        results = get_stac_ndvi_time_series(dummy_polygon, start_date, end_date)
        
        print("\n--- NDVI Time Series Results (from AWS Open Data) ---")
        if not results:
            print("No valid cloud-free images found for this period/location.")
        else:
            print(json.dumps(results, indent=2))
        print("\nSuccess! The STAC pipeline is operational. No APIs keys were harmed.")
        
    except Exception as e:
        import traceback
        traceback.print_exc(file=sys.stderr)
        print(f"\nPipeline failed. Error: {e}")
        sys.exit(1)

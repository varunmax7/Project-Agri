import os
import json
import sys
import math
import warnings
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

warnings.filterwarnings("ignore")

# GDAL/CURL settings for fast remote COG reads.
# - GDAL_DISABLE_READDIR_ON_OPEN: skip directory probing (one HTTP call less per asset)
# - VSI_CACHE: cache fetched byte-ranges in memory so repeated reads of the same
#   COG block do not re-hit the network
# - GDAL_HTTP_MERGE_CONSECUTIVE_RANGES: coalesce nearby range requests into one
# - CPL_VSIL_CURL_USE_HEAD: skip a wasted HEAD request before each GET
os.environ.setdefault('GDAL_DISABLE_READDIR_ON_OPEN', 'EMPTY_DIR')
os.environ.setdefault('CPL_VSIL_CURL_ALLOWED_EXTENSIONS', '.tif,.TIF,.tiff')
os.environ.setdefault('VSI_CACHE', 'TRUE')
os.environ.setdefault('VSI_CACHE_SIZE', '67108864')  # 64 MB
os.environ.setdefault('GDAL_HTTP_MAX_RETRY', '2')
os.environ.setdefault('GDAL_HTTP_RETRY_DELAY', '1')
os.environ.setdefault('GDAL_HTTP_MERGE_CONSECUTIVE_RANGES', 'YES')
os.environ.setdefault('CPL_VSIL_CURL_USE_HEAD', 'NO')

import pystac_client
import planetary_computer
import rasterio
import numpy as np
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds


# Microsoft Planetary Computer instead of AWS Earth Search. The data is the
# same Sentinel-2 L2A but served from Azure's global CDN, which from many
# Asian / European networks is dramatically faster than AWS us-west-2 S3.
# planetary_computer.sign_inplace adds a short-lived SAS token to each asset
# URL so plain rasterio can open them without any extra setup.
STAC_ENDPOINT = "https://planetarycomputer.microsoft.com/api/stac/v1"


def _read_scene(item, bbox):
    """Fetch a small NDVI mean over `bbox` for a single Sentinel-2 scene.
    Uses windowed rasterio reads — only the bytes covering the bbox are
    streamed, regardless of how big the underlying COG is."""
    try:
        with rasterio.open(item.assets['B04'].href) as ds:
            l, b, r, t = transform_bounds('EPSG:4326', ds.crs, *bbox)
            win = from_bounds(l, b, r, t, ds.transform)
            red = ds.read(1, window=win).astype('float32')
        with rasterio.open(item.assets['B08'].href) as ds:
            l, b, r, t = transform_bounds('EPSG:4326', ds.crs, *bbox)
            win = from_bounds(l, b, r, t, ds.transform)
            nir = ds.read(1, window=win).astype('float32')

        valid = (red > 0) & (nir > 0)
        if not valid.any():
            return None
        ndvi = (nir - red) / (nir + red + 1e-6)
        mean_ndvi = float(np.mean(ndvi[valid]))
        if math.isnan(mean_ndvi):
            return None
        return {
            "date": str(item.datetime)[:10],
            "ndvi": round(mean_ndvi, 4),
        }
    except Exception as exc:
        print(f"[scene {item.id[:30]}] read failed: {exc}", file=sys.stderr)
        return None


def get_stac_ndvi_time_series(roi_polygon_coords, start_date, end_date):
    """Fetch a Sentinel-2 NDVI time series via the Microsoft Planetary Computer.

    Cloud-cover is filtered server-side; the clearest scenes are kept and read
    in parallel via windowed rasterio so the bytes downloaded scale with the
    parcel size, not the underlying scene size."""

    print("Connecting to Microsoft Planetary Computer STAC API...")
    catalog = pystac_client.Client.open(
        STAC_ENDPOINT,
        modifier=planetary_computer.sign_inplace,
    )

    # Polygon bounding box in lng/lat
    xs = [c[0] for c in roi_polygon_coords]
    ys = [c[1] for c in roi_polygon_coords]
    bbox = (min(xs), min(ys), max(xs), max(ys))

    print(f"Searching for Sentinel-2 L2A images between {start_date} and {end_date}...")
    search = catalog.search(
        collections=["sentinel-2-l2a"],
        bbox=bbox,
        datetime=f"{start_date}/{end_date}",
        query={"eo:cloud_cover": {"lt": 40}},
    )

    items = list(search.items())
    print(f"Found {len(items)} candidate images.")
    if not items:
        return []

    # Cap at 5 scenes. Each scene is ~2 small range-reads (red + nir bands),
    # parallelised below. 5 keeps us comfortably under the 55 s subprocess
    # budget while still resolving a real NDVI curve.
    items.sort(key=lambda item: item.properties.get('eo:cloud_cover', 100))
    if len(items) > 5:
        items = items[:5]
        print(f"Using top 5 clearest images for faster processing.")

    print(f"Streaming pixel data for {len(items)} images...")
    with ThreadPoolExecutor(max_workers=len(items)) as ex:
        results = [r for r in ex.map(lambda it: _read_scene(it, bbox), items) if r]

    results.sort(key=lambda x: x['date'])
    print(f"Got {len(results)} valid NDVI observations.")
    return results


if __name__ == "__main__":
    try:
        if not sys.stdin.isatty():
            input_data = json.load(sys.stdin)
            polygon = input_data.get('polygon')
            start_date = input_data.get('start_date')
            end_date = input_data.get('end_date')

            original_stdout = sys.stdout
            sys.stdout = sys.stderr
            results = get_stac_ndvi_time_series(polygon, start_date, end_date)
            sys.stdout = original_stdout

            print(json.dumps(results))
            sys.exit(0)

        dummy_polygon = [
            [75.8340, 30.9010],
            [75.8350, 30.9010],
            [75.8350, 30.9020],
            [75.8340, 30.9020],
            [75.8340, 30.9010],
        ]
        end_date = datetime.today().strftime('%Y-%m-%d')
        start_date = (datetime.today() - timedelta(days=120)).strftime('%Y-%m-%d')
        results = get_stac_ndvi_time_series(dummy_polygon, start_date, end_date)
        print("\n--- NDVI Time Series Results ---")
        print(json.dumps(results, indent=2) if results else "No valid observations.")

    except Exception as e:
        import traceback
        traceback.print_exc(file=sys.stderr)
        print(f"\nPipeline failed. Error: {e}", file=sys.stderr)
        sys.exit(1)

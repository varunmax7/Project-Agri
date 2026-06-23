import os
import json
from datetime import datetime, timedelta
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# Crucial for reading public AWS buckets without credentials
os.environ['AWS_NO_SIGN_REQUEST'] = 'YES'

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
    dataset = odc.stac.load(
        items,
        bbox=bbox,
        bands=["red", "nir", "scl"],
        resolution=60,
        groupby="solar_day"
    )

    # 6. Process the data (Calculate NDVI)
    results = []
    import math
    total_timesteps = len(dataset.time)
    
    # Iterate through the time steps
    for i in range(total_timesteps):
        # Select the data for this specific date
        ds_time = dataset.isel(time=i)
        
        # SCL masking: 4=Vegetation, 5=Bare Soils, 6=Water. 
        # Exclude clouds (9), shadows (3), etc.
        valid_mask = ds_time.scl.isin([4, 5, 6])
        
        # Calculate NDVI: (NIR - Red) / (NIR + Red)
        # We convert to float32 to avoid integer division issues
        nir = ds_time.nir.astype('float32')
        red = ds_time.red.astype('float32')
        
        ndvi = (nir - red) / (nir + red)
        
        # Apply the mask
        ndvi_masked = ndvi.where(valid_mask)
        
        # Calculate the mean NDVI across all pixels in our bounding box for this date
        mean_ndvi = float(ndvi_masked.mean().values)
        
        # Get the date string
        date_str = str(ds_time.time.values)[:10]
        
        # Skip if no valid pixels (e.g., all clouds despite the catalog filter)
        if not math.isnan(mean_ndvi):
             results.append({
                "date": date_str,
                "ndvi": round(mean_ndvi, 4)
            })

    # Sort by date
    results.sort(key=lambda x: x['date'])
    print(f"Processed {total_timesteps} timesteps, {len(results)} valid NDVI observations.")
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

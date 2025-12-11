import json
import os

def generate_m3u_playlist(json_data, output_file="playlist.m3u"):
    """
    Generates an M3U playlist from the provided JSON data.
    """
    print(f"Starting playlist generation for {len(json_data)} entries...")
    
    with open(output_file, 'w') as f:
        f.write('#EXTM3U\n')
        
        valid_entries_count = 0
        for channel_id, details in json_data.items():
            # Extract URL, kid, and key
            url = details.get('mpdUrl', '')
            kid = details.get('kid', '')
            key = details.get('key', '')
            
            # Skip entries without a valid URL
            if not url or not url.startswith('http'):
                continue
                
            # Write M3U metadata line
            f.write(f'#EXTINF:-1 group-title="Stream",{channel_id}\n')
            
            # Add DRM properties if keys exist (formatted for inputstream.adaptive)
            if kid and key:
                f.write('#KODIPROP:inputstream.adaptive.license_type=com.widevine.alpha\n')
                f.write(f'#KODIPROP:inputstream.adaptive.license_key={kid}:{key}\n')
                
            # Write the stream URL
            f.write(f'{url}\n')
            valid_entries_count += 1
            
    print(f"Successfully created {output_file} with {valid_entries_count} streams.")

if __name__ == "__main__":
    # Define the input data file path
    data_file = 'api_data.json'
    
    if not os.path.exists(data_file):
        print(f"Error: Data file '{data_file}' not found. Exiting.")
    else:
        # Load the JSON data
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        # Generate the playlist
        generate_m3u_playlist(data)

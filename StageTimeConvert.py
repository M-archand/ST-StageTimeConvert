import argparse
import os
import json
import math
import csv

def ticks_to_formatted_time(ticks, rate=64):
    """
    Convert timer ticks to a time string (MM:SS.mmm) based on the given tick rate.
    Default tick rate is 64 (CS2/CS:GO).
    """
    total_seconds = ticks / rate
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    milliseconds = int(round((total_seconds - minutes*60 - seconds) * 1000))
    return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

def process_json_files(input_folder, output_csv):
    """
    Scan 'input_folder' for *'_stage_times.json' files, parse each file,
    and write rows to 'output_csv'.
    """
    fieldnames = ["MapName", "SteamID", "PlayerName", "Stage", "TimerTicks", "FormattedTime", "Velocity"]

    # Open the CSV file once and write all rows from all JSON files.
    with open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # Recursively scan the input folder for JSON files
        for root, _, files in os.walk(input_folder):
            for filename in files:
                if filename.endswith("_stage_times.json"):
                    # Map name is derived from the filename (minus "_stage_times.json")
                    map_name = filename.replace("_stage_times.json", "")
                    input_path = os.path.join(root, filename)

                    try:
                        with open(input_path, 'r', encoding='utf-8') as infile:
                            data = json.load(infile)
                    except (json.JSONDecodeError, OSError) as e:
                        print(f"Skipping {input_path} due to read/parse error: {e}")
                        continue

                    # 'data' is a dictionary keyed by SteamID => { "StageTimes": {...}, "StageVelos": {...} }
                    for steam_id, record in data.items():
                        stage_times = record.get("StageTimes", {})
                        stage_velos = record.get("StageVelos", {})

                        # For each stage, we have a timer tick count and a velocity
                        for stage_str, ticks in stage_times.items():
                            velocity = stage_velos.get(stage_str, "")
                            formatted_time = ticks_to_formatted_time(ticks)

                            row = {
                                "MapName": map_name,
                                "SteamID": steam_id,
                                "PlayerName": "",  # Blank for now
                                "Stage": stage_str,
                                "TimerTicks": ticks,
                                "FormattedTime": formatted_time,
                                "Velocity": velocity
                            }
                            writer.writerow(row)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="Path to folder containing *_stage_times.json files")
    ap.add_argument("-o", "--output", default="stage_times_output.csv", help="Output CSV file name (default: stage_times_output.csv)")
    args = ap.parse_args()

    input_folder = args.input
    output_csv = args.output

    process_json_files(input_folder, output_csv)
    print(f"Done! CSV saved to {output_csv}")

if __name__ == "__main__":
    main()
import os
import json

def main():
    directory = input("Enter the directory path to process .dat files (e.g., /storage/emulated/0/ChFiles/): ").strip()
    
    if not os.path.isdir(directory):
        print("Invalid directory. Exiting.")
        return
    
    print(f"Selected directory: {directory}")
    proceed = input("Do you want to start generating the JSON file? (y/n): ").strip().lower()

    if proceed != 'y':
        print("Exiting.")
        return

    # Get all .dat files in the selected directory
    dat_files = [f for f in os.listdir(directory) if f.endswith('.dat')]
    
    if not dat_files:
        print("No .dat files found in the selected directory.")
        return
    
    output_data = []

    for dat_file in dat_files:
        dat_path = os.path.join(directory, dat_file)
        try:
            # Read the content of the .dat file
            with open(dat_path, 'r') as file:
                content = json.load(file)  # Assuming .dat file contains JSON

            # Extract the required information
            guest_info = content.get("guest_account_info", {})
            uid = guest_info.get("com.garena.msdk.guest_uid", "")
            password = guest_info.get("com.garena.msdk.guest_password", "")
            
            if uid and password:
                output_data.append({"uid": uid, "password": password})
        except json.JSONDecodeError:
            print(f"Error: {dat_file} does not contain valid JSON data.")
        except Exception as e:
            print(f"Error reading {dat_file}: {e}")
    
    # Create the output JSON file
    output_file = os.path.join(directory, "ind_ind.json")
    try:
        with open(output_file, 'w') as json_file:
            json.dump(output_data, json_file, indent=4)
        print(f"JSON file created successfully: {output_file}")
    except Exception as e:
        print(f"Error writing JSON file: {e}")

if __name__ == "__main__":
    main()
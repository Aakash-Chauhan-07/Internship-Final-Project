import json
import time
from task_assignment import task_assignment_and_execution

def read_and_save_json(filename):
  """
  Continuously reads a JSON file, saves its content to a dictionary,
  and overwrites the file with an empty dictionary if content is found.
  """
  while True:
    try:
      # Open the file in read mode
      with open(filename, 'r') as file:
        # Try to load the JSON content
        try:
          print("Trying")
          data = json.load(file)
          # If content is found, save it in a dictionary
          if data:
            task_assignment_and_execution(data)
            print(f"Content found in {filename}: \n{data}")
            # Overwrite the file with an empty dictionary
            with open(filename, 'w') as outfile:
              json.dump({}, outfile)
          data = None
        except json.JSONDecodeError:
          print(f"{filename} is empty")
    except FileNotFoundError:
      print(f"File '{filename}' not found. Skipping...")
    finally:
      # Close the file (if opened)
      file.close() if 'file' in locals() else None

    # Take a break between reads (adjust as needed)
    time.sleep(5)

# Replace 'your_file.json' with the actual filename
filename = 'service.json'
read_and_save_json(filename)

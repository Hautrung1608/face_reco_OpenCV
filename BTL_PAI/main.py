import cv2 as cv
import time
import sqlite3
import numpy as np
from database import setup_database, fetch_from_database
from savedatabase import save_to_database

capture = cv.VideoCapture(0)  # to open Camera

# Accessing pretrained model
pretrained_model = cv.CascadeClassifier("face_detector.xml") 

# Flag to track if face was previously detected
previously_detected = False

# Setup the database
setup_database()

while True:
    boolean, frame = capture.read()
    if boolean == True:
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        coordinate_list = pretrained_model.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3) 
        
        # Drawing rectangle in frame
        for (x, y, w, h) in coordinate_list:
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Save image if a new face is detected
        if len(coordinate_list) > 0 and not previously_detected:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            cv.imwrite(f"images/detected_face_{timestamp}.jpg", frame)
            
            # Convert the image to a format that can be stored in the database
            _, buffer = cv.imencode('.jpg', frame)
            image_blob = buffer.tobytes()
            
            # Save to the database
            save_to_database(image_blob, timestamp)
            
            previously_detected = True  # Set flag to true as face is detected
        elif len(coordinate_list) == 0:
            previously_detected = False  # Reset flag when no face is detected
        
        # Display detected face
        cv.imshow("Live Face Detection", frame)
        
        # Condition to break out of while loop
        if cv.waitKey(20) == ord('q'):
            break

capture.release()
cv.destroyAllWindows()

# Fetch data from the database and display
#records = fetch_from_database()

#for record in records:
 #   id, timestamp, image_blob = record
  #  image = cv.imdecode(np.frombuffer(image_blob, np.uint8), cv.IMREAD_COLOR)
   # cv.imshow(f"Image ID: {id} Timestamp: {timestamp}", image)
   # cv.waitKey(0)

#cv.destroyAllWindows()

import matplotlib.pyplot as plt
import io
from PIL import Image
import pandas as pd
from database import fetch_from_database

# Fetch data from the database
records = fetch_from_database()

# Create a DataFrame from the fetched records
data = []
for record in records:
    id, timestamp, image_blob = record
    data.append({'ID': id, 'Timestamp': timestamp, 'Image': image_blob})

df = pd.DataFrame(data)

# Save images to files and insert file paths into the DataFrame
image_paths = []
for index, row in df.iterrows():
    image_bytes = row['Image']
    image = Image.open(io.BytesIO(image_bytes))
    image_path = f"show/image_{row['ID']}.png"  # Adjust the filename as needed
    image.save(image_path)
    image_paths.append(image_path)

df['Image Path'] = image_paths

# Save DataFrame to Excel
excel_file = "images_data.xlsx"  # Adjust the filename as needed
df.to_excel(excel_file, index=False)

print("Excel file with images saved successfully.")

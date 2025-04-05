import cv2
import numpy as np
import imutils
import easyocr
import mysql.connector
import matplotlib.pyplot as plt

conn = mysql.connector.connect(
    host="localhost",       
    user="root",   
    password="1234", 
    database="anpr"   
)
cursor = conn.cursor()

# table create
cursor.execute('''CREATE TABLE IF NOT EXISTS vehicle_info (
                  id INT AUTO_INCREMENT PRIMARY KEY, 
                  plate VARCHAR(20) UNIQUE, 
                  name VARCHAR(100), 
                  phone VARCHAR(15))''')

def process_image(image_path):
    """Processes an image to extract the number plate."""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    bfilter = cv2.bilateralFilter(gray, 11, 17, 17) 
    edged = cv2.Canny(bfilter, 30, 200) 

    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break

    if location is None:
        print("No number plate detected.")
        return None, img

    mask = np.zeros(gray.shape, np.uint8)
    cv2.drawContours(mask, [location], 0, 255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)

    (x, y) = np.where(mask == 255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2+1, y1:y2+1]

    # Perform OCR
    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)

    if result:
        text = result[0][-2]
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, text=text, org=(approx[0][0][0], approx[1][0][1] + 60), 
                    fontFace=font, fontScale=1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
        cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0, 255, 0), 3)
        return text, img
    else:
        print("Number plate text not detected.")
        return None, img

def check_or_register_vehicle(plate_number):
    """Checks if the vehicle is already in the database or registers a new one."""
    cursor.execute("SELECT * FROM vehicle_info WHERE plate=%s", (plate_number,))
    existing_record = cursor.fetchone()

    if existing_record:
        print("\n✅ Vehicle found in database:")
        print(f"Plate Number: {existing_record[1]}")
        print(f"Owner's Name: {existing_record[2]}")
        print(f"Phone Number: {existing_record[3]}")
    else:
        print("\n🚨 Vehicle not found in the database.")
        register = input("Do you want to register this vehicle? (yes/no): ").strip().lower()
        
        if register == "yes":
            name = input("Enter Owner's Name: ")
            phone = input("Enter Phone Number: ")
            cursor.execute("INSERT INTO vehicle_info (plate, name, phone) VALUES (%s, %s, %s)", 
                           (plate_number, name, phone))
            conn.commit()
            print("✅ Vehicle information saved successfully!")
        else:
            print("Registration skipped.")

def view_registered_vehicles():
    """Displays all registered vehicles from the database."""
    cursor.execute("SELECT * FROM vehicle_info")
    records = cursor.fetchall()

    if not records:
        print("\n🚘 No registered vehicles found.")
    else:
        print("\n📜 Registered Vehicles:")
        print("-" * 50)
        print(f"{'ID':<5}{'Plate Number':<15}{'Owner':<20}{'Phone':<15}")
        print("-" * 50)
        for record in records:
            print(f"{record[0]:<5}{record[1]:<15}{record[2]:<20}{record[3]:<15}")
        print("-" * 50)

def show_image(img, title="Image"):
    """Displays an image using matplotlib."""
    plt.figure(figsize=(8, 6))
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis("off")
    plt.show()

while True:
    print("\n🚗 **ANPR System - Choose an option:**")
    print("1️⃣ Check or Register a Vehicle")
    print("2️⃣ View Registered Vehicles")
    print("3️⃣ Exit")
    
    choice = input("Enter your choice: ").strip()

    if choice == "1":
        image_path = 'image1.jpg'  
        plate_number, processed_img = process_image(image_path)

        if plate_number:
            print("\nDetected Number Plate:", plate_number)
            check_or_register_vehicle(plate_number)
        show_image(processed_img, "Processed Image")

    elif choice == "2":
        view_registered_vehicles()

    elif choice == "3":
        print("🔴 Exiting ANPR System. Goodbye!")
        break

    else:
        print("❌ Invalid choice. Please select a valid option.")

cursor.close()
conn.close()

import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8x.pt')


def predict_and_show(image_path):
    # Load the input image
    image = cv2.imread(image_path)

    # Check if the image was loaded successfully
    if image is None:
        print(f"Error: Unable to load image at path '{image_path}'. Please check the file path.")
        return

    # Run inference on the image
    results = model(image)

    # Filter results for specific classes (sports ball: 32, baseball bat: 34)
    filtered_boxes = []
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])  # Get class ID
            if class_id in [32, 34]:  # Filter specific classes
                filtered_boxes.append(box)

    # Annotate the image with filtered predictions
    for box in filtered_boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
        class_id = int(box.cls[0])
        confidence = box.conf[0]  # Confidence score

        # Update class names for 32 and 34
        class_name = "ball" if class_id == 32 else "bat" if class_id == 34 else model.names[class_id]

        # Draw the bounding box
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Put class label and confidence
        label = f"{class_name}: {confidence:.2f}"
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show the image
    cv2.imshow("Predictions", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save the output image
    # output_path = "output.jpg"
    # cv2.imwrite(output_path, image)
    # print(f"Predicted image saved as {output_path}")


# Example usage
image_path = r"pullshot.jpg"  # Replace with your input image path
predict_and_show(image_path)

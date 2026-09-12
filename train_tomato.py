from ultralytics import YOLO

# Load YOLOv11 classification model
model = YOLO("yolo11n-cls.pt")

# Train
results = model.train(
    data=r"C:\Crop_Project\dataset\tomato",
    epochs=30,
    imgsz=224,
    batch=32,
    name="tomato_disease"
)

print("Training completed!")
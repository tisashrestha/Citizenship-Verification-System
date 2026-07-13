import os
import cv2
import albumentations as A


input_folder = "cit"
output_folder = "augmented"

os.makedirs(output_folder, exist_ok=True)


if not os.path.exists(input_folder):
    raise FileNotFoundError(
        "Folder 'cit' not found. Create a folder named cit and put images inside it."
    )



transform = A.Compose([

    A.Affine(
        rotate=(-8, 8),
        scale=(0.9, 1.1),
        translate_percent=(-0.05, 0.05),
        border_mode=cv2.BORDER_CONSTANT,
        fill=(255, 255, 255),
        p=0.9
    ),

    A.Perspective(
        scale=(0.02, 0.06),
        p=0.4
    ),

    A.OneOf([
        A.RandomBrightnessContrast(
            brightness_limit=0.35,
            contrast_limit=0.35,
            p=1
        ),

        A.RandomGamma(
            gamma_limit=(70, 130),
            p=1
        ),

        A.CLAHE(
            clip_limit=3,
            p=1
        )

    ], p=0.9),


    A.HueSaturationValue(
        hue_shift_limit=10,
        sat_shift_limit=25,
        val_shift_limit=20,
        p=0.6
    ),


    A.OneOf([

        A.GaussNoise(
            std_range=(0.02, 0.08),
            p=1
        ),

        A.MotionBlur(
            blur_limit=5,
            p=1
        ),

        A.GaussianBlur(
            blur_limit=(3, 5),
            p=1
        )

    ], p=0.5),


    A.ImageCompression(
        quality_range=(60, 95),
        p=0.5
    )

])


AUG_PER_IMAGE = 5


images = [
    f for f in os.listdir(input_folder)
    if f.lower().endswith(
        (".jpg", ".jpeg", ".png")
    )
]


print("Found images:", len(images))


if len(images) == 0:
    raise Exception("No images found in cit folder")


saved = 0


for img_name in images:

    img_path = os.path.join(
        input_folder,
        img_name
    )

    image = cv2.imread(img_path)


    if image is None:
        print("Skipping:", img_name)
        continue


    image = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )


    for i in range(AUG_PER_IMAGE):

        augmented = transform(
            image=image
        )


        aug_image = cv2.cvtColor(
            augmented["image"],
            cv2.COLOR_RGB2BGR
        )


        filename = (
            os.path.splitext(img_name)[0]
            +
            f"_aug_{i}.jpg"
        )


        save_path = os.path.join(
            output_folder,
            filename
        )


        cv2.imwrite(
            save_path,
            aug_image
        )


        saved += 1



print("\n")
print("Augmentation completed")
print("\n")
print("Original images :", len(images))
print("Augmented images:", saved)
print("Saved folder    :", output_folder)
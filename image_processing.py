from PIL import Image, ImageTk
import imagehash


# Получение всех хешей изображения: оригинал, зеркальные и повороты
def get_all_image_hashes(image_path):
    try:
        img = Image.open(image_path)
        hashes = []
        hashes.append(imagehash.average_hash(img))  # Оригинал
        hashes.append(imagehash.average_hash(img.rotate(90, expand=True)))  # 90°
        hashes.append(imagehash.average_hash(img.rotate(180, expand=True)))  # 180°
        hashes.append(imagehash.average_hash(img.rotate(270, expand=True)))  # 270°
        hashes.append(
            imagehash.average_hash(img.transpose(Image.FLIP_LEFT_RIGHT))
        )  # Зеркально по горизонтали
        hashes.append(
            imagehash.average_hash(img.transpose(Image.FLIP_TOP_BOTTOM))
        )  # Зеркально по вертикали
        return hashes
    except:
        return []


# Отображение предпросмотра изображения
def display_image(file_path, image_label):
    try:
        img = Image.open(file_path)
        img.thumbnail((200, 200))
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk
    except Exception as e:
        raise ValueError(f"Не удалось загрузить изображение: {e}")

from utils import calculate_file_hash, find_all_files
from image_processing import get_all_image_hashes


def find_duplicates_and_similars(main_folder, progress_callback):
    files = find_all_files(main_folder)
    file_hashes = {}
    duplicates = {}
    similars = {}

    total_files = len(files)

    # Поиск дубликатов
    for idx, file in enumerate(files):
        file_hash = calculate_file_hash(file)
        if file_hash in file_hashes:
            duplicates[file] = file_hashes[file_hash]
        else:
            file_hashes[file_hash] = file
        progress_callback((idx + 1) / total_files * 50)

    # Поиск схожих изображений
    for idx, file1 in enumerate(files):
        hashes1 = get_all_image_hashes(file1)
        if hashes1:
            for file2 in files:
                if file1 != file2:
                    hashes2 = get_all_image_hashes(file2)
                    if hashes2:
                        for h1 in hashes1:
                            for h2 in hashes2:
                                if abs(h1 - h2) <= 5:  # Порог для схожести
                                    similars[file1] = file2
        progress_callback(50 + (idx + 1) / total_files * 50)

    return duplicates, similars


def generate_report(duplicates, similars):
    with open("duplicates_report.txt", "w") as report:
        report.write("Точные дубликаты:\n")
        for file, duplicate in duplicates.items():
            report.write(f"{file} - копия {duplicate}\n")

        report.write("\nСхожие файлы:\n")
        for file1, file2 in similars.items():
            report.write(f"{file1} - похож на {file2}\n")

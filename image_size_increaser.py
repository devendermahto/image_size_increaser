import os

def increase_image_size(file_path, min_size_mb=2, max_size_mb=5):
    with open(file_path, 'rb') as f:
        image_data = f.read()

    # Create a large metadata string to increase file size
    metadata = str_repeat("metadata1234567890", 50000)
    new_image_data = image_data + metadata.encode()

    output_path = os.path.splitext(file_path)[0] + "IMG" + os.path.splitext(file_path)[1]
    with open(output_path, 'wb') as f:
        f.write(new_image_data)

    while os.path.getsize(output_path) < min_size_mb * 1024 * 1024:
        with open(output_path, 'ab') as f:
            f.write(str_repeat("metadata1234567890", 1000).encode())

    while os.path.getsize(output_path) > max_size_mb * 1024 * 1024:
        with open(output_path, 'rb') as f:
            new_image_data = f.read()

        new_image_data = new_image_data[:-1000]
        with open(output_path, 'wb') as f:
            f.write(new_image_data)

    return output_path

def str_repeat(string, times):
    return string * times

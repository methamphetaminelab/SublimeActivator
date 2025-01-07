from loguru import logger
import sys
import shutil
import time
import os

logger.remove()
logger.add(sys.stderr, format="[<level>{level}</level>] {message}", level="INFO", colorize=True)

def replace_signature(file_path, signature_map):
    try:
        if not os.path.isfile(file_path):
            logger.error(f"File {file_path} does not exist.")
            return

        start_time = time.time()

        backup_path = f"{file_path}.bak"
        shutil.copy(file_path, backup_path)
        logger.success(f"Backup created at {backup_path}")

        with open(file_path, 'rb') as file:
            data = bytearray(file.read())

        if not signature_map:
            logger.warning("No signatures provided for replacement.")
        
        for old_signature, new_signature in signature_map.items():
            data = data.replace(old_signature, new_signature)
            logger.success(f"Replaced signature: [{' '.join([f'{byte:02x}' for byte in old_signature])}] -> [{' '.join([f'{byte:02x}' for byte in new_signature])}]")

        with open(file_path, 'wb') as file:
            file.write(data)

        logger.success(f"Signatures replaced and saved in {file_path}")
    
    except FileNotFoundError:
        logger.error(f"File {file_path} not found.")
    except IOError as e:
        logger.error(f"Error while working with the file: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")

    elapsed_time = time.time() - start_time
    logger.info(f"Program completed in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    signature_map = {
        b'\x80\x79\x05\x00\x0F\x94\xC2': b'\xC6\x41\x05\x01\xB2\x00\x90'
    }

    replace_signature(input("Enter the file path (example: D:/Sublime Text/sublime_text.exe): "), signature_map)

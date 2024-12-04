from textnode import TextType, TextNode
import os, shutil, logging
from utils import generate_pages_recursive

logging.basicConfig(
    filename="main.log",
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def clear_directory_contents(target: str):
    # delete the contents of the target directory
    if not os.path.exists(target):
        logging.error(f"Target directory '{target}' does not exist. Exiting.")
        raise Exception("Target directory does not exist. Exiting.")

    # This will also remove the directory, so let's recreate it
    shutil.rmtree(target)
    logging.info(f"Re-creating directory '{target}'")
    os.mkdir(target)
    return


def recursive_copy(source: str, destination: str):
    # recursively copy from source to destination
    logging.info(f"Start copy operation for '{source}' to '{destination}'")

    if not os.path.exists(source):
        logging.error(f"Source '{source}' does not exist. Exiting.")
        raise Exception(f"Source {source} does not exist. Exiting.")

    for item in os.listdir(source):

        logging.info(f"Processing item '{item}'")

        if os.path.isfile(os.path.join(source, item)):
            target = os.path.join(destination, item)
            logging.info(f"Copying '{os.path.join(source,item)}' to '{target}'")
            shutil.copy(os.path.join(source, item), target)

        elif os.path.isdir(os.path.join(source, item)):
            target = os.path.join(destination, os.path.basename(item))
            logging.info(f"Creating directory '{target}'")
            os.mkdir(target)

            for nested_item in os.listdir(os.path.join(source, item)):
                recursive_copy(os.path.join(source, item), target)
    return


def main():
    logging.info("Starting...")

    logging.info("Clearing directory contents...")
    clear_directory_contents("public")

    logging.info("Copying files...")
    recursive_copy("static", "public")

    logging.info("Generating pages...")
    generate_pages_recursive("content", "template.html", "public")

    logging.info("Done.")


if __name__ == "__main__":
    main()

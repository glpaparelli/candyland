"""Context file"""

import os
import math
import click
import requests
import importlib
from pathlib import Path
from zipfile import ZipFile
from rich.progress import Progress


def get_scraper(kind):
    """Build the scraper object from the scrapers folder"""
    files = os.listdir(f"./scrapers/{kind}")
    scraper_file = files.pop()
    scraper_file = scraper_file.replace(".py", "")

    module = importlib.import_module("." + scraper_file, f"scrapers.{kind}")
    # (module, class name)
    return getattr(module, scraper_file.capitalize())()


def get_reading_material(scraper, download_dir_path, search_query):
    """Get manga/comics by name using the provided scraper"""

    # Retrieve <material_name, url> and build a list of chapters urls
    material_name, material_url = scraper.search(search_query)
    chapters_urls = scraper.get_chapters_urls(material_url)

    material_dir_path = str(Path(download_dir_path) / material_name)
    if not os.path.exists(material_dir_path):
        os.mkdir(material_dir_path)

    for chapter_url in chapters_urls:
        # Create the .cbr to store the downloaded manga
        chapter_name = material_name + "_" + scraper.get_chapter_number(chapter_url)
        chapter_path = Path(material_dir_path) / chapter_name
        cbr = ZipFile(f"{chapter_path}.cbr", "w")

        with Progress() as progress:
            task = progress.add_task(f"[red] Downloading {chapter_name}...", total=100)

            # Download images
            images_urls = scraper.get_chapter_images_urls(chapter_url)
            for i, image_url in enumerate(images_urls, start=1):
                image_data = requests.get(image_url).content
                image_path = Path(material_dir_path) / f"{i}.jpg"
                with open(image_path, "wb") as handler:
                    handler.write(image_data)
                cbr.write(image_path)
                os.remove(image_path)

                # Update progressbar
                progress.update(task, advance=math.ceil(100 / len(images_urls)))

            cbr.close()


@click.command()
@click.argument("kind", type=click.Choice(["manga", "comics"], case_sensitive=False))
@click.argument("name", type=str)
@click.option(
    "--download-dir-path",
    "-d",
    default=str(Path.home() / "Downloads" / "Candyland"),
    help="Path to the directory that will contain the downloads.",
)
def candyland(kind, name, download_dir_path):
    # Create download directory
    if not os.path.exists(download_dir_path):
        os.mkdir(download_dir_path)

    # Search the content named `name` and download it
    scraper = get_scraper(kind)

    get_reading_material(scraper, download_dir_path, name)


if __name__ == "__main__":
    candyland()

"""strategy class"""
import abc


class Candy:
    @abc.abstractmethod
    def search(self, name):
        """Retrieve a url for a manga/comics based on its name provided."""
        pass

    @abc.abstractmethod
    def get_chapters_urls(self, reading_material_url):
        """return the list of urls of the chapters of the comics/manga"""
        pass

    @abc.abstractmethod
    def get_chapter_images_urls(self, chapter_url):
        """return the list of image urls for a specific chapter"""
        pass

    @abc.abstractmethod
    def get_chapter_number(self, chapter_url):
        "return the chapter name"
        pass

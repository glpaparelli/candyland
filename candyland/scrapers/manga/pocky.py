"""Scraper for Mangas from https://mangapill.com/"""
import requests
from scrapers import Candy
from bs4 import BeautifulSoup


class Pocky(Candy):
    def __init__(self):
        self.domain = "https://mangapill.com"

    def search(self, name):
        bs = BeautifulSoup(
            requests.get(f"{self.domain}/search", params={"q": name}).text,
            features="html.parser",
        )
        first_match = bs.find(
            class_="my-3 grid justify-end gap-3 grid-cols-2 md:grid-cols-3 lg:grid-cols-5"
        ).find("div")
        manga_name = first_match.find(
            class_="mt-3 font-black leading-tight line-clamp-2"
        ).text
        manga_url = first_match.find("a")["href"]
        return manga_name, self.domain + manga_url

    def get_chapters_urls(self, manga_url):
        # Scrape the list of urls to each chapter of the manga
        bs = BeautifulSoup(requests.get(manga_url).text, features="html.parser")
        chapters_urls = bs.find(id="chapters").find_all("a", href=True)
        chapters_urls = list(map(lambda x: self.domain + x["href"], chapters_urls))
        chapters_urls.reverse()
        return chapters_urls

    def get_chapter_images_urls(self, chap_url):
        # get links to images, one image is one page of the chapter
        bs = BeautifulSoup(requests.get(chap_url).text, features="html.parser")
        chapter_imgages_urls = bs.find_all(lambda tag: "data-src" in tag.attrs)
        chapter_imgages_urls = list(map(lambda x: x["data-src"], chapter_imgages_urls))
        return chapter_imgages_urls

    def get_chapter_number(self, chapter_url):
        return chapter_url.split("-")[-1]

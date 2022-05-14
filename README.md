# Candyland
Candyland is a framework for manga/comics download through web scraping. 

It exploits the [Strategy](https://en.wikipedia.org/wiki/Strategy_pattern) Design Pattern to be extendible and to allow the definition of new scrapers to support other sites. 

***WARNING:*** This code is written for exercise and for personal use only. The authors, the contributors and whoever may be involved decline any responsability for any illegal use of the program and any of its future derivations

## How to Use
- To download a manga: 
	- `python3 candyland manga <name of the manga>`
- To download a comic:
	- *not supported yet*
	- `python3 candyland comics <name of the comic>`

## Supported Sites
- **manga:**
	- *pocky*: [MangaPill](https://mangapill.com/)
- **comics:**
	- *skittles (todo):* [ComicExtra](https://www.comicextra.com/)

### How to support a new Site
To support a new site is enough to define a new `Candy`, which is a new scraper. 
If the site is about mangas the scraper has to be placed in the folder `/scrapers/manga`, if it is about comics the folder is `scrapers/comics`. 

By **naming convention** the scrapers about comics are named as american candy while scrapers about mangas are named after japanese candy. 

Either way the new scraper has to extend the class `Candy` and to implement the following: 
- `__init__(self)`: the field `domain` has to defined and it has to contain the url of the site the scraper is about
- `search(self, name)`:
	- `name` is the manga/comics title passed by the user
	- this method return a pair <reading_material_name, url> where:
		- `reading_material_name` is the real name of the comics/manga, extracted by the result of the site search  
		- `url` is the url of the comics/manga
- `get_chapter_urls(self, reading_material_url)`:
	- `reading_material_url` is the url about the searched comic/manga
	- this method return a list of urls about the chapters of the searched comics/manga
- `get_chapter_images_urls(self, chapter_url)`:
	- `chapter_url` is the url about the chapter of the searched comic/manga
	- this method return a list of urls about the images of the chapter of the searched comic/manga
- `get_chapter_number(self, chapter_url)`
	- `chapter_url` is the url about the chapter of the searched comic/manga
	- this method return the number of the chapter of the searched comic/manga

## Roadmap 
1. support to new sites:
    - [ComicExtra](https://www.comicextra.com/)
    - ...
2. further customization:
    - set a default scraper
    - scraper usage policy:
        - try each scraper until the wanted comic/manga is found
        - ...
    - set the output file format (for now only .cbr files are produced)
    - possibity to download a list of comics/mangas
3. parallelization for better performance
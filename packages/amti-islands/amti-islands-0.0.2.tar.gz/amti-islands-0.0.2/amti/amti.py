#!/usr/bin/env python3
"""Scrape AMTI for island data"""

import urllib
import random
from pathlib import Path
from typing import NamedTuple, Generator

import requests
import bs4

def deg_to_decimal(coordinate: str) -> float:
    """Takes a single degree-format and converts it to decimal"""
    direction = {"N": 1, "S": -1, "E": 1, "W": -1}
    coordinate = coordinate.replace("°", " ").replace("'", " ").replace("\"", " ") \
                           .replace("”", " ")
    new = coordinate.split()
    new_dir = new.pop()
    new.extend(["0", "0", "0"])
    return (int(new[0]) + int(new[1]) / 60 \
            + int(new[2]) / 3600) * direction[new_dir]

# pylint: disable=too-few-public-methods
class SoupAMTI:
    """Base class for BeautifulSoup parsing"""

    def __init__(self, path: str) -> None:
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": "curl/7.83.1"})
        self._soup = self._get_soup(path)

    def _get_html(self, path: str) -> str:
        try:
            with open(f"assets/{path}.html", encoding="utf8") as amti_cn_fd:
                html = amti_cn_fd.read()
            return html
        except FileNotFoundError:
            url = f"https://amti.csis.org/{path}/"
            response = self._session.get(url)
            response.raise_for_status()
            return response.content.decode()

    def _get_file(self, url: str) -> Path:
        url_path = urllib.parse.urlparse(url).path.strip("/") # type: ignore
        path = Path(f"assets/{url_path}")
        if path.exists():
            return path
        response = self._session.get(url, stream=True)
        response.raise_for_status()
        if response.status_code != 200:
            raise Exception(response)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as path_fd:
            for chunk in response:
                path_fd.write(chunk)
        return path

    def _get_soup(self, path: str) -> bs4.element.Tag:
        html = self._get_html(path)
        return bs4.BeautifulSoup(html, features="lxml").main

# pylint: disable=too-few-public-methods
class Island(SoupAMTI):
    """Island dataclass"""

    Coordinates = NamedTuple("Coordinates", [("lat", float), ("long", float)])

    def __init__(self, title: str, names: dict, img_url: str, url: str) -> None:
        url_path = urllib.parse.urlparse(url).path.strip("/") # type: ignore
        super().__init__(url_path)

        tracker_info = self._tracker_info()
        gps = tracker_info["GPS"].split(", ")

        self.url = url
        self.title = title
        self.names = names
        self._img_url = img_url

        self.occupier = tracker_info.get("Occupied by")
        self.legal_status = tracker_info.get("Legal Status")
        self.geo = self.Coordinates(deg_to_decimal(gps[0]),
                                    deg_to_decimal(gps[1]))

    @property
    def img_file(self) -> Path:
        """Local path to satellite image"""
        return self._get_file(self._img_url)

    def __repr__(self) -> str:
        return f"<Island({self.title})>"

    def _tracker_info(self) -> dict:
        data_output = self._soup.article.header.find("div",
                                                     attrs={"id": "data-output"})
        tracker_info = data_output.find("div", attrs={"id": "tracker-info"}) \
                       .find_all("div", attrs={"class": None})
        tracker_info_dict = {}
        for div in tracker_info:
            info = div.text.split(":  ")
            tracker_info_dict[info[0]] = info[1]
        return tracker_info_dict

class AMTI(SoupAMTI):
    """Wrapper for calling AMTI"""

    def __init__(self, path: str = "island-tracker/china") -> None:
        super().__init__(path)
        self._articles = self._soup.find_all("article",
                                             attrs={"class": "island-tracker"})

    def islands(self) -> Generator[Island, None, None]:
        """Island generator"""
        articles = self._articles
        for article in articles:
            yield self._island_factory(article)

    def random_island(self) -> Island:
        """Return a random island"""
        article = random.choice(self._articles)
        return self._island_factory(article)

    @staticmethod
    def _island_factory(article: bs4.element.Tag) -> Island:
        title = article.h2.text
        img_url = article.a.img.get("data-large-file").split("?")[0]
        div_names = article.div.find_all("div", attrs={"class": None})
        names = {}
        for div_name in div_names:
            name = div_name.text.split(":  ")
            names[name[0]] = name[1]
        url = article.a["href"]
        return Island(title, names, img_url, url)

def main() -> None:
    """Entry point"""
    amti = AMTI()

    for island in amti.islands():
        print(island)

if __name__ == "__main__":
    main()

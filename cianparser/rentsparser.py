import requests
from bs4 import BeautifulSoup
import transliterate
from re import findall
from cianparser.constants import *


class ParserRentOffers:
    def __init__(self, type_accommodation: str, location_id: str, rooms, start_page: int, end_page: int,
                 deal_type: str):
        self.session = requests.Session()
        self.session.headers = {'Accept-Language': 'ru', "Accept": "text/html"}

        self.result = []
        self.type_accommodation = type_accommodation
        self.location_id = location_id
        self.rooms = rooms
        self.start_page = start_page
        self.end_page = end_page
        self.deal_type = deal_type
        self.duration_type = 4  # Means flat

        self.url = None

    def build_url(self):
        rooms_path = ""
        if type(self.rooms) is tuple:
            for count_of_room in self.rooms:
                if type(count_of_room) is int:
                    if count_of_room > 0 and count_of_room < 6:
                        rooms_path += ROOM.format(count_of_room)
                elif type(count_of_room) is str:
                    if count_of_room == "studio":
                        rooms_path += STUDIO
        elif type(self.rooms) is int:
            if self.rooms > 0 and self.rooms < 6:
                rooms_path += ROOM.format(self.rooms)
        elif type(self.rooms) is str:
            if self.rooms == "studio":
                rooms_path += STUDIO
            elif self.rooms == "all":
                rooms_path = ""
        base_link = BASE_LINK.replace("DEAL_TYPE", self.deal_type)
        return base_link + ACCOMMODATION_TYPE_PARAMETER.format(self.type_accommodation) + \
               DURATION_TYPE_PARAMETER.format(self.duration_type) + rooms_path

    def load_page(self, number_page=1):
        self.url = self.build_url().format(number_page, self.location_id)

        res = self.session.get(url=self.url)

        res.raise_for_status()
        return res.text

    def parse_page(self, html: str, number_page: int):
        try:
            soup = BeautifulSoup(html, 'lxml')
        except:
            soup = BeautifulSoup(html, 'html.parser')

        offers = soup.select('div[class="_93444fe79c--wrapper--W0WqH"] > article[data-name="CardComponent"]')
        if number_page == self.start_page:
            print(f"Setting {len(offers)} offers [", end="")
            print("=>" * len(offers), end="")
            print("] 100%")

        print(f"{number_page} page: ", end="")
        print("[ ", end="")
        for block in offers:
            self.parse_block(block=block)
        print("] 100%")

    def parse_page_offer(self, html_offer):
        soup_offer_page = BeautifulSoup(html_offer, 'lxml')
        try:
            text_offer = soup_offer_page.select("div[data-name='BtiContainer'] > div[data-name='BtiHouseData']")[0].text
            year = int(text_offer[text_offer.find("Год постройки") + 13: text_offer.find("Год постройки") + 17])
        except:
            print("LOG: Year couldn't be retrieved")
            year = -1
            year_soup = soup_offer_page.select(
                "div[data-testid='object-summary-description-info'] > div[data-testid='object-summary-description-value']")
            for var in year_soup:
                f = findall(r"\b\d\d\d\d\b", var.text)
                if len(f) == 1:
                    year = f[0]

        try:
            text_offer = soup_offer_page.select("div[data-name='ObjectSummaryDescription'] > div > div:nth-child(1)")[
                0].text
            comm = (text_offer[: text_offer.find("Общая")])
            comm_meters = int(findall(r'\d+', comm)[0])
        except IndexError:
            text_offer = soup_offer_page.select("div[data-name='ObjectSummaryDescription'] > div")[0].text
            comm = (text_offer[: text_offer.find("Общая")])
            comm_meters = int(findall(r'\d+', comm)[0])
        except:
            comm_meters = -1

        overall_floors = -1
        exact_floor = -1
        try:
            text_offer = soup_offer_page.select(
                "div[data-testid='object-summary-description-info'] > div[data-testid='object-summary-description-value']")

            for value in text_offer:
                f = findall(r'\d+', value.text)
                if len(f) == 2:
                    exact_floor = f[0]
                    overall_floors = f[1]
        except:
            print("LOG: overall_floors and exact_floor couldn't be retrieved")

        kitchen_meters = -1
        try:
            text_offer = soup_offer_page.select(
                "div[data-testid='object-summary-description-info-block'] > div["
                "data-testid='object-summary-description-info']")
            for info in text_offer:
                if info.select("div[data-testid='object-summary-description-title']")[0].text == "Кухня":
                    kitchen_meters = int(
                        findall(r"\d+", info.select("div[data-testid='object-summary-description-value']")[0].text)[0])
        except IndexError:
            text_offer = soup_offer_page.select("div[data-name='ObjectSummaryDescription'] > div")[0].text
            if "Кухня" in text_offer:
                kitchen = (text_offer[text_offer.find("Кухня") - 6: text_offer.find("Кухня")])
                kitchen_meters = int(findall(r'\d+', kitchen)[0])
            else:
                kitchen_meters = -1
        except:
            kitchen_meters = -1

        return (year, comm_meters, kitchen_meters, exact_floor, overall_floors)

    def parse_block(self, block):

        title = block.select('div[data-name="LinkArea"]')[0].select("span[data-mark='OfferTitle']")[0].text
        docs_checked = False
        print(title)
        try:
            author = block.select("div[class='_93444fe79c--main-info--Nib9U']")[0].select("a")[0].get("href")
            author += " " + block.select("div[class='_93444fe79c--main-info--Nib9U']")[0].select("a")[0].text

            author_type = block.select("div[class='_93444fe79c--container--GyJAp'] > span[style='letter-spacing:1px']")[
                0].text

        except:
            try:
                print("LOG: Author couldn't be retrieved 1")
                author = block.select('div[class="_93444fe79c--main-info--Nib9U"]')[0].select(
                    "div[class='_93444fe79c--name-container--enElO']")[0].text
                author_type = \
                    block.select("div[class='_93444fe79c--container--GyJAp'] > span[style='letter-spacing:1px']")[
                        0].text

            except:
                print("LOG: Author couldn't be retrieved 2")
                author = block.select("div[data-name='Agent']")[0].select("span[data-name='AgentTitle']")[0].text
                author_type = \
                    block.select("div[class='_93444fe79c--container--GyJAp' > span[style='letter-spacing:1px']")[0].text

        try:
            docs_checked = block.select(
                "div[data-name='ContentRow'] > div[data-name='Proof']")[0].text
        except:
            print("LOG: Docs couldn't be checked")

        link = block.select("div[data-name='LinkArea']")[0].select("a")[0].get('href')

        subtitle = ''
        try:
            meters = int(title[title.find("м²") - 4: title.find("м²")])

        except:
            try:
                print("LOG: Meters couldn't be retrieved 1")
                meters = int(title[title.find("м²") - 5: title.find("м²")].split(',')[0])

            except:
                print("LOG: Meters couldn't be retrieved 2")
                subtitle = \
                    block.select('div[data-name="LinkArea"]')[0].select("div[class='_93444fe79c--subtitle--vHiOV']")[
                        0].text

                m = findall(r"[-+]?(?:\d*,\d+|\d+)", subtitle)[1]
                meters = ''
                if "," in m:
                    m = m.replace(",", ".")
                if "." in m:
                    meters = float(m)
                else:
                    meters = int(m)
                print("Meters: " + str(meters))

        if "1-комн" in title or "Студия" in title or "1-комн" in subtitle or "Студия" in subtitle:
            how_many_rooms = 1
        elif "2-комн" in title or "2-комн" in subtitle:
            how_many_rooms = 2
        elif "3-комн" in title or "3-комн" in subtitle:
            how_many_rooms = 3
        elif "4-комн" in title or "4-комн" in subtitle:
            how_many_rooms = 4
        else:
            how_many_rooms = -1

        address_long = block.select("div[data-name='LinkArea']")[0].select("div[class='_93444fe79c--labels--L8WyJ']")[
            0].text
        print("Long address")
        print(address_long)

        price_long = block.select("div[data-name='LinkArea']")[0].select("span[data-mark='MainPrice']")[0].text
        price_per_month = "".join(price_long[:price_long.find("₽/мес") - 1].split())
        price_per_month = int(price_per_month)

        if "%" in price_long:
            commissions = int(price_long[price_long.find("%") - 2:price_long.find("%")].replace(" ", ""))
        else:
            commissions = 0

        try:
            author = transliterate.translit(author, reversed=True)
        except:
            pass
        self.session = requests.Session()
        self.session.headers = {'Accept-Language': 'ru', "Accept": "text/html"}
        res = self.session.get(url=link)
        res.raise_for_status()
        html_offer_page = res.text

        year_of_construction, comm_meters, kitchen_meters, exact_floor, overall_floors = self.parse_page_offer(
            html_offer=html_offer_page)
        print("=>", end="")
        result = {
            "accommodation": self.type_accommodation,
            "how_many_rooms": how_many_rooms,
            "price_per_month": price_per_month,
            # "street": street,
            # "district": district,
            "address": address_long,
            "floor": exact_floor,
            "overall_floors": overall_floors,
            "square_meters": meters,
            "commissions": commissions,
            "author": author,
            "author_type": author_type,
            "docs_checked": docs_checked,
            "year_of_construction": year_of_construction,
            "comm_meters": comm_meters,
            "kitchen_meters": kitchen_meters,
            "link": link
        }
        self.result.append(result)

    def get_results(self):
        return self.result

    def run(self):
        print(f"\n{' ' * 15}Start collecting information from pages..")

        for number_page in range(self.start_page, self.end_page + 1):
            try:
                html = self.load_page(number_page=number_page)
                self.parse_page(html=html, number_page=number_page)
            except Exception as e:
                print(e)
                print(e.with_traceback())
                print(f"This page number {number_page} doesn't exist... Ending parse\n")
                break

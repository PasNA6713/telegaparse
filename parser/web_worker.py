from imports import *


class EndOfPages(Exception):
    pass


def get_url(filter_params={"markets": [], "categories": [], "districts": [], "regions": []}) -> str:
    """create link with accepted filter params"""

    def make_str(data: list, tag: str) -> str:
        result = ""
        for i in data:
            result += f"&{tag}%5B%5D=" + str(i)
        return result

    start_price_from = ""
    start_price_to = ""
    current_price_from = ""
    current_price_to = ""
    search_text = ""
    marketplaces = make_str(filter_params["markets"], "marketplaces")
    categories = make_str(filter_params["categories"], "categorie_childs")
    districts = make_str(filter_params["districts"], "districts")
    regions = make_str(filter_params["regions"], "regions")
    if 'start price' in filter_params.keys():
        start_price_from = filter_params['start price']['from']
        start_price_to = filter_params['start price']['to']
    if 'current price' in filter_params.keys():
        current_price_from = filter_params['current price']['from']
        current_price_to = filter_params['current price']['to']
    if "search text" in filter_params.keys():
        search_text = filter_params['search text']
    print(f"https://торги-россии.рф/search?title_search=&search={search_text}{marketplaces}{categories}{districts}{regions}&trades-sectiont&begin-price-from={start_price_from}&begin-price-to={start_price_to}&current-price-from={current_price_from}&current-price-to={current_price_to}")
    return f"https://торги-россии.рф/search?title_search=&search={search_text}{marketplaces}{categories}{districts}{regions}&trades-section&begin-price-from={start_price_from}&begin-price-to={start_price_to}&current-price-from={current_price_from}&current-price-to={current_price_to}"


@retry(3)
class Url():
    """object for saving current page"""

    def __init__(self, filter_params=None, page=1):
        if filter_params:
            self._link = get_url(filter_params) + f"&page={page}"
        else:
            self._link = get_url() + f"&page={page}"
        page = BS(requests.get(self._link).text, features="lxml")
        pages_num = page.findAll("a", {"class": "page-link"})
        if pages_num:
            self._max_pages = int(pages_num[-2].text)
        else:
            self._max_pages = 0
        self.goods = [i["href"] for i in page.findAll("a", {"class": "lot-description__link"})]

    def __str__(self):
        return self._link

    def __repr__(self):
        return f"{self._link} : {str(self.goods)}"

    def __next__(self):
        last_page = int(self._link.split("=")[-1])
        if last_page < self._max_pages:
            page = last_page + 1
            self._link = self._link.rstrip(str(last_page)) + str(page)
            self.goods = [i["href"] for i in
                          BS(requests.get(self._link).text, features="lxml").findAll("a", {
                              "class": "lot-description__link"})]
            return self
        else:
            raise EndOfPages


@retry(3)
def get_lot_info(url: str) -> dict:
    """generate lot info from it's url"""
    lot = {
        "date": {
            "bidding": "",
            "start_bid": "",
            "end_bid": ""
        },
        "marketplace": {
            "name": "",
            "url": ""
        },
        "description": {
            "title": "",
            "full": ""
        },
        "cost": {
            "current": "",
            "step": "",
            "flag": ""
        },
        "debtor": {
            "full_name": "",
            "inn": "",
            "ogrn": ""
        },
        "organizer": {
            "full_name": "",
            "inn": "",
            "ogrn": "",
            "email": "",
            "phone": ""
        },
        "bidding_type": "",
        "object": "",
        "region": "",
        "state": "",
        "pictures": []
    }

    html = BS(requests.get(url).text, features="lxml")
    header = html.findAll("td", {"class": "lot-summary-table__cell"})
    labels = [i for i in html.findAll("p") if i.find("span", {"class": "param-label"})]
    try:
        debtor = html.find("li", {"id": "debtor-info"}).findAll("p")
    except Exception:
        debtor = []
    try:
        organizer = html.find("li", {"id": "organizer"}).findAll("p")
    except Exception:
        organizer = []

    try:
        flag = html.find('svg', {"class": "lot-cost__img"}).find("use")["xlink:href"]
        if flag == '#up-arrow':
            flag = "up"
        elif flag == '#down-arrow':
            flag = "down"
        elif flag == '#collateral':
            flag = "commercial"
    except Exception:
        flag = ""

    lot["cost"]["flag"] = flag
    lot["cost"]["current"] = html.find("p", {"class": "lot-cost__value"}).text
    lot["description"]["title"] = html.find("h2", {"class": "lot-caption__title js-share-search"}).text

    for i in range(len(header)):
        if header[i].text == "Статус:":
            lot["state"] = header[i + 1].text
        elif header[i].text == "Начало приема ценовых предложений:":
            lot["date"]["bidding"] = header[i + 1].text
        elif header[i].text == "Начало приёма заявок:":
            lot['date']['start_bid'] = header[i + 1].text
        elif header[i].text == "Конец приёма заявок:":
            lot['date']['end_bid'] = header[i + 1].text
        elif header[i].text == "Тип торгов:":
            lot['bidding_type'] = header[i + 1].find("a")["data-tooltip"]
        elif header[i].text == "Площадка:":
            lot['marketplace']['name'] = header[i + 1].text.strip()
            lot['marketplace']['url'] = html.find("a", {"class": "button button--blue"})["href"]

    for i in range(len(labels)):
        if labels[i].find("span", {"class": "param-label"}).text == "Регион:":
            lot["region"] = labels[i].find("span", {"class": "js-share-search"}).text
        elif labels[i].find("span", {"class": "param-label"}).text == "Категория:":
            try:
                lot["object"] = labels[i].find("a").text
            except Exception:
                pass
        elif labels[i].find("span", {"class": "param-label"}).text == "Начальная стоимость:":
            lot["cost"]["current"] = labels[i].find("span", {"class": "js-share-search"}).text
        elif labels[i].find("span", {"class": "param-label"}).text == "Шаг:":
            lot["cost"]["step"] = labels[i].find("span", {"class": "js-share-search"}).text.replace("\xa0", "")
        elif labels[i].find("span", {"class": "param-label"}).text == "Общая информация:":
            lot["description"]["full"] = labels[i].find("span", {"class": "js-share-search"}).text

    for i in debtor:
        if i.find("span", {"class": "param-label"}).text == "Фамилия, имя, отчество:":
            lot["debtor"]["full_name"] = i.find("span", {"class": "js-share-search"}).text.replace("\n", " ").strip()
        elif i.find("span", {"class": "param-label"}).text == "ИНН:":
            lot["debtor"]["inn"] = i.find("span", {"class": "js-share-search"}).text
        elif i.find("span", {"class": "param-label"}).text == "ОГРН:":
            lot["debtor"]["ogrn"] = i.find("span", {"class": "js-share-search"}).text

    for i in organizer:
        if i.find("span", {"class": "param-label"}).text == "Фамилия, имя, отчество:":
            lot["organizer"]["full_name"] = i.find("span", {"class": "js-share-search"}).text
        elif i.find("span", {"class": "param-label"}).text == "ИНН:":
            lot["organizer"]["inn"] = i.find("span", {"class": "js-share-search"}).text
        elif i.find("span", {"class": "param-label"}).text == "ОГРН:":
            lot["organizer"]["ogrn"] = i.find("span", {"class": "js-share-search"}).text
        elif i.find("span", {"class": "param-label"}).text == "e-mail:":
            lot["organizer"]["email"] = i.find("span", {"class": "js-share-search"}).text
        elif i.find("span", {"class": "param-label"}).text == "Телефон:":
            lot["organizer"]["phone"] = i.find("span", {"class": "js-share-search"}).text

    lot["pictures"] = [f"https://xn----etbpba5admdlad.xn--p1ai/{i['data-src']}"
                       for i in html.findAll("img", {"class": "lot-gallery__img owl-lazy"})]
    return lot


class WebWorker:
    """class for working with website"""

    def __init__(self, filter_params: dict = {}):
        if filter_params:
            self._cur_page = Url(filter_params)
        else:
            self._cur_page = Url()
        self._is_page_ends = False

        self._lots = deque(self._cur_page.goods)  # deque of lot's links
        self._lots_info = deque(
            [get_lot_info(self._lots.popleft()) for i in range(4) if self._lots])  # deque of lot's info

    def next_page(self):
        """extend lot's links or toggle self._is_page_ends into true if pages ends"""
        try:
            next(self._cur_page)
            self._lots.extend(self._cur_page.goods)
        except EndOfPages:
            self._is_page_ends = True

    def get_lots_info(self, number_of_lots: int = 4):
        """
        Extend lot's info and call self.next_page() if we have lesser then 25 links in self.lots
        Do nothing if lots and pages ends
        """
        for i in range(number_of_lots):
            if self._lots_info:
                yield self._lots_info.popleft()

                while len(self._lots_info) < number_of_lots * 2:
                    if self._lots:
                        cur_lot = (get_lot_info(self._lots.popleft()))
                        if cur_lot["marketplace"]["url"] != self._lots_info[-1]["marketplace"]["url"]:
                            self._lots_info.append(cur_lot)
                    else:
                        break

                if len(self._lots) < 25 and self._is_page_ends is False:
                    self.next_page()

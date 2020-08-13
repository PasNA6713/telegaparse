from imports import *


class EndOfPages(Exception):
	pass

def _get_url(filter_params = {"markets": [], "categories": [], "districts": [], "regions": []}) -> str:
	def make_str(data: list, tag: str) -> str:
		result = ""
		for i in data:
			result += f"&{tag}%5B%5D=" + str(i)
		return result

	start_price_from = ""
	start_price_to = ""
	current_price_from = ""
	current_price_to = ""
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

	return f"https://торги-россии.рф/search?title_search=&search={marketplaces}{categories}{districts}{regions}&trades-section=bankrupt&begin-price-from={start_price_from}&begin-price-to={start_price_to}&current-price-from={current_price_from}&current-price-to={current_price_to}"


@retry(3)
class _url():
	def __init__(self, filter_params=None, page=1):
		if filter_params:
			self.link = _get_url(filter_params) + f"&page={page}"
		else:
			self.link = _get_url() + f"&page={page}"
		page = BS(requests.get(self.link).text, features="lxml")
		pages_num = page.findAll("a", {"class": "page-link"})
		if pages_num:
			self.max_pages = int(pages_num[-2].text)
		else: self.max_pages = 0
		self.goods = [i["href"] for i in page.findAll("a", {"class": "lot-description__link"})]
        
	def __str__(self):
		return self.link
    
	def __repr__(self):
		return f"{self.link} : {str(self.goods)}"
    
	def __next__(self):
		last_page = int(self.link.split("=")[-1])
		if last_page < self.max_pages:
			page = last_page + 1
			self.link = self.link.rstrip(str(last_page)) + str(page)
			self.goods = [i["href"] for i in BS(requests.get(self.link).text).findAll("a", {"class": "lot-description__link"})]
			return self
		else: raise EndOfPages


@retry(3)
def _get_lot_info(url: str) -> dict:
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
				"step": ""
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

	header = html.findAll("td",{"class": "lot-summary-table__cell"})
	labels = [i for i in html.findAll("p") if i.find("span", {"class": "param-label"})]
	debtor = html.find("li", {"id": "debtor-info"}).findAll("p")
	organizer = html.find("li", {"id": "organizer"}).findAll("p")

	lot["cost"]["current"] = html.find("p", {"class": "lot-cost__value"}).text
	lot["description"]["title"] = html.find("h2", {"class": "lot-caption__title js-share-search"}).text

	for i in range(len(header)):
		if header[i].text=="Статус:":
			lot["state"] = header[i+1].text
		elif header[i].text=="Начало приема ценовых предложений:":
			lot["date"]["bidding"] = header[i+1].text
		elif header[i].text=="Начало приёма заявок:":
			lot['date']['start_bid'] = header[i+1].text
		elif header[i].text=="Конец приёма заявок:":
			lot['date']['end_bid'] = header[i+1].text
		elif header[i].text=="Тип торгов:":
			lot['bidding_type'] = header[i+1].find("a")["data-tooltip"]
		elif header[i].text=="Площадка:":
			lot['marketplace']['name'] = header[i+1].text.strip()
			lot['marketplace']['url'] = html.find("a", {"class": "button button--blue"})["href"]

	for i in range(len(labels)):
		if labels[i].find("span", {"class": "param-label"}).text == "Регион:":
			lot["region"] = labels[i].find("span", {"class": "js-share-search"}).text
		elif labels[i].find("span", {"class": "param-label"}).text == "Категория:":
			try: lot["object"] = labels[i].find("a").text
			except Exception: pass
		elif labels[i].find("span", {"class": "param-label"}).text == "Начальная стоимость:":
			lot["cost"]["current"] = labels[i].find("span", {"class": "js-share-search"}).text
		elif labels[i].find("span", {"class": "param-label"}).text == "Шаг:":
			lot["cost"]["step"] = labels[i].find("span", {"class": "js-share-search"}).text.replace("\xa0","")
		elif labels[i].find("span", {"class": "param-label"}).text == "Общая информация:":
			lot["description"]["full"] = labels[i].find("span", {"class": "js-share-search"}).text

	for i in debtor:
		if i.find("span", {"class": "param-label"}).text == "Фамилия, имя, отчество:":
			lot["debtor"]["full_name"] = i.find("span", {"class": "js-share-search"}).text.replace("\n"," ").strip()
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
			self.cur_page = _url(filter_params)
		else:
			self.cur_page = _url()
		
		self.page_ends = False
		self.lots = deque(self.cur_page.goods) # deque of lot's links
		self.lots_info = deque([_get_lot_info(self.lots.popleft()) for i in range(9) if self.lots]) # deque of lot's info
        

	def next_page(self):
		"""extend lot's links or toggle self.page_ends into true if pages ends"""
		try:
			next(self.cur_page)
			self.lots.extend(self.cur_page.goods)
		except EndOfPages:
			self.page_ends = True

        
	def add_lots_info(self, number_of_lots: int = 4):
		"""
		Extend lot's info and call self.next_page() if we have lesser then 25 links in self.lots
		Do nothing if lots and pages ends
		"""
		result = [_get_lot_info(self.lots.popleft()) for i in range(number_of_lots) if self.lots]
		if len(self.lots) < 25 and self.page_ends is False:
			self.next_page()
		self.lots_info.extend(result)
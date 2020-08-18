from imports import *


class district:
	"""class for saving districk & inner regions"""
	def __init__(self, name: str, code: int, regions: list):
		self.name = name
		self.code = code
		self.regions = regions
    
	def __str__(self):
		return f"{self.name} : {self.code} : {self.regions}"
    
	def __repr__(self):
		return f"{self.name} : {self.code} : {self.regions}"


@retry(3)
def get_dict():
	print("Processing...")
	"""method for getting all filter params from website and saving into .json"""
	categories = {}
	regions = {}
	districts = []
	markets = {}

	"""get categories & marketplaces"""
	for i in BS(requests.get("https://xn----etbpba5admdlad.xn--p1ai/search?title_search=&search=&trades-section=&begin-price-from=&begin-price-to=&current-price-from=&current-price-to=")
					.text, features="lxml").findAll("label", {"class": "checkbox"}):
	   try:
	   	if "category" in i.find("input")["id"]:
	   		categories[i.find("span").text] = i.find("input")["value"]
	   	if "market" in i.find("input")["id"]:
	   		markets[i.find("span").text] = i.find("input")["value"]
	   except Exception: pass
	
	"""get regions & districkts"""
	for i in BS(requests.get("https://xn----etbpba5admdlad.xn--p1ai/search?title_search=&search=&trades-section=&begin-price-from=&begin-price-to=&current-price-from=&current-price-to=")
					.text, features="lxml").findAll("div", {"class": "item"}):
	   if "district" in i.find("input")["id"]:
	      district_code = i.find("input", {"class": "checkbox__input item-checkbox"})["value"]
	      district_name = i.find("div", {"class": "item-header"}).text.strip("\n")
	        
	      cur_regions = []
	      for j in i.findAll("label"):
	      	if "region" in j.find("input")["id"]:
	      		cur_regions.append(int(j.find("input")["value"]))
	      		regions[j.find("span").text] = j.find("input")["value"]
	      districts.append(district(district_name, district_code, cur_regions))

	"""make catalog dict"""
	dictionary = {}
	for i in districts:
		dictionary[i.name] = {"code": i.code, "regions": i.regions}
    
	catalog = {
				"categories": categories, 
            "regions": regions, 
            "districts": dictionary, 
            "markets": markets
            }

	"""save dict into .json"""
	with open("settings.json", 'w') as f:
		json.dump(catalog, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
	get_dict()
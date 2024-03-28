import scrapy
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from scrapy.http import HtmlResponse
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, init
from scrapy import FormRequest
import pdb

HEADERS = {
             "Connection": "keep-alive",
             "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
             "Accept": "application/json, text/javascript, /; q=0.01",
             "X-Requested-With": "XMLHttpRequest",
             "sec-ch-ua-mobile": "?0",
             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",  # noqa
             "Content-Type": "application/x-www-form-urlencoded",
             "Origin": "https://www.darbydental.com",
             "Sec-Fetch-Site": "same-origin",
             "Sec-Fetch-Mode": "cors",
             "Sec-Fetch-Dest": "empty",
             "Referer": "https://www.darbydental.com/DarbyHome.aspx",
             "Accept-Language": "en-US,en;q=0.9",
         }
init()
class Main(scrapy.Spider):
    name = "products"

    def start_requests(self):
        
        # # Set up Chrome options and service
        # chrome_options = webdriver.ChromeOptions()
        # set_trace()
        
        login_url = "https://www.darbydental.com/api/Login/Login"  
        data = {
            "username": "alex@joinordo.com",
            "password": "corp80216",
            "next": ""
        }
       
        
        yield scrapy.FormRequest(url=login_url,formdata=data,headers = HEADERS, callback=self.parse_url)
        
    def parse_url(self,response):
        my_url = response.url
        my_url = my_url.replace('/api/Login/Login','')
        yield scrapy.Request(my_url,callback=self.parse_Catagories)

    def parse_Catagories(self, response):
        
        main_Catagories = response.css(".bigcathover::attr(href)").getall()[1:]  #For Main catagories...
        main_Catagories_title = response.css(".bigcathover::text").getall()[1:]
        
        for link ,title in zip(main_Catagories, main_Catagories_title):
            absolute_url = urljoin(response.url , link)
            
            yield scrapy.Request(absolute_url , callback = self.parse , meta = {
                "CatagoryName" : title.strip().replace('\r\n', ' '),
                "CatagoryURL" : absolute_url})
            # break
    
    def parse(self, response):
        cat_name = response.meta["CatagoryName"]
        cat_url = response.meta["CatagoryURL"]
        products_inside_Catagories = response.css(".card-body.text-center a::attr(href)").getall()
        
        for product_link in products_inside_Catagories:
            absolute_url = urljoin(response.url, product_link)
            yield scrapy.Request(absolute_url , callback = self.product_information_gathering,meta = {
                "CatagoryName":cat_name,
                "CatagoryURL" : cat_url
            })

        NEXT_page = f"https://www.darbydental.com/categories/{cat_name}?filter=Category&filter=Category&filterval={cat_name}&filterval={cat_name}"
        # NEXT_page = f"https://www.darbydental.com/categories/{cat_name}"
        if NEXT_page:
                
                #Get all important data....
                view_State = response.css("input#__VIEWSTATE::attr(value)").get() 
                my_cat_name = response.css("input#Categories2_siteCategories_hfName_0::attr(value)").get()
                cleaning = response.css("input#Categories2_siteCategories_hfName_7::attr(value)").get().replace('\xa0',' ')
                sub_name = response.css("input#Categories2_siteCategories_hfName_14::attr(value)").get().replace('\xa0',' ')
                name1 = response.css("input#Categories2_siteCategories_hfName_21::attr(value)").get().replace('\xa0',' ')
                name2 = response.css("input#Categories2_siteCategories_hfName_28::attr(value)").get().replace('\xa0',' ')
                repair_serv = response.css("input#Categories2_siteCategories_hfName_35::attr(value)").get().replace('\xa0',' ')
                alloys = response.css("input#Categories2_siteCategories_hfName_1::attr(value)").get().replace('\xa0',' ')
                core = response.css("input#Categories2_siteCategories_hfName_8::attr(value)").get().replace('\xa0',' ')
                equipment = response.css("input#Categories2_siteCategories_hfName_15::attr(value)").get().replace('\xa0',' ')
                imp_tray = response.css("input#Categories2_siteCategories_hfName_22::attr(value)").get().replace('\xa0',' ')
                orthodontics = response.css("input#Categories2_siteCategories_hfName_29::attr(value)").get().replace('\xa0',' ')
                retraction_mata = response.css("input#Categories2_siteCategories_hfName_36::attr(value)").get().replace('\xa0',' ')
                asthetics = response.css("input#Categories2_siteCategories_hfName_2::attr(value)").get().replace('\xa0',' ')
                cosmetic_dentistry = response.css("input#Categories2_siteCategories_hfName_9::attr(value)").get().replace('\xa0',' ')
                evacuation = response.css("input#Categories2_siteCategories_hfName_16::attr(value)").get().replace('\xa0',' ')
                infection_control = response.css("input#Categories2_siteCategories_hfName_23::attr(value)").get().replace('\xa0',' ')
                pharmaceutical = response.css("input#Categories2_siteCategories_hfName_30::attr(value)").get().replace('\xa0',' ')
                rubber_dam = response.css("input#Categories2_siteCategories_hfName_37::attr(value)").get().replace('\xa0',' ')
                articulating = response.css("input#Categories2_siteCategories_hfName_3::attr(value)").get().replace('\xa0',' ')
                crowns = response.css("input#Categories2_siteCategories_hfName_10::attr(value)").get().replace('\xa0',' ')
                finishing = response.css("input#Categories2_siteCategories_hfName_17::attr(value)").get().replace('\xa0',' ')
                instruments = response.css("input#Categories2_siteCategories_hfName_24::attr(value)").get().replace('\xa0',' ')
                pin_and_post = response.css("input#Categories2_siteCategories_hfName_31::attr(value)").get().replace('\xa0',' ')
                surgical = response.css("input#Categories2_siteCategories_hfName_38::attr(value)").get().replace('\xa0',' ')
                burs = response.css("input#Categories2_siteCategories_hfName_4::attr(value)").get().replace('\xa0',' ')
                diamonds = response.css("input#Categories2_siteCategories_hfName_11::attr(value)").get().replace('\xa0',' ')
                gloves = response.css("input#Categories2_siteCategories_hfName_18::attr(value)").get().replace('\xa0',' ')
                it_services = response.css("input#Categories2_siteCategories_hfName_25::attr(value)").get().replace('\xa0',' ')
                practice_builder = response.css("input#Categories2_siteCategories_hfName_32::attr(value)").get().replace('\xa0',' ')
                uncatagorixzed = response.css("input#Categories2_siteCategories_hfName_39::attr(value)").get().replace('\xa0',' ')
                cad_and_cam = response.css("input#Categories2_siteCategories_hfName_5::attr(value)").get().replace('\xa0',' ')
                disposable_product = response.css("input#Categories2_siteCategories_hfName_12::attr(value)").get().replace('\xa0',' ')
                handpieces = response.css("input#Categories2_siteCategories_hfName_19::attr(value)").get().replace('\xa0',' ')
                laboratory = response.css("input#Categories2_siteCategories_hfName_26::attr(value)").get().replace('\xa0',' ')
                preventive_product = response.css("input#Categories2_siteCategories_hfName_33::attr(value)").get().replace('\xa0',' ')
                waxes = response.css("input#Categories2_siteCategories_hfName_40::attr(value)").get().replace('\xa0',' ')
                cements = response.css("input#Categories2_siteCategories_hfName_6::attr(value)").get().replace('\xa0',' ')
                emergency_supplies = response.css("input#Categories2_siteCategories_hfName_13::attr(value)").get().replace('\xa0',' ')
                implant_products = response.css("input#Categories2_siteCategories_hfName_20::attr(value)").get()
                matrix = response.css("input#Categories2_siteCategories_hfName_27::attr(value)").get().replace('\xa0',' ')
                refining = response.css("input#Categories2_siteCategories_hfName_34::attr(value)").get().replace('\xa0',' ')
                x_ray = response.css("input#Categories2_siteCategories_hfName_41::attr(value)").get().replace('\xa0',' ')
                view_state_generator = response.css("input#__VIEWSTATEGENERATOR::attr(value)").get().replace('\xa0',' ')
                date = response.css("input#serverTime::attr(value)").get()
                
                my_data = {
                        "ctl00$masterSM": "ctl00$MainContent$UpdatePanel1|ctl00$MainContent$ppager$ctl04$pagelink",
                        "ctl00$logonControl$txtUsername": "alex@joinordo.com",
                        "ctl00$logonControl$txtPassword": "corp80216",
                        "ctl00$ddlPopular": "-1",
                        "ctl00$bigSearchTerm": "",
                        "search_param": "all",
                        "ctl00$Categories2$siteCategories$ctl00$hfName": my_cat_name,
                        "ctl00$Categories2$siteCategories$ctl07$hfName": cleaning,
                        "ctl00$Categories2$siteCategories$ctl14$hfName": sub_name,
                        "ctl00$Categories2$siteCategories$ctl21$hfName": name1,
                        "ctl00$Categories2$siteCategories$ctl28$hfName": name2,
                        "ctl00$Categories2$siteCategories$ctl35$hfName": repair_serv,
                        "ctl00$Categories2$siteCategories$ctl01$hfName": alloys,
                        "ctl00$Categories2$siteCategories$ctl08$hfName": core,
                        "ctl00$Categories2$siteCategories$ctl15$hfName": equipment,
                        "ctl00$Categories2$siteCategories$ctl22$hfName": imp_tray,
                        "ctl00$Categories2$siteCategories$ctl29$hfName": orthodontics,
                        "ctl00$Categories2$siteCategories$ctl36$hfName": retraction_mata,
                        "ctl00$Categories2$siteCategories$ctl02$hfName": asthetics,
                        "ctl00$Categories2$siteCategories$ctl09$hfName": cosmetic_dentistry,
                        "ctl00$Categories2$siteCategories$ctl16$hfName": evacuation,
                        "ctl00$Categories2$siteCategories$ctl23$hfName": infection_control,
                        "ctl00$Categories2$siteCategories$ctl30$hfName": pharmaceutical,
                        "ctl00$Categories2$siteCategories$ctl37$hfName": rubber_dam,
                        "ctl00$Categories2$siteCategories$ctl03$hfName": articulating,
                        "ctl00$Categories2$siteCategories$ctl10$hfName": crowns,
                        "ctl00$Categories2$siteCategories$ctl17$hfName": finishing,
                        "ctl00$Categories2$siteCategories$ctl24$hfName": instruments,
                        "ctl00$Categories2$siteCategories$ctl31$hfName": pin_and_post,
                        "ctl00$Categories2$siteCategories$ctl38$hfName": surgical,
                        "ctl00$Categories2$siteCategories$ctl04$hfName": burs,
                        "ctl00$Categories2$siteCategories$ctl11$hfName": diamonds,
                        "ctl00$Categories2$siteCategories$ctl18$hfName": gloves,
                        "ctl00$Categories2$siteCategories$ctl25$hfName": it_services,
                        "ctl00$Categories2$siteCategories$ctl32$hfName": practice_builder,
                        "ctl00$Categories2$siteCategories$ctl39$hfName": uncatagorixzed,
                        "ctl00$Categories2$siteCategories$ctl05$hfName": cad_and_cam,
                        "ctl00$Categories2$siteCategories$ctl12$hfName": disposable_product,
                        "ctl00$Categories2$siteCategories$ctl19$hfName": handpieces,
                        "ctl00$Categories2$siteCategories$ctl26$hfName": laboratory,
                        "ctl00$Categories2$siteCategories$ctl33$hfName": preventive_product,
                        "ctl00$Categories2$siteCategories$ctl40$hfName": waxes,
                        "ctl00$Categories2$siteCategories$ctl06$hfName": cements,
                        "ctl00$Categories2$siteCategories$ctl13$hfName": emergency_supplies,
                        "ctl00$Categories2$siteCategories$ctl20$hfName": implant_products,
                        "ctl00$Categories2$siteCategories$ctl27$hfName": matrix,
                        "ctl00$Categories2$siteCategories$ctl34$hfName": refining,
                        "ctl00$Categories2$siteCategories$ctl41$hfName": x_ray,
                        "ctl00$alternateSideBar$customLists": "/scripts/productListView.aspx?filter=Category&filterval=Acrylics&customLists=",
                        "ctl00$MainContent$customListsSm":"/scripts/productListView.aspx?filter=Category&filterval=Acrylics&customLists=",
                        "ctl00$MainContent$currentPage": "2",
                        "ctl00$MainContent$pageCount": "20",
                        "ctl00$MainContent$currentSort": "popularity",
                        "ctl00$MainContent$selPerPage": "30",
                        "ctl00$MainContent$sorter": "popularity",
                        "ctl00$serverTime": date,
                        "ctl00$footer$txtContactFullName": "",
                        "ctl00$footer$hfRepEmail": "",
                        "ctl00$footer$txtContactEmail": "",
                        "ctl00$footer$txtContactPhone": "",
                        "ctl00$footer$txtContactCompany": "",
                        "ctl00$footer$ddlContactDepartment": "0",
                        "ctl00$footer$txtContactMessage": "",
                        "g-recaptcha-response": "",
                        "captcha": "",
                        "ctl00$footer$hfCaptcha": "",
                        "__EVENTTARGET": "ctl00$MainContent$ppager$ctl04$pagelink",
                        "__EVENTARGUMENT": "",
                        "__LASTFOCUS": "",
                        "__VIEWSTATE": view_State,
                        "__VIEWSTATEGENERATOR": view_state_generator,
                        
                }
               
                yield scrapy.FormRequest(NEXT_page,callback=self.parse,formdata=my_data,headers=HEADERS, meta = {"CatagoryName": cat_name ,"CatagoryURL":cat_url})
        

    def product_information_gathering(self, response):
        
        # prodLink = response.meta["ProdLink"]
        product_name = response.css("#MainContent_lblName::text").get()
        product_description = response.css("#MainContent_lblDescription > div > p::text").get()
        item_number = response.css("#MainContent_lblItemNo::text").get()
        # product_Url = response.meta["ProductLink"]
        #For Image Url...
        item_number_updated = item_number.replace('-','')
        unknown_sequence = item_number_updated[::-1]
        complex_seq = unknown_sequence[0:4].replace('','/')
        original_url = 'https://storprodwebcontent.blob.core.windows.net/resources/PrintAndWebImages/PrintImages'+complex_seq+''+item_number_updated+'.jpg'
        
        product_price = response.css("span#MainContent_lblPrice::text").get()
        product_price = product_price.split()
        product_price = product_price[2].replace("ea.","")  

        if product_description is None:
            # product_description = f"No Description Available for This Product..."
            product_description = response.css("span#MainContent_lblDescription ::text").get()

        yield {
            "Catagory Information" : response.meta["CatagoryName"],
            # "Product Information Link" : prodLink,
            "Product Name": product_name,
            "Product Description": product_description,
            "Item_Number(Sku)": item_number,
            "Product Image Link": original_url,
            "Product Price": product_price,
            }
        # import pdb
        # pdb.set_trace()
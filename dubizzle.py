import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt 
from datetime import timedelta
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///data.db')

Base = declarative_base()

class property_ad(Base): 
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    scrapping_date =Column(String)
    ad_date_finder=Column(String)
    title_finder=Column(String)
    price_finder=Column(String)
    seller_finder=Column(String)
    city_area_finder=Column(String)
    ad_id_finder=Column(String)
    space_sqm_finder=Column(String)
    prpty_type_finder=Column(String)
    bed_room_finder=Column(String)
    bath_rooms_finder=Column(String)
    furnished_finder=Column(String)
    floor_finder=Column(String)
    payment_method_finder=Column(String)

Base.metadata.create_all(engine)


Session = sessionmaker(bind =engine)
session = Session()



def ad_date_converter(ad_date_finder):
    """ This function takes the string of ad date in the website, compare it to scrapping date, and convert it to date format"""
    splitted = ad_date_finder.split()
    if splitted[2] == "أيام" or 'يوم':
        result = dt.today()-timedelta(days=int(splitted[1]))
    elif splitted[2]== 'أسبوع' or 'أسابيع':
        result = dt.today()-timedelta(weeks=int(splitted[1]))
    elif splitted[2] == 'ساعات' or 'ساعة':
        result = dt.today() - timedelta(hours=splitted[2])
    elif splitted[2] == 'دقائق':
        result = dt.today() - timedelta(minutes=splitted[2])
    return result


def finder(tag_,cls): 
    try:
      result = s.find(tag_,class_=cls).get_text()
    except:
        result = None
    return result


#This function was made to ignore the empty results of some elements in the table of the amenities. 
def nexter(tag_,text_):
    try: 
        result = s.find(tag_,string=text_).find_next_sibling().get_text()
    except:
        result = None
    return result

h = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'}
website = 'https://www.dubizzle.com.eg'
url = 'https://www.dubizzle.com.eg/properties/apartments-duplex-for-rent/?page='

ad_links = []


for page_num in range(1,188):


    page = url+str(page_num)
    #  now the page will be = https://www.dubizzle.com.eg/properties/apartments-duplex-for-rent/?page=[1-189]
    print(f'adding page number {page}')

    # We're requesting the page mentioned before. 
    r = requests.get(page,headers=h).content
    s = BeautifulSoup(r,'html.parser')

    # Finding all the ads_url per page number, teh function find_all will put save them as a list 
    ad_link_finder = s.find_all('div',class_='_9bea76df')
    
    ad_link_finder = s.find_all('div',class_='_9bea76df')

    # looping inside ad_link_finder, then getting the above the tag, since it's without class, then appending in in the ad_links bucket above. 
    ad_finder_looper = [ad_links.append(website+i.find_next('a').get('href')) for i in ad_link_finder]

    for ad in ad_links:
        r = requests.get(ad,headers=h).content
        s = BeautifulSoup(r,'html.parser')
        
        try:
                
            ad_date_finder = s.find('div',class_='_1075545d d059c029 _858a64cf').find_next('div',class_='_1075545d e3cecb8b _5f872d11').find_next('span',class_='_6d5b4928').find_next('span').get_text()

            ad_date = ad_date_converter(ad_date_finder)

            title_finder = finder('h1','a38b8112')
        
            print(f"Now Scrapping: {title_finder}")

            price_finder =int(finder('span','_56dab877').replace(' ج.م','').replace(',',''))
            
            seller_finder = s.find('div',class_='_1075545d _6caa7349 _42f36e3b d059c029').find_next('div',class_='_1075545d _96d4439a').find_next('span',class_='_6d5b4928 be13fe44').get_text()
        
            city_area_finder=s.find('div',class_='_1075545d d059c029 _858a64cf').find_next('div',class_='_1075545d e3cecb8b _5f872d11').find_next('span',class_='_6d5b4928').get_text()
        
            ad_id_finder = s.find('div',class_='_171225da').get_text().replace('رقم الإعلان','')
            
            space_sqm_finder = nexter('span','المساحة (م٢)')
        
            prpty_type_finder = nexter('span','النوع')
        
            bed_room_finder  = nexter('span','غرف نوم')

            bath_rooms_finder = nexter('span','الحمامات')
        
            furnished_finder = nexter('span','مفروش')
        
            floor_finder  = nexter('span','الطابق')

            payment_method_finder = nexter('span','طريقة الدفع')

            property = property_ad(
                scrapping_date = str(dt.today()),
                ad_date_finder = ad_date,
                title_finder=  title_finder,
                price_finder = price_finder,
                seller_finder= seller_finder,
                city_area_finder= city_area_finder,
                ad_id_finder=  ad_id_finder,
                space_sqm_finder= space_sqm_finder,
                prpty_type_finder= prpty_type_finder,
                bed_room_finder=  bed_room_finder,
                bath_rooms_finder= bath_rooms_finder,
                furnished_finder=   furnished_finder,
                floor_finder=  floor_finder,
                payment_method_finder = payment_method_finder,
            )



            session.add(property)
            session.commit()    
        except:
            pass


print('Scrapping process has finished.')
import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt 
import gspread

gc = gspread.service_account('bot_creds.json')
sh = gc.open('Pythoner')



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
# url = 'https://www.dubizzle.com.eg/properties/apartments-duplex-for-sale/alexandria/?page='
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

            

            all_values_row = [
                str(dt.today()),
                ad_date_finder,
                title_finder,
                price_finder,
                seller_finder,
                city_area_finder,
                ad_id_finder,
                space_sqm_finder,
                prpty_type_finder,
                bed_room_finder,
                bath_rooms_finder,
                furnished_finder,
                floor_finder,
                payment_method_finder,
                ]
                

            sh.worksheet('Sheet6').append_row(all_values_row)
        except:
            pass
print('Scrapping process has finished.')
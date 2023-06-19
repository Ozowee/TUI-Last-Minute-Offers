import requests
import time
import json
from discord_webhook import *
from utils import get_proxy,log,log_error,log_error_p,log_info,log_success

offers_file = "pingedoffers.json"

with open("access.json",'r') as accessFile:
    jsonFile = json.load(accessFile)
    WebhookUrlUnder4kPLN = jsonFile['Keys']['WebhookUrlUnder4kPLN']
    WebhookUrlUnder10kPLN = jsonFile['Keys']['WebhookUrlUnder10kPLN']
    WebhookUrlOver10kPLN = jsonFile['Keys']['WebhookUrlOver10kPLN']

def Monitor():
    headers = {
        'Host': 'www.tui.pl',
        'sec-ch-ua': '"Opera GX";v="99", "Chromium";v="113", "Not-A.Brand";v="24"',
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json;charset=UTF-8',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0',
        'x-save': 'true',
        'sec-ch-ua-platform': '"Windows"',
        'Origin': 'https://www.tui.pl',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.tui.pl/last-minute?pm_source=MENU&pm_name=Last_Minute&q=%3AcategoryDESC%3AbyPlane%3AT%3AadditionalType%3AGT03%2523TUZ-LAST25%3AdF%3A6%3AdT%3A14%3ActAdult%3A2%3ActChild%3A0%3AminHotelCategory%3AdefaultHotelCategory%3AtripAdvisorRating%3AdefaultTripAdvisorRating%3Abeach_distance%3AdefaultBeachDistance%3AtripType%3AWS&fullPrice=false',
        'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    json_data = {
        'childrenBirthdays': [],
        'departuresCodes': [],
        'destinationsCodes': [],
        'durationFrom': 6,
        'durationTo': 14,
        'numberOfAdults': 2,
        'offerType': 'BY_PLANE',
        'site': 'last-minute?pm_source=MENU&pm_name=Last_Minute&q=%3AcategoryDESC%3AbyPlane%3AT%3AadditionalType%3AGT03%2523TUZ-LAST25%3AdF%3A6%3AdT%3A14%3ActAdult%3A2%3ActChild%3A0%3AminHotelCategory%3AdefaultHotelCategory%3AtripAdvisorRating%3AdefaultTripAdvisorRating%3Abeach_distance%3AdefaultBeachDistance%3AtripType%3AWS&fullPrice=false',
        'filters': [
            {
                'filterId': 'priceSelector',
                'selectedValues': [],
            },
            {
                'filterId': 'board',
                'selectedValues': [],
            },
            {
                'filterId': 'amountRange',
                'selectedValues': [],
            },
            {
                'filterId': 'minHotelCategory',
                'selectedValues': [
                    'defaultHotelCategory',
                ],
            },
            {
                'filterId': 'tripAdvisorRating',
                'selectedValues': [
                    'defaultTripAdvisorRating',
                ],
            },
            {
                'filterId': 'beach_distance',
                'selectedValues': [
                    'defaultBeachDistance',
                ],
            },
            {
                'filterId': 'facilities',
                'selectedValues': [],
            },
            {
                'filterId': 'WIFI',
                'selectedValues': [],
            },
            {
                'filterId': 'sport_and_wellness',
                'selectedValues': [],
            },
            {
                'filterId': 'room_type',
                'selectedValues': [],
            },
            {
                'filterId': 'room_attributes',
                'selectedValues': [],
            },
            {
                'filterId': 'hotel_chain',
                'selectedValues': [],
            },
            {
                'filterId': 'airport_distance',
                'selectedValues': [],
            },
            {
                'filterId': 'flight_category',
                'selectedValues': [],
            },
            {
                'filterId': 'additionalType',
                'selectedValues': [
                    'GT03#TUZ-LAST25',
                ],
            },
        ],
        'metaData': {
            'page': 0,
            'pageSize': 50,
            'sorting': 'categoryDESC',
        },
    }
    pingedOfferslist = []
    tuiUrl = "https://www.tui.pl"

    while True:
        try:
            response = requests.post('https://www.tui.pl/api/www/search/offers', headers=headers, json=json_data,proxies=get_proxy())
            if response.status_code !=200:
                log_error_p(f"Connection error, status code {response.status_code}")
            else:
                with open(offers_file,'r') as offersFile:
                    offersJSON = json.load(offersFile)
                for offer in response.json()['offers']:
                    offerCode = offer['offerCode']
                    if offerCode not in str(offersJSON['Offers']):
                        data = {
                            "ID":offerCode
                            }
                        offersJSON['Offers'].append(data)
                        log_success("New offer added!")
                        hotelName = offer['hotelName']
                        offerUrl = tuiUrl+offer['offerUrl']
                        hotelStars = str(offer['hotelStandard']).split('.')[0]
                        country = offer['breadcrumbs'][0]['label']
                        offerPricePerPerson = offer['discountPerPersonPrice']
                        departureDate = offer['departureDate']
                        returnDate = offer['returnDate']
                        departureAirport = offer['departureAirport']
                        hotelImage = offer['imageUrl']
                        boardType = offer['boardType']
                        try:
                            tripAdvisorRating = offer['tripAdvisorRating']
                            tripAdvisorReviewsNo = offer['tripAdvisorReviewsNo']
                        except KeyError:
                            tripAdvisorRating = "N/A"
                            tripAdvisorReviewsNo = 0
                        if int(hotelStars)==1:
                            hotelStarsEmote = "⭐"
                        if int(hotelStars)==2:
                            hotelStarsEmote = "⭐⭐"
                        if int(hotelStars)==3:
                            hotelStarsEmote = "⭐⭐⭐"
                        if int(hotelStars)==4:
                            hotelStarsEmote = "⭐⭐⭐⭐"
                        if int(hotelStars)==5:
                            hotelStarsEmote = "⭐⭐⭐⭐⭐"
                        
                        if int(offerPricePerPerson) <= 4000:
                            webhookURL = WebhookUrlUnder4kPLN #do 4k
                        if int(offerPricePerPerson) > 4000 and int(offerPricePerPerson) < 10000:
                            webhookURL = WebhookUrlUnder10kPLN #od 4k
                        if int(offerPricePerPerson) >= 10000:
                            webhookURL = WebhookUrlOver10kPLN #od 10k
                        webhook = DiscordWebhook(url=webhookURL, username ="tui",avatar_url='https://i.imgur.com/RWFzrEi.png',timeout=10)
                        embed = DiscordEmbed(title=f":flag_pl:{departureAirport}->{country}",url=offerUrl, color='0x50d68d')
                        embed.set_image(url=hotelImage)
                        embed.add_embed_field(name='Date:', value=f"{departureDate} - {returnDate}",inline=True)
                        embed.add_embed_field(name=f'Price', value=f"{offerPricePerPerson} zł/os",inline=True)
                        embed.add_embed_field(name=f'Hotel', value=hotelName,inline=True)
                        embed.add_embed_field(name=f'HotelStars:', value=hotelStarsEmote,inline=True)
                        embed.add_embed_field(name='TripAdvisorRating:', value=f'{tripAdvisorRating} [{tripAdvisorReviewsNo} ocen]', inline=True)
                        embed.add_embed_field(name=f'Offer Type:', value=boardType,inline=True)
                        embed.set_footer(text=f'COOKERZY by Rafał#6750',icon_url = 'https://i.imgur.com/RWFzrEi.png')
                        embed.set_timestamp()
                        webhook.add_embed(embed)
                        webhook.execute()
                        log_success("Webhook sent!")
                        time.sleep(1)
                        continue
                    else:
                        log_info("Offer already pinged!")
                        continue
                with open(offers_file,'w') as f:
                    jsonObject = json.dumps(offersJSON,indent=4)
                    f.write(jsonObject)
                log("Sleeping")
                time.sleep(300)
        except requests.ConnectionError:
            log_error_p("Proxy error... waiting 5s")
            time.sleep(5)
            continue
Monitor()

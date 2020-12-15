import requests
import json
import random
import urllib3
urllib3.disable_warnings()


class get_stock():

    def __init__(self):

        # Global settings
        self.base_url = "https://www.packershoes.com"  # Don't add a / at the end

        # Search settings
        self.keywords = ["JACKET", 'BROOKE']  # Seperate keywords with a comma
        self.size = "L"

        # If a size is sold out, a random size will be chosen instead, as a backup plan
        self.random_size = False

        # To avoid a Shopify soft-ban, a delay of 7.5 seconds is recommended if
        # starting a task much earlier than release time (minutes before release)
        # Otherwise, a 1 second or less delay will be ideal
        search_delay = 1

        self.email = 'joemama@gmail.com'
        self.fname = "Bill"
        self.lname = "Nye"
        self.addy1 = "123 Jolly St"
        self.addy2 = ""  # Can be left blank
        self.city = "Toronto"
        self.province = "Ontario"
        self.country = "United States"
        self.postal_code = "M1G1E4"
        self.phone = "4169671111"
        self.card_number = "4510000000000000"  # No spaces
        self.cardholder = "FirstName LastName"
        self.exp_m = "12"  # 2 digits
        self.exp_y = "2017"  # 4 digits
        self.cvv = "666"  # 3 digits






    def get_products(self):
        '''
        Gets all the products from a Shopify site.
        '''
        # Download the products
        link = self.base_url + "/products.json"
        self.s = requests.session()
        r = self.s.get(link, verify=False, proxies=dict(http=f'socks5://p.webshare.io:9999', https=f'socks5://p.webshare.io:9999'))
        self.cookies = self.s.cookies

        # Load the product data
        products_json = json.loads(r.text)
        products = products_json["products"]



        # Return the products
        self.keyword_search(products)


    def keyword_search(self, products):
        '''
        Searches through given products from a Shopify site to find the a product
        containing all the defined keywords.
        '''
        # Go through each product
        for product in products:
            # Set a counter to check if all the keywords are found
            keys = 0
            # Go through each keyword
            for keyword in self.keywords:
                # If the keyword exists in the title
                if(keyword.upper() in product["title"].upper()):
                    # Increment the counter
                    keys += 1
                # If all the keywords were found ----> Continue on
                if(keys == len(self.keywords)):
                    # Return the product
                    print(product)
                    self.find_size(product)



    def find_size(self, product):
        '''
        Find the specified size of a product from a Shopify site.
        '''
        # Go through each variant for the product
        for variant in product["variants"]:
            # Check if the size is found
            # Use 'in' instead of '==' in case the site lists sizes as 11 US
            if(self.size in variant["title"]):
                self.variant = str(variant["id"])

                print(self.variant)
                # Return the variant for the size
                self.URLGen()

        # If the size isn't found but random size is enabled
        if(self.random_size == True):
            # Initialize a list of variants
            variants = []

            # Add all the variants to the list
            for variant in product["variants"]:
                variants.append(variant["id"])
                print(variants)

            # Randomly select a variant
            self.variant = str(random.choice(variants))
            print("Random Size")



            # Return the result
            self.URLGen()

    def URLGen(self):
        self.link = self.base_url + '/cart/' + self.variant + ":1"
        print(self.link)

   



class checkout():

    def __init__(self):
        get_stock.__init__(self)


    def get_payment_token(self):
        '''
        Given credit card details, the payment token for a Shopify checkout is
        returned.
        '''
        # POST information to get the payment token
        link = "https://elb.deposit.shopifycs.com/sessions"

        payload = {
            "credit_card": {
                "number": self.card_number,
                "name": self.cardholder,
                "month": self.exp_m,
                "year": self.exp_y,
                "verification_value": self.cvv
            }
        }

        r = self.s.post(link, json=payload, verify=False, proxies=dict(http=f'socks5://p.webshare.io:9999', https=f'socks5://p.webshare.io:9999'))
        # Extract the payment token
        self.payment_token = json.loads(r.text)["id"]
        self.add_to_cart()

    def add_to_cart(self):
        '''
        Given a session and variant ID, the product is added to cart and the
        response is returned.
        '''
        # Add the product to cart
        link = self.base_url + "/cart/add.js?quantity=1&id=" + self.variant
        response = self.s.get(link, verify=False)
        print(response.text)

        # Return the response
        self.submit_customer_info()

    def submit_customer_info(self):
        '''
        Given a session and cookies for a Shopify checkout, the customer's info
        is submitted.
        '''
        # Submit the customer info
        payload = {
            "utf8": u"\u2713",
            "_method": "patch",
            "authenticity_token": "",
            "previous_step": "contact_information",
            "step": "shipping_method",
            "checkout[email]": self.email,
            "checkout[buyer_accepts_marketing]": "0",
            "checkout[shipping_address][first_name]": self.fname,
            "checkout[shipping_address][last_name]": self.lname,
            "checkout[shipping_address][company]": "",
            "checkout[shipping_address][address1]": self.addy1,
            "checkout[shipping_address][address2]": self.addy2,
            "checkout[shipping_address][city]": self.city,
            "checkout[shipping_address][country]": self.country,
            "checkout[shipping_address][province]": self.province,
            "checkout[shipping_address][zip]": self.postal_code,
            "checkout[shipping_address][phone]": self.phone,
            "checkout[remember_me]": "0",
            "checkout[client_details][browser_width]": "1710",
            "checkout[client_details][browser_height]": "1289",
            "checkout[client_details][javascript_enabled]": "1",
            "button": ""
        }

        link = self.base_url + "//checkout.json"
        response = self.s.get(link, cookies=self.cookies, verify=False)

        # Get the checkout URL
        link = response.url
        checkout_link = link

        # POST the data to the checkout URL
        response = self.s.post(link, cookies=self.cookies, json=payload, verify=False)

        # Return the response and the checkout link
        print(response.text, checkout_link)

        if response.status_code == 200:
            print('Checkout Complete')
            print(response.text)
        else:
            print("Checkout Failed Retrying")
            i = 1
            get_stock()

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

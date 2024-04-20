# Technology website (articals, store, reviews, news)
#### Description: 

	The project in general is a website that serves people in the field of technology by providing them with the latest articles and news and making some reviews of the latest laptops and smartphones, and also the most characteristic of this site is to help visitors find the best offers for laptops and smartphones from Amazon and eBay, let me talk about a picture More detailed information about each section of the site:

	- First the home page contains a random collection of articles, reviews and offers.

	- Second, the articles cover the common technical problems that most people face, and the most important tips for using laptops and smartphones.

	- Third, the reviews focus on covering everything new in the world of technology with a detailed explanation of the most important new features that have been added recently, and I have designed a table dedicated to each product to facilitate understanding and knowledge of the main characteristics of each device.

	- Fourth, I have designed a page to compare smartphones to each other to make it easier for visitors to determine the most appropriate phone for them, by choosing two phones, and then the characteristics of each device are displayed next to the characteristics of the other device to simplify the comparison.
	"http://127.0.0.1:5000/compareReviews/1/Phones/"

	- Fifthly, I designed a page to compare the laptops to each other, where the visitor selects the two devices he wants to compare between them, to facilitate the selection process between the two devices.
	"http://127.0.0.1:5000/compareReviews/3/Laptops/"

	- Sixth, I programmed the administrators' page for adding articles, reviews and products (offers), editing pages, and finally removing pages.

	- Seventh, the login page for site administrators.
	"http://127.0.0.1:5000/login/"

	- Seventh, Contact us page. I wrote a code that receives messages from visitors and sends them to the site's e-mail.
	"http://127.0.0.1:5000/contact/"

	- Finally, the most important and complex sections of the site are the offers section, and it consists of the following:

		1) I designed a custom page to show the offers that were added on the site, and I designed a filter with several variables to make it easier to find the desired product.
		"http://127.0.0.1:5000/offers/"

		2) I designed a special page to add a new offer with a focus only on two stores, Amazon and Ebay.
		"http://127.0.0.1:5000/offers/create/"

		3) Finally, I programmed an algorithm that checks the offers currently added on the site. This algorithm updates the prices of the added products when the verification process begins, and deletes the product if the store runs out of stock. Each store has its own algorithm designed.
		Ebay -> "http://127.0.0.1:5000/checkOffersNow/checkOffersEBay/"
		Amazon.com -> "http://127.0.0.1:5000/checkOffersNow/checkOffersAmazonUSA/"
		Amazon.sa -> "http://127.0.0.1:5000/checkOffersNow/checkOffersAmazonSa/"

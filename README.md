# Online E-commerce Scraping

## Introduction

This project focuses on collecting size charts and body measurements from clothing on various e-commerce websites. The goal is to build a model that, using an image of a person, can estimate the body measurements of that person. This data can help improve the accuracy of size recommendations and provide better shopping experiences for customers.

## Project Structure

```plaintext
./.gitignore
./requirements.txt
./amazon_online_shop_india
./amazon_online_shop_india/amazon_online_shop_india
./amazon_online_shop_india/amazon_online_shop_india/pipelines.py
./amazon_online_shop_india/amazon_online_shop_india/spiders
./amazon_online_shop_india/amazon_online_shop_india/spiders/__init__.py
./amazon_online_shop_india/amazon_online_shop_india/spiders/any_women_clothes_products.py
./amazon_online_shop_india/amazon_online_shop_india/functions.py
./amazon_online_shop_india/amazon_online_shop_india/__init__.py
./amazon_online_shop_india/amazon_online_shop_india/middlewares.py
./amazon_online_shop_india/amazon_online_shop_india/settings.py
./amazon_online_shop_india/amazon_online_shop_india/items.py
./amazon_online_shop_india/scrapy.cfg

./flipkart_shop
./flipkart_shop/flipkart_shop
./flipkart_shop/flipkart_shop/pipelines.py
./flipkart_shop/flipkart_shop/spiders
./flipkart_shop/flipkart_shop/spiders/flipkart_kameez.py
./flipkart_shop/flipkart_shop/spiders/flipkart.py
./flipkart_shop/flipkart_shop/spiders/flipkart_sari.py
./flipkart_shop/flipkart_shop/spiders/__init__.py
./flipkart_shop/flipkart_shop/spiders/flipkart_salwar.py
./flipkart_shop/flipkart_shop/spiders/flipkart_lehenga.py
./flipkart_shop/flipkart_shop/__init__.py
./flipkart_shop/flipkart_shop/middlewares.py
./flipkart_shop/flipkart_shop/settings.py
./flipkart_shop/flipkart_shop/items.py
./flipkart_shop/scrapy.cfg

./hm_online_fashion
./hm_online_fashion/scrapy.cfg
./hm_online_fashion/hm_online_fashion
./hm_online_fashion/hm_online_fashion/pipelines.py
./hm_online_fashion/hm_online_fashion/spiders
./hm_online_fashion/hm_online_fashion/spiders/hm_kids_clothes.py
./hm_online_fashion/hm_online_fashion/spiders/hm_women_clothes.py
./hm_online_fashion/hm_online_fashion/spiders/hm_babies_clothes.py
./hm_online_fashion/hm_online_fashion/spiders/__init__.py
./hm_online_fashion/hm_online_fashion/spiders/hm_men_clothes.py
./hm_online_fashion/hm_online_fashion/__init__.py
./hm_online_fashion/hm_online_fashion/middlewares.py
./hm_online_fashion/hm_online_fashion/settings.py
./hm_online_fashion/hm_online_fashion/items.py
```

## Installation

To set up this project, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/soszaboss/online-shop-data-scraping-with-scrapy.git
    ```

2. Navigate to the project directory:
    ```bash
    cd online-shop-data-scraping-with-scrapy
    ```

3. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Navigate to the project directory:
    ```bash
    cd amazon_online_shop_india
    ```

2. Run the spiders:
    ```bash
    scrapy crawl any_women_clothes_products
    ```

    Similarly, you can navigate to `hm_online_fashion` and run:
    ```bash
    scrapy crawl hm_women_clothes
    ```

## Challenges and Solutions

### Flipkart

**Challenge:** The number of items returned in the search results is inaccurate. After the 25th pagination, no more items are found, even if the site indicates there are more.

**Solution:** 
We created a loop to iterate through the first 25 paginations. The loop is designed to stop if no products are scraped within 60 seconds, ensuring the program doesn't run indefinitely when no more items are available.

### Amazon

**Challenge:** Amazon employs robust anti-bot measures and CAPTCHAs that prevent scraping.

**Solution:**
We use a combination of proxies and fake headers to bypass Amazon's anti-bot systems. This approach helps to simulate genuine user requests, allowing the scraper to collect the necessary data without being blocked.

### H&M

**Challenge:**
    1. Dynamic Content Loading: H&M's website loads products dynamically, which requires careful handling to ensure all products are scraped.
    2. Complex CSS Selectors: Extracting specific elements, such as size charts and body measurements, involves navigating complex CSS selectors and XPaths.

## Contributing

We welcome contributions! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b my-feature-branch`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin my-feature-branch`
5. Submit a pull request.

from crawl4ai import AsyncWebCrawler
from config import Config


async def run_web_crawler():
    # Initialize list to store extracted content
    extracted_contents = []

    # Check if there are URLs to crawl
    if not Config.TARGET_URLS:
        print("No target URLs found in configuration")
        return extracted_contents

    print(f"Starting web crawler for {len(Config.TARGET_URLS)} URLs")

    # Start the async web crawler in headless mode
    async with AsyncWebCrawler(headless=True) as crawler:
        # Loop through each target URL
        for url in Config.TARGET_URLS:
            # Skip empty URLs
            url = url.strip()
            if not url:
                continue

            try:
                print(f"Crawling URL: {url}")

                # Crawl the URL and extract content
                result = await crawler.arun(url=url)

                # Extract cleaned markdown or text content
                if result.success:
                    content = result.markdown or result.cleaned_html or ""
                    extracted_contents.append(content)
                    print(f"Successfully extracted content from {url} ({len(content)} characters)")
                else:
                    print(f"Failed to crawl {url}: {result.error_message}")

            except TimeoutError:
                print(f"Timeout error while crawling {url}")
                continue

            except Exception as e:
                print(f"Error crawling {url}: {str(e)}")
                continue

    print(f"Crawling complete. Extracted content from {len(extracted_contents)} out of {len(Config.TARGET_URLS)} pages")
    return extracted_contents

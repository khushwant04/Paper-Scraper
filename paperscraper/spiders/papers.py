import os
import scrapy

class PapersWithCodeSpider(scrapy.Spider):
    name = "papers"
    allowed_domains = ["paperswithcode.com", "arxiv.org"]
    start_urls = ["https://paperswithcode.com/sota"]

    custom_settings = {
        'CONCURRENT_REQUESTS': 64,  # Number of concurrent requests
        'DOWNLOAD_DELAY': 0.2,       # Delay between requests to avoid overwhelming the server
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,  # Limit concurrent requests per domain
        'CONCURRENT_REQUESTS_PER_IP': 8,       # Limit concurrent requests per IP
    }

    def parse(self, response):
        """
        Parse the State-of-the-Art (SOTA) page to extract links to task pages.
        """
        # Extract task links from different categories (Computer Vision, NLP, etc.)
        task_links = response.css('a[href*="/task/"]::attr(href)').getall()
        
        # Iterate over each task link
        for task_link in task_links:
            task_url = response.urljoin(task_link)
            # Extract the task name from the link to create folders later
            task_name = task_link.split('/')[-1]  # e.g., "decoder", "object-detection"
            # Pass the task name to the next parse method
            yield scrapy.Request(task_url, callback=self.parse_task_page, meta={'task_name': task_name})

    def parse_task_page(self, response):
        """
        Parse the individual task page to extract links to papers.
        """
        task_name = response.meta['task_name']

        # Extract paper links from the task page
        paper_links = response.css('a[href*="/paper/"]::attr(href)').getall()
        
        # Iterate over each paper link
        for paper_link in paper_links:
            paper_url = response.urljoin(paper_link)
            yield scrapy.Request(paper_url, callback=self.parse_paper, meta={'task_name': task_name})

    def parse_paper(self, response):
        """
        Parse the individual paper page to find PDF download links.
        """
        task_name = response.meta['task_name']
        
        # Look for arxiv.org links for PDF
        pdf_link = response.css('a[href*="arxiv.org/pdf"]::attr(href)').get()

        # Fallback to other PDF links on the page if Arxiv isn't available
        if not pdf_link:
            pdf_link = response.css('a:contains("PDF")::attr(href)').get()

        if pdf_link:
            pdf_url = response.urljoin(pdf_link)
            if not self.is_file_downloaded(task_name, pdf_url):
                yield scrapy.Request(pdf_url, callback=self.download_pdf, meta={'task_name': task_name})
            else:
                self.log(f"File already downloaded: {pdf_url}")

    def is_file_downloaded(self, task_name, pdf_url):
        """
        Check if the PDF file has already been downloaded.
        """
        # Create directory based on the task name if it doesn't exist
        folder_path = os.path.join("papers", task_name)
        os.makedirs(folder_path, exist_ok=True)

        # Extract the filename from the URL
        file_name = pdf_url.split('/')[-1] + ".pdf"
        file_path = os.path.join(folder_path, file_name)

        # Check if the file already exists
        return os.path.exists(file_path)

    def download_pdf(self, response):
        """
        Download the PDF file and save it to the appropriate folder based on the task name.
        """
        task_name = response.meta['task_name']

        # Create directory based on the task name if it doesn't exist
        folder_path = os.path.join("papers", task_name)
        os.makedirs(folder_path, exist_ok=True)

        # Extract the filename from the URL
        file_name = response.url.split('/')[-1] + ".pdf"
        file_path = os.path.join(folder_path, file_name)

        # Save the PDF file locally
        with open(file_path, 'wb') as f:
            f.write(response.body)

        self.log(f"Downloaded file {file_name} in {folder_path}")

# Scrapy settings for paperscraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "paperscraper"

SPIDER_MODULES = ["paperscraper.spiders"]
NEWSPIDER_MODULE = "paperscraper.spiders"

# Enable FilesPipeline
ITEM_PIPELINES = {
    'scrapy.pipelines.files.FilesPipeline': 1,
}

# Folder where the PDFs will be stored
FILES_STORE = 'research-papers'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "paperscraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 256  # Increased for better performance

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 0.1  # Reduced delay to 0.5 seconds
RANDOMIZE_DOWNLOAD_DELAY = True  # Randomize download delay

# Enable and configure the AutoThrottle extension (disabled by default)
AUTOTHROTTLE_ENABLED = True  # Enable AutoThrottle
AUTOTHROTTLE_START_DELAY = 0.5  # Initial download delay
AUTOTHROTTLE_MAX_DELAY = 2  # Reduced max download delay for high latencies
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.5  # Target concurrency for requests
AUTOTHROTTLE_DEBUG = True  # Enable throttling stats for debugging

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#     "Accept-Language": "en",
# }

# Enable or disable spider middlewares
# SPIDER_MIDDLEWARES = {
#     "paperscraper.middlewares.PaperscraperSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# DOWNLOADER_MIDDLEWARES = {
#     "paperscraper.middlewares.PaperscraperDownloaderMiddleware": 543,
# }

# Enable or disable extensions
# EXTENSIONS = {
#     "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# ITEM_PIPELINES = {
#     "paperscraper.pipelines.PaperscraperPipeline": 300,
# }

# Enable and configure HTTP caching (disabled by default)
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

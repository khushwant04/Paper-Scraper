# Paper-Scraper

A Scrapy spider that crawls Papers with Code task pages and downloads the linked paper PDFs (usually from arXiv) into one folder per task.

> **Status:** Papers with Code was shut down in 2025, and `paperswithcode.com/sota` now redirects to Hugging Face Papers. The spider's selectors were written for the old site, so the crawl is unlikely to find task pages any more. To reuse the code, point `start_urls` and the CSS selectors at a source that is still live (for example, arXiv listing pages).

## How it works

```
/sota  ->  /task/<task-name>  ->  /paper/<slug>  ->  arxiv.org/pdf/...  ->  papers/<task-name>/<id>.pdf
```

1. `parse`: collects every `/task/` link on the SOTA index.
2. `parse_task_page`: collects `/paper/` links on each task page.
3. `parse_paper`: picks the first `arxiv.org/pdf` link. If there is none, it takes the first link whose text contains "PDF".
4. `download_pdf`: writes the response body to `papers/<task-name>/`. Files that already exist are skipped.

The crawl obeys `robots.txt` and has AutoThrottle enabled. The spider also sets a 0.1 s download delay and caps concurrency at 8 requests per domain.

## Project structure

```
scrapy.cfg
paperscraper/
  settings.py          Throttling, robots.txt, pipelines
  spiders/papers.py    PapersWithCodeSpider (name: "papers")
  items.py, pipelines.py, middlewares.py   Scrapy project boilerplate
```

## Usage

```bash
git clone https://github.com/khushwant04/Paper-Scraper.git
cd Paper-Scraper
pip install -r requirements.txt
scrapy crawl papers
```

PDFs are saved under `./papers/<task-name>/`, which is git-ignored.

## Notes

- `FilesPipeline` and `FILES_STORE = 'research-papers'` are configured in `settings.py`, but the spider never yields items, so the pipeline does nothing. All files are written directly by `download_pdf`.
- The saved filename is the last URL segment plus `.pdf`, so URLs that already end in `.pdf` produce `*.pdf.pdf`.

## Related

- [Research-Papers](https://github.com/khushwant04/Research-Papers): a dataset of 1,296 AI/ML paper PDFs on Hugging Face.

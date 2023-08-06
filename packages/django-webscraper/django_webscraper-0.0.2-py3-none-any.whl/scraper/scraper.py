
import logging
from copy import deepcopy
from typing import Dict, List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from .models import Source

logger = logging.getLogger(__name__)


class BaseScraper:
    """
    1. Get links from main page
    2. For each link:
        a. is it new?
            Yes. Store
            No. Update
    """
    def __init__(self, model):
        self.model = model
        self.base_url = ''  # https://wwf.recruitio.dk
        self.links_path = ''  # job-openings/
        self.url_filters: list = []  # ['uopfordret-ansogning', 'jobagent', '{{result.Url}}']
        self.fields_to_be_scraped: List[str] = ['url', 'title']  # Base fields that always should be scraped

    def _get(self, url: str):
        response = requests.get(url, timeout=60)
        if response.status_code == 404:
            logger.warning(f"URL {url} not found")
            return (b'', response.status_code)
        response.raise_for_status
        return (response.content, response.status_code)

    def _get_consecutive_failed_count(self, link_obj) -> int:
        statuses = link_obj.statuses.all().order_by('-created_at')
        fail_count = 0
        for status in statuses:
            if status.status != 200:
                fail_count += 1
            else:
                # No more consecutive fails
                break
        return fail_count

    def parse_list_of_links(self, html: bytes) -> List[dict]:
        """
        This depends on how we need to implement getting the list of elements
        """
        raise NotImplementedError

    def get_list_of_links(self) -> List[Dict[str, str]]:
        source, source_created = Source.objects.get_or_create(source_url=self.base_url)
        url = urljoin(self.base_url, self.links_path)

        # Get page
        response_content, status_code = self._get(url)

        # Parse document
        result = self.parse_list_of_links(response_content)
        # Use temp copy of result for storing links
        result_copy = deepcopy(result)

        logger.info(f"Found {len(result)} links in source")
        # 1. Store links
        for link in result_copy:
            self.model.objects.update_or_create(
                url=link.pop('url'),
                source=source,
                defaults={
                    **link,
                    'exists_in_source': True,
                }
            )

        # 2. Get all links from DB
        db_links = self.model.objects.filter(source=source, is_disabled=False)
        db_links_new = db_links.filter(statuses=None)
        logger.info(f"{db_links_new.count()} new links")
        # Set db items `exists_in_source` not in current result as False
        db_links.exclude(url__in=[res['url'] for res in result]).update(exists_in_source=False)

        # Get content of each link
        for item in db_links:
            item_result = self.get_single_page(item)
            if item_result['status_code'] == 200:
                item.content = item_result['content']
                item.save()

        return result

    def get_single_page(self, link_obj) -> Dict[str, str]:
        logger.info(f"Get content for {link_obj.url}...")
        result = {}
        response_content, status_code = self._get(link_obj.url)
        result['status_code'] = status_code
        # Save status
        status_obj = link_obj.statuses.create(
            status=result['status_code']
        )
        if status_code == 200:
            # Only parse content is status is ok
            logger.info(f"Parse content for {link_obj.url}...")
            result.update(self.parse_single_page(response_content))
        else:
            # Check how many previous times it has failed
            # If failed X times, disable link
            consecutive_fails = self._get_consecutive_failed_count(link_obj)
            logger.warning(f"Link {link_obj} failed {consecutive_fails} times")
            if consecutive_fails > 5:
                # Disable link for future scrapes
                link_obj.is_disabled = True
                link_obj.disabled_reason = 'Too many failed attempts'
                link_obj.save()
                logger.warning(f"Link {link_obj} disabled for future scrapes")

        return result

    def parse_single_page(self, html):
        raise NotImplementedError


class KattkommandoSydScraper(BaseScraper):
    """
    base_url: domain
    base_url = ''  # https://wwf.recruitio.dk
    links_path = '' # /job-openings/. If empty, you can only scrape a single page
    """
    def __init__(self, model):
        super().__init__(model)
        self.base_url = 'https://kks.nu/'  # https://wwf.recruitio.dk
        self.links_path = 'katt/'  # job-openings/
        # self.url_filters = ['uopfordret-ansogning', 'jobagent', '{{result.Url}}']
        self.fields_to_be_scraped = ['url', 'title']

    def parse_list_of_links(self, html: bytes) -> list:
        soup = BeautifulSoup(html, 'html.parser')
        link_containers = soup.select('div.catarchive-grid-item')
        result = []
        for item in link_containers:
            # Get the link, nothing else
            link_url = item.select_one('header > a')['href']  # type: ignore
            link_text = item.select_one('h2 > a').text.strip()  # type: ignore
            result.append(
                {
                    'url': link_url,
                    'content': link_text
                }
            )
        return result

    def parse_single_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.select_one('header.entry-header').text.strip()  # type: ignore
        body = soup.select_one('div.entry-content').decode_contents()  # type: ignore
        return {'title': title, 'content': body}

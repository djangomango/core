from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse


class PageSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return [
            'page:index',
        ]

    def location(self, item):
        return reverse(item)

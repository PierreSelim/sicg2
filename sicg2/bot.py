"""Bot module who updates the database."""

from argparse import ArgumentParser
import sys
import time

import pywikibot
from pywikibot.pagegenerators import RandomPageGenerator

import pageviewapi.period
from pageviewapi.client import ZeroOrDataNotLoadedException

from logger import logger
from sicg2 import __version__
from database import SicgDB


LOG = logger()
PY3 = sys.version_info >= (3, )


def pageview90(lang, title):
    """Pageviews over the last 90 days on given language of Wikipedia"""
    project = '{lang}.wikipedia'.format(lang=lang)
    page_title = title
    if not PY3:
        page_title = title.encode('utf-8')
    return pageviewapi.period.sum_last(project,
                                       page_title,
                                       last=90,
                                       access='all-access',
                                       agent='all-agents')


def isthereanimage(page):
    """Returns whether there is an image in the article or not."""
    imagepattern = ["<gallery>", "File:", "Image:", ".jpg", ".JPG", ".gif",
                    ".GIF", ".PNG", ".SVG", ".TIF",
                    ".png", ".svg", ".tif", ".jpeg", ".JPEG"]
    text = page.text
    return any(pattern in text for pattern in imagepattern)


def bot(lang='fr'):
    """Bot main loop."""
    start_time = time.time()
    LOG.info('sicg2 v%s started', __version__)
    site = pywikibot.Site(lang, 'wikipedia')
    random_generator = RandomPageGenerator(site=site, namespaces=0)
    LOG.info('Generator: %s', random_generator)
    pages = []
    zerodata = []
    db = SicgDB.get()
    try:
        # Scan of random pages
        for page in random_generator:
            pages.append(page)
            try:
                views = pageview90(lang, page.title())
                if not isthereanimage(page):
                    db.insert(
                        page_title=page.title(),
                        views=views,
                        url=page.full_url())
                    LOG.info('%s %s', page.title(), page)
            except ZeroOrDataNotLoadedException:
                LOG.warning('pageviewapi<404> for %s', page.title())
                zerodata.append(page.title())
    except KeyboardInterrupt:
        end_time = time.time()
        LOG.info('End of analysis: %.3f sec / %d pages / %.3f pages/sec.',
                 end_time - start_time,
                 len(pages),
                 len(pages) / (end_time - start_time))
        LOG.info('Zero data for %d pages (%.3f): %s',
                 len(zerodata),
                 (100. * len(zerodata)) / len(pages),
                 zerodata)


def main():
    """main."""
    description = 'Analyzing Wikipedia to surface image content gap.'
    parser = ArgumentParser(description=description)
    parser.add_argument('-w', '--wikipedia',
                        type=str,
                        dest='lang',
                        required=False,
                        default='fr',
                        help='Language code for Wikipedia')

    args = parser.parse_args()
    kwargs = {
        'lang': args.lang
    }
    bot(**kwargs)


if __name__ == '__main__':
    main()

from .common import InfoExtractor
from ..utils import (
    extract_attributes,
    get_element_html_by_class,
    get_element_html_by_id,
)


class FormulaEIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?fiaformulae\.com/en/video/boxset/player/(?P<id>[0-9]+)\S*'
    _TESTS = [
        {
            'url': 'https://www.fiaformulae.com/en/video/boxset/player/485168/full-race-2014-beijing-e-prix-round-1',

            'md5': '63d2ecad434ff32cacef03a35a9ef025',
            'info_dict': {
                # For videos, only the 'id' and 'ext' fields are required to RUN the test:
                'id': '6341829932112',
                'ext': 'mp4',
                'uploader_id': '6275361344001',
                'title': 'FULL RACE: 2014 Beijing E-Prix, Round 1',
                'upload_date': '20231127',
                'timestamp': 1701077681,
                'duration': 2218.667,
                'tags': [],
                'thumbnail': 'https://resources.formula-e.pulselive.com/formula-e/photo/2023/11/29/60afbb09-3a08-4983-b8ec-1aebd165ca62/RR_S1_BEIIJING.jpg',
                # 'tags': 'season:1,content:registered,label:full-race,content-tag:full-races,content-tag:beijing,video:boxset-season-one,content-tag:boxset,category:racing',
                # Then if the test run fails, it will output the missing/incorrect fields.
                # Properties can be added as:
                # * A value, e.g.
                #     'title': 'Video title goes here',
                # * MD5 checksum; start the string with 'md5:', e.g.
                #     'description': 'md5:098f6bcd4621d373cade4e832627b4f6',
                # * A regular expression; start the string with 're:', e.g.
                #     'thumbnail': r're:^https?://.*\.jpg$',
                # * A count of elements in a list; start the string with 'count:', e.g.
                #     'tags': 'count:10',
                # * Any Python type, e.g.
                #     'view_count': int,

            },
        },
    ]
    BRIGHTCOVE_URL_TEMPLATE = 'http://players.brightcove.net/6275361344001/default_default/index.html?videoId=%s'

    def _real_extract(self, url):
        race_id = self._match_id(url)
        webpage = self._download_webpage(url, race_id)

        thumbnail = self._og_search_thumbnail(webpage)

        videoplayerInstance = extract_attributes(get_element_html_by_id(f'video-player__instance--{race_id}', webpage))
        bc_id = videoplayerInstance.get('data-video-id')
        player_id = videoplayerInstance.get('data-player')

        videoplayer = extract_attributes(get_element_html_by_class('video-player', webpage))
        title = videoplayer.get('data-video-title')

        heroinfoWrapper = extract_attributes(get_element_html_by_class('hero__info-wrapper', webpage))
        date = heroinfoWrapper.get('data-video-date')

        return {
            'uploader_id': player_id,
            'thumbnail': thumbnail,
            'title': title,
            'upload_date': date.replace('-', ''),
            'ie_key': 'BrightcoveNew',
            'id': bc_id,
            '_type': 'url_transparent',
            'url': f'http://players.brightcove.net/6275361344001/default_default/index.html?videoId={bc_id}',
        }

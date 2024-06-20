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
                'tags': list,
                'season': 'Season 1',
                'season_number': 1,
                'thumbnail': 'https://resources.formula-e.pulselive.com/formula-e/photo/2023/11/29/60afbb09-3a08-4983-b8ec-1aebd165ca62/RR_S1_BEIIJING.jpg',
            },
        }, {
            'url': 'https://www.fiaformulae.com/en/video/boxset/player/485337?playlistId=485829',
            'md5': 'a17ab09ec9fa25fada709c962d5c8d1a',
            'info_dict': {
                'id': '6341831037112',
                'ext': 'mp4',
                'uploader_id': '6275361344001',
                'title': 'FULL RACE: 2016 Marrakesh E-Prix, Round 2',
                'upload_date': '20231128',
                'timestamp': 1701079652,
                'duration': 2330.603,
                'tags': list,
                'season': 'Season 3',
                'season_number': 3,
                'thumbnail': 'https://resources.formula-e.pulselive.com/formula-e/photo/2023/11/29/1d5dba68-cc70-40bf-ada4-43e968601554/RR_S3_MARRAKESH.jpg',
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
        tags = videoplayer.get('data-content-tags')
        tags = tags.split(',')

        heroinfoWrapper = extract_attributes(get_element_html_by_class('hero__info-wrapper', webpage))
        date = heroinfoWrapper.get('data-video-date')

        heroVideo = extract_attributes(get_element_html_by_class('hero__video', webpage))
        season = int(heroVideo.get('data-season-tag'))

        return {
            'uploader_id': player_id,
            'thumbnail': thumbnail,
            'title': title,
            'upload_date': date.replace('-', ''),
            'ie_key': 'BrightcoveNew',
            'id': bc_id,
            'tags': tags,
            'season': f'Season {season}',
            'season_number': season,
            '_type': 'url_transparent',
            'url': f'http://players.brightcove.net/6275361344001/default_default/index.html?videoId={bc_id}',
        }

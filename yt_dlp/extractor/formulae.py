import datetime as dt

from .common import InfoExtractor


class FormulaEIE(InfoExtractor):
    # TODO: make boxsets match and work on other languages too
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
    PLAYLIST_URL_TEMPLATE = 'https://api.formula-e.pulselive.com/content/formula-e/playlist/en/%s'
    VIDEO_URL_TEMPLATE = 'https://api.formula-e.pulselive.com/content/formula-e/video/en/%s'

    def _real_extract(self, url):
        data = self._download_json(f'https://api.formula-e.pulselive.com/content/formula-e/video/en/{self._match_id(url)}', self._match_id)
        race_id = self._match_id(url)
        self.to_screen(data)
        title = data.get('title')
        description = data.get('description')
        thumbnail = data.get('imageUrl')
        bc_id = data.get('mediaId')
        # This can fail
        date = dt.datetime.fromisoformat(data.get('date')).strftime('%Y%m%d')

        tags = data.get('tags')
        for tag in tags:
            if tag['label'].startswith('season:'):
                self.to_screen(tag['label'])
                season = tag['label'].split(':')[1]
                season = int(season)

        return {
            'uploader_id': '6275361344001',
            'thumbnail': thumbnail,
            'title': title,
            'upload_date': date.replace('-', ''),
            'ie_key': 'BrightcoveNew',
            'id': race_id,
            'tags': tags,
            'description': description,
            'season': f'Season {season}',
            'thumbnails': [{'url': thumbnail}],
            'season_number': season,
            '_type': 'url_transparent',
            'url': f'http://players.brightcove.net/6275361344001/default_default/index.html?videoId={bc_id}',
        }


class FormulaEPlaylistIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?fiaformulae\.com/en/video/boxset/(?P<id>[0-9]+)\S*'
    _TESTS = [{
        'url': 'https://yourextractor.com/watch/42',
        'md5': 'TODO: md5 sum of the first 10241 bytes of the video file (use --test)',
        'info_dict': {
            # For videos, only the 'id' and 'ext' fields are required to RUN the test:
            'id': '42',
            'ext': 'mp4',
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
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        # TODO: more code goes here, for example ...
        title = self._html_search_regex(r'<h1>(.+?)</h1>', webpage, 'title')

        return {
            'id': video_id,
            'title': title,
            'description': self._og_search_description(webpage),
            'uploader': self._search_regex(r'<div[^>]+id="uploader"[^>]*>([^<]+)<', webpage, 'uploader', fatal=False),
            # TODO: more properties (see yt_dlp/extractor/common.py)
        }

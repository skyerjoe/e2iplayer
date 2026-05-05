# -*- coding: utf-8 -*-
###################################################
# LOCAL import
###################################################
from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import TranslateTXT as _, SetIPTVPlayerLastHostError
from Plugins.Extensions.IPTVPlayer.components.isubprovider import CSubProviderBase, CBaseSubProviderClass
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG, printExc, GetDefaultLang, byteify, RemoveDisallowedFilenameChars, GetSubtitlesDir
from Plugins.Extensions.IPTVPlayer.libs.urlparserhelper import hex_md5
###################################################
from Plugins.Extensions.IPTVPlayer.p2p3.UrlLib import urllib_quote
from Plugins.Extensions.IPTVPlayer.p2p3.pVer import isPY2
from Plugins.Extensions.IPTVPlayer.p2p3.manipulateStrings import strEncode

###################################################
# FOREIGN import
###################################################
import re
try:
    import json
except Exception:
    import simplejson as json
try:
    if isPY2():
        try:
            from cStringIO import StringIO
        except Exception:
            from StringIO import StringIO
    else:
        from io import BytesIO
    import gzip
except Exception:
    pass
from Components.config import config
###################################################
# E2 GUI COMMPONENTS
###################################################

###################################################
# Config options for HOST
###################################################


def GetConfigList():
    optionList = []
    return optionList
###################################################


class OpenSubtitlesRest(CBaseSubProviderClass):

    def __init__(self, params={}):
        self.USER_AGENT = 'IPTVPlayer v1'
        # self.USER_AGENT    = 'Subliminal v0.3'
        self.MAIN_URL = 'https://rest.opensubtitles.org/'
        self.HTTP_HEADER = {'User-Agent': self.USER_AGENT, 'Referer': self.MAIN_URL, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate'}

        params['cookie'] = 'opensubtitlesorg3.cookie'
        CBaseSubProviderClass.__init__(self, params)

        self.defaultParams = {'header': self.HTTP_HEADER, 'ignore_http_code_ranges': [], 'use_cookie': False, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
        self.languages = [{"iso": "af", "id": "afr", "name": "Afrikaans"}, {"iso": "sq", "id": "alb", "name": "Albanian"}, {"iso": "ar", "id": "ara", "name": "Arabic"}, {"iso": "an", "id": "arg", "name": "Aragonese"}, {"iso": "hy", "id": "arm", "name": "Armenian"}, {"iso": "as", "id": "asm", "name": "Assamese"}, {"iso": "ast", "id": "ast", "name": "Asturian"}, {"iso": "ay", "id": "aym", "name": "Aymara"}, {"iso": "az", "id": "aze", "name": "Azerbaijani"}, {"iso": "eu", "id": "baq", "name": "Basque"}, {"iso": "be", "id": "bel", "name": "Belarusian"}, {"iso": "bn", "id": "ben", "name": "Bengali"}, {"iso": "bs", "id": "bos", "name": "Bosnian"}, {"iso": "br", "id": "bre", "name": "Breton"}, {"iso": "bg", "id": "bul", "name": "Bulgarian"}, {"iso": "my", "id": "bur", "name": "Burmese"}, {"iso": "ca", "id": "cat", "name": "Catalan"}, {"iso": "ceb", "id": "ceb", "name": "Cebuano"}, {"iso": "ce", "id": "che", "name": "Chechen"}, {"iso": "zh", "id": "chi", "name": "Chinese"}, {"iso": "cv", "id": "chv", "name": "Chuvash"}, {"iso": "co", "id": "cos", "name": "Corsican"}, {"iso": "hr", "id": "cro", "name": "Croatian"}, {"iso": "cs", "id": "cze", "name": "Czech"}, {"iso": "da", "id": "dan", "name": "Danish"}, {"iso": "nl", "id": "dut", "name": "Dutch"}, {"iso": "en", "id": "eng", "name": "English"}, {"iso": "eo", "id": "epo", "name": "Esperanto"}, {"iso": "et", "id": "est", "name": "Estonian"}, {"iso": "fo", "id": "fao", "name": "Faroese"}, {"iso": "fi", "id": "fin", "name": "Finnish"}, {"iso": "fr", "id": "fre", "name": "French"}, {"iso": "fy", "id": "fry", "name": "Frisian"}, {"iso": "gd", "id": "gla", "name": "Gaelic"}, {"iso": "gl", "id": "glg", "name": "Galician"}, {"iso": "ka", "id": "geo", "name": "Georgian"}, {"iso": "de", "id": "ger", "name": "German"}, {"iso": "el", "id": "gre", "name": "Greek"}, {"iso": "kl", "id": "kal", "name": "Greenlandic"}, {"iso": "gn", "id": "grn", "name": "Guarani"}, {"iso": "gu", "id": "guj", "name": "Gujarati"}, {"iso": "ht", "id": "hat", "name": "Haitian"}, {"iso": "ha", "id": "hau", "name": "Hausa"}, {"iso": "haw", "id": "haw", "name": "Hawaiian"}, {"iso": "he", "id": "heb", "name": "Hebrew"}, {"iso": "hi", "id": "hin", "name": "Hindi"}, {"iso": "hu", "id": "hun", "name": "Hungarian"}, {"iso": "is", "id": "ice", "name": "Icelandic"}, {"iso": "ig", "id": "ibo", "name": "Igbo"}, {"iso": "id", "id": "ind", "name": "Indonesian"}, {"iso": "ia", "id": "ina", "name": "Interlingua"}, {"iso": "ie", "id": "ile", "name": "Interlingue"}, {"iso": "iu", "id": "iku", "name": "Inuktitut"}, {"iso": "ik", "id": "ipk", "name": "Inupiak"}, {"iso": "ga", "id": "gle", "name": "Irish"}, {"iso": "it", "id": "ita", "name": "Italian"}, {"iso": "ja", "id": "jpn", "name": "Japanese"}, {"iso": "jv", "id": "jav", "name": "Javanese"}, {"iso": "kn", "id": "kan", "name": "Kannada"}, {"iso": "ks", "id": "kas", "name": "Kashmiri"}, {"iso": "kk", "id": "kaz", "name": "Kazakh"}, {"iso": "km", "id": "khm", "name": "Khmer"}, {"iso": "rw", "id": "kin", "name": "Kinyarwanda"}, {"iso": "ky", "id": "kir", "name": "Kirghiz"}, {"iso": "rn", "id": "run", "name": "Kirundi"}, {"iso": "ko", "id": "kor", "name": "Korean"}, {"iso": "ku", "id": "kur", "name": "Kurdish"}, {"iso": "lo", "id": "lao", "name": "Laothian"}, {"iso": "la", "id": "lat", "name": "Latin"}, {"iso": "lv", "id": "lav", "name": "Latvian"}, {"iso": "li", "id": "lim", "name": "Limburgian"}, {"iso": "ln", "id": "lin", "name": "Lingala"}, {"iso": "lt", "id": "lit", "name": "Lithuanian"}, {"iso": "lb", "id": "ltz", "name": "Luxembourgish"}, {"iso": "mk", "id": "mac", "name": "Macedonian"}, {"iso": "mg", "id": "mal", "name": "Malagasy"}, {"iso": "ms", "id": "may", "name": "Malay"}, {"iso": "ml", "id": "mal", "name": "Malayalam"}, {"iso": "mt", "id": "mlt", "name": "Maltese"}, {"iso": "mni", "id": "mni", "name": "Manipuri"}, {"iso": "mi", "id": "mao", "name": "Maori"}, {"iso": "mr", "id": "mar", "name": "Marathi"}, {"iso": "mo", "id": "mol", "name": "Moldavian"}, {"iso": "mn", "id": "mon", "name": "Mongolian"}, {"iso": "me", "id": "mne", "name": "Montenegrin"}, {"iso": "ne", "id": "nep", "name": "Nepali"}, {"iso": "no", "id": "nor", "name": "Norwegian"}, {"iso": "oc", "id": "oci", "name": "Occitan"}, {"iso": "or", "id": "ory", "name": "Oriya"}, {"iso": "om", "id": "orm", "name": "Oromo"}, {"iso": "pa", "id": "pan", "name": "Panjabi"}, {"iso": "pap", "id": "pap", "name": "Papiamento"}, {"iso": "fa", "id": "per", "name": "Persian"}, {"iso": "pl", "id": "pol", "name": "Polish"}, {"iso": "pt", "id": "por", "name": "Portuguese"}, {"iso": "ps", "id": "pus", "name": "Pushto"}, {"iso": "qu", "id": "que", "name": "Quechua"}, {"iso": "ro", "id": "rum", "name": "Romanian"}, {"iso": "ru", "id": "rus", "name": "Russian"}, {"iso": "se", "id": "sme", "name": "Sami"}, {"iso": "sm", "id": "smo", "name": "Samoan"}, {"iso": "sg", "id": "sag", "name": "Sango"}, {"iso": "sa", "id": "san", "name": "Sanskrit"}, {"iso": "sc", "id": "srd", "name": "Sardinian"}, {"iso": "sr", "id": "scc", "name": "Serbian"}, {"iso": "sh", "id": "shn", "name": "Shan"}, {"iso": "sn", "id": "sna", "name": "Shona"}, {"iso": "sd", "id": "snd", "name": "Sindhi"}, {"iso": "si", "id": "sin", "name": "Singhalese"}, {"iso": "sk", "id": "slo", "name": "Slovak"}, {"iso": "sl", "id": "slv", "name": "Slovenian"}, {"iso": "so", "id": "som", "name": "Somali"}, {"iso": "es", "id": "spa", "name": "Spanish"}, {"iso": "su", "id": "sun", "name": "Sundanese"}, {"iso": "sw", "id": "swa", "name": "Swahili"}, {"iso": "sv", "id": "swe", "name": "Swedish"}, {"iso": "tl", "id": "tgl", "name": "Tagalog"}, {"iso": "tg", "id": "taj", "name": "Tajik"}, {"iso": "ta", "id": "tam", "name": "Tamil"}, {"iso": "tt", "id": "tat", "name": "Tatar"}, {"iso": "te", "id": "tel", "name": "Telugu"}, {"iso": "th", "id": "tha", "name": "Thai"}, {"iso": "bo", "id": "tib", "name": "Tibetan"}, {"iso": "ti", "id": "tir", "name": "Tigrinya"}, {"iso": "to", "id": "ton", "name": "Tonga"}, {"iso": "ts", "id": "tso", "name": "Tsonga"}, {"iso": "tr", "id": "tur", "name": "Turkish"}, {"iso": "tk", "id": "tuk", "name": "Turkmen"}, {"iso": "tw", "id": "twi", "name": "Twi"}, {"iso": "ug", "id": "uig", "name": "Uighur"}, {"iso": "uk", "id": "ukr", "name": "Ukrainian"}, {"iso": "ur", "id": "urd", "name": "Urdu"}, {"iso": "uz", "id": "uzb", "name": "Uzbek"}, {"iso": "vi", "id": "vie", "name": "Vietnamese"}, {"iso": "vo", "id": "vol", "name": "Volapuk"}, {"iso": "cy", "id": "wel", "name": "Welsh"}, {"iso": "xh", "id": "xho", "name": "Xhosa"}, {"iso": "ji", "id": "yid", "name": "Yiddish"}, {"iso": "yo", "id": "yor", "name": "Yoruba"}, {"iso": "za", "id": "zha", "name": "Zhuang"}, {"iso": "zu", "id": "zul", "name": "Zulu"}]

        self.dInfo = params['discover_info']

    def _cleanSearchString(self, title):
        """
        Clean search string to extract only relevant title parts.
        Removes episode descriptions and translations in parentheses.
        KEEPS season/episode info (S##E##) which is needed for correct results.
        Works for both English and German subtitles.
        
        Example: "Chicago P.D. S05E03: Das Versprechen (The Thing About Heroes)" -> "Chicago P.D. S05E03"
        """
        printDBG("OpenSubtitlesRest._cleanSearchString input[%s]" % title)
        
        # Remove content in parentheses (descriptions, translations)
        cleaned = re.sub(r'\s*\([^)]*\)', '', title)
        
        # Remove everything after colon if it's episode description (but keep S##E## which comes before colon)
        # Pattern: match S##E## optionally, then remove colon and everything after
        if ':' in cleaned:
            # Find if there's a season/episode pattern
            match = re.search(r'([Ss]\d{1,2}[Ee]\d{1,2})', cleaned)
            if match:
                # Keep up to and including the season/episode info
                se_pos = match.end()
                # Find the colon after season/episode
                colon_pos = cleaned.find(':', se_pos)
                if colon_pos != -1:
                    cleaned = cleaned[:colon_pos]
            else:
                # No season/episode found, just split at colon
                cleaned = cleaned.split(':')[0]
        
        # Clean up extra whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        printDBG("OpenSubtitlesRest._cleanSearchString output[%s]" % cleaned)
        return cleaned

    def _searchTMDB(self, title):
        """
        Search TheMovieDB API to bypass IMDB Top 100 ranking limitation.
        Returns list of results with IMDb IDs.
        Supports both movies and TV series.
        """
        printDBG("OpenSubtitlesRest._searchTMDB title[%s]" % title)
        results = []
        
        try:
            # TMDB API search endpoint
            url = "https://api.themoviedb.org/3/search/multi?query=%s&include_adult=false" % urllib_quote(title)
            
            sts, data = self.cm.getPage(url)
            if not sts:
                printDBG("OpenSubtitlesRest._searchTMDB TMDB API failed")
                return results
            
            data = byteify(json.loads(data))
            
            # Extract results
            if 'results' in data:
                count = 0
                for item in data['results']:
                    if count >= 5:  # Limit to 5 results
                        break
                    
                    media_type = item.get('media_type', 'unknown')
                    item_title = item.get('title') or item.get('name', '')
                    year = ''
                    
                    if not item_title:
                        continue
                    
                    if media_type == 'movie':
                        year = item.get('release_date', '')[:4]
                    elif media_type == 'tv':
                        year = item.get('first_air_date', '')[:4]
                    else:
                        continue
                    
                    if year:
                        result_title = "%s %s" % (item_title, year)
                        results.append({
                            'title': result_title,
                            'base_title': item_title,
                            'year': year,
                            'imdbid': ''  # TMDB results need external lookup for IMDB ID
                        })
                        count += 1
        
        except Exception:
            printExc()
        
        printDBG("OpenSubtitlesRest._searchTMDB found %d results" % len(results))
        return results

    def getMoviesTitles(self, cItem, nextCategory):
        printDBG("OpenSubtitlesRest.getMoviesTitles")
        
        # Clean the search string first
        cleaned_title = self._cleanSearchString(self.params['confirmed_title'])
        printDBG("OpenSubtitlesRest.getMoviesTitles cleaned title[%s]" % cleaned_title)
        
        # Try IMDB first
        sts, tab = self.imdbGetMoviesByTitle(cleaned_title)
        if not sts:
            tab = []
        
        printDBG("OpenSubtitlesRest.getMoviesTitles IMDB results count: %d" % len(tab))
        
        # If IMDB returns few results, try TMDB fallback
        if len(tab) < 3:
            printDBG("OpenSubtitlesRest.getMoviesTitles - IMDB insufficient results, trying TMDB fallback")
            tmdb_results = self._searchTMDB(cleaned_title)
            
            # Merge results, avoiding duplicates
            existing_titles = set([item.get('base_title', '').lower() for item in tab])
            for tmdb_item in tmdb_results:
                if tmdb_item.get('base_title', '').lower() not in existing_titles:
                    tab.append(tmdb_item)
                    existing_titles.add(tmdb_item.get('base_title', '').lower())
            
            printDBG("OpenSubtitlesRest.getMoviesTitles merged results count: %d" % len(tab))
        
        printDBG(tab)
        for item in tab:
            params = dict(cItem)
            params.update(item)  # item = {'title', 'imdbid', 'base_title', 'year'}
            params.update({'category': nextCategory})
            self.addDir(params)

        if 0 == len(self.currList):
            self.getLanguages(cItem, 'get_search')

    def getType(self, cItem):
        printDBG("OpenSubtitlesRest.getType")
        imdbid = cItem['imdbid']
        title = cItem['title']
        type = self.getTypeFromThemoviedb(imdbid, title)
        if type == 'series':
            promSeason = self.dInfo.get('season')
            sts, tab = self.imdbGetSeasons(imdbid, promSeason)
            if not sts:
                return
            for item in tab:
                params = dict(cItem)
                params.update({'category': 'get_episodes', 'item_title': cItem['title'], 'season': item, 'title': _('Season %s') % item})
                self.addDir(params)
        elif type == 'movie':
            self.getLanguages(cItem, 'get_search')

    def getEpisodes(self, cItem, nextCategory):
        printDBG("OpenSubtitlesRest.getEpisodes")
        imdbid = cItem['imdbid']
        # itemTitle = cItem['item_title']
        season = cItem['season']

        promEpisode = self.dInfo.get('episode')
        sts, tab = self.imdbGetEpisodesForSeason(imdbid, season, promEpisode)
        if not sts:
            return
        for item in tab:
            params = dict(cItem)
            params.update(item)  # item = "episode_title", "episode", "eimdbid"
            title = 's{0}e{1} {2}'.format(str(season).zfill(2), str(item['episode']).zfill(2), item['episode_title'])
            params.update({'category': nextCategory, 'title': title})
            self.addDir(params)

    def getLanguages(self, cItem, nextCategory):
        printDBG("OpenSubOrgProvider.getLanguages")
        lang = GetDefaultLang()
        tmpList = []

        defaultLanguageItem = None
        engLanguageItem = None
        for item in self.languages:
            params = {'title': '{0} [{1}]'.format(_(item['name']), item['id']), 'search_lang': item['id']}
            if lang == item['iso']:
                defaultLanguageItem = params
            elif 'en' == item['iso']:
                engLanguageItem = params
            else:
                tmpList.append(params)

        if None is not engLanguageItem:
            tmpList.insert(0, engLanguageItem)

        if None is not defaultLanguageItem:
            tmpList.insert(0, defaultLanguageItem)

        # tmpList.insert(0, {'title':_('All'), 'search_lang':''})

        for item in tmpList:
            params = dict(cItem)
            params.update(item)
            params.update({'category': nextCategory})
            self.addDir(params)

    def _getSubtitleTitle(self, item):
        title = item.get('MovieReleaseName', '')
        if '' == title:
            title = item.get('SubFileName', '')
        if '' == title:
            title = item.get('MovieName', '')
        title = '[%s] %s' % (item['ISO639'], title.strip())

        cdMax = item.get('SubSumCD', '1')
        cd = item.get('SubActualCD', '1')
        if cdMax != '1':
            title += ' CD[{0}/{1}]'.format(cdMax, cd)

        # lastTime = item.get('SubLastTS', '')
        # if '' != lastTime: title += ' [{0}]'.format(lastTime)

        return RemoveDisallowedFilenameChars(title)

    def _getFileName(self, subItem):
        title = self._getSubtitleTitle(subItem).replace('_', '.').replace('.' + subItem['SubFormat'], '').replace(' ', '.')
        match = re.search(r'[^.]', title)
        if match:
            title = title[match.start():]

        fileName = "{0}_{1}_0_{2}_{3}".format(title, subItem['ISO639'], subItem['IDSubtitle'], subItem['IDMovieImdb'])
        try:
            fps = float(subItem['MovieFPS'])
            if fps > 0:
                fileName += '_fps{0}'.format(fps)
        except Exception:
            printExc()
        fileName += '.' + subItem['SubFormat']
        return fileName

    def getSearchList(self, cItem):
        printDBG("OpenSubtitlesRest.getSearchList")
        queryTab = []

        langid = cItem.get('search_lang', '')
        imdbid = cItem.get('imdbid', '')
        if imdbid != '':
            queryTab.append('imdbid-%s' % str(imdbid).zfill(7))
        else:
            if 'imdbid' in cItem:
                title = self.imdbGetOrginalByTitle(cItem['imdbid'])[1].get('title', cItem.get('base_title', ''))
            else:
                title = self.params['confirmed_title']
            queryTab.append('query-%s' % urllib_quote(title))

        if langid != '':
            queryTab.append('sublanguageid-%s' % langid)

        if 'season' in cItem and 'episode' in cItem:
            queryTab.append('episode-%s' % cItem['episode'])
            queryTab.append('season-%s' % cItem['season'])

        url = self.getFullUrl('/search/%s/' % ('/'.join(queryTab)))
        sts, data = self.cm.getPage(url, self.defaultParams)
        if not sts:
            return

        subFormats = self.getSupportedFormats(all=True)
        try:
            data = byteify(json.loads(data))
            for item in data:
                link = item.get('SubDownloadLink', '')
                if self.cm.isValidUrl(link) and item.get('SubFormat', '') in subFormats and link.endswith('.gz'):
                    title = self._getSubtitleTitle(item)
                    fileName = self._getFileName(item)
                    try:
                        fps = float(item['MovieFPS'])
                    except Exception:
                        fps = 0
                    params = dict(cItem)
                    params.update({'title': title, 'file_name': fileName, 'lang': item['ISO639'], 'fps': fps, 'encoding': item.get('SubEncoding', ''), 'imdbid': item['IDMovieImdb'], 'url': link})
                    self.addSubtitle(params)
        except Exception:
            printExc()

    def downloadSubtitleFile(self, cItem):
        printDBG("OpenSubtitlesRest.downloadSubtitleFile")
        retData = {}
        title = cItem['title']
        fileName = cItem['file_name']
        baseUrl = cItem['url']
        lang = cItem['lang']
        encoding = cItem['encoding']
        imdbid = cItem['imdbid']
        fps = cItem.get('fps', 0)

        urlParams = dict(self.defaultParams)
        urlParams['max_data_size'] = self.getMaxFileSize()

        login = config.plugins.iptvplayer.opensuborg_login.value
        password = config.plugins.iptvplayer.opensuborg_password.value
        loginUrl = 'http://api.opensubtitles.org/xml-rpc'
        loginData = '''<methodCall>
                         <methodName>LogIn</methodName>
                           <params>
                             <param>
                               <value><string>{0}</string></value>
                             </param>
                             <param>
                               <value><string>{1}</string></value>
                             </param>
                           <param>
                             <value><string>{2}</string></value>
                           </param>
                           <param>
                             <value><string>{3}</string></value>
                           </param>
                         </params>
                       </methodCall>'''

        if baseUrl.startswith('https://'):
            baseUrl = 'http://' + baseUrl.split('://', 1)[-1]

        url = baseUrl
        attempt = 0
        while attempt < 3:
            attempt += 1
            sts, data = self.cm.getPage(url, urlParams)
            if not sts:
                params = dict(self.defaultParams)
                params['raw_post_data'] = True
                post_data = loginData.format(login, hex_md5(password), 'en', self.USER_AGENT)
                sts2, data = self.cm.getPage(loginUrl, params, post_data)
                if sts2:
                    data = self.cm.ph.getDataBeetwenMarkers(data, '<name>token</name>', '</string>', False)[1].rsplit('>', 1)[-1].strip()
                    if data != '':
                        url = baseUrl.replace('/filead/', '/sid-%s/filead/' % data)
                        continue
                if login != '':
                    login = ''
                    password = ''
                    continue
            break

        if not sts:
            SetIPTVPlayerLastHostError(_('Failed to download subtitle.'))
            return retData

        try:
            if isPY2():
                buf = StringIO(data)
            else:
                buf = BytesIO(strEncode(data))
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
        except Exception:
            printExc()
            SetIPTVPlayerLastHostError(_('Failed to gzip.'))
            return retData

        if encoding != '':
            try:
                data = data.decode(encoding).encode('UTF-8')
            except Exception:
                encoding = ''
                printExc()

        filePath = GetSubtitlesDir(fileName)
        if self.writeFile(filePath, data):
            if encoding != '':
                retData = {'title': title, 'path': filePath, 'lang': lang, 'imdbid': imdbid, 'fps': fps}
            elif self.converFileToUtf8(filePath, filePath, lang):
                retData = {'title': title, 'path': filePath, 'lang': lang, 'imdbid': imdbid, 'fps': fps}

        return retData

    def handleService(self, index, refresh=0):
        printDBG('handleService start')

        CBaseSubProviderClass.handleService(self, index, refresh)

        name = self.currItem.get("name", '')
        category = self.currItem.get("category", '')

        printDBG("handleService: name[%s], category[%s] " % (name, category))
        self.currList = []

    # MAIN MENU
        if name is None:
            self.getMoviesTitles({'name': 'category'}, 'get_type')
        elif category == 'get_type':
            # take actions depending on the type
            self.getType(self.currItem)
        elif category == 'get_episodes':
            self.getEpisodes(self.currItem, 'get_languages')
        elif category == 'get_languages':
            self.getLanguages(self.currItem, 'get_search')
        elif category == 'get_search':
            self.getSearchList(self.currItem)

        CBaseSubProviderClass.endHandleService(self, index, refresh)


class IPTVSubProvider(CSubProviderBase):

    def __init__(self, params={}):
        CSubProviderBase.__init__(self, OpenSubtitlesRest(params))

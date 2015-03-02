#!/bin/python
# -*- coding: utf-8 -*-
###############################################################################
#  Connect to game-kouryaku.info to download all the magic news - V1.0        #
#  Copyright 2015 Benito Palacios (aka pleonex)                               #
#                                                                             #
#  Licensed under the Apache License, Version 2.0 (the "License");            #
#  you may not use this file except in compliance with the License.           #
#  You may obtain a copy of the License at                                    #
#                                                                             #
#      http://www.apache.org/licenses/LICENSE-2.0                             #
#                                                                             #
#  Unless required by applicable law or agreed to in writing, software        #
#  distributed under the License is distributed on an "AS IS" BASIS,          #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.   #
#  See the License for the specific language governing permissions and        #
#  limitations under the License.                                             #
###############################################################################

import scrapy

URL = "http://game-kouryaku.info/ninokuni/tuusin"
EXT = ".html"
DATES = ["1012"]


class MagicnewsSpider(scrapy.Spider):
    name = 'magicnews'
    allowed_domains = ['game-kouryaku.info']
    start_urls = [URL + month + EXT for month in DATES]

    def parse(self, response):
        for entry in response.xpath('//p[@class="madou"]'):
            print entry.xpath('span/text()')[0].extract()
            print entry.xpath('text()')[0].extract()
#!/bin/bash

source /home/jules/git/xyz.wallofcode.news.script/webscript_scraper/env/bin/activate
python3 /home/jules/git/xyz.wallofcode.news.script/webscript_scraper/main_scraper.py > ~/scraper.log 2>&1

# ptt_crawler

Crawl titles, date, url of ptt articls based on given keywords.

## Usage
```
python ptt_crawler.py start_day start_year end_day end_year
```
EX:
如果我們要找2017年1月1號到2018年10月11號，那start_day就會是101, start_year就會是2017，
end_day就會是1011, start_year就會是2018.
```
python ptt_crawler.py 101 2017 1011 2018
```

## Input
+ start_day
+ start_year
+ end_day
+ end_year

## Output
+ all_articles.txt
+ 檔案內容格式: date,title,URL

## keywords
1. Find the url of articles include keywords (空汙, 廢氣, 空氣品質, 空氣汙染, PM, PM2.5, 空氣質量, Pm2.5, pm2.5, 霧霾, 霾害) in given time interval.
2. You can augment keywords in line 235.

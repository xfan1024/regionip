# chinaiprange

This project aim to get ip range for country and region from APNIC

## regionip.py exmaple
```shell
python3 regionip.py CN HK MO TW >example/China.txt
python3 regionip.py CN >example/China-mainland.txt
python3 regionip.py JP >example/Japan.txt
python3 regionip.py US AL AK AZ AR CA CO \
                    CT DE FL GA HI ID IL \
                    IN IA KS KY LA ME MD \
                    MA MI MN MS MO MT NE \
                    NV NH NJ NM NY NC ND \
                    OH OK OR PA RI SC SD \
                    TN TX UT VT VA WA WV \
                    WI WY >example/America.txt
python3 regionip.py --exclude CN >example/exclude-China-mainland.txt
```

## china_ip_range.py (deprecated)
```shell
python china_ip_range.py > mainland.cidr
```

# Period Iterator

Period Iterator is a library easing you to iterate through given period.

## Usage

```python
from period_iterator.period_iterator import period_iterator

period = period_iterator('2020-02-01,2020-02-03', 'Asia/Bangkok')

while True:
    print(period.cursor.begin()) # Begin of day
    print(period.cursor.end()) # End of day
    print(period.cursor.date()) # Date
    if not period.next():
        break

# Expected Output
#
# 2020-02-01T00:00:00+07:00
# 2020-02-01T23:59:59+07:00
# 2020-02-01
# 2020-02-02T00:00:00+07:00
# 2020-02-02T23:59:59+07:00
# 2020-02-02
# 2020-02-03T00:00:00+07:00
# 2020-02-03T23:59:59+07:00
# 2020-02-03
```

## License

[MIT](https://github.com/chonla/period-iterator/blob/master/LICENSE)

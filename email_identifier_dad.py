import re, sys, json

sample = "Blvd, Toronto (S) Dec 22 09:00 AM - 10:00 AM Showing DAVID CHAOHONG DONG HOMELIFE LANDMARK REALTY INC. 905-305-1600   /MLS*"

# Phone number regex. Accepts numbers in numerous formats.
phoneRegex = re.compile(r'''(
    (\d{3}|\(\d{3}\))?            # area code
    (\s|-|\.)?                    # separator
    \d{3}                         # first 3 digits
    (\s|-|\.)                     # separator
    \d{4}                         # last 4 digits
    (\s*(ext|x|ext.)\s*\d{2,5})?  # extension
    )''', re.VERBOSE)

# Regex that identifies all-caps sub-strings.
name_company_Regex = re.compile(r'([A-Z]{2,})')

# Regex that identifies the date in the format: Month Day XX:XX AM/PM - XX:XX AM/PM
dateRegex = re.compile(r'''
    (Jan|Feb|Mar|Apr|May|Jun|June|Jul|July|Aug|Sep|Sept|Oct|Nov|Dec)    # month (group 1)
    \s? # optional newline character
    (\d{1,2}) # day of the month (group 2)
    \s
    (\d{2}:\d{2}\s(AM|PM)\s-\s\d{2}:\d{2}\s(AM|PM))
    ''', re.VERBOSE)

# Regex that identifies substring ending with (\w). Will be the address at the beginning of the passed string.
addressRegex = re.compile(r'.+\(.\)')

try:
    data = json.loads(sys.argv[1])
except:
    print("ERROR")
    sys.exit(1)

result = {}


def email_identifier(string):
    caps = name_company_Regex.findall(string)
    caps[:] = [x for x in caps if x != "AM" and x != "PM" and x != "MLS"]
    name = ' '.join(caps[:2])
    company = ' '.join(caps[3:])
    address = addressRegex.search(string).group()
    number = phoneRegex.search(string).group()
    date = dateRegex.search(string).group()
    result["Name: "] = name
    result["Company: "] = company
    result["Address: "] = address
    result["Number: "] = number
    result["Date: "] = date

email_identifier(data)

print(json.dumps(result))



# Example json extraction template 

import requests as req 
import json

f = open("example.json", "r")
data = json.load(f)

print("Example outputs")
print(data["organization"]["city"])
print(data["organization"]["ntee_code"])
print(data["filings_with_data"][0]["totrevenue"])
print("EOF")

f.close()
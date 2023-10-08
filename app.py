from flask import Flask, request
import requests
import json
import re

app = Flask(__name__)
MAX_INT_COMPARISON = 99999999999999999999999999
def_revs = "0," +  str(MAX_INT_COMPARISON)
@app.route('/')
def index():
    return open("template/index.html").read()

def parseDict(list):
    if list == []:
        return "No Data found. Check fields for possible errors"
    outputStr = ""
    for i in list:
        if ord(i["annual_net_revenue"][0]) & ord('N') is not ord('N') and 'gross_revenue' in i.keys():
            str = f"<b>{i['name']}</b> <br/>&nbsp&nbsp&nbsp&nbspEIN: {i['EIN']} <br/>&nbsp&nbsp&nbsp&nbspCity/State: {i['city']}/{i['state']} <br/>&nbsp&nbsp&nbsp&nbspAnnual Revenue: {i['annual_net_revenue']} <br/>&nbsp&nbsp&nbsp&nbspNet Revenue: {i['gross_revenue']}<br/><br/>"
        else:
            str = f"<b>{i['name']}</b> <br/>&nbsp&nbsp&nbsp&nbspEIN: {i['EIN']} <br/>&nbsp&nbsp&nbsp&nbspCity/State: {i['city']}/{i['state']} <br/>&nbsp&nbsp&nbsp&nbspAnnual Revenue: {i['annual_net_revenue']}<br/><br/>"
        outputStr += str
    return outputStr

@app.route('/handle_search', methods=['POST'])
def search_data():
    # Getting inputs from AJAX
    cityName = request.form.get('city_name')
    stateName = request.form.get('state_name')
    grossRev = request.form.get('AGR_name')
    totalRev = request.form.get('ANR_name')
    if grossRev == "":
        grossRev = def_revs
    if totalRev:
        totalRev = def_revs
    
    return parseDict( filter(stateName, cityName, grossRev, totalRev))


# Base URL for Nonprofit Explorer API
BASE_URL = "https://projects.propublica.org/nonprofits/api/v2"


# Function to make the API call
def get_results_from_api(endpoint, params={}):
    response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def Compare(min, max, target):
    if min < target and max > target:
        return True
    return False
    
# Nonprofit Salary Search Function
def search_nonprofit_salaries(stateName=None, cityName=None, minGrossRev=0, maxGrossRev=MAX_INT_COMPARISON, minTotalRev=0, maxTotalRev=MAX_INT_COMPARISON):
    q_param = []
    if cityName:
        q_param.append(cityName)
    params = {
        "q": q_param,
        "formtype": [0,1,2]  # 0 represents Form 990
    }
    if stateName:
        params["state[id]"] = stateName

    results = get_results_from_api("search.json", params)

    nonprofit_details = []
    final_ans = []

     # Process each organization's EIN to fetch detailed data
    for org in results.get("organizations", []):
        ein = org["ein"]
        details = get_results_from_api(f"organizations/{ein}.json")
        # Simplification: extracting only a few fields from the details.
        if len(details['filings_with_data']) > 0:
            extracted_data = {
                "name": details["organization"]["name"],
                "EIN": details["organization"]["ein"],
                "city": details["organization"]["city"],
                "state": details["organization"]["state"],
                "annual_net_revenue": str(details["organization"]["revenue_amount"]),
                "gross_revenue": str(details["filings_with_data"][0]["totrevenue"]),
                "income": details["organization"]["income_amount"],
                "NTEE code": details["organization"]["ntee_code"],
                "data_source": str(details["data_source"])
            }
            nonprofit_details.append(extracted_data)
        else:
            extracted_data = {
                "name": details["organization"]["name"],
                "EIN": details["organization"]["ein"],
                "city": details["organization"]["city"],
                "state": details["organization"]["state"],
                "annual_net_revenue": str(details["organization"]["revenue_amount"]),
                "income": details["organization"]["income_amount"],
                "NTEE code": details["organization"]["ntee_code"],
                "data_source": str(details["data_source"])
            }
            nonprofit_details.append(extracted_data)


    for item in nonprofit_details:
        if "annual_net_revenue" in item.keys() and (ord(item["annual_net_revenue"][0]) & ord('N')) is not ord('N'):
            print("not condition yet")
            print(item["annual_net_revenue"])
            if item["annual_net_revenue"] is None or Compare(minGrossRev, maxGrossRev, int(item["annual_net_revenue"])):
                #print("good annual")
                final_ans.append(item)
        elif "gross_revenue" in item.keys() and not item["gross_net_revenue"] == None:
            #print("not condition yet")
            if item["gross_revenue"] is None or Compare(minTotalRev, maxTotalRev, int(item["annual_net_revenue"])):
                #print("good gross")
                final_ans.append(item)
        else:
            if "gross_revenue" in item.keys() and "annual_net_revenue" in item.keys() and not item["annual_net_revenue"] == None and not item["gross_net_revenue"] == None:
                #print("not condition yet")
                if Compare(minGrossRev, maxGrossRev, int(item["gross_net_revenue"])) and Compare(minTotalRev, maxTotalRev, int(item["annual_net_revenue"])):
                  #print("good both")
                  final_ans.append(item)
    
    return final_ans


def filter(stateName, cityName, grossRev, totalRev):
    minGrossRev, maxGrossRev = 0, MAX_INT_COMPARISON
    minTotalRev, maxTotalRev = 0, MAX_INT_COMPARISON
    if not grossRev == "":
        minGrossRev, maxGrossRev = grossRev.split(',')
    if not totalRev == "":
        minTotalRev, maxTotalRev = totalRev.split(',')
    
    nonprofits = search_nonprofit_salaries(stateName, cityName, int(minGrossRev), int(maxGrossRev), int(minTotalRev), int(maxTotalRev))

    result = [{}]
    for item in nonprofits:
        result.append(item)
    MAX = 15
    if MAX > len(result):
        MAX = len(result)
    if len(result) > 0:
        result = result[1:len(result)]
    return result[0:MAX]


if __name__ == '__main__':
    app.run(debug=True)

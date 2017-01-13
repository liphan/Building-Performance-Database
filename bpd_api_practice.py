import pandas as pd

import json
import requests
import urlparse
import csv
from pandas.io.json import json_normalize
# Inputs
BPD_URL     = "https://bpd-api.lbl.gov"
USER_NAME   = 'liphan.pang@gmail.com'  # Replace with API username (string)
API_KEY     = '96c67bb3-59b8-4da0-baa0-4ac91fc8c3e2'  # Replace with API key      (string)
HEADERS     = {"Content-Type": "application/json",
               "Authorization": "ApiKey {}:{}".format(USER_NAME, API_KEY)}
TIMEOUT     = {"metadata":{"message":"error",
                           "error":"Timeout error"}}
BADGATE     = {"metadata":{"message":"error",
                           "error":"Bad Gateway"}}

assert USER_NAME and API_KEY, "Please initialize with USER_NAME and API_KEY."

# API Interfacing Functions
def rootquery():
    url      = BPD_URL
    response = requests.get(url=url,
                            data=json.dumps({}),
                            headers=HEADERS,
                            verify=True)
    return "{}\n{}".format(response.json()["message"], url)

def fields(payload=None):
    try:
        if payload != None:
            if payload == {}:
                url      = urlparse.urljoin(BPD_URL, "/api/v2/introspection/fields")
                response = requests.get(url)
                return response.json()
            else:
                url      = urlparse.urljoin(BPD_URL, "/api/v2/introspection/fields?{}={}".format(payload.keys()[0], payload[payload.keys()[0]]))
                response = requests.get(url)
                return response.json()
        else: print "ERROR: Incorrect inputs to api function."
    except ValueError: return "Fail: ValueError"

def group_by(payload={}):
    if payload == {}:
        url      = urlparse.urljoin(BPD_URL, "/api/v2/introspection/group_by")
        response = requests.get(url)
        return response.json()
    else:
        url      = urlparse.urljoin(BPD_URL, "/api/v2/introspection/group_by?{}={}".format(payload.keys()[0], payload[payload.keys()[0]]))
        response = requests.get(url)
        return response.json()

def count(filters={}, recalculate=True):
    url      = urlparse.urljoin(BPD_URL, "/api/v2/analyze/count")
    payload  = {"filters": filters,
                "recalculate": recalculate}
    response = requests.post(url=url,
                             data=json.dumps(payload),
                             headers=HEADERS,
                             verify=True)
    return response.json()

def histogram(filters={}, group_by="floor_area", recalculate=True, resolution="high"):
    url      = urlparse.urljoin(BPD_URL, "/api/v2/analyze/histogram")
    payload  = {"filters": filters,
                "group_by": group_by,
                "recalculate": recalculate,
                "resolution": resolution}
    response = requests.post(url=url,
                             data=json.dumps(payload),
                             headers=HEADERS,
                             verify=True)

    if response.status_code == 504: return TIMEOUT
    else:                           return response.json()

def scatterplot(filters={}, xaxis="", yaxis="", addfields=[], limit=1000, seed=""):
    url     = urlparse.urljoin(BPD_URL, "/api/v2/analyze/scatterplot")
    payload = {"filters": filters,
               "additional_fields": addfields,
               "limit": limit}

    if yaxis != "": payload["y-axis"] = yaxis
    if seed != "":  payload["seed"] = seed
    if xaxis != "": payload["x-axis"] = xaxis

    response = requests.post(url=url,
                             data=json.dumps(payload),
                             headers=HEADERS,
                             verify=True)

    if response.status_code == 504: return TIMEOUT
    else:                           return response.json()

def table(filters={}, group_by="floor_area", analyze_by="source_eui", recalculate=True):
    url     = urlparse.urljoin(BPD_URL, "/api/v2/analyze/table")
    payload = {"filters": filters,
               "recalculate": recalculate}

    if analyze_by != "": payload["analyze_by"] = analyze_by
    if group_by != "":   payload["group_by"] = group_by

    response = requests.post(url=url,
                             data=json.dumps(payload),
                             headers=HEADERS,
                             verify=True)

    if response.status_code == 504: return TIMEOUT
    else:                           return response.json()

def comparepeergroup(from_filters, to_filters, analyze_by, base={}, method="actuarial", seed=[], recalculate=True):
    url = urlparse.urljoin(BPD_URL, "/api/v2/analyze/compare/peer-group")

    payload = {"from": from_filters,
               "to": to_filters,
               "analyze_by": analyze_by,
               "base": base,
               "method": method,
               "recalculate": recalculate}

    if seed != []: payload["seed"] = seed

    response = requests.post(url=url,
                             data=json.dumps(payload),
                             headers=HEADERS,
                             verify=True)

    if response.status_code == 504:   return TIMEOUT
    elif response.status_code == 502: return BADGATE
    else:                             return response.json()


""" Test """
#if __name__ == "__main__":
    # When run, the following code should print:
    # BPD 2.0
    # https://bpd-api.lbl.gov
    # success
    # success
    # success
    # success
    # success
    # success
    # success

    #Note: Remove ["metadata"]["message"] to see full object returned.

    # This block runs the introspective functions.
    #print rootquery()
    #print fields(payload={})#["metadata"]["message"]
    # print fields(payload={"field_type":"numerical"})["metadata"]["message"]
    # print group_by(payload={"field_type":"categorical"})["metadata"]["message"]
    #
    # # This block runs example queries for a peer group of Commercial buildings in California.

#peer_group = {"state":["CA"] }
    # print count(filters=peer_group)["metadata"]["message"]
    # print histogram(filters=peer_group,
    #                 group_by=["source_eui"])["metadata"]["message"]
    # print scatterplot(filters=peer_group,
    #                   xaxis="floor_area",
    #                   yaxis="source_eui")["metadata"]["message"]

# r = table(filters=peer_group,group_by=["facility_type","floor_area"],analyze_by="site_eui")#["metadata"]["message"]
# print r["table"]

#https://gist.github.com/amirziai/2808d06f59a38138fa2d

# def flatten_json(y):
#     out = {}
#
#     def flatten_json(row, name=''):
#         if type(row) is dict:
#             for n in row:
#                 flatten_json(row[n], name + n + '_')
#         elif type(row) is list:
#             i = 0
#             for n in row:
#                 flatten_json(n, name + str(i) + '_')
#                 i += 1
#         else:
#             out[str(name[:-1])]= str(row)
#
#     flatten_json(y)
#     return out
#
# flat = json_normalize(flatten_json(r['table']))
#
# with open('mycsvfile.csv', 'wb') as f:
#     w = csv.DictWriter(f, flat.keys())
#     w.writeheader()
#     w.writerow(flat)
#states = ['NY','CA','OR']
states = ['AL','AK','AZ','AR','CA','CO','CT','DC','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA',
            'MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','PR','RI','SC','SD','TN',
            'TX','UT','VA','WA','WV','WI','WY']    # ['GU','VT','VI'] returns error when run: x = r['table'], KeyError: 'table'
#x = r["table"]
for n in states:
    peer_group = {"state":[n] }
    r = table(filters=peer_group,group_by=["facility_type","floor_area"],analyze_by="site_eui")
    x = r['table']
    f = csv.writer(open("%s_facility_area.csv" %n, "wb+"))
    f.writerow(["count", "percentile_0", "facility_type", "floor_area_min", "floor_area_max", "percentile_50",
            "standard_dev",
            "percentile_25", "percentile_75", "percentile_100", "mean"])

    for x in x:

        f.writerow([x["count"],
                x["percentile_0"],
                x["group"][0]["value"],
                x["group"][1]["min"],
                x["group"][1]["max"],
                x["percentile_50"],
                x["standard_deviation"],
                x["percentile_25"],
                x["percentile_75"],
                x["percentile_100"],
                x["mean"]])

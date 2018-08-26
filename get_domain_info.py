#!/usr/bin/env python3
# -*-coding:utf-8 -*-
# Auth: awen
# E-mail:hi@awen.me



import requests
import dns.resolver
import tldextract
import sys
import argparse
import time


def domian_extract(domain):

    source_domain = tldextract.extract(domain)
    if source_domain.subdomain == '':
        domain = "{}.{}".format(source_domain.domain, source_domain.suffix)
    else:
        domain = "{}.{}.{}".format(source_domain.subdomain, source_domain.domain, source_domain.suffix)
    return domain

# Obtain one or more domain name filing information

def get_filing_info(*args):
    if args is not None:
        for list in args:
            for domain in list:
                source_domain = tldextract.extract(domain)
                domain = "{}.{}".format(source_domain.domain, source_domain.suffix)
                get_single_filing_info(domain)

# Get a single domain record information

def get_single_filing_info(domain):

    source_domain = tldextract.extract(domain)
    domain = "{}.{}".format(source_domain.domain, source_domain.suffix)
    url = "https://sapi.k780.com"
    querystring = {"app": "domain.beian", "domain": domain, "appkey": "xxxx",
                   "sign": "xxxxx", "format": "json"}
    headers = {
        'Cache-Control': "no-cache"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    res_json = response.json()
    issuccess = int(res_json['success'])
    isstatus = res_json['result']["status"]

    if issuccess == 1:
        # ALREADY_BEIAN
        if isstatus == "ALREADY_BEIAN":
            print("{}   {}".format(str(domain), "ALREADY_BEIAN"))
        # NOT_BEIAN
        elif isstatus == "NOT_BEIAN":
            print("{}   {}".format(str(domain), "NOT_BEIAN"))
        # WAIT_PROCESS
        elif isstatus == "WAIT_PROCESS":
            print("{}   {}".format(str(domain), "WAIT_PROCESS"))
    # Query failed
    elif issuccess == 0:
        print("Query failed")

# Get A record

def get_record_a(domain):

    try:
        domain = dns.resolver.query(domain, "A")
        iplist = []
        for domain in domain.response.answer:
            for ip in domain.items:
                if ip.rdtype == 1:
                    iplist.append(ip.address)
        return iplist

    except:
        return None

# Get CNAME record

def get_record_cname(domain):

    domian_extract(domain)
    try:
        domain = dns.resolver.query(domain, "CNAME")
        for domain in domain.response.answer:
            for ip in domain.items:
                if ip.rdtype == 5:
                    return ip.to_text()
    except:

        return None

# Get NS record

def get_record_ns(domain):

    domian_extract(domain)

    try:

        domain = dns.resolver.query(domain, "NS")
        for domain in domain.response.answer:
            for ip in domain.items:
                if ip.rdtype == 2:
                    return ip.to_text()
    except:

        return None

# Read domain name from file for filing query

def get_file_filing(file_path):

    if file_path is not None:
        with open(file_path) as f:
            for line in f:
                domain = line.strip("\n")
                source_domain = tldextract.extract(domain)
                domain = "{}.{}".format(source_domain.domain, source_domain.suffix)
                if get_single_filing_info(domain) is True:
                    print("{}   {}".format(str(domain), "ALREADY_BEIAN"))
                else:
                    print("{}   {}".format(str(domain), "NOT_BEIAN"))
    else:
        print("File path cannot be empty")

# Get multiple domain name resolutions as files

def get_record_file(file_path):

    if file_path is not None:
        with open(file_path) as f:
            ip_list = []
            print("{:<30s}{:<30s}{:<30s}{:30s}".format("Domain", "CNAME", "NS", "A"))
            for line in f:
                domain = line.strip("\n")
                domain = domian_extract(domain)
                getcname = get_record_cname(domain)
                getdns = get_record_a(domain)
                getns = get_record_ns(domain)

                if getdns is not None:
                    getdns_str = ",".join(f"{x}" for x in getdns)
                else:
                    getdns = ""

                if getcname is not None:
                    getcname = getcname
                else:
                    getcname = ""

                if getns is not None:
                    getns = getns
                else:
                    getns = ""

                print('{:<30s}{:<30s}{:<30s}{:<30s}'.format(domain, getcname, getns, getdns_str))

                if getdns is not None:
                    ip_list.append(getdns)


            # Formatting to remove duplicate IP
            formatList = []
            for id in ip_list:
                if id not in formatList:
                    formatList.append(id)
            myList = [x for j in formatList for x in j]
            print("=" * 12, "remove duplicates info", "=" * 14)
            print("{}".format(myList))

# Read the domain name from the list for parsing

def get_record_list(*args):
    if args is not None:
        print("{:<30s}{:<30s}{:<30s}{:30s}".format("Domain", "CNAME", "NS", "A"))
        for key in args:
            for line in key:
                domain = line.strip("\n")
                domain = domian_extract(domain)
                getcname = get_record_cname(domain)
                getdns = get_record_a(domain)
                getns = get_record_ns(domain)

                if getdns is not None:
                    getdns = ",".join(f"{x}" for x in getdns)
                else:
                    getdns = ""

                if getcname is not None:
                    getcname = getcname
                else:
                    getcname = ""

                if getns is not None:
                    getns = getns
                else:
                    getns = ""
                print('{:<30s}{:<30s}{:<30s}{:<30s}'.format(domain, getcname, getns, getdns))


# Get the IP address attribution

def get_ip_attribution(*args):
    for i in args:
        for ip in i:
            url = "http://freeapi.ipip.net/" + str(ip)
            headers = {
                'Cache-Control': "no-cache",
            }

            response = requests.request("GET", url, headers=headers)
            if response.status_code == 200:
                resp_json = response.json()
                if resp_json[-1] == '电信/联通/移动':
                    resp_json[-1] = 'BGP 线路'
                return_str =  ",".join(f"{x}" for x in resp_json)
                print(str(ip)+" 归属地是: "+return_str)
                time.sleep(2)


def menu():

    if len(sys.argv) == 1:
        sys.argv.append('--help')
        APP_DESC = """
            This is Get domain info Tools
            """
        print(APP_DESC)
    parser = argparse.ArgumentParser()
    parser.add_argument('-dl', '--domain_list', dest="domain_list", nargs="+",
                        help="Query single or multiple domain name filing information.")
    parser.add_argument('-df', '--domain_file', dest="domain_file",
                        help="Query multiple domain name filing information as files.")
    parser.add_argument('-rl', '--record_list', dest="record_list", nargs="+",
                        help="Query single or multiple domain name resolution.")
    parser.add_argument('-rf', '--record_file', dest="record_file",
                        help="Query multiple domain name resolutions as files.")
    parser.add_argument('-ip', '--ip', dest="ip", nargs="+", help="Query  IP attribution.")
    parser.add_argument('-a', '--auth', dest="auth", help="Show Auth Info.", action="store_true")
    parser.add_argument('-u', '--update', dest="update", help="Update Tools.", action="store_true")
    parser.add_argument('-v', '--version', dest="version", help="Show Version.", action="store_true")
    args = parser.parse_args()

    if args.domain_list:
        get_filing_info(args.domain_list)
    if args.domain_file:
        get_file_filing(args.domain_file)
    if args.record_list:
        get_record_list(args.record_list)
    if args.record_file:
        get_record_file(args.record_file)
    if args.ip:
        get_ip_attribution(args.ip)
    if args.version:
        print("Version:1.0")
    if args.auth:
        print("Auth:awen Email:hi@awen.me")

if __name__ == '__main__':
    menu()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import _config
import dojo
import argparse
import csv
import re

def print_findings(findings):
    def _extract_plugin(path_to_parse):
        if path_to_parse != 'pkgdb':
            m = re.search(r'([\w-]+)\.hpi', path_to_parse)
            if m is not None:
                return m.group(1)
            else:
                return 'core'
        return 'pkgdb or other'

    with open('findings_jira.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_NONE)
        writer.writerow(["Related test, Dojo ID, status, title, cve, jira, sla days, component, component version, file paths, plugin_extract"])
        for finding in findings:

            if re.search(r'^docker\.io', finding['component_name']):
                continue

            sla_days = finding['sla_days_remaining']
            fid = finding['id']
            title = finding['title']
            is_finding_active = finding['active']
            is_finding_mitigated = finding['is_Mitigated']
            is_finding_fp = finding['false_p']
            cve = finding['cve']
            jira = has_jira(fid)
            file_path = finding['file_path']
            component_name = finding['component_name']
            component_version = finding['component_version']
            related_test = finding['test']
            plugin_extract = _extract_plugin(finding['file_path'])

            if args.active_only and is_finding_active == False:
                continue
            # If option is passed, only display the findings with JIRA info
            if args.jira_only and jira is None:
                continue
            elif args.jira_only and jira:
                jira = f"{jira_issue_base_url}/{jira}"
            if is_finding_active:
                finding_status = "Active"
            else:
                finding_status = "Inactive"
            
            writer.writerow([f"{related_test}, {fid}, {finding_status}, {title}, {cve}, {jira}, {sla_days}, {component_name}, {component_version}, {file_path}, {plugin_extract}"])
            print(f"{related_test}, {fid}, {finding_status}, {title}, {cve}, {jira}, {sla_days}, {component_name}, {component_version}, {file_path}, {plugin_extract}")


def has_jira(fid):
    try:
        jira = list(filter(lambda x:x["finding"]==fid, jira_mappings))
        if not jira:
            return
        return jira[0]['jira_key']
    except Exception as e:
        print(f"AH! {e}")

def get_findings_with_jira(findings):
    findings_with_jira = {}
    try:
        for finding in findings:
            fid = finding['id']
            jira = list(filter(lambda x:x["finding"]==fid, jira_mappings))
            if not jira:
                continue
            jira_key = jira[0]['jira_key']
            findings_with_jira[fid] = jira_key
        return findings_with_jira
    except Exception as e:
        print(f"AH! {e}")

def fetch_jira_links():
    print("Fetching JIRA mappings...")
    return dojo_client.get_all_data('jira_finding_mappings')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='List findings SLA.')
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('--jira_only', action='store_true', help='Only consider findings with JIRA link')
    parser.add_argument('--related_findings', action='store_true', help='Get related metadata along with findings')
    parser.add_argument('--active_only', action='store_true', help='Only consider findings that are still active')
    parser.add_argument('dd_entity_id', type=str, help='DefectDojo entity ID (e.g product or engagement ID).')
    group.add_argument('--dd_product', action='store_true', help='Entity to process is a product.')
    group.add_argument('--dd_engagement', action='store_true', help='Entity to process is an engagement.')
    group.add_argument('--dd_test', action='store_true', help='Entity to process is a test.')
    args = parser.parse_args()

    dojo_client = dojo.DojoClient(base_url=_config.dd_api_url, api_key=_config.dd_token)
    jira_issue_base_url = f"{_config.jira_url}/browse"

    query_param = '' 
    if args.related_findings:
        query_param = 'related_fields=true&'
    if args.dd_engagement:
        query_param += 'test__engagement'
    if args.dd_product:
        query_param += 'test__engagement__product'
    if args.dd_test:
        query_param += 'test'
    findings = dojo_client.get_findings_results(query_param, args.dd_entity_id)
    
    jira_mappings = fetch_jira_links()
    print_findings(findings)

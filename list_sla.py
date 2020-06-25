#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import _config
import dojo
import argparse


def print_sla_remaining(findings):
    for finding in findings:
        i_days = finding['sla_days_remaining']
        fid = finding['id']
        ftitle = finding['title']
        is_finding_active = finding['active']
        finding_jira = has_jira(fid)

        if args.active_only and is_finding_active == False:
            continue

        # If option is passed, only display the findings with JIRA info
        if args.jira_only and finding_jira is None:
            continue
        elif args.jira_only and finding_jira:
            finding_jira = f"{jira_issue_base_url}/{finding_jira}"

        finding_status = ""
        if not is_finding_active:
            finding_status = "[INACTIVE] "

        if i_days is not None:
            if i_days > 0:
                print(f"{finding_status}Finding {fid} - {ftitle} ({finding_jira}): Fix due in {i_days} days.")
            elif i_days == 0:
                print(f"{finding_status}Finding {fid} - {ftitle} ({finding_jira}): Fix due today.")
            else:
                print(f"{finding_status}Finding {fid} - {ftitle} ({finding_jira}): SLA breached by {abs(i_days)} days.")

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
    parser.add_argument('--active_only', action='store_true', help='Only consider findings that are still active')
    parser.add_argument('dd_entity_id', type=str, help='DefectDojo entity ID (e.g product or engagement ID).')
    group.add_argument('--dd_product', action='store_true', help='Entity to process is a product.')
    group.add_argument('--dd_engagement', action='store_true', help='Entity to process is an engagement.')
    args = parser.parse_args()

    dojo_client = dojo.DojoClient(base_url=_config.dd_api_url, api_key=_config.dd_token)
    jira_issue_base_url = f"{_config.jira_url}/browse"

    if args.dd_engagement:
        query_param = 'test__engagement'
    if args.dd_product:
        query_param = 'test__engagement__product'
    findings = dojo_client.get_findings_results(query_param, args.dd_entity_id)
    
    jira_mappings = fetch_jira_links()
    print_sla_remaining(findings)

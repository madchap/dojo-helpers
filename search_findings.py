import _config
import dojo
import re
import argparse

def print_component_info(findings, search_pattern):
    for f in findings:
        title = f.get('title')
        cve = f.get('cve') or "No CVE"
        if re.search(rf".*{search_pattern}.*", title, re.IGNORECASE): 
            file_path = f.get('file_path') or "No file path"
            print(f"{title} ({cve}): {file_path}")

def list_tags(findings, search_pattern):
    for f in findings:
        tags = f.get('tags')
        if search_pattern in tags:
            file_path = f.get('file_path') or "No file path"
            cve = f.get('cve') or "No CVE"
            title = f.get('title')
            print(f"{tags} - {title} ({cve}):")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='List file_path for matching findings (based on title), or list findings that have a specific tag.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--do_tag', action='store_true', help='look for a tag')
    group.add_argument('--do_title_search', action='store_true', help='look for a pattern in the title')
    parser.add_argument('dd_engagement', type=str, help='DefectDojo engagement ID. Will process all tests within.')
    parser.add_argument('--title_search_pattern', type=str, help='Pattern to search in findings\' title. Must be specified if --do_title_search')
    parser.add_argument('--tag_name', type=str, help='Exact tag to search for. Must be specified if --do_tag.')
    args = parser.parse_args()

    dojo_client = dojo.DojoClient(base_url=_config.dd_api_url, api_key=_config.dd_token)

    # DefectDojo test to deal with
    dd_engagement = args.dd_engagement

    # use DD true findings json
    all_findings = dojo_client.get_findings_results('test__engagement', dd_engagement)
    
    if args.do_tag:
        list_tags(all_findings, args.tag_name)
    elif args.do_title_search:
        print_component_info(all_findings, args.title_search_pattern)

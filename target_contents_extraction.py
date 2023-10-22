import pandas as pd
import argparse
import datetime
import os
import re

'''INPUT PART'''
parse = argparse.ArgumentParser()
# Required
parse.add_argument('-C', '--CATALOG_FILE', type=str, required=True, help='File contains the list of targets that you want to extract.')
parse.add_argument('-I', '--INPUT_FILE', type=str, required=True, help='File to be extracted.')
parse.add_argument('-O', '--OUTPUT_FILE', type=str, required=True, help='Output file path.')
parse.add_argument('-R', '--REGEX', required=True, help="Regulation expression, format:'exp(target)ression' (' is needed), reference site: https://c.runoob.com/front-end/854/")
# Optional
parse.add_argument('-TR', '--TARGET_REGEX', default=None, help='The regex that extract the part of the content instead the whole line, default is extract whole line.')
parse.add_argument('-CSEP', '--CATALOG_SEPRATE', default='\t', help='The sepration of the catalog file, default if tab.')
parse.add_argument('-CN', '--COL_NUMBER', default=0, help='Target column number of the catalog file, default is 0.')
parse.add_argument('-CH', '--CATALOG_HEADER', type=int, default=None, help='Choose a line as the header line of the catalog file, default is None.')

args = parse.parse_args()
# Required
catalog_fi = args.CATALOG_FILE
fi = args.INPUT_FILE
fo = args.OUTPUT_FILE
regex = args.REGEX
# Optional
target_regex = args.TARGET_REGEX
catalog_sep_sign = args.CATALOG_SEPRATE
col_num = args.COL_NUMBER
catalog_header = args.CATALOG_HEADER

'''MAIN PART'''
# log file, contains all info that extract.
log_fo = os.path.join(os.path.dirname(fo), f'{datetime.date.today()}_log.txt')
log_info = {}

# Extract tagets catalog from the catalog file.
print(f'[*] Extracting catalog info from {os.path.basename(catalog_fi)}...')
df = pd.read_csv(catalog_fi, sep=catalog_sep_sign, header=None)
catalog = df[col_num].to_list()

# log
log_info.setdefault('catalog', [])
log_info['catalog'] = catalog

print(f'[*] Done, total {len(catalog)} targets extracted.')

# Starting extract targets from input file.
print(f'[*] Extracting taget lines from {os.path.basename(fi)}:')

log_line = {}
matched = []
matched_names = []
pattern = re.compile(regex)

matched_num = 0
with open(fi) as filo:
    lines = filo.readlines()
    total_line_num = len(lines)
    for i in range(total_line_num):
        result = pattern.search(lines[i])

        # If regex matched
        if result != None:
            # If name inside the catalog list
            if result.group(1) in catalog and result.group(1) not in matched_names:
                # if target_regex is None, extract whole line
                if target_regex == None:
                    matched.append(lines[i])
                    matched_names.append(result.group(1))
                    log_line.setdefault(i, '')
                    log_line[i] = lines[i]

                    matched_num += 1
                
                else:
                    target_pattern = re.compile(target_regex)
                    target_result = target_pattern.search(lines[i])
                    
                    if target_result != None:
                        matched.append(target_result.group(1))
                        matched_names.append(result.group(1))
                        log_line.setdefault(i, '')
                        log_line[i] = target_result.group(1)

                        matched_num += 1
        
        print(f'\r\tprogress {round(i/total_line_num*100)}%, matched number: {matched_num}', end='')

# log
log_info.setdefault('extracted_targets', [])
log_info['extracted_targets'] = matched_names

log_info.setdefault('extracted_line', [])
log_info['extracted_contents'] = log_line

print(f'\n[*] Done, total {len(matched)} lines extracted.')

# Generate output file
print(f'[*] Generating output file: {os.path.basename(fo)}...')
with open(fo, 'w') as out:
    for line in matched:
        line = line.replace('\n', '')
        out.write(f"{line}\n")

# Generate log file
with open(log_fo, 'w') as out:
    # Catalog
    out.write(f'Catalog({len(log_info["catalog"])}), {catalog_fi}\n')
    for target in log_info['catalog']:
        out.write(f'{target}\n')

    out.write('-'*72)
    
    # Input file
    out.write(f'\nInput, {fi}\n')

    out.write(f'Name lists({len(log_info["extracted_targets"])}):\n')
    for name in log_info['extracted_targets']:
        out.write(f'{name}\n')
    
    out.write(f"\ncontents({len(log_info['extracted_contents'].keys())}):\n")
    for line_num, line in log_info['extracted_contents'].items():
        out.write(f'{line_num} - {line}\n')

print(f'[*] Done.')

import csv
from collections import defaultdict
from os import listdir, popen
from os.path import isfile, join
from typing import Any, Dict, List, Optional, Tuple

import vcf


def binary_search(sorted_list: List[Tuple[int, int]], value: int, find_min: bool, start_idx: Optional[int] = 0) -> Optional[int]:
    # if our start position is greater than the last (highest) number in the sorted list
    if find_min and sorted_list[-1][0] < value:
        return None
    # if our end position is less than the first (lowest) number in the sorted list
    if not find_min and sorted_list[0][0] > value:
        return None

    low = max(0, start_idx)
    high = len(sorted_list) - 1

    while low <= high:
        mid = low + ((high - low)//2)  # // means chop off remainder, keep it an integer
        if sorted_list[mid][0] > value:
            high = mid - 1
        elif sorted_list[mid][0] == value:
            if find_min:
                high = mid - 1
            else:
                low = mid + 1
        else:
            low = mid + 1

    if find_min:
        return high if high >= 0 and sorted_list[high][0] == value else high + 1
    else:
        return low if low < len(sorted_list) and sorted_list[low][0] == value else low - 1


def test_b2_search():
    a = [(159045460, 138345), (159049511, 188427), (159051716, 2039), (159051718, 81668), (159051781, 140760), (159054878, 66455),
         (159062694, 182321), (159062696, 150191), (159062696, 165091), (159063588, 148002), (159065985, 2040), (159073251, 2041),
         (159073406, 143388), (159171798, 87410), (159171834, 161136)]
    assert binary_search(a, value=159062696, find_min=True) == 7
    assert binary_search(a, value=159062696, find_min=False) == 8


def test_b_search():
    a = [(1, 0), (2, 0), (4, 0), (4, 0), (5, 0), (8, 0), (12, 0), (15, 0), (15, 0), (23, 0), (54, 0)]
    assert binary_search(a, 3, find_min=True) == 2  # 3 is bigger than 2, less than 4, so 4 (at index 2) should return if looking for min
    assert binary_search(a, 3, find_min=False) == 1  # 3 is bigger than 2, less than 4, so 2 (at index 1) should return if looking for max
    assert binary_search(a, a[0][0] - 1, find_min=True) == 0  # number smaller than all numbers in list, so return first (0) index
    assert binary_search(a, a[-1][0] + 1, find_min=True) is None  # number bigger than all numbers in list, so return None
    assert binary_search(a, a[-1][0] + 1, find_min=False) == len(a) - 1
    assert binary_search(a, a[0][0] - 1, find_min=False) is None
    # test exact match
    assert binary_search(a, 8, find_min=True) == 5
    assert binary_search(a, 8, find_min=False) == 5
    # test the start index
    assert binary_search(a, 10, find_min=True) == 6
    assert binary_search(a, 10, find_min=True, start_idx=3) == 6
    assert binary_search(a, 10, find_min=True, start_idx=6) == 6
    assert binary_search(a, 10, find_min=True, start_idx=7) == 7


test_b_search()  # run test
test_b2_search()


def format_variant_file() -> Tuple[Dict[Any, List], List[Dict[str, Any]]]:
    with open("/home/mcarruth/Downloads/WES_all_variants.csv") as f:
        var_data: List = f.readlines()  # each row now an item in list
        print(f'{len(var_data)} variants found to be examined')

    pos_dict: Dict[Any, List] = {}
    result_list = []
    for i, row in enumerate(var_data[1:]):  # skip header row
        # we will enumerate here to keep track of i, the row number in the original list
        chromosome, pos, ref, *alt = row.split(',')  # * means "all the rest", have to use that since ALT column contains comma
        joined_alt = ",".join(alt).lstrip('"').rstrip('"\n')  # put the ALT back together, and strip out the newline
        result_list.append({"CHROM": chromosome, "POS": pos, "REF": ref, "ALT": joined_alt, "patients": defaultdict(dict)})

        # check if we're already seen this chrom, if not, create a new entry
        if chromosome not in pos_dict:
            pos_dict[chromosome] = [(int(pos), i)]
        else:  # add this position to the already existing list
            pos_dict[chromosome].append((int(pos), i))
    print(f'{len(pos_dict)} chromosomes found: {sorted(list(pos_dict.keys()))}')
    return pos_dict, result_list


def sort_positions(unsorted_positions) -> None:
    for pos in unsorted_positions.values():  # look at all the lists of positions
        # sort based on the first number, which is the position (i, the original row number, is the second number)
        # sorting will come in handy later b/c we will be able to use binary search
        pos.sort(key=lambda entry: entry[0])


def read_patient_file(filepath: str) -> Tuple[vcf.Reader, int]:
    print(f"reading patient file {filepath}")
    line_count = popen(f'wc -l {filepath}').read()
    est_lines = float(line_count.split()[0]) * 16.67  # rough guess for compression
    return vcf.Reader(filename=filepath, compressed=True), int(est_lines)


def log_milestone(num_lines_read: int, est_total: int, milestones_seen: List, patient_filename: str):
    percent_complete = num_lines_read*100//est_total
    if percent_complete % 25 == 0 and percent_complete not in milestones_seen:
        print(f'Now {percent_complete}% complete reading file {patient_filename}, read {num_lines_read} records of estimated {est_total}')
        milestones_seen.append(percent_complete)  # DRY


def pull_info_from_record(record_in_question, sample_name):
    # print(f'        reading {record} {record.INFO}')
    try:
        chromosome = record_in_question.CHROM
        genotype_str = record_in_question.genotype(sample_name)['GT']  # or record_in_question.samples[0].data.GT
        starting_pos = record_in_question.POS
        ending_pos = record_in_question.INFO['END'] if 'END' in record_in_question.INFO else record_in_question.end
        return chromosome, genotype_str, starting_pos, ending_pos
    except Exception:
        raise RuntimeError(f'error reading record: {record_in_question}')


def does_record_match_alleles(vcf_record, varient_entry: Dict) -> bool:
    if vcf_record.REF != varient_entry['REF']:
        return False
    alt_parts = varient_entry['ALT'].split(',')
    if str(vcf_record.ALT[0]) != alt_parts[0]:
        return False
    if str(vcf_record.ALT[1]) != alt_parts[1]:
        return False
    return True


def produce_output(result_list, patient_cols: List[str]) -> int:
    print('complete reading patient info. now compiling')
    with open("/home/mcarruth/Downloads/data.csv", "w", newline="") as csv_file:
        cols = ["CHROM", "POS", "REF", "ALT"]
        cols.extend(patient_cols)
        writer = csv.DictWriter(csv_file, fieldnames=cols)
        writer.writeheader()
        lines_seen = 0
        for r in result_list:
            for p in patient_cols:
                r[p] = r['patients'][p] if p in r['patients'] else 'N/A'  # if we don't have a record for this patient, add in N/A
                r.pop('patients')
                writer.writerow(r)
                lines_seen += 1
    return lines_seen


# read in variant file
positions, results = format_variant_file()
sort_positions(positions)

# time for patient data
# because the patient files have ranges, computationally it will be much faster to use those
# and search for which variants fall between those ranges and then copy the value
# -- this is where sorting helps --

mypath = "/home/mcarruth/Downloads/"  # change to where your patient files are
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith("_g.vcf.gz")]
patients_seen = []
for patient_file in onlyfiles:
    vcf_reader, est_total_lines = read_patient_file(join(mypath, patient_file))
    patients_seen.append(patient_file)
    lines_read, prev_low, prev_chrom, last_max, gt_ref, gt_het, gt_alt = 0, 0, 0, 0, 0, 0, 0
    milestones = []

    for lines_read, record in enumerate(vcf_reader):
        log_milestone(lines_read, est_total_lines, milestones, patient_file)
        chrom, genotype, start_pos, end_pos = pull_info_from_record(record, vcf_reader.samples[0])

        if start_pos >= last_max and chrom == prev_chrom:
            known_min = prev_low
        else:
            known_min, prev_low = 0, 0
            prev_chrom = chrom

        left_idx = binary_search(sorted_list=positions[chrom], value=int(start_pos), find_min=True, start_idx=known_min)
        if left_idx is not None:
            right_idx = binary_search(sorted_list=positions[chrom], value=int(end_pos), find_min=False, start_idx=known_min)
            if right_idx is not None:
                prev_low = left_idx
                for x in range(left_idx, right_idx + 1):
                    position, original_row_number = positions[chrom][x]
                    assert start_pos <= position <= end_pos, f'{position} from {record} faulty'
                    result_row = results[original_row_number]
                    if record.genotype(vcf_reader.samples[0])['GQ'] >= 20 and (
                            genotype == "0/0" or does_record_match_alleles(record, result_row)):
                        # 0/1, 1/1 etc must match on ref and alt as well
                        result_row["patients"][patient_file] = genotype
                        if genotype == "0/0":
                            gt_ref += 1
                        elif genotype == "0/1":
                            gt_het += 1
                        elif genotype == "1/1":
                            gt_alt += 1

        last_max = end_pos
    print(f'complete with {patient_file}, actual records = {lines_read} vs estimated: {est_total_lines}')
    print(f'     saw {gt_ref} 0/0 genotypes; {gt_het} 0/1 genotypes; {gt_alt} 1/1 genotypes')


# output
count_lines = produce_output(results, patients_seen)
assert count_lines == len(results)
# TODO, more tests/confirmations

import os
from lxml import etree
from collections import defaultdict

def count_occurrences(directory, xpath_error_pattern, xpath_proofread):
    type_count = defaultdict(int)  # ErrorPattern.type 카운트
    pos_count = defaultdict(int)  # Proofread.pos 카운트
    combined_count = defaultdict(int)  # 조합된 카운트

    # 지정된 폴더 내의 모든 XML 파일을 탐색
    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            file_path = os.path.join(directory, filename)

            # XML 파일 파싱
            with open(file_path, 'rb') as file:
                tree = etree.parse(file)
                root = tree.getroot()

                # ErrorPattern 요소와 그 자식 Proofread 요소 찾기
                error_annote_pattern_elements = root.xpath(xpath_error)
                for err_annote in error_annote_pattern_elements:
                    type_value = ''
                    pos_value = ''
                    error_pattern_elements = err_annote.xpath(xpath_error_pattern)
                    for ep_element in error_pattern_elements:
                        type_value = ep_element.get('type')
                        if type_value:
                            type_count[type_value] += 1

                    proofread_elements = err_annote.xpath(xpath_proofread)
                    for pr_element in proofread_elements:
                        pos_value = pr_element.get('pos')
                        if pos_value:
                            pos_count[pos_value] += 1

                    #if type_value and pos_value:  # 둘 다 존재하는 경우
                    combined_key = (type_value, pos_value)
                    combined_count[combined_key] += 1

    return type_count, pos_count, combined_count

# 폴더 경로 및 XPath 설정
directory = 'D:\\work\\TEST\\ptest'
xpath_error_pattern = ".//ErrorPattern"
xpath_proofread = ".//Proofread"
xpath_error = ".//LearnerErrorAnnotations"

# 각 요소별 출현 횟수 계산
type_occurrences, pos_occurrences, combined_occurrences = count_occurrences(directory, xpath_error_pattern, xpath_proofread)

# 결과 출력
print("ErrorPattern.type Occurrences:")
for type_val, count in type_occurrences.items():
    print(f"  type='{type_val}': {count} times")

print("\nProofread.pos Occurrences:")
for pos_val, count in pos_occurrences.items():
    print(f"  pos='{pos_val}': {count} times")

print("\nCombined Occurrences of ErrorPattern.type and Proofread.pos:")
for (type_val, pos_val), count in combined_occurrences.items():
    print(f"  type='{type_val}', pos='{pos_val}': {count} times")

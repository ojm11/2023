import os
from lxml import etree
from collections import Counter
import csv

def save_frequency_to_csv(frequency_data, csv_file_path):
    # CSV 파일 열기 및 작성
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # 헤더 작성
        writer.writerow(['Value', 'Frequency'])

        # 빈도 데이터 작성
        for value, count in frequency_data.items():
            writer.writerow([value, count])

def count_proofread_vv_values(directory, xpath_expression):
    vv_values_count = Counter()  # "VV" pos 값을 가진 Proofread 노드의 값의 빈도 카운트

    # 지정된 폴더 내의 모든 XML 파일을 탐색
    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            file_path = os.path.join(directory, filename)

            # XML 파일 파싱
            with open(file_path, 'rb') as file:
                tree = etree.parse(file)
                root = tree.getroot()

                # pos 속성이 "VV"인 Proofread 노드 찾기
                vv_proofread_nodes = root.xpath(xpath_expression)
                
                # 각 노드의 텍스트 값 카운트
                for node in vv_proofread_nodes:
                    vv_values_count[node.text] += 1

    return vv_values_count

# 폴더 경로 및 XPath 설정
directory = 'D:\\work\\TEST\\ptest'
xpath_expression = ".//Proofread[@pos='VV']"  # pos 속성이 "VV"인 Proofread 노드 찾기 위한 XPath
csvfile='D:\\work\\TEST\\a.csv'

# "VV" pos 값을 가진 Proofread 노드의 값의 빈도 카운트
vv_values_frequency = count_proofread_vv_values(directory, xpath_expression)

# 결과 출력
print("Frequency of Proofread Node Values with pos='VV':")
for value, count in vv_values_frequency.items():
    print(f"{value}, {count}")

# CSV 파일에 저장
save_frequency_to_csv(vv_values_frequency, csvfile)

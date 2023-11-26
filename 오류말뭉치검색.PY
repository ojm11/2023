import os
import csv
from lxml import etree

config_file_name = "default_path.txt"

def save_default_path(path, path2):
    with open(config_file_name, "w") as file:
        path3 = [path, path2]
        file.writelines(path3)

def load_default_path():
    if os.path.exists(config_file_name):
        with open(config_file_name, "r") as file:
            default_path = file.readline().strip()
            default_out_path = file.readline().strip()
            return default_path, default_out_path
    else :
        # 파일이 없으면 생성하고 기본 경로 저장
        with open(config_file_name, 'w') as file:
            default_path = os.getcwd() 
            default_out_path = os.path.join(default_path, "out.csv")
            path3 = [default_path + "\n", default_out_path + "\n"]
            file.writelines(path3)
            return default_path, default_out_path
    
def write_header(header) :

    rowheader = [
            header.findtext('LearningEnvironment'),
            header.findtext('SourceType'),
            header.findtext('AssignmentType'),
            header.findtext('AssignmentGenre'),
            header.findtext('AssignmentTheme'),
            header.findtext('WordCount'),
        ] + [
            header.find('LearnerInfo').findtext(tag) for tag in [
                'LearnerType',
                'LearnerTypeDetail',
                'AgeGroup',
                'DataGrade',
                'Nationality',
                'LearningPurpose',
                'MotherLanguage'
            ]
        ]

    return rowheader

def get_directory_name(default_path, default_out_path):
    if default_path:
        user_input = input(f"디렉토리명을 입력하세요 (기본: {default_path}): ")    
    else:
        user_input = input("디렉토리명을 입력하세요: ").strip()
    
    if default_out_path :
        user_input1 = input(f"출력파일명을 입력하세요 (기본: {default_out_path}):")
    else :
        user_input1 = input(f"출력파일명을 입력하세요 :")

    return user_input.strip() or default_path, user_input1.strip() or default_out_path

def makexpath(original_form,
                            logic,
                            correction_form, 
                            selected_error_sejong_pos, 
                            selected_error_aspect,
                            selected_error_location) :
    xpath_full = ""
    spv = ""
    if correction_form :
        spv += f"Proofread = '{correction_form}'"
        
    if spv != "" :
        xpath_full = f"{spv}"

    spv = ""
    for sp in selected_error_sejong_pos :
        if spv != "" :
            spv += " or "
        spv += f"@pos='{sp}'"
    
    if spv :
        if xpath_full != "":
            xpath_full += f" and "
        xpath_full += f"Proofread[{spv}]"

    spv = ""
    for s in selected_error_aspect :
        if spv != "" :
            spv += " or "
        spv += f"contains(concat(';', @type, ';'), ';{s};')" 

    if spv :
        if xpath_full != "":
            xpath_full += " and "
        xpath_full += f"ErrorPattern[{spv}]"

    spv = ""
    for sp in selected_error_location :
        if spv != "" :
            spv += " or "
        spv += f"@type='{sp}'"
    
    if spv :
        if xpath_full != "":
            xpath_full += " and "
        xpath_full += f"ErrorArea[{spv}]"
    return xpath_full

def find_matching_Errormorphemes(writer,
                            original_form,
                            logic,
                            xpath_full) :

    xpath_s_full = ''

    if xpath_full != '' :
        xpath_s_full = f".//LearnerErrorAnnotations/word/morph[{xpath_full}]"

    print(f"XPATH : {xpath_s_full}")

    # 지정된 폴더 내의 모든 XML 파일을 탐색
    for filename in os.listdir(directory_name):
        if filename.endswith('.xml'):
            file_path = os.path.join(directory_name, filename)

            # XML 파일 파싱
            with open(file_path, 'rb') as file:
                tree = etree.parse(file)
                root = tree.getroot()

                header = root.find('Header')
                
                if xpath_s_full != '':
                    morphs = root.xpath(xpath_s_full)
                else :
                    morphs = []

                for ma_morph in root.xpath('.//MorphemeAnnotations//word//morph'):
                    ma_text = ma_morph.text
                    ma_word = ma_morph.getparent()
                    ma_morph_ann = ma_word.getparent()
                    ma_sentence = ma_morph_ann.getparent()

                    ma_from = ma_sentence.get('from')
                    ma_to = ma_sentence.get('to')
                    
                    morph_from = ma_morph.get('from')
                    morph_to = ma_morph.get('to')
                    morph_sub = ma_morph.get('subsequence')
                    morph_pos = ma_morph.get('pos')
                    
                    full_s = ma_sentence.findtext("s")
                    lea_from = -1
                    lea_to = -1
                    lea_sub = -1
                    lea_v = ""
                    find = False
                    errorArea = ""
                    ErrorPattern = ""
                    lea_pos = ""
                    errorArea = ""
                    ErrorPattern = ""
                    lea_word_w = ""
                    lea_sentence_left = ""
                    lea_sentence_right = ""

                    ma_sentence_from_i = int(ma_from)
                    ma_sentence_to_i = int(ma_to)

                    for lea_morph in morphs:
                        lea_word = lea_morph.getparent()
                        lea_error_ann = lea_word.getparent()
                        lea_sentence = lea_error_ann.getparent()

                        lea_sentence_from1 = lea_sentence.get('from')
                        lea_sentence_to1 = lea_sentence.get('to')
                        lea_from1 = lea_morph.get('from')
                        lea_to1 = lea_morph.get('to')
                        lea_sub1 = lea_morph.get('subsequence')

                        if (ma_from == lea_sentence_from1 and
                            ma_to == lea_sentence_to1 and
                            morph_from == lea_from1 and
                            morph_to ==  lea_to1 and 
                            morph_sub == lea_sub1): 

                            lea_from = morph_from
                            lea_to = morph_to
                            lea_sub = morph_sub
                            lea_v = lea_morph.findtext('Proofread')
                            
                            lea_from_i = int(lea_from)
                            lea_to_i = int(lea_to)

                            lea_pos_t = lea_morph.find('Proofread')
                            if lea_pos_t is not None :
                                lea_pos = lea_pos_t.get('pos')
                            else :
                                lea_pos = ""

                            errorArea_t = lea_morph.find('ErrorArea')
                            if errorArea_t is not None :
                                errorArea = errorArea_t.get('type')
                            else :
                                errorArea = ""

                            ErrorPattern_t = lea_morph.find('ErrorPattern')
                            if ErrorPattern_t is not None :
                                ErrorPattern = ErrorPattern_t.get('type')
                            else :
                                ErrorPattern = ""

                            lea_word_w = lea_word.findtext('w')
                            find = True
                            
                            if ma_sentence_from_i <= lea_from_i and lea_to_i <= ma_sentence_to_i :
                                lea_sentence_left = full_s[:(lea_to_i - lea_from_i - 1)].strip()
                                lea_sentence_right = full_s[(lea_to_i - ma_sentence_from_i):].strip()

                            print(etree.tostring(lea_morph, pretty_print=True, encoding='utf-8').decode('utf-8'))
                            break
                    
                    # 조건검사
                    if logic == "AND" :
                        if find and original_form == ma_text:
                            find = True
                        else :
                            find = False
                    else :
                        if original_form == ma_text:
                            find = True
                    
                    if find :
                        headerinfo = write_header(header)
                        row = [
                                header.findtext('SampleSeq'),
                                ma_text,
                                morph_pos, 
                                lea_v,
                                lea_pos,
                                lea_sentence_left,
                                lea_word_w,
                                lea_sentence_right,
                                errorArea,
                                ErrorPattern,
                                ''
                            ] + headerinfo
                        
                        writer.writerow(row)
# 폴더 경로 및 XPath 설정
directory = 'D:\\work\\TEST\\ptest'


# 사용자 입력 받기 함수
def get_user_input(prompt):
    return input(prompt)


def get_user_choice(options, multiple=False, width=25):
    selected_item = []
    options_with_skip = [("SKIP", "선택하지 않음")] + options

    for idx, (tag, desc) in enumerate(options_with_skip, start=0):
        menu_item = f"{idx}. {tag}({desc})".ljust(width)
        print(menu_item, end='  ')
        if idx % 5 == 0:
            print()
    print("\n")

    while True:
        try:
            choice_s = input("메뉴 번호를 선택하세요 (태그를 선택하지 않으려면 'SKIP'을 선택하세요): ")
            if not choice_s :
                return selected_item
            
            choice = int(choice_s)
            if 0 == choice :
                return selected_item
            elif choice <= len(options_with_skip):
                selected_item.append(options_with_skip[choice][0])
                if not multiple :
                    selected_item
            else:
                print("유효한 메뉴 번호를 입력하세요.")
        except ValueError:
            print("숫자를 입력해야 합니다.")

# 태그 리스트 정의
logic_tags = [("AND","그리고"), ("OR", "또는")]
error_aspect_tags = [("OM", "누락"), ("ADD", "첨가"), ("REP", "대치"), ("MIF", "오형태")]
error_location_tags = [
("CNNP","고유명사"), ("CNNG","일반명사"), ("CNNB","의존명사"),
("CNP","대명사"),    ("CNR","수사"),      ("CVV","동사"),  
("CVA","형용사"),    ("CVX","보조용언"),  ("CVC", "지정사"),
("CMM","관형사"),    ("CMAG","일반부사"), ("CMAJ", "접속부사"),
("CIC","감탄사"),    ("CXPN","체언접두사"),("CXSN","명사파생접미사"),
("CXSV","동사파생접미사"),("CXSA","형용사파생접미사"),("CXR","어근"),
]

sejong_pos_tags = [
    ("NNG", "일반명사"),
    ("NNP", "고유명사"),
    ("NNB", "의존명사"),
    ("NP", "대명사"),
    ("NR", "수사"),
    ("VV", "동사"),
    ("VA", "형용사"),
    ("VX", "보조용언"),
    ("VCP", "긍정지정사"),
    ("VCN", "부정지정사"),
    ("MAG", "일반부사"),
    ("MAJ", "접속부사"),
    ("MM", "관형사"),
    ("IC", "감탄사"),
    ("JKS", "주격조사"),
    ("JKC", "보격조사"),
    ("JKG", "관형격조사"),
    ("JKO", "목적격조사"),
    ("JKB", "부사격조사"),
    ("JKV", "호격조사"),
    ("JKQ", "인용격조사"),
    ("JX", "보조사"),
    ("JC", "접속조사"),
    ("EP", "선어말어미"),
    ("EF", "종결어미"),
    ("EC", "연결어미"),
    ("ETN", "명사형전성어미"),
    ("ETM", "관형형전성어미"),
    ("XPN", "접두사"),
    ("XSN", "명사파생접미사"),
    ("XSV", "동사파생접미사"),
    ("XSA", "형용사파생접미사"),
    ("XR", "어근"),
    ("SF", "마침표, 물음표, 느낌표"),
    ("SP", "쉼표, 가운뎃점, 콜론, 빗금"),
    ("SS", "따옴표, 괄호표, 줄표"),
    ("SE", "줄임표"),
    ("SO", "붙임표(물결, 숨김, 빠짐)"),
    ("SL", "외국어"),
    ("SH", "한자"),
    ("SW", "기타 기호"),
    ("SN", "숫자"),
    ("NA", "분석불능범주")
]

# 기본 경로 로드
default_path, default_out_path = load_default_path()
if default_path == "":
    default_path = os.getcwd()

if default_out_path == "" :
    curpath = os.getcwd() 
    default_out_path = os.path.join(curpath, "out.csv")

# 사용자로부터 디렉토리명 입력 받기
directory_name, csv_file = get_directory_name(default_path, default_out_path)

original_form = get_user_input("원형태를 입력하세요: ")
correction_form = get_user_input("교정형태를 입력하세요: ")

selected_logic = ""

if original_form and correction_form :
  while True :
    print("검색 조건을 선택하세요:")
    logic_menu = "1. 그리고    2. 또는"
    retv = input(logic_menu)
    if not retv :
        selected_logic = "AND"
    else :
        logic_c = int(retv)
        if logic_c == 1 :
            selected_logic = "AND"
            break
        elif logic_c == 2 :
            selected_logic = "OR"
            break

# 태그 선택
print("교정품사를 선택하세요:")
selected_error_sejong_pos = get_user_choice(sejong_pos_tags, True)

print("오류양상을 선택하세요:")
selected_error_aspect = get_user_choice(error_aspect_tags, True)

print("오류위치를 선택하세요:")
selected_error_location = get_user_choice(error_location_tags, True)

logic = ""
if selected_logic == "AND" :
    logic = " 그리고 "
elif  selected_logic == "OR":
    logic = " 또는 "

# 결과 출력
print(f"원형태: {original_form} {logic}")
print(f"교정형태: {correction_form}")
print(f"교정품사: {selected_error_sejong_pos}")
print(f"오류양상: {selected_error_aspect}")
print(f"오류위치: {selected_error_location}")

andOp = False
if original_form != "" and logic == "AND":
   if correction_form != "" or \
    len(selected_error_sejong_pos) > 0 or \
    len(selected_error_aspect) > 0 or \
    len(selected_error_location) > 0 :
        andOp = True

# CSV 헤더 정의
headers = ['SampleSeq', 
            '원형태',
            '원품사',
            '교정형태',
            '교정품사',
            '앞문맥',
            '중심어',
            '뒤문맥',
            '오류위치',
            '오류양상',
            '오류층위',
           'LearningEnvironment', 
           'SourceType', 
           'AssignmentType', 
           'AssignmentGenre', 
           'AssignmentTheme', 
           'WordCount', 
           'LearnerType', 
           'LearnerTypeDetail', 
           'AgeGroup', 
           'DataGrade', 
           'Nationality', 
           'LearningPurpose', 
           'MotherLanguage'
           ]

with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)

    xpath_full = makexpath(original_form,
                            logic,
                            correction_form, 
                            selected_error_sejong_pos, 
                            selected_error_aspect,
                            selected_error_location)
    
    find_matching_Errormorphemes(writer,
                            original_form,
                            logic,
                            xpath_full)
        
    # if andOp :
    #     find_matching_morphemes_and(directory_name)
    # else :
    #     find_matching_morphemes(directory_name)
    #     find_matching_Errormorphemes(writer,
    #                         correction_form,
    #                         selected_error_sejong_pos,
    #                         selected_error_aspect,
    #                         selected_error_location
    #                         )


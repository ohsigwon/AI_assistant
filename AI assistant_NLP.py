# koNLPy 설치
pip install konlpy

# 얘가 최종 완성본

import pandas as pd
from konlpy.tag import Kkma
from datetime import datetime, timedelta

# KoNLPy 객체 생성
kkma = Kkma()

# 예시 과제 데이터 (학교 사이트에서 추출한 데이터)
data = {
    'subject': ['확률과 통계', '심화수학', '생물학'],
    'title': ['2024년 3학년 수학 확률과 통계 세특활동1) 심화 개념 탐구 활동 (학종 준비 친구들 대상)', '2024년 3학년 수학 심화수학 추가 보고서 제출', '세포 구조'],
    'due_date': ['2024-07-21', '2024-07-20', '2024-06-26'],
    'description': [
        '''안녕하세요 3학년 친구들
확률과 통계 심화 개념 탐구 활동지 작성 안내 드립니다.선생님이 첨부한 한글파일 2가지를 모두 꼼꼼히 확인하고기한에 맞춰 작성해 주세요.
3학년 생기부 작성이 빠르게 이루어저야   하는 만큼 추가 기한은   절대 드리지 않을 예정이니 반드시 기한에 맞춰 제출해 주세요.

첨부파일 1과 2를 참고하여 활동지 제출하기
(주제 선정 및 작성과 관련한 질문은 자신의 확통 담당 선생님께 질문해 주세요)''',
        '''추가 보고서 제출란입니다.
기한은 7/19 자정까지입니다.
(K1반은 심화수학 교과서 문제풀이 7/16 자정까지 제출)''',
        '세포의 구조를 상세히 설명하세요.'
    ]
}

# 데이터프레임 생성
df = pd.DataFrame(data)
df['due_date'] = pd.to_datetime(df['due_date'])

def extract_info(input_text):
    # 형태소 분석을 통해 명사 추출
    nouns = kkma.nouns(input_text)
    return nouns

def get_assignments_due_this_week():
    today = datetime.now()
    end_of_week = today + timedelta(days=(6-today.weekday()))
    assignments = df[(df['due_date'] >= today) & (df['due_date'] <= end_of_week)]
    return assignments

def get_assignment_info_by_subject(subject):
    assignments = df[df['subject'].str.contains(subject)]
    return assignments

def main():
    input_text = input("질문을 입력하세요: ")
    nouns = extract_info(input_text)

    if '이번주' in input_text or '이번 주'in input_text:
        assignments = get_assignments_due_this_week()
        if not assignments.empty:
            info_text = "이번 주까지 마감인 과제들:\n"
            for index, row in assignments.iterrows():
                info_text += (
                    f"\n과제 정보:\n"
                    f"제목: {row['title']}\n"
                    f"마감일: {row['due_date'].strftime('%Y-%m-%d')}\n"
                    f"설명: {row['description']}\n"
                )
        else:
            info_text = "이번 주까지 마감인 과제가 없습니다."
    else:
        subject_found = False
        for noun in nouns:
            assignments = get_assignment_info_by_subject(noun)
            if not assignments.empty:
                subject_found = True
                info_text = f"{noun} 과목의 과제 정보:\n"
                for index, row in assignments.iterrows():
                    info_text += (
                        f"\n과제 정보:\n"
                        f"제목: {row['title']}\n"
                        f"마감일: {row['due_date'].strftime('%Y-%m-%d')}\n"
                        f"설명: {row['description']}\n"
                    )
                break

        if not subject_found:
            info_text = "해당 과제 정보를 찾을 수 없습니다."

    print(info_text)

if __name__ == "__main__":
    main()

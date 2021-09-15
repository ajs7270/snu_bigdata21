import csv
import numpy as np
import random
from typing import List, Tuple

with open("student_list.csv", "r", encoding='utf-8') as f:
    reader = csv.reader(f)
    student_list = []
    for line in reader:
        student_list.append(line[:6])

# 데이터 확인
print("학생의 수:",len(student_list))
for student in student_list:
    print(student)

def list_chunk(origin_list: List[str], n : int) -> List[List[str]]:
    return [origin_list[i:i+n] for i in range(0, len(origin_list), n)]

def student_swap(std_list:List[List[str]], x: Tuple[int, int], y: Tuple[int,int])-> List[List[str]]:
    std_list[x[0]][x[1]],std_list[y[0]][y[1]] = std_list[y[0]][y[1]],std_list[x[0]][x[1]]

    return std_list

def generate_rand_idx() -> Tuple[Tuple[int, int], Tuple[int, int]]:
    team_x = np.random.randint(9)
    team_y = np.random.randint(9)

    # 같은 팀일 경우 한번 더 뽑음
    while team_x == team_y:
        team_y = np.random.randint(9)

    student_x = np.random.randint(4)
    student_y = np.random.randint(4)

    return ((team_x, student_x), (team_y, student_y))


def object_function(teams: List[List[str]]) -> int:
    # array에 이름을 빼주고 str type을 int type으로 교체
    team_array = np.array(teams)[:, :, 1:].astype(np.int64)
    # 분산을 구하기 위해 중간 계산 결과값을 저장
    score_avg = np.mean(team_array, axis=1)
    team_var = np.var(score_avg, axis=0)
    sum_var = np.sum(team_var)

    return sum_var


# 두 학생을 swap 하여 loss를 줄이는 방식 => local optima에 빠질 수 있음
# 아래 결과를 보면 314657 th 번째 이후부터는 local optima에 빠져
# 업데이트를 하지 않음을 확인할 수 있음

num_of_member = 4

# 팀을 만들때 한번 흔들어줌
random.shuffle(student_list)
teams = list_chunk(student_list, num_of_member)

cur_loss = object_function(teams)

result = []
for i in range(300000000):
    # 랜덤하게 swap할 학생 인덱스 찾기

    x, y = generate_rand_idx()
    swap_teams = student_swap(teams, x, y)
    swap_loss = object_function(swap_teams)

    if cur_loss > swap_loss:
        result = swap_teams
        cur_loss = swap_loss
        print(i, "th iteration :", cur_loss)

print("=====================")
print("final loss :", cur_loss)
for idx, team in enumerate(result):
    print("Team", idx + 1)
    for student in team:
        print(student)
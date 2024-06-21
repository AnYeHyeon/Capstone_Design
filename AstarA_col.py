import random
import copy
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# 컨테이너 배치를 Matrix형태로 바꾸기
def adjust_matrix_and_add_identifiers(A, W, H):
    adjusted_A = []
    for i, row in enumerate(A):
        adjusted_A_row = []
        for j, value in enumerate(row):
            key = f"({i},{j})"
            adjusted_A_row.append({key: value})
        adjusted_A.append(adjusted_A_row)
    return adjusted_A

# 다음 옮길 컨테이너 고르기
def find_moving_container(A, last_moved_container):
    containers = []
    weights = []

    for col in range(len(A[0])):
        # 각 열의 위쪽에서 아래쪽으로 탐색하여 가장 위쪽에 있는 0이 아닌 컨테이너를 찾음
        for row in range(len(A)):
            value = list(A[row][col].values())[0]
            if value != 0:
                # 가장 위쪽에 있는 0이 아닌 컨테이너를 찾았지만, 마지막으로 옮긴 컨테이너가 아니어야 함
                if (row, col) != last_moved_container:
                    containers.append((row, col))
                    weights.append(value)
                break  # 가장 위쪽에 있는 첫 번째 0이 아닌 컨테이너를 찾으면 탐색 중지
    
    # 가중치 기반으로 선택
    if containers:
        selected_container = random.choices(containers, weights=weights, k=1)[0]
        return selected_container

# 컨테이너를 둘 빈 자리 고르기
def find_valid_empty_slot(A, moving_con_col):
    # 빈 자리(0인 위치) 찾기
    empty_slots = [(i, j) for i in range(len(A)) for j in range(len(A[0])) if list(A[i][j].values())[0] == 0]

    for _ in range(len(empty_slots)):
        empty_row, empty_col = random.choice(empty_slots)  
        
        # 같은 열이면 불가능
        if empty_col == moving_con_col:
            continue
        # 선택된 빈 자리의 아래가 빈 자리이면 불가능
        if empty_row < len(A) - 1 and list(A[empty_row + 1][empty_col].values())[0] == 0:
            continue
        
        # 유효한 빈 자리를 찾으면 반환
        return (empty_row, empty_col)
    
    return None  # 유효한 빈 자리를 찾지 못함

def is_sorted_ascending(column):
    values = [list(cell.values())[0] for cell in column]
    return all(values[i] <= values[i + 1] for i in range(len(values) - 1))

def move_and_sort(A, W, H):
    # 초기 상태를 변형 전의 A를 기준으로 기록
    initial_state = adjust_matrix_and_add_identifiers(A, W, H)
    process_log = []  # 각 상태를 기록할 리스트
    process_log.append((initial_state.copy(), 0, "Initial state"))  # 초기 상태 기록

    # 변형 및 식별자 추가 후의 상태
    A = adjust_matrix_and_add_identifiers(A, W, H)
    move_count = 0
    all_sorted = False
    last_moved_container = None  # 마지막으로 옮긴 컨테이너 위치를 저장할 변수

    # 모든 열이 적합한지 확인
    if all(is_sorted_ascending([row[i] for row in A]) for i in range(W)):
        all_sorted = True
        print("All containers are already suitable.")
        return A, move_count, process_log  # 이미 정렬된 경우 반환
    
    while not all_sorted:
        # 1 옮길 컨테이너 고르기
        moving_con = find_moving_container(A, last_moved_container)
        # print(moving_con)
        if not moving_con:
            # 유효한 이동할 컨테이너가 없으면 반복 종료
            print("No valid moving container is found.")
            break

        moving_con_row, moving_con_col = moving_con
        current_container = list(A[moving_con_row][moving_con_col].items())

        # 2 빈자리 선택
        empty_slot = find_valid_empty_slot(A, moving_con_col)
        # print(empty_slot)
        if not empty_slot:
            # 유효한 빈 자리가 없으면 반복을 계속해서 새로운 자리를 찾음
            print("No valid empty slot found.")
            continue

        # 3 빈 자리를 새로 선택했으니 컨테이너를 이동
        empty_row, empty_col = empty_slot

        # 현재 컨테이너 위치와 빈 자리를 교체
        A[empty_row][empty_col], A[moving_con_row][moving_con_col] = A[moving_con_row][moving_con_col], A[empty_row][empty_col]
        last_moved_container = (empty_row, empty_col)

        move_count += 1
        log_message = f"{current_container} to {empty_slot}. Move count: {move_count}"
        process_log.append((copy.deepcopy(A), move_count, log_message))  # 상태와 이동 횟수, 로그 메시지 기록

        # 정렬 상태 확인
        if all(is_sorted_ascending([row[i] for row in A]) for i in range(W)):
            all_sorted = True
            print("########## Final State ##########")
            break

    return A, move_count, process_log  # 최종 상태 반환

def run_experiments(num_trials, A, W, H):
    adjusted_As = []

    for trial in range(num_trials):
        print(f"Trial {trial + 1}:")
        adjusted_A_matrix, move_count, process_log = move_and_sort(A, W, H)
        adjusted_As.append((adjusted_A_matrix, move_count, process_log))
        print(f"Move count: {move_count}\n")

    # Move count가 가장 작은 결과 찾기
    min_moves = min(adjusted_As, key=lambda x: x[1])
    best_matrix, best_move_count, best_process_log = min_moves

    return best_matrix, best_move_count, best_process_log


def main():
    A = [
        [0, 0, 0],
        [1, 3, 3],
        [2, 2, 2],
    ]

    W = 3
    H = 3
    num_trials = 20

    try:
        best_matrix, best_move_count, best_process_log = run_experiments(num_trials, A, W, H)

        print("Best adjusted_A with the least move count:")
        for row in best_matrix:
            print(row)
        print(f"Minimum Move count: {best_move_count}")

        print("\nProcess log of the best adjusted_A:")
        for step, (matrix_state, count, log_message) in enumerate(best_process_log):
            print(f"Step {step}: {log_message}")
            for row in matrix_state:
                print(row)
            print()

    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/process', methods=['POST'])
# def process():
#     data = request.json
#     A = data['A']
#     W = int(data['W'])
#     H = int(data['H'])
    
#     best_matrix, best_move_count, best_process_log = run_experiments(20, A, W, H)  # N번 실험

#     return jsonify({
#         'best_matrix': best_matrix,
#         'best_move_count': best_move_count,
#         'best_process_log': best_process_log
#     })

# if __name__ == '__main__':
#     app.run(debug=True)
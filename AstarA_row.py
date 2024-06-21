import random

from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# 입력 매트릭스의 각 행의 길이를 맞추는 함수
def normalize_matrix(A, W):
    new_A = []
    for row in A:
        new_row = row + [0] * (W - len(row))  # 부족한 부분을 0으로 채움
        new_A.append(new_row)
    return new_A    

# 컨테이너 배치를 Matrix형태로 바꾸기
def adjust_matrix_and_add_identifiers(A, W, H):
    original_H = len(A)
    original_W = len(A[0]) if original_H > 0 else 0
    
    if original_H > H or original_W > W:
        raise ValueError("Given matrix is larger than specified dimensions.")
    
    adjusted_A = [[{'': 0}] * W for _ in range(H)]
    identifier = ord('a')
    
    for i in range(H):
        for j in range(W):
            if i < original_H and j < original_W and A[i][j] != 0:
                adjusted_A[i][j] = {chr(identifier): A[i][j]}
                identifier += 1
            else:
                adjusted_A[i][j] = {chr(identifier): 0}
                identifier += 1
    
    return adjusted_A

# 다음 옮길 컨테이너 고르기
def find_moving_container(A, last_moved_container):
    containers = []
    weights = []

    for row in range(len(A)):
        # 각 행의 오른쪽에서 왼쪽으로 탐색하여 가장 오른쪽에 있는 0이 아닌 컨테이너를 찾음
        for col in reversed(range(len(A[0]))):
            value = list(A[row][col].values())[0]
            if value != 0:
                # 가장 오른쪽에 있는 0이 아닌 컨테이너를 찾았지만, 마지막으로 옮긴 컨테이너가 아니어야 함
                if (row, col) != last_moved_container:
                    containers.append((row, col))
                    weights.append(value)
                break  # 가장 오른쪽에 있는 첫 번째 0이 아닌 컨테이너를 찾으면 탐색 중지
    # print(containers)
        
        # 가중치 기반으로 선택
    if containers:
        selected_container = random.choices(containers, weights=weights, k=1)[0]
        return selected_container

# 컨테이너를 둘 빈 자리 고르기
def find_valid_empty_slot(A, moving_con_row):
    # 빈 자리(0인 위치) 찾기
    empty_slots = [(i, j) for i in range(len(A)) for j in range(len(A[0])) if list(A[i][j].values())[0] == 0]

    for _ in range(len(empty_slots)):
        empty_row, empty_col = random.choice(empty_slots)  
        # print("empty_row: " + str(empty_row))   
        # 같은 행이면 불가능
        if empty_row == moving_con_row:
            continue
        # 선택된 빈 자리의 왼쪽이 빈 자리이면 불가능
        if empty_col > 0 and list(A[empty_row][empty_col - 1].values())[0] == 0:
            continue
        
        # 유효한 빈 자리를 찾으면 반환
        return (empty_row, empty_col)
    
    return None  # 유효한 빈 자리를 찾지 못함

def is_sorted_descending(row):
    values = [list(cell.values())[0] for cell in row]
    return all(values[i] >= values[i + 1] for i in range(len(values) - 1))

def move_and_sort(A, W, H):
    A = normalize_matrix(A, W)  # 매트릭스의 각 행의 길이를 맞춤
    A = adjust_matrix_and_add_identifiers(A, W, H)
    process_log = []  # 각 상태를 기록할 리스트
    
    process_log.append((A.copy(), 0, "Initial state"))  # 초기 상태 기록

    move_count = 0
    all_sorted = False
    last_moved_container = None # 마지막으로 옮긴 컨테이너 위치를 저장할 변수

    # 모든 스택이 적합한지 확인
    if all(is_sorted_descending(row) for row in A):
        all_sorted = True
        print("All containers are already suitable.")
    else:        
        while not all_sorted:
            
            # 1 옮길 컨테이너 고르기
            moving_con = find_moving_container(A, last_moved_container)
            # print(moving_con)
            moving_con_row, moving_con_col = moving_con
            current_container = list(A[moving_con_row][moving_con_col].items())
            if not moving_con:
                # print("No valid moving container is found.")
                break

            # 2 빈자리 선택
            empty_slot = find_valid_empty_slot(A, moving_con_row)
            if not empty_slot:
                # print("No valid empty slot found.")
                continue

            # 3 빈 자리를 새로 선택했으니 컨테이너를 이동
            empty_row, empty_col = empty_slot

            # 현재 컨테이너 위치와 빈 자리를 교체
            A[empty_row][empty_col], A[moving_con_row][moving_con_col] = A[moving_con_row][moving_con_col], A[empty_row][empty_col]
            last_moved_container = (empty_row, empty_col)

            move_count += 1
            log_message = f"{current_container} to {empty_slot}. Move count: {move_count}"
            process_log.append((A.copy(), move_count, log_message))  # 상태와 이동 횟수, 로그 메시지 기록

            # 매트릭스 상태 확인
            # for row in A:
            #     print(row)
            # print()

            # 정렬 상태 확인
            if all(is_sorted_descending(row) for row in A):
                all_sorted = True
                print("########## Final State ##########")
                # for row in A:
                #     print(row)
                # print(f"Move count: {move_count}")
                # print("All containers are suitable.")
                break
 
    return A, move_count, process_log

def run_experiments(num_trials, A, W, H):
    results = []

    for trial in range(num_trials):
        print(f"Trial {trial + 1}:")
        result_matrix, move_count, process_log = move_and_sort(A, W, H)
        results.append((result_matrix, move_count, process_log))
        print(f"Move count: {move_count}\n")

    # Move count가 가장 작은 결과 찾기
    min_moves = min(results, key=lambda x: x[1])
    best_matrix, best_move_count, best_process_log = min_moves

    return best_matrix, best_move_count, best_process_log

# def main():
#     A = [
#         [2, 1, 4],
#         [2, 3],
#         [2, 4],
#         [2, 3]
#     ]

#     W = 4
#     H = 4
#     num_trials = 20

#     try:
#         best_matrix, best_move_count, best_process_log = run_experiments(num_trials, A, W, H)

#         print("Best result with the least move count:")
#         for row in best_matrix:
#             print(row)
#         print(f"Minimum Move count: {best_move_count}")

#         print("\nProcess log of the best result:")
#         for step, (matrix_state, count, log_message) in enumerate(best_process_log):
#             print(f"Step {step}: {log_message}")
#             for row in matrix_state:
#                 print(row)
#             print()

#     except ValueError as e:
#         print(e)

# if __name__ == "__main__":
#     main()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    A = data['A']
    W = int(data['W'])
    H = int(data['H'])
    
    best_matrix, best_move_count, best_process_log = run_experiments(20, A, W, H)  # N번 실험

    return jsonify({
        'best_matrix': best_matrix,
        'best_move_count': best_move_count,
        'best_process_log': best_process_log
    })

if __name__ == '__main__':
    app.run(debug=True)
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
        for row in range(len(A)):
            value = list(A[row][col].values())[0]
            if value != 0:
                if (row, col) != last_moved_container:
                    containers.append((row, col))
                    weights.append(value)
                break
    
    if containers:
        selected_container = random.choices(containers, weights=weights, k=1)[0]
        return selected_container

# 컨테이너를 둘 빈 자리 고르기
def find_valid_empty_slot(A, moving_con_col):
    empty_slots = [(i, j) for i in range(len(A)) for j in range(len(A[0])) if list(A[i][j].values())[0] == 0]

    for _ in range(len(empty_slots)):
        empty_row, empty_col = random.choice(empty_slots)  
        if empty_col == moving_con_col:
            continue
        if empty_row < len(A) - 1 and list(A[empty_row + 1][empty_col].values())[0] == 0:
            continue
        
        return (empty_row, empty_col)
    
    return None

def is_sorted_ascending(column):
    values = [list(cell.values())[0] for cell in column]
    return all(values[i] <= values[i + 1] for i in range(len(values) - 1))

def move_and_sort(A, W, H):
    initial_state = adjust_matrix_and_add_identifiers(A, W, H)
    process_log = []
    process_log.append((copy.deepcopy(initial_state), 0, "Initial state"))

    A = adjust_matrix_and_add_identifiers(A, W, H)
    move_count = 0
    all_sorted = False
    last_moved_container = None

    if all(is_sorted_ascending([row[i] for row in A]) for i in range(W)):
        all_sorted = True
        return A, move_count, process_log
    
    while not all_sorted:
        moving_con = find_moving_container(A, last_moved_container)
        if not moving_con:
            break

        moving_con_row, moving_con_col = moving_con
        current_container = list(A[moving_con_row][moving_con_col].items())

        empty_slot = find_valid_empty_slot(A, moving_con_col)
        if not empty_slot:
            continue

        empty_row, empty_col = empty_slot

        A[empty_row][empty_col], A[moving_con_row][moving_con_col] = A[moving_con_row][moving_con_col], A[empty_row][empty_col]
        last_moved_container = (empty_row, empty_col)

        move_count += 1
        log_message = f"{current_container} to {empty_slot}. Move count: {move_count}"
        process_log.append((copy.deepcopy(A), move_count, log_message))

        if all(is_sorted_ascending([row[i] for row in A]) for i in range(W)):
            all_sorted = True
            break

    return A, move_count, process_log

def run_experiments(num_trials, A, W, H):
    adjusted_As = []

    for trial in range(num_trials):
        adjusted_A_matrix, move_count, process_log = move_and_sort(A, W, H)
        adjusted_As.append((adjusted_A_matrix, move_count, process_log))

    min_moves = min(adjusted_As, key=lambda x: x[1])
    best_matrix, best_move_count, best_process_log = min_moves

    return best_matrix, best_move_count, best_process_log

# 보기 쉽게 변환하는 함수 추가
def prettify_matrix(matrix):
    formatted_output = []
    for row in matrix:
        formatted_row = []
        for element in row:
            formatted_row.append(element)
        formatted_output.append(formatted_row)
    # 간결한 JSON 문자열로 변환
    return [[{k: v} for elem in row for k, v in elem.items()] for row in formatted_output]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    A = data['A']
    W = int(data['W'])
    H = int(data['H'])
    
    best_matrix, best_move_count, best_process_log = run_experiments(100, A, W, H)

    # 보기 좋게 변환된 결과 생성
    pretty_best_matrix = prettify_matrix(best_matrix)
    pretty_best_process_log = [
        (prettify_matrix(matrix_state), count, log_message)
        for matrix_state, count, log_message in best_process_log
    ]

    response = {
        'best_matrix': pretty_best_matrix,
        'best_move_count': best_move_count,
        'best_process_log': pretty_best_process_log
    }

    return jsonify(response)



if __name__ == '__main__':
    app.run(debug=True)

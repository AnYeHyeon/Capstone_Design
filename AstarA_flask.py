from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# 여기에 앞서 작성한 Python 코드를 함수로 포함시킵니다.
# normalize_matrix, adjust_matrix_and_add_identifiers, find_moving_container,
# find_valid_empty_slot, is_sorted_descending, move_and_sort, run_experiments 함수를 포함시킵니다.

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    A = data['A']
    W = int(data['W'])
    H = int(data['H'])
    
    best_matrix, best_move_count, best_process_log = run_experiments(1, A, W, H)  # 1번 실험

    return jsonify({
        'best_matrix': best_matrix,
        'best_move_count': best_move_count,
        'best_process_log': best_process_log
    })

if __name__ == '__main__':
    app.run(debug=True)

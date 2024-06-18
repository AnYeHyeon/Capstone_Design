import random

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

def find_rightmost_values(A, exclude_position=None):
    values_positions = []
    for row in range(len(A)):
        for col in range(len(A[0])-1, -1, -1):
            if list(A[row][col].values())[0] != 0:
                if exclude_position is None or (row, col) != exclude_position:
                    values_positions.append((row, col))
                break  # 행의 가장 오른쪽에 있는 값만 검사
    return values_positions

def find_valid_empty_slot(A, empty_slots, avoid_row):
    for _ in range(len(empty_slots)):
        empty_row, empty_col = random.choice(empty_slots)
        # 같은 행을 피하고, 왼쪽 값이 0인 경우 피하기
        if empty_row == avoid_row or (empty_col > 0 and list(A[empty_row][empty_col - 1].values())[0] == 0):
            continue  # 피해야 할 조건에 해당하는 경우 패스
        return (empty_row, empty_col)
    
    return None  # 유효한 빈 자리를 찾지 못한 경우

def move_and_sort(A, empty_slots):
    last_moved = None
    H, W = len(A), len(A[0])
    iterations = 0
    move_count = 0  # 이동 횟수 카운트 변수 추가

    while iterations < 5:  # 최대 5회 반복
        rightmost_positions = find_rightmost_values(A, last_moved)
        if not rightmost_positions:
            print("No valid rightmost values found.")
            break

        # 가장 큰 값을 우선 선택하도록 정렬
        rightmost_positions.sort(key=lambda pos: list(A[pos[0]][pos[1]].values())[0], reverse=True)
        
        for chosen_position in rightmost_positions:
            chosen_row, chosen_col = chosen_position
            chosen_value = list(A[chosen_row][chosen_col].values())[0]

            # 이전에 이동한 위치는 제외
            if last_moved and (chosen_row, chosen_col) == last_moved:
                continue

            empty_slot = find_valid_empty_slot(A, empty_slots, chosen_row)
            if not empty_slot:
                print("No valid empty slot found.")
                continue  # 다음 후보로 넘어감

            empty_row, empty_col = empty_slot

            # 교환
            A[chosen_row][chosen_col], A[empty_row][empty_col] = A[empty_row][empty_col], A[chosen_row][chosen_col]
            
            # 빈 자리 업데이트
            empty_slots.remove((empty_row, empty_col))
            empty_slots.append((chosen_row, chosen_col))

            move_count += 1  # 이동할 때마다 이동 횟수 증가

            print(f"Moving {A[empty_row][empty_col]} from {chosen_position} to {empty_slot}: (Move {move_count})")
            for row in A:
                print(row)
            print()

            last_moved = (empty_row, empty_col)
            break  # 한 번 이동 후, 다시 가장 오른쪽 값들 갱신하여 진행

        iterations += 1

    # 정렬 유지
    for row in range(H):
        for col in range(W-1):
            for next_col in range(col+1, W):
                if list(A[row][col].values())[0] < list(A[row][next_col].values())[0]:
                    A[row][col], A[row][next_col] = A[row][next_col], A[row][col]

    return A, empty_slots, last_moved, move_count  # 이동 횟수를 반환

def main():
    A = [
        [2, 1],
        [2, 3],
        [2, 3]
    ]

    W = 3
    H = 3

    try:
        A = adjust_matrix_and_add_identifiers(A, W, H)
        empty_slots = [(i, j) for i in range(H) for j in range(W) if list(A[i][j].values())[0] == 0]

        print("Initial state:")
        for row in A:
            print(row)
        print()

        A, empty_slots, last_moved, move_count = move_and_sort(A, empty_slots)

        print("Final state:")
        for row in A:
            print(row)
        print(f"Total number of moves: {move_count}")  # 이동 횟수 출력

    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
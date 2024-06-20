import random

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
def find_moving_container(A):
    moving_container = []
    for row in range(len(A)):
        for col in reversed(range(len(A[0]))):
            if list(A[row][col].values())[0] != 0:
                moving_container.append((row, col))
                break
    return moving_container

# 컨테이너를 둘 빈 자리 고르기
def find_valid_empty_slot(A, empty_slots, avoid_row):
    for _ in range(len(empty_slots)):
        empty_row, empty_col = random.choice(empty_slots)
        
        # 같은 행이면 불가능
        if empty_row == avoid_row:
            continue
        # 0을 제외한 가장 오른쪽에 있는 컨테이너 선택
        if empty_col == len(A[0]) - 1 or (empty_col < len(A[0]) - 1 and list(A[empty_row][empty_col + 1].values())[0] == 0):
            return (empty_row, empty_col)
    # print(empty_row, empty_col)
    return None  # No valid empty slot found

def is_sorted_descending(row):
    values = [list(cell.values())[0] for cell in row]
    return all(values[i] >= values[i + 1] for i in range(len(values) - 1))

def move_and_sort(A, W, H):
    A = adjust_matrix_and_add_identifiers(A, W, H)

    print("Initial state:")
    for row in A:
        print(row)
    print()

    move_count = 0
    all_sorted = False

    # 모든 스택이 적합한지 확인
    if all(is_sorted_descending(row) for row in A):
        all_sorted = True
        print("All rows are sorted in descending order.")
    else:
        print("Not sorted yet.")
        
        while all_sorted == False:
            moving_container = find_moving_container(A)
            # print(moving_container) # 옮길 컨데이터 고르기
            if not moving_container:
                print("No valid moving container is found.")
                break

            moving_container.sort(key=lambda pos: list(A[pos[0]][pos[1]].values())[0], reverse=True) # 옮길 컨테이너 후보 중 인덱스값 큰거 고르기
            # print(moving_container)


            for moving_container_position in moving_container:
                moving_con_row, moving_con_col = moving_container_position
                moving_container = list(A[moving_con_row][moving_con_col].items())
                print(moving_container)


        #         empty_slot = find_valid_empty_slot(A, empty_slots, moving_con_row)
        #         if not empty_slot:
        #             print("No valid empty slot found.")
        #             continue

        #         empty_row, empty_col = empty_slot

        #         A[moving_con_row][moving_con_col], A[empty_row][empty_col] = A[empty_row][empty_col], A[moving_con_row][moving_con_col]

        #         empty_slots.remove((empty_row, empty_col))
        #         empty_slots.append((moving_con_row, moving_con_col))

                # move_count += 1

        #         # print(f"(Move {move_count}) Moving {A[empty_row][empty_col]} from {moving_container_position} to {empty_slot}")
        #         for row in A:
        #             print(row)
        #         print()

    return A, move_count


def main():
    A = [
        [2, 1],
        [2, 3],
        [2, 3]
    ]

    W = 3
    H = 3

    try:
        
        A, move_count = move_and_sort(A, W, H)

    #     print("Final state:")
    #     for row in A:
    #         print(row)
    #     print(f"Total number of moves: {move_count}")

    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()

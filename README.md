# For Capstone Design
### A star From the container terminal to the container in the bay A* Algorithm for Optimal Refinancing
위 코드를 수정해서 A*알고리즘으로 각 stack의 인덱스가 내림차순으로 정렬되는 최적화 문제를 해결.

## **Consideration**

Input 

```
A = [
        [2, 1],
        [2, 3],
        [2, 3]
    ]   
    
    W = 3
    H = 3
```

1. 주어진 W와 H를 맞추기 위해 빈자리는 0으로 채운다.
2. 0 값은 옮길 수 없다.
3. 각 stack의 0 뒤에는 어떤 인덱스로 올 수 없다.
4. 옮길때 마다 각 스택이 내림차순으로 정렬되어 있는지 검증하고 다시 재배치를 시작한다.
5. 1회 재배치 시, 가장 오른쪽에 있는 컨테이너(’알파벳’:’인덱스’)만 옮길 수 있다.
6. 가장 뒤에 있는 컨테이너 중 가장 인덱스가 큰 컨테이너를 **우선으로** 주어진 0(빈자리) 중에 배치한다.
7. **작은 인덱스 위에 큰 인덱스를 옮길 수 없다.**
8. 맨 아래에 있는 0에는 가장 인덱스가 큰 컨테이너를 우선으로 가장 큰 것을 선택한다.
9. 각 열의 가장 오른쪽에 있는 0이 아닌 값만을 이동할 수 있음. 
10. 각 열의 가장 오른쪽에 있는 값이 아니면 이동할 수 없음.
11. 이동할 때, 왼쪽에(밑) 0값이 있으면 이동할 수 없음.
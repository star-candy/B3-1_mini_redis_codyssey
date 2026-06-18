class MinHeap:
    # heap 구조 관리 위한 1차원 배열
    def __init__(self):
        self.data = []

    def push(self, item):
        # 가장 아래에 item 저장, 위로 올라가며 heap구조 재정렬
        self.data.append(item)
        self._heapify_up(len(self.data)-1)

    def pop (self):
        # root 값 제거 및 반환, 가장 아래 값을 root로 이동
        # 아래로 내려가며 heap 구조 재정렬
        if not self.data: # 빈 배열인 경우
            return None
        if len(self.data) == 1: # 원소 하나인 경우 단순 배열 pop
            return self.data.pop()
        
        root = self.data[0] # 기존 최솟값 저장
        self.data[0] = self.data.pop() # 가장 아래 값을 root로 이동
        self._heapify_down(0)
        return root

    def peek(self):
        # 최솟값 반환 (제거 안 함)
        return self.data[0] if self.data else None

    def size(self) -> int:
        return len(self.data)

    def _heapify_up(self, index):
        parent = (index - 1) // 2 # 배열에서 부모 인덱스 계산
        # 인덱스가 root가 아니면서, 현재 노드가 부모 노드보다 작은 경우 swap
        if index > 0 and self.data[index][0] < self.data[parent][0]:
            self.data[index], self.data[parent] = self.data[parent], self.data[index]
            self._heapify_up(parent) # 재귀적으로 반복

    def _heapify_down(self, index):
        smallest = index # 현재 노드를 가장 작은 값으로 설정
        left = 2 * index + 1 # 왼쪽 자식 인덱스
        right = 2 * index + 2 # 오른쪽 자식 인덱스

        if left < len(self.data) and self.data[left][0] < self.data[smallest][0]:
            smallest = left # 왼쪽 자식이 더 작은 경우
        if right < len(self.data) and self.data[right][0] < self.data[smallest][0]:
            smallest = right # 오른쪽 자식이 더 작은 경우

        if smallest != index: # smallest가 현재 노드가 아닌 경우 (부모보다 자식이 작은 경우) swap 한다. 
            self.data[index], self.data[smallest] = self.data[smallest], self.data[index]
            self._heapify_down(smallest) # 재귀적으로 반복
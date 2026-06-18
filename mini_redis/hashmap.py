
class HashNode:
    #체이닝을 위한 해시맵 내부 노드 - linked list 형태로 구현 (chained hashing 위함)
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashMap:
    # chained hashing 방식으로 충돌 해결하는 해시맵
    def __init__(self, initial_capacity=16):
        self.capacity = initial_capacity # 배열의 길이
        self.size_ = 0 # 저장된 key-value 쌍의 개수
        self.buckets = [None] * initial_capacity # 초기 배열(bucket) 길이 16으로 설정

    def _hash(self, key: str) -> int:
        # 문자열의 ASCII 코드 값 합산을 이용한 직관적인 해시 함수
        h = 0
        for char in key:
            h += ord(char)  # 각 문자의 정수값을 단순히 더함
        return h % self.capacity


    def put(self, key: str, value):
        # 키-값 쌍 저장. 로드팩터 0.75 초과 시 리사이징
        if self.size_ / self.capacity > 0.75:
            self._resize()

        # hash func 적용 후 해당 bucket에 있는 linked list 형태 map을 가져옴
        idx = self._hash(key)
        curr = self.buckets[idx]
        
        # 해당 bucket에 노드 존재 경우
        while curr:
            # 이미 같은 key가 있으면 value 업데이트
            if curr.key == key:
                curr.value = value
                return
            # 특정 노드에 key 값 없으면 다음 linked list의 node로 이동
            curr = curr.next
            
        # 같은 key 노드 없을 경우 새 노드를 구성 및 연결
        # 버킷[idx] ➔ [새로운 노드] ➔ [기존 노드 A] ➔ [기존 노드 B] ➔ None 형태로 연결 (새 노드를 가장 앞에)
        new_node = HashNode(key, value)
        new_node.next = self.buckets[idx]
        self.buckets[idx] = new_node
        self.size_ += 1

    def get(self, key: str):
        # key에 맞는 value 반환
        idx = self._hash(key)
        curr = self.buckets[idx] # 해당 버킷의 첫 번째 노드 가져옴 (linked list 형태)
        while curr: #linked list 순회
            if curr.key == key:
                return curr.value
            curr = curr.next
        return None #key가 존재하지 않으면 None 반환
    
    def remove(self, key: str) -> bool:
        # 키-값 쌍 삭제. 성공 시 True, 실패 시 False 반환
        idx = self._hash(key)
        curr = self.buckets[idx]
        prev = None
        while curr: # linked list 순회
            if curr.key == key: # 삭제할 key 찾았을 때
                if prev: # 삭제할 노드가 linked list 중간에 있을 때
                    prev.next = curr.next # 이전 노드가 삭제할 노드의 다음 노드를 가리키도록 연결
                else: # 삭제할 노드가 linked list 맨 앞에 있을 때
                    self.buckets[idx] = curr.next # 버킷[idx]이 삭제할 노드의 다음 노드를 가리키도록 연결
                self.size_ -= 1
                return True # 삭제 성공
            prev = curr
            curr = curr.next
        return False # key가 존재하지 않으면 False 반환

    def contains(self, key: str) -> bool:
        return self.get(key) != None
                
    def size(self) -> int:
        return self.size_

    def _resize(self):
        #버킷이 0.75정도 찼을때 크기를 2배 늘리고 다시 해싱
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size_ = 0

        # old_buckets의 모든 노드를 새로운 buckets에 다시 해싱하여 삽입
        for bucket in old_buckets:
            curr = bucket
            while curr:
                self.put(curr.key, curr.value)
                curr = curr.next
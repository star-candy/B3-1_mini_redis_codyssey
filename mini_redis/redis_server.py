import time
from dll import DoubleyLinkedList, Node
from hashmap import HashMap
from heap import MinHeap

class MiniRedis:
    def __init__(self):
        self.store = HashMap() # key -> (value 저장)
        self.lru = DoubleyLinkedList() # LRU :잘 찾지 않는 데이터 정리 전략
        self.ttl_map = HashMap() # key -> expire_time 저장, 실제 ttl get, set 용도
        self.ttl_heap = MinHeap() # (expire_time, key) 저장, ttl 만료 확인 용도

        self.used_memory = 0
        self.maxmemory = 0
        self.evicted_key = 0 # memory 초과로 인해 방출된 키 갯수

    def _get_bytes_len(self, s: str) -> int: # byte 크기 * 글자 수 반환
        return len(s.encode('utf-8')) 

    def _cleanup_expired(self):
        # heap을 검사하여 ttl 만료 요소를 제거함.
        now = time.time()
        while self.ttl_heap.size() > 0:
            expire_at, key = self.ttl_heap.peek() # 가장 작은 값을 확인
            if expire_at <= now: # ttl 만료된 경우
                self.ttl_heap.pop() # heap에서 제거
            
                actual_expire = self.ttl_map.get(key) #  ttl_map에서도 ttl 받아온 뒤 제거
                if actual_expire is not None and actual_expire <= now:
                    self._delete_entry(key)
            else:
                break # heap root부터 확인하므로 ttl 만료가 아니라면 heap 전체가 만료되지 않음


        
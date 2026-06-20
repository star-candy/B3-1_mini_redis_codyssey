
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

    def _check_and_remove_if_expired(self, key: str) -> bool:
        "키 만료여부 확인, 만료 시 삭제"
        expire_at = self.ttl_map.get(key) # expire time 받아오기
        if expire_at is not None and expire_at <= time.time(): # 만료시
            self._delete_entry(key)
            return True
        return False
    
    def _delete_entry(self, key: str):
        # 해당 키와 관련된 모든 자료구조 삭제, 메모리 차감
        node = self.store.get(key)
        if node:
            self.used_memory -= (self._get_bytes_len(node.key) + self._get_bytes_len(node.value))
            self.lru.remove_node(node)
            self.store.remove(key)
        self.ttl_map.remove(key)

    def _enforce_enviction(self):
        # maxmem 초과시 lru 노드 제거
        if self.maxmemory <= 0:
            return
        # maxmemory 초과 및 lru 리스트에 데이터 존재시 lru 제거
        while self.used_memory > self.maxmemory and self.lru.tail.prev != self.lru.head:
            lru_node = self.lru.tail.prev #가장 사용되지 않은 데이터
            self._delete_entry(lru_node.key) # 해당 데이터 제거
            self.evicted_key += 1 # evict key 수 증가

    def config_set(self, param: str, value: str):
        if param.lower() == "maxmemory":
            try:
                val = int(value)
                if val < 0:
                    raise ValueError
                self.maxmemory = val # maxmemory 설정
                self._enforce_enviction() # maxmem 초과시 데이터 삭제
                return "OK"
            except ValueError:
                return "(error) 입력값이 양의 정수 형태가 아닙니다"
        return "(error) 지원하지 않는 파라미터 입니다."

    def info_memory(self) -> str: # 메모리 관련 정보 return
        return f"used_memory:{self.used_memory}\nmaxmemory:{self.maxmemory}\nevicted_keys:{self.evicted_key}"
        
    def set(self, key: str, value: str):
        self._cleanup_expired() # 데이터 추가 전 만료된 데이터 제거
        entry_size = self._get_bytes_len(key) + self._get_bytes_len(value) # 추가 메모리 길이

        # 추가 단일 데이터 크기가 maxmem을 초과하는 경우
        if 0 < self.maxmemory < entry_size:
            return "(error) maxmemory 초과, 저장 불가능"

        self._check_and_remove_if_expired(key) # key가 이미 존재하는 경우, 만료시간 확인 후 삭제

        if self.store.contains(key): # key가 이미 존재하는 경우, value 덮어쓰고 메모리 재계산
            node = self.store.get(key)
            self.used_memory -= (self._get_bytes_len(node.value)) # 기존 value 메모리 차감
            node.value = value # 새 value 저장
            self.used_memory += self._get_bytes_len(value) # 새 value 메모리 추가
            self.lru.move_to_front(node) # lru 업데이트
            self.ttl_map.remove(key) # 기존 ttl 초기화
        else: # 새로운 키 key인 경우 
            node = Node(key, value)
            self.store.put(key, node)
            self.lru.insert_front(node)
            self.used_memory += entry_size
        
        self._enforce_enviction() # put후 메모리 초과시 lru 제거
        return "OK"

    def get(self, key: str):
        self._cleanup_expired()
        # 해당 데이터 만료, 혹은 미존재 경우
        if self._check_and_remove_if_expired(key) or not self.store.contains(key):
            return "(nil)"

        node = self.store.get(key)
        self.lru.move_to_front(node) # 해당 노드를 맨앞으로
        return f'"{node.value}"'
        
    def delete(self, key: str):
        self._cleanup_expired()
        # 해당 키 존재하지 않는 경우
        if self._check_and_remove_if_expired(key) or not self.store.contains(key):
            return "(integer) 0" 
        self._delete_entry(key)
        return "(integer) 1"
            
    def exist(self, key: str):
        self._cleanup_expired()
        if self._check_and_remove_if_expired(key) or not self.store.contains(key):
            return "(integer) 0"
        return "(integer) 1"

    def dbsize(self):
        self._cleanup_expired()
        return f"(integer) {self.store.size()}"

    def keys(self):
        self._cleanup_expired()
        all_keys = self.store.keys()
        # 모든 키 중 만료된 것 제외
        valid_keys = [k for k in all_keys if not self._check_and_remove_if_expired(k)]

        if not valid_keys:
            return "(empty array)"
            
        return '\n'.join(f'{i+1}"{k}"' for i, k in enumerate(valid_keys))
            
    def expire(self, key:str, seconds: str):
        # ttl 업데이트
        self._cleanup_expired()
        try:
            sec = int(seconds)
        except ValueError:
            return "(error) 입력값이 정수가 아닙니다."
            
        if self._check_and_remove_if_expired(key) or not self.store.contains(key):
            return "(integer) 0" # 동작 미수행 종료
            
        if sec <= 0: # 0초이하이면 즉시 제거
            self._delete_entry(key)
            return "(integer) 1" # 정상적으로 제거

        expire_at = time.time() + sec
        self.ttl_map.put(key, expire_at) # ttl_map에 expire_at 수정 (기존 키값 존재시 덮어쓰기)
        self.ttl_heap.push((expire_at, key)) # ttl_heap에 expire_at 수정 (기존 키값 존재시 덮어쓰기)
        return "(integer) 1" # 정상적으로 저장

    def ttl(self, key: str):
        # ttl 확인
        self._cleanup_expired()
        if self._check_and_remove_if_expired(key) or not self.store.contains(key):
            return "(integer) -2" # 동작 미수행 종료
            
        expire_at = self.ttl_map.get(key)
        if expire_at is None:
            return "(integer) -1" # ttl 미설정
            
        remain = int(expire_at - time.time())
        return f"(integer) {remain if remain > 0 else 0}" # 음수일 경우 0반환
        
        
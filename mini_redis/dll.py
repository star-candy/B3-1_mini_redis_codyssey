class Node:
    # 이중 연결 리스트용 노드
    # prev, next 포인터를 가지고 있어야 함
    def __init__(self, key = None, value = None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class DoubleyLinkedList:
    def __init__(self):
        # 초기 이중 연결 리스트 구성
        # head가 tail을, tail은 head를 바라보는 형태
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def insert_front(self, node: Node):
        # head 뒤에 node 추가
        # 즉 새로 추가된 node의 next, prev, head의 next, 기존 head 뒤에 있던 node의 prev 수정 필요

        #[HEAD] <--> [TAIL]
        # 노드 추가
        #[HEAD] <--> [Node1] <--> [TAIL]

        # 새로 추가된 node의 next prev 연결
        node.next = self.head.next #기존 head 뒤에 있던 노드가 추가된 노드의 뒤로 가도록
        node.prev = self.head # head는 추가된 노드의 앞이 됨
        
        self.head.next.prev = node #기존 head 뒤에 있던 노드의 앞이 추가된 노드가 됨
        self.head.next = node #head 뒤에 노드를 추가하고, head가 앞으로 감
    
    def remove_node(self, node: Node):
        # head와 tail을 이중 연결 리스트 뼈대로 사용중
        # 따라서 해당 노드가 제거되지 않도록 구성
        if node.prev and node.next:
            # 제거 대상 노드와 prev, next 노드간 연결 제거
            node.prev.next = node.next
            node.next.prev = node.prev
            # 제거 대상 노드의 포인터 초기화
            node.prev = None
            node.next = None
            
    def move_to_front(self, node: Node):
        # 특정 노드를 가장 앞(head 뒤)으로 이동
        # 제거 후 다시 추가하는 방식
        self.remove_node(node)
        self.insert_front(node)
        

    def remove_back(self) -> Node:
        # tail 앞의 노드를 제거하고 반환
        if self.tail.prev == self.head: #내부 값이 없는 초기 이중 리스트 경우
            return None
        lru_node = self.tail.prev # 가장 오래된 노드 가리키는 prev 값 할당
        self.remove_node(lru_node) 
        return lru_node

   
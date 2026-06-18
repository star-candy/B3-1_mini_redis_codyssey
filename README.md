## 1. double linked list란?
- ![alt text](images/image.png)
#### 각 노드가 앞 뒤 노드에 대한 포인터를 가지고 있어 양방향 탐색이 가능한 리스트 
- 단순 연결 리스트의 경우 삽입, 삭제를 위해 앞 노드에 대한 주소 필요
    - 해당 주소 얻기 위해 처음부터 다시 search해야 하는 비효율성 존재
- 이중 연결 리스트는 각 노드가 prev, next 포인터를 가지고 있어 양방향 탐색 가능
    - 따라서 삽입, 삭제 시 앞 노드뿐만 아니라 뒤 노드에 대한 주소도 알고 있어 효율적으로 삽입, 삭제 가능

## 1-1. double linked list 구성
- head와 tail은 가상의 노드로 실제 데이터 저장 안 함
    - head와 tail 노드를 이중 연결 리스트를 구성하는 골격으로 사용.
    - 초기 이중 연결 리스트 구성 : head <--> tail

## 2. hash map이란?
- ![alt text](images/image1.png)
- key-value 쌍을 저장하는 자료구조로, key를 통해 value에 빠르게 접근 가능 (map 구조)
    - key-value 쌍 형태의 저장 방식인 map을 구현한 것.
    - key는 중복 저장될 수 없음
    - 동일 키로 put 작업 시 기존 값 대신 새로운 값으로 대체


- hash function을 통해 key 값을 해시 값으로 변환하여 배열의 인덱스로 사용
    - map 객체가 저장될 위치를 hash function을 통해 결정.
    - 단 키가 다름에도 hash function이 같은 인덱스를 반환할 경우 해시 충돌 (collision) 발생


## 2-1. 충돌(collision) 해결방안 chained hashing
- ![alt text](images/image2.png)
- 같은 hash 값을 가지는 key-value 쌍들을 linked list 형태로 관리
    - 1차원 배열형태 bucket에 linked list 형태의 데이터를 저장
    - 즉, hash map의 index에 해당하는 bucket에 linked list가 저장되는 방식
    - 충돌이 발생한다면 동일 bucket에 linked list를 연결하는 방식으로 해결 가능

## 3. heap (min-heap) 구조란?
![alt text](images/image3.png)
- 완전 이진트리를 기초로 하는 자료구조
    - leaf node를 제외한 모든 노드는 left, right 자식을 가져야 함.
    - min heap의 경우 부모 노드가 자식 노드 값보다 항상 작아야 함.

- 코드상에서는 heap은 일차원 배열 형태로 구성됨
    - root 노드는 0번
    - 왼쪽 자식노드는 i*2 + 1
    - 오른쪽 자식 노드는 i*2 + 2
    - 부모 노드는 (i-1)//2

## 3-1. 삽입, 삭제 시 힙 재구조화 (reheapification)
- 삽입 과정
    - 임의의 노드를 min heap의 오른쪽 끝에 추가
    - 본인이 부모 노드보다 작은지 여부를 확인하며 위로 올라가며 재배치
- ![alt text](images/image4.png)

- root node가 삭제된 경우
    - 오른쪽 끝에 있던 노드를 root 노드 위치로 이동
    - 해당 노드가 자식보다 큰지 여부를 확인하며 아래로 재배치
- ![alt text](images/image5.png)
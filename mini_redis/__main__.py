import sys
from redis_server import MiniRedis

def parse_line(line: str) -> list:
# 따옴표 포함 문자열을 하나의 인자로 파싱
    tokens = [] # 반환할 문자열 리스트
    curr = [] # 현재 파싱중인 문자열
    in_quotes = False # 따옴표 안인지 아닌지 판단

    for char in line:
        if char == '"': # 따옴표 만나면
            in_quotes = not in_quotes
        elif char == ' ' and not in_quotes: # 공백 + 따옴표 안이 아니라면 해당 문자열 파싱
            if curr:
                tokens.append("".join(curr)) # 문자열로 변환해 tokens에 저장
                curr = [] # 현재 문자열 리스트 초기화
        else: # 따옴표 내부라면 현재 문자열 리스트에 추가
            curr.append(char)

    if curr:
        tokens.append("".join(curr)) 
    return tokens

def main():
    db = MiniRedis()

    while True:
        try:
            line = input("mini-redis> ").strip()
            if not line:
                continue

            tokens = parse_line(line)
            if not tokens:
                continue

            cmd = tokens[0].upper()
            args = tokens[1:]

            if cmd in ("QUIT", "EXIT"): # redis 종료 문자
                break

            elif cmd == "SET": #key, value 저장
                if len(args) != 2:
                    print("(error) SET 커멘드는 key, value 2개의 argument가 필요합니다.")
                else:
                    print(db.set(args[0], args[1]))
            
            elif cmd == "GET": # value 반환
                if len(args) != 1:
                    print("(error) GET 커멘드는 1개의 argument가 필요합니다.")
                else:
                    print(db.get(args[0]))

            elif cmd == "DEL":
                if len(args) != 1:
                    print("(error) DEL 커멘드는 1개의 argument가 필요합니다.")
                else:
                    print(db.delete(args[0]))

            elif cmd == "EXISTS": # key 존재 확인
                if len(args) != 1:
                    print("(error) EXISTS 커멘드는 1개의 argument가 필요합니다.")
                else:
                    print(db.exists(args[0]))

            elif cmd == "DBSIZE": # 저장된 key 갯수 반환
                if len(args) != 0:
                    print("(error) DBSIZE 커멘드는 0개의 argument가 필요합니다.")
                else:
                    print(db.dbsize())

            elif cmd == "KEYS": # 저장된 모든 키 반환
                if len(args) != 0:
                    print("(error) KEYS 커멘드는 0개의 argument가 필요합니다.")
                else:
                    print(db.keys())

            elif cmd == "CONFIG": # 설정 변경
                if len(args) != 3 or args[0].upper() != "SET":
                    print("(error) CONFIG SET 커멘드는 3개의 argument가 필요합니다.")
                else:
                    print(db.config_set(args[1], args[2]))

            elif cmd == "INFO": # 메모리 정보 반환
                if len(args) != 1 or args[0].lower() != "memory":
                    print("(error) INFO memory 커멘드는 1개의 argument가 필요합니다.")
                else:
                    print(db.info_memory())

            elif cmd == "EXPIRE": # 특정 키에 대한 TTL(유통기한) 설정
                if len(args) != 2:
                    print("(error) EXPIRE 커멘드는 2개의 argument가 필요합니다.")
                else:
                    print(db.expire(args[0], args[1]))

            elif cmd == "TTL": # 키의 남은 유통기한 반환
                if len(args) != 1:
                    print("(error) TTL 커멘드는 1개의 argument가 필요합니다.")
                else:
                    print(db.ttl(args[0]))
            
            else:
                print(f"(error) ERR unknown command '{cmd}'")

        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            print(f"(error) ERR internal server error: {str(e)}")

if __name__ == "__main__":
    main()

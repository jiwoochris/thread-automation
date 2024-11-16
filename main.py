from MetaThreads.metathreads import MetaThreads
from MetaThreads.metathreads import config
import time

from MetaThreads.metathreads.exceptions import ChallengeRequiredException, LoginFailedException, ResponseErrorException, URLGenerationError

def get_credentials():
    username = input("아이디를 입력하세요: ")
    password = input("비밀번호를 입력하세요: ")
    return username, password

def login_with_retries(threads: MetaThreads, max_retry: int =3) -> str | None:
    retries = 0
    while retries < max_retry:
        username, password = get_credentials()

        try:
            if threads.login(username, password):
                print("로그인 성공!")
                return username
            
        except ChallengeRequiredException as e:
            print(f"""[2단계 인증이 필요합니다.] 2가지 중 1가지 방법을 통해 2단계 인증을 완료하고 다시 로그인 해주세요.
1. 다음 링크에서 인증을 완료해주세요: {e.challenge_url}
2. 모바일로 인스타그램 계정에 로그인 하고 인증을 완료해주세요.""")
            retries += 1
        except LoginFailedException:
            print("로그인에 실패했습니다. 다시 시도해주세요.")
            retries += 1
        except URLGenerationError as e:
            print(f"URL 생성 에러: {e.message}")
            retries += 1
        except ResponseErrorException as e:
            print(f"응답 에러: {e.message}")
            retries += 1
        except Exception as e:
            print(f"로그인에 실패했습니다. 다시 시도해주세요. 에러: {e}")
            retries += 1

        print(f"남은 시도 횟수: {max_retry - retries}\n")
        time.sleep(3)
            
    return None

def extract_usernames(data):
    usernames = []
    for user_list in data:
        for user in user_list['users']:
            usernames.append(user['username'])
    return usernames


def main():
    
    print("[로그인]")
    
    threads = MetaThreads()

    username = login_with_retries(threads)
    if username is None:
        print("로그인 실패. 프로그램을 종료합니다.")
        return


    # check logged in user
    print(f"User {threads.me['username']}({threads.me['full_name']}) -> 로그인 완료")
    print("===================================================================")


    followers = threads.get_user_friends(username, followers=True)
    followers = extract_usernames(followers["data"])

    print(f"[팔로워 명단] -> 나를 팔로우 하는 (총 {len(followers)}명)")
    print(followers)
    print("===================================================================")

    followings = threads.get_user_friends(username, following=True)
    followings = extract_usernames(followings["data"])

    print(f"[팔로잉 명단] -> 내가 팔로잉 하는 (총 {len(followings)}명)")
    print(followings)
    print("===================================================================")

    unfollowers = set(followings) - set(followers)

    print(f"[나를 언팔한 사람들] -> 총 {len(unfollowers)}명")
    print(unfollowers)
    print("===================================================================")

    unfollowing_unfollowers = input("나를 언팔 한 사람들을 모두 삭제하시겠습니까? (Y/n): ")

    if unfollowing_unfollowers.lower() == 'y':
        
        for unfollower in unfollowers:
            threads.unfollow(unfollower)
            print(f"{unfollower}님을 언팔로우 했습니다.")

            time.sleep(3)
        
        print("언팔로우 작업이 완료되었습니다.")
    else:
        print("언팔로우 작업을 취소합니다.")

    input("프로그램을 종료합니다. (아무 키나 눌러 프로그램을 종료)")



if __name__ == "__main__":
    main()

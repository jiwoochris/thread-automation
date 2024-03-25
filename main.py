from metathreads import MetaThreads
from metathreads import config
import time

def get_credentials():
    username = input("아이디를 입력하세요: ")
    password = input("비밀번호를 입력하세요: ")
    return username, password

def extract_usernames(data):
    usernames = []
    for user_list in data:
        for user in user_list['users']:
            usernames.append(user['username'])
    return usernames


def main():
    
    print("[로그인]")
    username, password = get_credentials()

    #config.TIMEOUT = 5
    #config.PROXY = {'http': 'proxy_here', 'https': 'proxy_here'}
    
    threads = MetaThreads()

    if not all([username, password]):
        username = str(input("유저 아이디 혹은 이메일을 입력해주세요. :"))
        password = str(input("비밀번호를 입력해주세요. :"))
    threads.login(username, password)

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

            time.sleep(5)
        
        print("언팔로우 작업이 완료되었습니다.")
    else:
        print("언팔로우 작업을 취소합니다.")


if __name__ == "__main__":
    main()

import pandas as pd

#챗봇 모델 만들기
class Lev_ChatBot:
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)
        
    def load_data(self, filepath):
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()  # 질문열만 뽑아 파이썬 리스트로 저장
        answers = data['A'].tolist()   # 답변열만 뽑아 파이썬 리스트로 저장
        return questions, answers #질문과 답변 반환 
    
    def find_best_answer(self, input_sentence): #질문을 받음
        distances = [lev_distance(input_sentence, question) for question in self.questions] #질문열에 있는 질문들과 내가 입력한 질문의 거리 계산
        best_match_index = distances.index(min(distances)) #위 거리들 리스트 중 가장 작은 거리를 best_match_inde로 반환
        return self.answers[best_match_index] #질문과 가장 유사한 답변 반환

#레벤슈타인 거리 구하기 
def lev_distance(a, b):
    if a == b: return 0 # a와 b가 같으면 0을 반환 
    a_len = len(a) # a 길이 선언
    b_len = len(b) # b 길이 선언
    if a =="": return b_len #a가 공백이면 b_len을 반환
    if b =="": return a_len #b가 공백이면 a_len을 반환
    matrix = [[] for _ in range(a_len + 1)] # matrix생성. 리스트를 사용하여 1차원 초기화
    for i in range(a_len + 1): # 0으로 초기화
        matrix[i] = [0 for _ in range(b_len + 1)]  # 리스트를 사용하여 2차원 초기화
    # 0일 때 초깃값을 설정 후 행렬 채우기 
    for i in range(a_len + 1):
        matrix[i][0] = i
    for j in range(b_len + 1):
        matrix[0][j] = j
    for i in range(1, a_len + 1):
        ac = a[i - 1]
        for j in range(1, b_len + 1):
            bc = b[j - 1] 
            cost = 0 if (ac == bc) else 1  
            matrix[i][j] = min([
                matrix[i - 1][j] + 1,     # 문자 제거: 위쪽 수에서 +1
                matrix[i][j - 1] + 1,     # 문자 삽입: 왼쪽 수에서 +1   
                matrix[i - 1][j - 1] + cost # 문자 변경: 대각선에서 +1, 문자가 동일하면 대각선 숫자 복사
            ])
    return matrix[a_len][b_len] #비교한 결과 리턴


# 학습데이터 불러오기
filepath = 'ChatbotData.csv'

# 챗봇 인스턴스 생성
chatbot = Lev_ChatBot(filepath)
# '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    response = chatbot.find_best_answer(input_sentence)
    print('Lev_Chatbot:', response)
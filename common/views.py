from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from test_info.models import TasteTestQuestion, TasteTestAnswer
from rest_framework.response import Response

# 파일을 불러와서 바로 등록하는 방법도 있지만 그 파일을 또 만들어야 하는 상황이라
# 시간 관계상 조금이라도 빠르게 할 수 있는 방법으로 함.
# 추후 다시 입력해야 하는 일이 생긴다면 그때 파일에서 읽어서 입력하는 방식으로 수정 예정

# fmt: off
class BulkCreateTasteQuestionView(APIView):
    @extend_schema(tags=["Utils BE전용"])
    def post(self, request):
        # 데이터 리스트 생성
        data = [
            TasteTestQuestion(taste_question='불닭볶음면을 먹고 난 당신의 모습은?', taste_question_category='spicy'),
            TasteTestQuestion(taste_question='당신의 혀는 어떤 파티를 좋아하나요?', taste_question_category='intensity'),
            TasteTestQuestion(taste_question='당신의 위장은 어떤 차와 비슷한가요?', taste_question_category='oily'),
            TasteTestQuestion(taste_question='당신의 주식 취향을 동물로 표현한다면?', taste_question_category='flour_rice'),
            TasteTestQuestion(taste_question='당신의 지갑이 음식에게 하는 말은?', taste_question_category='cost'),
            TasteTestQuestion(taste_question='매운 맛이 없으면 인생도 심심해! 매운 음식은 내 삶의 원동력이야.', taste_question_category='spicy_weight'),
            TasteTestQuestion(taste_question='맛있으면 0 칼로리, 비싸면 0 원이라 나는 믿어. 가성비보다 가심비!', taste_question_category='cost_weight'),
        ]
        TasteTestQuestion.objects.bulk_create(data)

        return Response("성공")

class BulkCreateTasteAnswerView(APIView):
    @extend_schema(tags=["Utils BE전용"])
    def post(self, request):
        # 데이터 리스트 생성
        data = [
            TasteTestAnswer(taste_answer='냄새만 맡아도 매워...',                   taste_score=1, taste_question_id=15),
            TasteTestAnswer(taste_answer='도서관 독서모임 수준의 순한맛',            taste_score=1, taste_question_id=16),
            TasteTestAnswer(taste_answer='경차: 기름기 없는 깔끔한 음식만',          taste_score=1, taste_question_id=17),
            TasteTestAnswer(taste_answer='빵 먹는 비둘기: 밀가루 음식만 찾아요',      taste_score=1, taste_question_id=18),
            TasteTestAnswer(taste_answer='3,000원의 행복을 찾아줘',                 taste_score=1, taste_question_id=19),
            TasteTestAnswer(taste_answer='전혀그렇지않다',                          taste_score=1, taste_question_id=20),
            TasteTestAnswer(taste_answer='매우 그렇다',                            taste_score=1, taste_question_id=21),
            TasteTestAnswer(taste_answer='냉장고 문을 붙잡고 우유를 들이킴',      taste_score=2, taste_question_id=15),
            TasteTestAnswer(taste_answer='조용한 카페 브런치 정도의 은은한 맛',  taste_score=2, taste_question_id=16),
            TasteTestAnswer(taste_answer='세단: 약간의 기름기는 OK',  taste_score=2, taste_question_id=17),
            TasteTestAnswer(taste_answer='피자 좋아하는 닌자 거북이: 밀가루 위주지만 가끔 밥도', taste_score=2, taste_question_id=18),
            TasteTestAnswer(taste_answer='적당히 먹고 남겨줘',      taste_score=2, taste_question_id=19),
            TasteTestAnswer(taste_answer='그렇지 않다',       taste_score=2, taste_question_id=20),
            TasteTestAnswer(taste_answer='그런편이다',        taste_score=2, taste_question_id=21),
            TasteTestAnswer(taste_answer='빨개진 얼굴로 땀을 닦아내며 "맛있다" 중얼거림', taste_score=3, taste_question_id=15),
            TasteTestAnswer(taste_answer='신나는 클럽 파티처럼 활기찬 맛', taste_score=3, taste_question_id=16),
            TasteTestAnswer(taste_answer='SUV: 적당히 기름진 음식도 거뜬해요', taste_score=3, taste_question_id=17),
            TasteTestAnswer(taste_answer='잡식성 판다: 밥이든 빵이든 다 좋아요', taste_score=3, taste_question_id=18),
            TasteTestAnswer(taste_answer='맛있다면 가격은 상관없어', taste_score=3, taste_question_id=19),
            TasteTestAnswer(taste_answer='보통', taste_score=3, taste_question_id=20),
            TasteTestAnswer(taste_answer='보통', taste_score=3, taste_question_id=21),
            TasteTestAnswer(taste_answer='"이 정도야~" 하며 여유롭게 먹음',        taste_score=4, taste_question_id=15),
            TasteTestAnswer(taste_answer='락 페스티벌급 강렬한 맛',    taste_score=4, taste_question_id=16),
            TasteTestAnswer(taste_answer='트럭: 기름진 음식도 문제없이 소화해요',    taste_score=4, taste_question_id=17),
            TasteTestAnswer(taste_answer='밥 좋아하는 햄스터: 밥 위주지만 가끔 빵도',   taste_score=4, taste_question_id=18),
            TasteTestAnswer(taste_answer='FLEX! 오늘은 다 쏜다',        taste_score=4, taste_question_id=19),
            TasteTestAnswer(taste_answer='그런편이다',         taste_score=4, taste_question_id=20),
            TasteTestAnswer(taste_answer='그렇지 않다',          taste_score=4, taste_question_id=21),
            TasteTestAnswer(taste_answer='불의 정령이 되어 용암을 마시는 중',         taste_score=5, taste_question_id=15),
            TasteTestAnswer(taste_answer='우주 폭발 수준의 극강의 맛',     taste_score=5, taste_question_id=16),
            TasteTestAnswer(taste_answer='우주선: 기름 범벅이어도 끄떡없어요',     taste_score=5, taste_question_id=17),
            TasteTestAnswer(taste_answer='쌀만 고집하는 황새: 무조건 밥이어야 해요',    taste_score=5, taste_question_id=18),
            TasteTestAnswer(taste_answer='여기 카드 줄 테니 맘껏 써',         taste_score=5, taste_question_id=19),
            TasteTestAnswer(taste_answer='매우 그렇다',          taste_score=5, taste_question_id=20),
            TasteTestAnswer(taste_answer='전혀그렇지않다',           taste_score=5, taste_question_id=21),
        ]
        TasteTestAnswer.objects.bulk_create(data)

        return Response("성공")

    # fmt: on

import numpy as np


def calculate_weights(user):
    # 본 특성 7개 + 필터 옵션 6개의 모든 가중치를 기본값 1로 처리
    weights = np.ones(13)

    # 매운맛 선호도 가중치
    if user.spicy_weight in [1, 5]:
        weights[0] = 1.3
    elif user.spicy_weight in [2, 4]:
        weights[0] = 1.0
    else:
        weights[0] = 0.5

    # 음식 강도는 기본값 유지

    # 기름기 선호도 가중치
    if user.oily_preference in [1, 2]:
        weights[2] = 1.5
    else:
        weights[2] = 1.2

    # 탄수화물 선호도 가중치
    if user.flour_rice_preference in [1, 5]:
        weights[3] = 1.3
    else:
        weights[3] = 1.0

    # 가격 민감도 가중치
    if user.cost_weight in [1, 2]:
        weights[4] = 0
    elif user.cost_weight == 3:
        weights[4] = 0.8
    elif user.cost_weight == 4:
        weights[4] = 1.0
    else:
        weights[4] = 1.3

    # 매운맛 가중치
    weights[5] = user.spicy_weight

    # 가격 가중치
    weights[6] = user.cost_weight

    return weights
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from .models import Food


def calculate_weights(user_preferences, spicy_weight, cost_weight):
    # 본 특성 7개 + 필터 옵션 6개의 모든 가중치를 기본값 1로 처리
    weights = np.ones(12)

    # 매운맛 선호도 가중치
    if spicy_weight in [1, 5]:
        weights[0] = 1.3
    elif spicy_weight in [2, 4]:
        weights[0] = 1.0
    else:
        weights[0] = 0.5

    # 음식 강도는 기본값 유지

    # 기름기 선호도 가중치
    if user_preferences[2] in [1, 2]:
        weights[2] = 1.5
    else:
        weights[2] = 1.2

    # 탄수화물 선호도 가중치
    if user_preferences[3] in [1, 5]:
        weights[3] = 1.3
    else:
        weights[3] = 1.0

    # 가격 민감도 가중치
    if cost_weight in [1, 2]:
        weights[4] = 0
    elif cost_weight == 3:
        weights[4] = 0.8
    elif cost_weight == 4:
        weights[4] = 1.0
    else:
        weights[4] = 1.3

    # 매운맛 가중치
    weights[5] = spicy_weight

    # 가격 가중치
    weights[6] = cost_weight

    return weights


def calculate_filters(user_preferences, filters):
    filtered_prefs = np.zeros(12)
    filtered_prefs[:5] = user_preferences

    # 필터 중 하나라도 True이면 적용
    # 전부 False면 기본
    if any(filters.values()):
        if filters.get("is_lunch", True):
            filtered_prefs[5] = 1
        if filters.get("is_dinner", True):
            filtered_prefs[6] = 1
        if filters.get("is_snack", True):
            filtered_prefs[7] = 1
        if filters.get("is_date", True):
            filtered_prefs[8] = 1
        if filters.get("is_party", True):
            filtered_prefs[9] = 1
        if filters.get("is_diet", True):
            filtered_prefs[10] = 1

    return filtered_prefs


def recommend_foods(user_preferences, weights, filters, recommends_cnt):
    filtered_user_preferences = calculate_filters(user_preferences, filters)
    weighted_user_prefs = filtered_user_preferences * weights

    recommends = {}

    foods = Food.objects.all()

    for food in foods:
        # 음식의 특성 배열을 만듦
        food_prefs = np.array(
            [
                food.spicy_preference,
                food.intensity_preference,
                food.oily_preference,
                food.flour_rice_preference,
                food.cost_preference,
                int(food.is_lunch),
                int(food.is_dinner),
                int(food.is_snack),
                int(food.is_date),
                int(food.is_party),
                int(food.is_diet),
                food.id
            ]
        )

        # 매운맛과 가격이 사용자의 최대 허용치를 초과하면 건너뛰기
        if food_prefs[0] > user_preferences[0] or food_prefs[4] > user_preferences[4]:
            continue

        # 필터 조건 확인 (필터가 적용된 경우)
        if any(filters.values()) and not (
            (filters.get("is_lunch") and food.is_lunch)
            or (filters.get("is_dinner") and food.is_dinner)
            or (filters.get("is_snack") and food.is_snack)
            or (filters.get("is_date") and food.is_date)
            or (filters.get("is_party") and food.is_party)
            or (filters.get("is_diet") and food.is_diet)
        ):
            continue

        weighted_food_prefs = np.array(food_prefs) * weights
        sim = cosine_similarity(
            weighted_user_prefs.reshape(1, -1), weighted_food_prefs.reshape(1, -1)
        )[0][0]
        recommends[food] = sim

    sorted_foods = sorted(recommends.items(), key=lambda x: x[1], reverse=True)
    return sorted_foods[:recommends_cnt]

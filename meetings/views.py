from django.db.models import Case, IntegerField, Value, When
from django.utils import timezone
from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from categories.models import (
    Location,
    MeetingAgeGroup,
    MeetingGenderGroup,
    MeetingPaymentMethod,
    TimeSortCategory,
)
from categories.serializers import LocationSerializer, TimeCategorySerializer
from profiles.views import UserLikedMeetingView
from users.models import CustomUser

from .models import Meeting, MeetingMember
from .serializers import (
    JoinMeetingMemberSerializer,
    MeetingCreateSerializer,
    MeetingDetailSerializer,
    MeetingListSerializer,
    MeetingMemberSerializer,
    MeetingUpdateSerializer,
)


class MeetingListView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        tags=["meeting"],
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="MeetingListResponse",
                    fields={
                        "meetings": MeetingListSerializer(many=True),
                        "time_categories": TimeCategorySerializer(many=True),
                        "location_categories": LocationSerializer(many=True),
                    },
                )
            )
        },
        operation_id="meeting_list",
    )
    def get(self, request):
        # meeting_time이 현 시간보다 크거나 같아야 한다.
        meetings = Meeting.objects.filter(meeting_time__gt=timezone.now()).order_by(
            "-created_at"
        )

        time_categories = TimeSortCategory.objects.order_by(
            Case(
                When(sort_name="가장 가까운순", then=Value(0)),
                defalut=Value(1),
                output_field=IntegerField(),
            )
        )
        location_categories = Location.objects.order_by(
            Case(
                When(location_name="전체", then=Value(0)),
                defalut=Value(1),
                output_field=IntegerField(),
            )
        )

        # 시리얼라이저로 데이터를 시리얼라이즈
        meeting_data = MeetingListSerializer(meetings, many=True).data
        time_sort_data = TimeCategorySerializer(time_categories, many=True).data
        location_data = LocationSerializer(location_categories, many=True).data

        # 결합된 데이터 생성
        meeting_list = {
            "meetings": meeting_data,
            "time_categories": time_sort_data,
            "location_categories": location_data,
        }

        return Response(meeting_list, status=status.HTTP_200_OK)


# 미팅 리스트 필터링 요청시 응답할 API
class FilterMeetingListView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = MeetingListSerializer

    @extend_schema(tags=["meeting"])
    def get(self, request, time_category, location_category):

        location_category_id = Location.objects.get(location_name=location_category).id

        if location_category == "전체":
            meetings = Meeting.objects.all()
        else:
            meetings = Meeting.objects.filter(location_id=location_category_id)

        if time_category == "최신순":
            meetings = meetings.filter(meeting_time__gt=timezone.localtime()).order_by(
                "-created_at"
            )
        else:
            meetings = meetings.filter(meeting_time__gt=timezone.localtime()).order_by(
                "meeting_time"
            )

        serializer = self.serializer_class(instance=meetings, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# 번개 게시물 디테일 조회
class MeetingDetailView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        tags=["meeting"],
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="MeetingDetailResponse",
                    fields={
                        "meeting": MeetingDetailSerializer(),
                        "meeting_member": MeetingMemberSerializer(many=True),
                    },
                )
            )
        },
        operation_id="meeting_detail",
    )
    def get(self, request, uuid):
        # 리퀘스트에서 유저 정보를 확인하고
        # 유저정보가 있다면 해당 유저의 프로필에서 좋아요 정보를 확인하고
        # 요청 받은 리뷰와 동일한 uuid가 있다면 is_like = Ture반환
        # user 정보 객체
        user = request.user

        is_liked = False
        is_host = False

        try:
            selected_meeting = Meeting.objects.get(uuid=uuid)
            meeting_member_ids = MeetingMember.objects.filter(
                meeting_id=selected_meeting.id
            ).values_list("user_id", flat=True)
            meeting_member = CustomUser.objects.filter(id__in=meeting_member_ids)

            if not user.is_anonymous:
                user_liked_Meeting_view = UserLikedMeetingView()
                user_liked_Meeting_response = user_liked_Meeting_view.get(request)

                # 요청자의 좋아요 리스트에 해당 글이 있는가?
                if user_liked_Meeting_response.status_code == 200:
                    liked_review_data = user_liked_Meeting_response.data
                    for meeting in liked_review_data:
                        uuid = str(meeting.get("uuid"))
                        if uuid == str(selected_meeting.uuid):
                            is_liked = True
                            break
                # 요청자가 게시글 작성자인가?
                if user.id == selected_meeting.user_id:
                    is_host = True

        except Meeting.DoesNotExist:
            raise NotFound("The meeting does not exist")

        meeting_detail = {
            "meeting": MeetingDetailSerializer(instance=selected_meeting).data,
            "meeting_member": MeetingMemberSerializer(
                instance=meeting_member, many=True
            ).data,
            "is_liked": is_liked,
            "is_host": is_host,
        }

        # 게시물 조회 시 조회수 상승
        selected_meeting.hits += 1
        selected_meeting.save()

        return Response(meeting_detail, status=status.HTTP_200_OK)


# 번개 모임 생성
class MeetingCreateView(APIView):
    serializer_class = MeetingCreateSerializer

    @extend_schema(tags=["meeting"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        location_name = serializer.data["location_name"]
        payment_method_name = serializer.data["payment_method_name"]
        age_group_name = serializer.data["age_group_name"]
        gender_group_name = serializer.data["gender_group_name"]

        try:
            location = Location.objects.get(location_name=location_name)
            payment_method = MeetingPaymentMethod.objects.get(
                payment_method=payment_method_name
            )
            age_group = MeetingAgeGroup.objects.get(age_group=age_group_name)
            gender_group = MeetingGenderGroup.objects.get(
                gender_group=gender_group_name
            )
        except (
            Location.DoesNotExist,
            MeetingPaymentMethod.DoesNotExist,
            MeetingAgeGroup.DoesNotExist,
            MeetingGenderGroup.DoesNotExist,
        ):
            return Response(
                {"detail": "Data Not Found"}, status=status.HTTP_400_BAD_REQUEST
            )

        # 번개 모임 생성
        created_meeting = Meeting.objects.create(
            user=request.user,
            title=request.data["title"],
            location=location,
            payment_method=payment_method,
            age_group=age_group,
            gender_group=gender_group,
            meeting_time=request.data["meeting_time"],
            description=request.data.get("description"),
            meeting_image_url=request.data["meeting_image_url"],
            maximum=request.data["maximum"],
        )

        # 번개 모임을 생성 시 번개 멤버 생성하고 호스트로 만든다.
        MeetingMember.objects.create(
            user=request.user,
            meeting=created_meeting,  # 생성된 미팅 객체 조회
            is_host=True,
        )

        return Response(
            {"created_meeting": serializer.data, "meeting_uuid": created_meeting.uuid},
            status=status.HTTP_201_CREATED,
        )


# 번개 모임 수정
class MeetingUpdateView(APIView):

    serializer_class = MeetingUpdateSerializer

    @extend_schema(tags=["meeting"])
    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            selected_meeting = Meeting.objects.get(uuid=request.data["meeting_uuid"])
            title = request.data["title"]
            location = Location.objects.get(location_name=request.data["location_name"])
            payment_method = MeetingPaymentMethod.objects.get(
                payment_method=request.data["payment_method_name"]
            )
            age_group = MeetingAgeGroup.objects.get(
                age_group=request.data["age_group_name"]
            )
            gender_group = MeetingGenderGroup.objects.get(
                gender_group=request.data["gender_group_name"]
            )
            meeting_time = request.data["meeting_time"]
            description = request.data["description"]
            meeting_image_url = request.data["meeting_image_url"]
            maximum = request.data["maximum"]

        except (
            Meeting.DoesNotExist,
            Location.DoesNotExist,
            MeetingPaymentMethod.DoesNotExist,
            MeetingAgeGroup.DoesNotExist,
            MeetingGenderGroup.DoesNotExist,
        ):
            return Response(
                {"detail": "data not found"}, status=status.HTTP_404_NOT_FOUND
            )

        selected_meeting.title = title
        selected_meeting.location_id = location.pk
        selected_meeting.payment_method_id = payment_method.pk
        selected_meeting.age_group_id = age_group.pk
        selected_meeting.gender_group_id = gender_group.pk
        selected_meeting.meeting_time = meeting_time
        selected_meeting.description = description
        selected_meeting.meeting_image_url = meeting_image_url
        selected_meeting.maximum = maximum

        selected_meeting.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


# 번개 모임 삭제
class MeetingDeleteView(APIView):

    serializer_class = JoinMeetingMemberSerializer

    @extend_schema(tags=["meeting"])
    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            selected_meeting = Meeting.objects.get(uuid=request.data["meeting_uuid"])

        except Meeting.DoesNotExist:
            return Response(
                {"detail": "meeting does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        selected_meeting.delete()

        return Response({"detail": "delete success"}, status=status.HTTP_200_OK)

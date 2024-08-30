from django.db.models import Case, IntegerField, Value, When
from django.utils import timezone
from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import status
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
from users.models import CustomUser

from .models import Meeting, MeetingMember
from .serializers import (
    DeleteMeetingMemberSerializer,
    JoinMeetingSerializer,
    MeetingCreateSerializer,
    MeetingDetailSerializer,
    MeetingListSerializer,
    MeetingMemberSerializer,
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
        meetings = Meeting.objects.filter(meeting_time__gte=timezone.now()).order_by(
            "meeting_time"
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

        time_sort_id = TimeSortCategory.objects.get(sort_name=time_category).id
        location_category_id = Location.objects.get(location_name=location_category).id

        if location_category == "전체":
            meetings = Meeting.objects.all().order_by(time_sort_id=time_sort_id)
        else:
            meetings = Meeting.objects.filter(location_category_id=location_category_id).order_by(time_sort_id=time_sort_id)

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
        try:
            selected_meeting = Meeting.objects.get(uuid=uuid)
            meeting_member_ids = MeetingMember.objects.filter(
                meeting_id=selected_meeting.id
            ).values_list("user_id", flat=True)
            meeting_member = CustomUser.objects.filter(id__in=meeting_member_ids)
        except Meeting.DoesNotExist:
            raise NotFound("The meeting does not exist")

        meeting_detail = {
            "meeting": MeetingDetailSerializer(instance=selected_meeting).data,
            "meeting_member": MeetingMemberSerializer(
                instance=meeting_member, many=True
            ).data,
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

        location_id = request.data["location"]
        payment_method_id = request.data["payment_method"]
        age_group_id = request.data["age_group"]
        gender_group_id = request.data["gender_group"]

        location = Location.objects.get(id=location_id)
        payment_method = MeetingPaymentMethod.objects.get(id=payment_method_id)
        age_group = MeetingAgeGroup.objects.get(id=age_group_id)
        gender_group = MeetingGenderGroup.objects.get(id=gender_group_id)

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

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 모임 참여 취소
class DeleteMeetingMemberView(APIView):
    serializer_class = DeleteMeetingMemberSerializer

    @extend_schema(tags=["meeting"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        meeting = Meeting.objects.get(id=request.data["meeting"])

        # 미팅 멤버에서 삭제
        MeetingMember.objects.get(user=user, meeting=meeting).delete()

        return Response(
            {"detail": "Successful cancellation of meeting attendance"},
            status=status.HTTP_200_OK,
        )


# 번개에 참여하기
class JoinMeetingView(APIView):
    serializer_class = JoinMeetingSerializer

    @extend_schema(tags=["meeting"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        meeting_id = Meeting.objects.get(uuid=request.data["uuid"]).id
        is_host = False

        if MeetingMember.objects.filter(user=user, meeting_id=meeting_id).exists():
            return Response(
                {"detail": "meeting member is already exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        MeetingMember.objects.create(user=user, meeting_id=meeting_id, is_host=is_host)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

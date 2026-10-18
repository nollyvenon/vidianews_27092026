// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'user_management_models.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
    'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models');

SubscriberProfile _$SubscriberProfileFromJson(Map<String, dynamic> json) {
  return _SubscriberProfile.fromJson(json);
}

/// @nodoc
mixin _$SubscriberProfile {
  int get id => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  String get subscriptionTier => throw _privateConstructorUsedError;
  String get subscriptionStatus => throw _privateConstructorUsedError;
  DateTime get subscriptionStartDate => throw _privateConstructorUsedError;
  DateTime? get subscriptionEndDate => throw _privateConstructorUsedError;
  int get articlesRead => throw _privateConstructorUsedError;
  double get totalSessionTime => throw _privateConstructorUsedError;
  double get engagementScore => throw _privateConstructorUsedError;
  double get churnRiskScore => throw _privateConstructorUsedError;
  DateTime get lastActivityAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $SubscriberProfileCopyWith<SubscriberProfile> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $SubscriberProfileCopyWith<$Res> {
  factory $SubscriberProfileCopyWith(
          SubscriberProfile value, $Res Function(SubscriberProfile) then) =
      _$SubscriberProfileCopyWithImpl<$Res, SubscriberProfile>;
  @useResult
  $Res call(
      {int id,
      int userId,
      String subscriptionTier,
      String subscriptionStatus,
      DateTime subscriptionStartDate,
      DateTime? subscriptionEndDate,
      int articlesRead,
      double totalSessionTime,
      double engagementScore,
      double churnRiskScore,
      DateTime lastActivityAt});
}

/// @nodoc
class _$SubscriberProfileCopyWithImpl<$Res, $Val extends SubscriberProfile>
    implements $SubscriberProfileCopyWith<$Res> {
  _$SubscriberProfileCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? subscriptionTier = null,
    Object? subscriptionStatus = null,
    Object? subscriptionStartDate = null,
    Object? subscriptionEndDate = freezed,
    Object? articlesRead = null,
    Object? totalSessionTime = null,
    Object? engagementScore = null,
    Object? churnRiskScore = null,
    Object? lastActivityAt = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      subscriptionTier: null == subscriptionTier
          ? _value.subscriptionTier
          : subscriptionTier // ignore: cast_nullable_to_non_nullable
              as String,
      subscriptionStatus: null == subscriptionStatus
          ? _value.subscriptionStatus
          : subscriptionStatus // ignore: cast_nullable_to_non_nullable
              as String,
      subscriptionStartDate: null == subscriptionStartDate
          ? _value.subscriptionStartDate
          : subscriptionStartDate // ignore: cast_nullable_to_non_nullable
              as DateTime,
      subscriptionEndDate: freezed == subscriptionEndDate
          ? _value.subscriptionEndDate
          : subscriptionEndDate // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      articlesRead: null == articlesRead
          ? _value.articlesRead
          : articlesRead // ignore: cast_nullable_to_non_nullable
              as int,
      totalSessionTime: null == totalSessionTime
          ? _value.totalSessionTime
          : totalSessionTime // ignore: cast_nullable_to_non_nullable
              as double,
      engagementScore: null == engagementScore
          ? _value.engagementScore
          : engagementScore // ignore: cast_nullable_to_non_nullable
              as double,
      churnRiskScore: null == churnRiskScore
          ? _value.churnRiskScore
          : churnRiskScore // ignore: cast_nullable_to_non_nullable
              as double,
      lastActivityAt: null == lastActivityAt
          ? _value.lastActivityAt
          : lastActivityAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$SubscriberProfileImplCopyWith<$Res>
    implements $SubscriberProfileCopyWith<$Res> {
  factory _$$SubscriberProfileImplCopyWith(_$SubscriberProfileImpl value,
          $Res Function(_$SubscriberProfileImpl) then) =
      __$$SubscriberProfileImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int userId,
      String subscriptionTier,
      String subscriptionStatus,
      DateTime subscriptionStartDate,
      DateTime? subscriptionEndDate,
      int articlesRead,
      double totalSessionTime,
      double engagementScore,
      double churnRiskScore,
      DateTime lastActivityAt});
}

/// @nodoc
class __$$SubscriberProfileImplCopyWithImpl<$Res>
    extends _$SubscriberProfileCopyWithImpl<$Res, _$SubscriberProfileImpl>
    implements _$$SubscriberProfileImplCopyWith<$Res> {
  __$$SubscriberProfileImplCopyWithImpl(_$SubscriberProfileImpl _value,
      $Res Function(_$SubscriberProfileImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? subscriptionTier = null,
    Object? subscriptionStatus = null,
    Object? subscriptionStartDate = null,
    Object? subscriptionEndDate = freezed,
    Object? articlesRead = null,
    Object? totalSessionTime = null,
    Object? engagementScore = null,
    Object? churnRiskScore = null,
    Object? lastActivityAt = null,
  }) {
    return _then(_$SubscriberProfileImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      subscriptionTier: null == subscriptionTier
          ? _value.subscriptionTier
          : subscriptionTier // ignore: cast_nullable_to_non_nullable
              as String,
      subscriptionStatus: null == subscriptionStatus
          ? _value.subscriptionStatus
          : subscriptionStatus // ignore: cast_nullable_to_non_nullable
              as String,
      subscriptionStartDate: null == subscriptionStartDate
          ? _value.subscriptionStartDate
          : subscriptionStartDate // ignore: cast_nullable_to_non_nullable
              as DateTime,
      subscriptionEndDate: freezed == subscriptionEndDate
          ? _value.subscriptionEndDate
          : subscriptionEndDate // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      articlesRead: null == articlesRead
          ? _value.articlesRead
          : articlesRead // ignore: cast_nullable_to_non_nullable
              as int,
      totalSessionTime: null == totalSessionTime
          ? _value.totalSessionTime
          : totalSessionTime // ignore: cast_nullable_to_non_nullable
              as double,
      engagementScore: null == engagementScore
          ? _value.engagementScore
          : engagementScore // ignore: cast_nullable_to_non_nullable
              as double,
      churnRiskScore: null == churnRiskScore
          ? _value.churnRiskScore
          : churnRiskScore // ignore: cast_nullable_to_non_nullable
              as double,
      lastActivityAt: null == lastActivityAt
          ? _value.lastActivityAt
          : lastActivityAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$SubscriberProfileImpl implements _SubscriberProfile {
  const _$SubscriberProfileImpl(
      {required this.id,
      required this.userId,
      required this.subscriptionTier,
      required this.subscriptionStatus,
      required this.subscriptionStartDate,
      this.subscriptionEndDate,
      this.articlesRead = 0,
      this.totalSessionTime = 0.0,
      this.engagementScore = 0.0,
      this.churnRiskScore = 0.0,
      required this.lastActivityAt});

  factory _$SubscriberProfileImpl.fromJson(Map<String, dynamic> json) =>
      _$$SubscriberProfileImplFromJson(json);

  @override
  final int id;
  @override
  final int userId;
  @override
  final String subscriptionTier;
  @override
  final String subscriptionStatus;
  @override
  final DateTime subscriptionStartDate;
  @override
  final DateTime? subscriptionEndDate;
  @override
  @JsonKey()
  final int articlesRead;
  @override
  @JsonKey()
  final double totalSessionTime;
  @override
  @JsonKey()
  final double engagementScore;
  @override
  @JsonKey()
  final double churnRiskScore;
  @override
  final DateTime lastActivityAt;

  @override
  String toString() {
    return 'SubscriberProfile(id: $id, userId: $userId, subscriptionTier: $subscriptionTier, subscriptionStatus: $subscriptionStatus, subscriptionStartDate: $subscriptionStartDate, subscriptionEndDate: $subscriptionEndDate, articlesRead: $articlesRead, totalSessionTime: $totalSessionTime, engagementScore: $engagementScore, churnRiskScore: $churnRiskScore, lastActivityAt: $lastActivityAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$SubscriberProfileImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.subscriptionTier, subscriptionTier) ||
                other.subscriptionTier == subscriptionTier) &&
            (identical(other.subscriptionStatus, subscriptionStatus) ||
                other.subscriptionStatus == subscriptionStatus) &&
            (identical(other.subscriptionStartDate, subscriptionStartDate) ||
                other.subscriptionStartDate == subscriptionStartDate) &&
            (identical(other.subscriptionEndDate, subscriptionEndDate) ||
                other.subscriptionEndDate == subscriptionEndDate) &&
            (identical(other.articlesRead, articlesRead) ||
                other.articlesRead == articlesRead) &&
            (identical(other.totalSessionTime, totalSessionTime) ||
                other.totalSessionTime == totalSessionTime) &&
            (identical(other.engagementScore, engagementScore) ||
                other.engagementScore == engagementScore) &&
            (identical(other.churnRiskScore, churnRiskScore) ||
                other.churnRiskScore == churnRiskScore) &&
            (identical(other.lastActivityAt, lastActivityAt) ||
                other.lastActivityAt == lastActivityAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      userId,
      subscriptionTier,
      subscriptionStatus,
      subscriptionStartDate,
      subscriptionEndDate,
      articlesRead,
      totalSessionTime,
      engagementScore,
      churnRiskScore,
      lastActivityAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$SubscriberProfileImplCopyWith<_$SubscriberProfileImpl> get copyWith =>
      __$$SubscriberProfileImplCopyWithImpl<_$SubscriberProfileImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$SubscriberProfileImplToJson(
      this,
    );
  }
}

abstract class _SubscriberProfile implements SubscriberProfile {
  const factory _SubscriberProfile(
      {required final int id,
      required final int userId,
      required final String subscriptionTier,
      required final String subscriptionStatus,
      required final DateTime subscriptionStartDate,
      final DateTime? subscriptionEndDate,
      final int articlesRead,
      final double totalSessionTime,
      final double engagementScore,
      final double churnRiskScore,
      required final DateTime lastActivityAt}) = _$SubscriberProfileImpl;

  factory _SubscriberProfile.fromJson(Map<String, dynamic> json) =
      _$SubscriberProfileImpl.fromJson;

  @override
  int get id;
  @override
  int get userId;
  @override
  String get subscriptionTier;
  @override
  String get subscriptionStatus;
  @override
  DateTime get subscriptionStartDate;
  @override
  DateTime? get subscriptionEndDate;
  @override
  int get articlesRead;
  @override
  double get totalSessionTime;
  @override
  double get engagementScore;
  @override
  double get churnRiskScore;
  @override
  DateTime get lastActivityAt;
  @override
  @JsonKey(ignore: true)
  _$$SubscriberProfileImplCopyWith<_$SubscriberProfileImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

SubscriberActivity _$SubscriberActivityFromJson(Map<String, dynamic> json) {
  return _SubscriberActivity.fromJson(json);
}

/// @nodoc
mixin _$SubscriberActivity {
  int get id => throw _privateConstructorUsedError;
  int get subscriberId => throw _privateConstructorUsedError;
  String get activityType => throw _privateConstructorUsedError;
  int? get contentId => throw _privateConstructorUsedError;
  Map<String, dynamic>? get metadata => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $SubscriberActivityCopyWith<SubscriberActivity> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $SubscriberActivityCopyWith<$Res> {
  factory $SubscriberActivityCopyWith(
          SubscriberActivity value, $Res Function(SubscriberActivity) then) =
      _$SubscriberActivityCopyWithImpl<$Res, SubscriberActivity>;
  @useResult
  $Res call(
      {int id,
      int subscriberId,
      String activityType,
      int? contentId,
      Map<String, dynamic>? metadata,
      DateTime createdAt});
}

/// @nodoc
class _$SubscriberActivityCopyWithImpl<$Res, $Val extends SubscriberActivity>
    implements $SubscriberActivityCopyWith<$Res> {
  _$SubscriberActivityCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? subscriberId = null,
    Object? activityType = null,
    Object? contentId = freezed,
    Object? metadata = freezed,
    Object? createdAt = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      subscriberId: null == subscriberId
          ? _value.subscriberId
          : subscriberId // ignore: cast_nullable_to_non_nullable
              as int,
      activityType: null == activityType
          ? _value.activityType
          : activityType // ignore: cast_nullable_to_non_nullable
              as String,
      contentId: freezed == contentId
          ? _value.contentId
          : contentId // ignore: cast_nullable_to_non_nullable
              as int?,
      metadata: freezed == metadata
          ? _value.metadata
          : metadata // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>?,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$SubscriberActivityImplCopyWith<$Res>
    implements $SubscriberActivityCopyWith<$Res> {
  factory _$$SubscriberActivityImplCopyWith(_$SubscriberActivityImpl value,
          $Res Function(_$SubscriberActivityImpl) then) =
      __$$SubscriberActivityImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int subscriberId,
      String activityType,
      int? contentId,
      Map<String, dynamic>? metadata,
      DateTime createdAt});
}

/// @nodoc
class __$$SubscriberActivityImplCopyWithImpl<$Res>
    extends _$SubscriberActivityCopyWithImpl<$Res, _$SubscriberActivityImpl>
    implements _$$SubscriberActivityImplCopyWith<$Res> {
  __$$SubscriberActivityImplCopyWithImpl(_$SubscriberActivityImpl _value,
      $Res Function(_$SubscriberActivityImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? subscriberId = null,
    Object? activityType = null,
    Object? contentId = freezed,
    Object? metadata = freezed,
    Object? createdAt = null,
  }) {
    return _then(_$SubscriberActivityImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      subscriberId: null == subscriberId
          ? _value.subscriberId
          : subscriberId // ignore: cast_nullable_to_non_nullable
              as int,
      activityType: null == activityType
          ? _value.activityType
          : activityType // ignore: cast_nullable_to_non_nullable
              as String,
      contentId: freezed == contentId
          ? _value.contentId
          : contentId // ignore: cast_nullable_to_non_nullable
              as int?,
      metadata: freezed == metadata
          ? _value._metadata
          : metadata // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>?,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$SubscriberActivityImpl implements _SubscriberActivity {
  const _$SubscriberActivityImpl(
      {required this.id,
      required this.subscriberId,
      required this.activityType,
      this.contentId,
      final Map<String, dynamic>? metadata,
      required this.createdAt})
      : _metadata = metadata;

  factory _$SubscriberActivityImpl.fromJson(Map<String, dynamic> json) =>
      _$$SubscriberActivityImplFromJson(json);

  @override
  final int id;
  @override
  final int subscriberId;
  @override
  final String activityType;
  @override
  final int? contentId;
  final Map<String, dynamic>? _metadata;
  @override
  Map<String, dynamic>? get metadata {
    final value = _metadata;
    if (value == null) return null;
    if (_metadata is EqualUnmodifiableMapView) return _metadata;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(value);
  }

  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'SubscriberActivity(id: $id, subscriberId: $subscriberId, activityType: $activityType, contentId: $contentId, metadata: $metadata, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$SubscriberActivityImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.subscriberId, subscriberId) ||
                other.subscriberId == subscriberId) &&
            (identical(other.activityType, activityType) ||
                other.activityType == activityType) &&
            (identical(other.contentId, contentId) ||
                other.contentId == contentId) &&
            const DeepCollectionEquality().equals(other._metadata, _metadata) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, id, subscriberId, activityType,
      contentId, const DeepCollectionEquality().hash(_metadata), createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$SubscriberActivityImplCopyWith<_$SubscriberActivityImpl> get copyWith =>
      __$$SubscriberActivityImplCopyWithImpl<_$SubscriberActivityImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$SubscriberActivityImplToJson(
      this,
    );
  }
}

abstract class _SubscriberActivity implements SubscriberActivity {
  const factory _SubscriberActivity(
      {required final int id,
      required final int subscriberId,
      required final String activityType,
      final int? contentId,
      final Map<String, dynamic>? metadata,
      required final DateTime createdAt}) = _$SubscriberActivityImpl;

  factory _SubscriberActivity.fromJson(Map<String, dynamic> json) =
      _$SubscriberActivityImpl.fromJson;

  @override
  int get id;
  @override
  int get subscriberId;
  @override
  String get activityType;
  @override
  int? get contentId;
  @override
  Map<String, dynamic>? get metadata;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$SubscriberActivityImplCopyWith<_$SubscriberActivityImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

EmailCampaign _$EmailCampaignFromJson(Map<String, dynamic> json) {
  return _EmailCampaign.fromJson(json);
}

/// @nodoc
mixin _$EmailCampaign {
  int get id => throw _privateConstructorUsedError;
  String get name => throw _privateConstructorUsedError;
  int get templateId => throw _privateConstructorUsedError;
  String get subject => throw _privateConstructorUsedError;
  String get fromEmail => throw _privateConstructorUsedError;
  int get recipientCount => throw _privateConstructorUsedError;
  int get sentCount => throw _privateConstructorUsedError;
  int get openCount => throw _privateConstructorUsedError;
  int get clickCount => throw _privateConstructorUsedError;
  double get openRate => throw _privateConstructorUsedError;
  double get clickRate => throw _privateConstructorUsedError;
  String get status => throw _privateConstructorUsedError;
  DateTime? get scheduledAt => throw _privateConstructorUsedError;
  DateTime? get sentAt => throw _privateConstructorUsedError;
  DateTime? get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $EmailCampaignCopyWith<EmailCampaign> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $EmailCampaignCopyWith<$Res> {
  factory $EmailCampaignCopyWith(
          EmailCampaign value, $Res Function(EmailCampaign) then) =
      _$EmailCampaignCopyWithImpl<$Res, EmailCampaign>;
  @useResult
  $Res call(
      {int id,
      String name,
      int templateId,
      String subject,
      String fromEmail,
      int recipientCount,
      int sentCount,
      int openCount,
      int clickCount,
      double openRate,
      double clickRate,
      String status,
      DateTime? scheduledAt,
      DateTime? sentAt,
      DateTime? createdAt});
}

/// @nodoc
class _$EmailCampaignCopyWithImpl<$Res, $Val extends EmailCampaign>
    implements $EmailCampaignCopyWith<$Res> {
  _$EmailCampaignCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? templateId = null,
    Object? subject = null,
    Object? fromEmail = null,
    Object? recipientCount = null,
    Object? sentCount = null,
    Object? openCount = null,
    Object? clickCount = null,
    Object? openRate = null,
    Object? clickRate = null,
    Object? status = null,
    Object? scheduledAt = freezed,
    Object? sentAt = freezed,
    Object? createdAt = freezed,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      name: null == name
          ? _value.name
          : name // ignore: cast_nullable_to_non_nullable
              as String,
      templateId: null == templateId
          ? _value.templateId
          : templateId // ignore: cast_nullable_to_non_nullable
              as int,
      subject: null == subject
          ? _value.subject
          : subject // ignore: cast_nullable_to_non_nullable
              as String,
      fromEmail: null == fromEmail
          ? _value.fromEmail
          : fromEmail // ignore: cast_nullable_to_non_nullable
              as String,
      recipientCount: null == recipientCount
          ? _value.recipientCount
          : recipientCount // ignore: cast_nullable_to_non_nullable
              as int,
      sentCount: null == sentCount
          ? _value.sentCount
          : sentCount // ignore: cast_nullable_to_non_nullable
              as int,
      openCount: null == openCount
          ? _value.openCount
          : openCount // ignore: cast_nullable_to_non_nullable
              as int,
      clickCount: null == clickCount
          ? _value.clickCount
          : clickCount // ignore: cast_nullable_to_non_nullable
              as int,
      openRate: null == openRate
          ? _value.openRate
          : openRate // ignore: cast_nullable_to_non_nullable
              as double,
      clickRate: null == clickRate
          ? _value.clickRate
          : clickRate // ignore: cast_nullable_to_non_nullable
              as double,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      scheduledAt: freezed == scheduledAt
          ? _value.scheduledAt
          : scheduledAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      sentAt: freezed == sentAt
          ? _value.sentAt
          : sentAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      createdAt: freezed == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$EmailCampaignImplCopyWith<$Res>
    implements $EmailCampaignCopyWith<$Res> {
  factory _$$EmailCampaignImplCopyWith(
          _$EmailCampaignImpl value, $Res Function(_$EmailCampaignImpl) then) =
      __$$EmailCampaignImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String name,
      int templateId,
      String subject,
      String fromEmail,
      int recipientCount,
      int sentCount,
      int openCount,
      int clickCount,
      double openRate,
      double clickRate,
      String status,
      DateTime? scheduledAt,
      DateTime? sentAt,
      DateTime? createdAt});
}

/// @nodoc
class __$$EmailCampaignImplCopyWithImpl<$Res>
    extends _$EmailCampaignCopyWithImpl<$Res, _$EmailCampaignImpl>
    implements _$$EmailCampaignImplCopyWith<$Res> {
  __$$EmailCampaignImplCopyWithImpl(
      _$EmailCampaignImpl _value, $Res Function(_$EmailCampaignImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? templateId = null,
    Object? subject = null,
    Object? fromEmail = null,
    Object? recipientCount = null,
    Object? sentCount = null,
    Object? openCount = null,
    Object? clickCount = null,
    Object? openRate = null,
    Object? clickRate = null,
    Object? status = null,
    Object? scheduledAt = freezed,
    Object? sentAt = freezed,
    Object? createdAt = freezed,
  }) {
    return _then(_$EmailCampaignImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      name: null == name
          ? _value.name
          : name // ignore: cast_nullable_to_non_nullable
              as String,
      templateId: null == templateId
          ? _value.templateId
          : templateId // ignore: cast_nullable_to_non_nullable
              as int,
      subject: null == subject
          ? _value.subject
          : subject // ignore: cast_nullable_to_non_nullable
              as String,
      fromEmail: null == fromEmail
          ? _value.fromEmail
          : fromEmail // ignore: cast_nullable_to_non_nullable
              as String,
      recipientCount: null == recipientCount
          ? _value.recipientCount
          : recipientCount // ignore: cast_nullable_to_non_nullable
              as int,
      sentCount: null == sentCount
          ? _value.sentCount
          : sentCount // ignore: cast_nullable_to_non_nullable
              as int,
      openCount: null == openCount
          ? _value.openCount
          : openCount // ignore: cast_nullable_to_non_nullable
              as int,
      clickCount: null == clickCount
          ? _value.clickCount
          : clickCount // ignore: cast_nullable_to_non_nullable
              as int,
      openRate: null == openRate
          ? _value.openRate
          : openRate // ignore: cast_nullable_to_non_nullable
              as double,
      clickRate: null == clickRate
          ? _value.clickRate
          : clickRate // ignore: cast_nullable_to_non_nullable
              as double,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      scheduledAt: freezed == scheduledAt
          ? _value.scheduledAt
          : scheduledAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      sentAt: freezed == sentAt
          ? _value.sentAt
          : sentAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      createdAt: freezed == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$EmailCampaignImpl implements _EmailCampaign {
  const _$EmailCampaignImpl(
      {required this.id,
      required this.name,
      required this.templateId,
      required this.subject,
      required this.fromEmail,
      required this.recipientCount,
      required this.sentCount,
      required this.openCount,
      required this.clickCount,
      this.openRate = 0,
      this.clickRate = 0,
      required this.status,
      this.scheduledAt,
      this.sentAt,
      this.createdAt});

  factory _$EmailCampaignImpl.fromJson(Map<String, dynamic> json) =>
      _$$EmailCampaignImplFromJson(json);

  @override
  final int id;
  @override
  final String name;
  @override
  final int templateId;
  @override
  final String subject;
  @override
  final String fromEmail;
  @override
  final int recipientCount;
  @override
  final int sentCount;
  @override
  final int openCount;
  @override
  final int clickCount;
  @override
  @JsonKey()
  final double openRate;
  @override
  @JsonKey()
  final double clickRate;
  @override
  final String status;
  @override
  final DateTime? scheduledAt;
  @override
  final DateTime? sentAt;
  @override
  final DateTime? createdAt;

  @override
  String toString() {
    return 'EmailCampaign(id: $id, name: $name, templateId: $templateId, subject: $subject, fromEmail: $fromEmail, recipientCount: $recipientCount, sentCount: $sentCount, openCount: $openCount, clickCount: $clickCount, openRate: $openRate, clickRate: $clickRate, status: $status, scheduledAt: $scheduledAt, sentAt: $sentAt, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$EmailCampaignImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.templateId, templateId) ||
                other.templateId == templateId) &&
            (identical(other.subject, subject) || other.subject == subject) &&
            (identical(other.fromEmail, fromEmail) ||
                other.fromEmail == fromEmail) &&
            (identical(other.recipientCount, recipientCount) ||
                other.recipientCount == recipientCount) &&
            (identical(other.sentCount, sentCount) ||
                other.sentCount == sentCount) &&
            (identical(other.openCount, openCount) ||
                other.openCount == openCount) &&
            (identical(other.clickCount, clickCount) ||
                other.clickCount == clickCount) &&
            (identical(other.openRate, openRate) ||
                other.openRate == openRate) &&
            (identical(other.clickRate, clickRate) ||
                other.clickRate == clickRate) &&
            (identical(other.status, status) || other.status == status) &&
            (identical(other.scheduledAt, scheduledAt) ||
                other.scheduledAt == scheduledAt) &&
            (identical(other.sentAt, sentAt) || other.sentAt == sentAt) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      name,
      templateId,
      subject,
      fromEmail,
      recipientCount,
      sentCount,
      openCount,
      clickCount,
      openRate,
      clickRate,
      status,
      scheduledAt,
      sentAt,
      createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$EmailCampaignImplCopyWith<_$EmailCampaignImpl> get copyWith =>
      __$$EmailCampaignImplCopyWithImpl<_$EmailCampaignImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$EmailCampaignImplToJson(
      this,
    );
  }
}

abstract class _EmailCampaign implements EmailCampaign {
  const factory _EmailCampaign(
      {required final int id,
      required final String name,
      required final int templateId,
      required final String subject,
      required final String fromEmail,
      required final int recipientCount,
      required final int sentCount,
      required final int openCount,
      required final int clickCount,
      final double openRate,
      final double clickRate,
      required final String status,
      final DateTime? scheduledAt,
      final DateTime? sentAt,
      final DateTime? createdAt}) = _$EmailCampaignImpl;

  factory _EmailCampaign.fromJson(Map<String, dynamic> json) =
      _$EmailCampaignImpl.fromJson;

  @override
  int get id;
  @override
  String get name;
  @override
  int get templateId;
  @override
  String get subject;
  @override
  String get fromEmail;
  @override
  int get recipientCount;
  @override
  int get sentCount;
  @override
  int get openCount;
  @override
  int get clickCount;
  @override
  double get openRate;
  @override
  double get clickRate;
  @override
  String get status;
  @override
  DateTime? get scheduledAt;
  @override
  DateTime? get sentAt;
  @override
  DateTime? get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$EmailCampaignImplCopyWith<_$EmailCampaignImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

UserSegment _$UserSegmentFromJson(Map<String, dynamic> json) {
  return _UserSegment.fromJson(json);
}

/// @nodoc
mixin _$UserSegment {
  int get id => throw _privateConstructorUsedError;
  String get name => throw _privateConstructorUsedError;
  String get segmentType => throw _privateConstructorUsedError;
  String? get description => throw _privateConstructorUsedError;
  int get userCount => throw _privateConstructorUsedError;
  Map<String, dynamic>? get filterCriteria =>
      throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $UserSegmentCopyWith<UserSegment> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $UserSegmentCopyWith<$Res> {
  factory $UserSegmentCopyWith(
          UserSegment value, $Res Function(UserSegment) then) =
      _$UserSegmentCopyWithImpl<$Res, UserSegment>;
  @useResult
  $Res call(
      {int id,
      String name,
      String segmentType,
      String? description,
      int userCount,
      Map<String, dynamic>? filterCriteria});
}

/// @nodoc
class _$UserSegmentCopyWithImpl<$Res, $Val extends UserSegment>
    implements $UserSegmentCopyWith<$Res> {
  _$UserSegmentCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? segmentType = null,
    Object? description = freezed,
    Object? userCount = null,
    Object? filterCriteria = freezed,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      name: null == name
          ? _value.name
          : name // ignore: cast_nullable_to_non_nullable
              as String,
      segmentType: null == segmentType
          ? _value.segmentType
          : segmentType // ignore: cast_nullable_to_non_nullable
              as String,
      description: freezed == description
          ? _value.description
          : description // ignore: cast_nullable_to_non_nullable
              as String?,
      userCount: null == userCount
          ? _value.userCount
          : userCount // ignore: cast_nullable_to_non_nullable
              as int,
      filterCriteria: freezed == filterCriteria
          ? _value.filterCriteria
          : filterCriteria // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>?,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$UserSegmentImplCopyWith<$Res>
    implements $UserSegmentCopyWith<$Res> {
  factory _$$UserSegmentImplCopyWith(
          _$UserSegmentImpl value, $Res Function(_$UserSegmentImpl) then) =
      __$$UserSegmentImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String name,
      String segmentType,
      String? description,
      int userCount,
      Map<String, dynamic>? filterCriteria});
}

/// @nodoc
class __$$UserSegmentImplCopyWithImpl<$Res>
    extends _$UserSegmentCopyWithImpl<$Res, _$UserSegmentImpl>
    implements _$$UserSegmentImplCopyWith<$Res> {
  __$$UserSegmentImplCopyWithImpl(
      _$UserSegmentImpl _value, $Res Function(_$UserSegmentImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? segmentType = null,
    Object? description = freezed,
    Object? userCount = null,
    Object? filterCriteria = freezed,
  }) {
    return _then(_$UserSegmentImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      name: null == name
          ? _value.name
          : name // ignore: cast_nullable_to_non_nullable
              as String,
      segmentType: null == segmentType
          ? _value.segmentType
          : segmentType // ignore: cast_nullable_to_non_nullable
              as String,
      description: freezed == description
          ? _value.description
          : description // ignore: cast_nullable_to_non_nullable
              as String?,
      userCount: null == userCount
          ? _value.userCount
          : userCount // ignore: cast_nullable_to_non_nullable
              as int,
      filterCriteria: freezed == filterCriteria
          ? _value._filterCriteria
          : filterCriteria // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>?,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$UserSegmentImpl implements _UserSegment {
  const _$UserSegmentImpl(
      {required this.id,
      required this.name,
      required this.segmentType,
      this.description,
      this.userCount = 0,
      final Map<String, dynamic>? filterCriteria})
      : _filterCriteria = filterCriteria;

  factory _$UserSegmentImpl.fromJson(Map<String, dynamic> json) =>
      _$$UserSegmentImplFromJson(json);

  @override
  final int id;
  @override
  final String name;
  @override
  final String segmentType;
  @override
  final String? description;
  @override
  @JsonKey()
  final int userCount;
  final Map<String, dynamic>? _filterCriteria;
  @override
  Map<String, dynamic>? get filterCriteria {
    final value = _filterCriteria;
    if (value == null) return null;
    if (_filterCriteria is EqualUnmodifiableMapView) return _filterCriteria;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(value);
  }

  @override
  String toString() {
    return 'UserSegment(id: $id, name: $name, segmentType: $segmentType, description: $description, userCount: $userCount, filterCriteria: $filterCriteria)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$UserSegmentImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.segmentType, segmentType) ||
                other.segmentType == segmentType) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.userCount, userCount) ||
                other.userCount == userCount) &&
            const DeepCollectionEquality()
                .equals(other._filterCriteria, _filterCriteria));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      name,
      segmentType,
      description,
      userCount,
      const DeepCollectionEquality().hash(_filterCriteria));

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$UserSegmentImplCopyWith<_$UserSegmentImpl> get copyWith =>
      __$$UserSegmentImplCopyWithImpl<_$UserSegmentImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$UserSegmentImplToJson(
      this,
    );
  }
}

abstract class _UserSegment implements UserSegment {
  const factory _UserSegment(
      {required final int id,
      required final String name,
      required final String segmentType,
      final String? description,
      final int userCount,
      final Map<String, dynamic>? filterCriteria}) = _$UserSegmentImpl;

  factory _UserSegment.fromJson(Map<String, dynamic> json) =
      _$UserSegmentImpl.fromJson;

  @override
  int get id;
  @override
  String get name;
  @override
  String get segmentType;
  @override
  String? get description;
  @override
  int get userCount;
  @override
  Map<String, dynamic>? get filterCriteria;
  @override
  @JsonKey(ignore: true)
  _$$UserSegmentImplCopyWith<_$UserSegmentImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

UserPreferenceProfile _$UserPreferenceProfileFromJson(
    Map<String, dynamic> json) {
  return _UserPreferenceProfile.fromJson(json);
}

/// @nodoc
mixin _$UserPreferenceProfile {
  int get id => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  List<String> get preferredCategories => throw _privateConstructorUsedError;
  List<String> get preferredLanguages => throw _privateConstructorUsedError;
  List<String> get notificationChannels => throw _privateConstructorUsedError;
  String get emailFrequency => throw _privateConstructorUsedError;
  bool get digestEnabled => throw _privateConstructorUsedError;
  bool get personalizationEnabled => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $UserPreferenceProfileCopyWith<UserPreferenceProfile> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $UserPreferenceProfileCopyWith<$Res> {
  factory $UserPreferenceProfileCopyWith(UserPreferenceProfile value,
          $Res Function(UserPreferenceProfile) then) =
      _$UserPreferenceProfileCopyWithImpl<$Res, UserPreferenceProfile>;
  @useResult
  $Res call(
      {int id,
      int userId,
      List<String> preferredCategories,
      List<String> preferredLanguages,
      List<String> notificationChannels,
      String emailFrequency,
      bool digestEnabled,
      bool personalizationEnabled});
}

/// @nodoc
class _$UserPreferenceProfileCopyWithImpl<$Res,
        $Val extends UserPreferenceProfile>
    implements $UserPreferenceProfileCopyWith<$Res> {
  _$UserPreferenceProfileCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? preferredCategories = null,
    Object? preferredLanguages = null,
    Object? notificationChannels = null,
    Object? emailFrequency = null,
    Object? digestEnabled = null,
    Object? personalizationEnabled = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      preferredCategories: null == preferredCategories
          ? _value.preferredCategories
          : preferredCategories // ignore: cast_nullable_to_non_nullable
              as List<String>,
      preferredLanguages: null == preferredLanguages
          ? _value.preferredLanguages
          : preferredLanguages // ignore: cast_nullable_to_non_nullable
              as List<String>,
      notificationChannels: null == notificationChannels
          ? _value.notificationChannels
          : notificationChannels // ignore: cast_nullable_to_non_nullable
              as List<String>,
      emailFrequency: null == emailFrequency
          ? _value.emailFrequency
          : emailFrequency // ignore: cast_nullable_to_non_nullable
              as String,
      digestEnabled: null == digestEnabled
          ? _value.digestEnabled
          : digestEnabled // ignore: cast_nullable_to_non_nullable
              as bool,
      personalizationEnabled: null == personalizationEnabled
          ? _value.personalizationEnabled
          : personalizationEnabled // ignore: cast_nullable_to_non_nullable
              as bool,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$UserPreferenceProfileImplCopyWith<$Res>
    implements $UserPreferenceProfileCopyWith<$Res> {
  factory _$$UserPreferenceProfileImplCopyWith(
          _$UserPreferenceProfileImpl value,
          $Res Function(_$UserPreferenceProfileImpl) then) =
      __$$UserPreferenceProfileImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int userId,
      List<String> preferredCategories,
      List<String> preferredLanguages,
      List<String> notificationChannels,
      String emailFrequency,
      bool digestEnabled,
      bool personalizationEnabled});
}

/// @nodoc
class __$$UserPreferenceProfileImplCopyWithImpl<$Res>
    extends _$UserPreferenceProfileCopyWithImpl<$Res,
        _$UserPreferenceProfileImpl>
    implements _$$UserPreferenceProfileImplCopyWith<$Res> {
  __$$UserPreferenceProfileImplCopyWithImpl(_$UserPreferenceProfileImpl _value,
      $Res Function(_$UserPreferenceProfileImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? preferredCategories = null,
    Object? preferredLanguages = null,
    Object? notificationChannels = null,
    Object? emailFrequency = null,
    Object? digestEnabled = null,
    Object? personalizationEnabled = null,
  }) {
    return _then(_$UserPreferenceProfileImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      preferredCategories: null == preferredCategories
          ? _value._preferredCategories
          : preferredCategories // ignore: cast_nullable_to_non_nullable
              as List<String>,
      preferredLanguages: null == preferredLanguages
          ? _value._preferredLanguages
          : preferredLanguages // ignore: cast_nullable_to_non_nullable
              as List<String>,
      notificationChannels: null == notificationChannels
          ? _value._notificationChannels
          : notificationChannels // ignore: cast_nullable_to_non_nullable
              as List<String>,
      emailFrequency: null == emailFrequency
          ? _value.emailFrequency
          : emailFrequency // ignore: cast_nullable_to_non_nullable
              as String,
      digestEnabled: null == digestEnabled
          ? _value.digestEnabled
          : digestEnabled // ignore: cast_nullable_to_non_nullable
              as bool,
      personalizationEnabled: null == personalizationEnabled
          ? _value.personalizationEnabled
          : personalizationEnabled // ignore: cast_nullable_to_non_nullable
              as bool,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$UserPreferenceProfileImpl implements _UserPreferenceProfile {
  const _$UserPreferenceProfileImpl(
      {required this.id,
      required this.userId,
      required final List<String> preferredCategories,
      final List<String> preferredLanguages = const ['en'],
      final List<String> notificationChannels = const ['email'],
      this.emailFrequency = 'daily',
      this.digestEnabled = true,
      this.personalizationEnabled = true})
      : _preferredCategories = preferredCategories,
        _preferredLanguages = preferredLanguages,
        _notificationChannels = notificationChannels;

  factory _$UserPreferenceProfileImpl.fromJson(Map<String, dynamic> json) =>
      _$$UserPreferenceProfileImplFromJson(json);

  @override
  final int id;
  @override
  final int userId;
  final List<String> _preferredCategories;
  @override
  List<String> get preferredCategories {
    if (_preferredCategories is EqualUnmodifiableListView)
      return _preferredCategories;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_preferredCategories);
  }

  final List<String> _preferredLanguages;
  @override
  @JsonKey()
  List<String> get preferredLanguages {
    if (_preferredLanguages is EqualUnmodifiableListView)
      return _preferredLanguages;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_preferredLanguages);
  }

  final List<String> _notificationChannels;
  @override
  @JsonKey()
  List<String> get notificationChannels {
    if (_notificationChannels is EqualUnmodifiableListView)
      return _notificationChannels;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_notificationChannels);
  }

  @override
  @JsonKey()
  final String emailFrequency;
  @override
  @JsonKey()
  final bool digestEnabled;
  @override
  @JsonKey()
  final bool personalizationEnabled;

  @override
  String toString() {
    return 'UserPreferenceProfile(id: $id, userId: $userId, preferredCategories: $preferredCategories, preferredLanguages: $preferredLanguages, notificationChannels: $notificationChannels, emailFrequency: $emailFrequency, digestEnabled: $digestEnabled, personalizationEnabled: $personalizationEnabled)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$UserPreferenceProfileImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            const DeepCollectionEquality()
                .equals(other._preferredCategories, _preferredCategories) &&
            const DeepCollectionEquality()
                .equals(other._preferredLanguages, _preferredLanguages) &&
            const DeepCollectionEquality()
                .equals(other._notificationChannels, _notificationChannels) &&
            (identical(other.emailFrequency, emailFrequency) ||
                other.emailFrequency == emailFrequency) &&
            (identical(other.digestEnabled, digestEnabled) ||
                other.digestEnabled == digestEnabled) &&
            (identical(other.personalizationEnabled, personalizationEnabled) ||
                other.personalizationEnabled == personalizationEnabled));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      userId,
      const DeepCollectionEquality().hash(_preferredCategories),
      const DeepCollectionEquality().hash(_preferredLanguages),
      const DeepCollectionEquality().hash(_notificationChannels),
      emailFrequency,
      digestEnabled,
      personalizationEnabled);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$UserPreferenceProfileImplCopyWith<_$UserPreferenceProfileImpl>
      get copyWith => __$$UserPreferenceProfileImplCopyWithImpl<
          _$UserPreferenceProfileImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$UserPreferenceProfileImplToJson(
      this,
    );
  }
}

abstract class _UserPreferenceProfile implements UserPreferenceProfile {
  const factory _UserPreferenceProfile(
      {required final int id,
      required final int userId,
      required final List<String> preferredCategories,
      final List<String> preferredLanguages,
      final List<String> notificationChannels,
      final String emailFrequency,
      final bool digestEnabled,
      final bool personalizationEnabled}) = _$UserPreferenceProfileImpl;

  factory _UserPreferenceProfile.fromJson(Map<String, dynamic> json) =
      _$UserPreferenceProfileImpl.fromJson;

  @override
  int get id;
  @override
  int get userId;
  @override
  List<String> get preferredCategories;
  @override
  List<String> get preferredLanguages;
  @override
  List<String> get notificationChannels;
  @override
  String get emailFrequency;
  @override
  bool get digestEnabled;
  @override
  bool get personalizationEnabled;
  @override
  @JsonKey(ignore: true)
  _$$UserPreferenceProfileImplCopyWith<_$UserPreferenceProfileImpl>
      get copyWith => throw _privateConstructorUsedError;
}

NotificationMessage _$NotificationMessageFromJson(Map<String, dynamic> json) {
  return _NotificationMessage.fromJson(json);
}

/// @nodoc
mixin _$NotificationMessage {
  int get id => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  String get channel => throw _privateConstructorUsedError;
  String get title => throw _privateConstructorUsedError;
  String get message => throw _privateConstructorUsedError;
  String get status => throw _privateConstructorUsedError;
  DateTime? get readAt => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $NotificationMessageCopyWith<NotificationMessage> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $NotificationMessageCopyWith<$Res> {
  factory $NotificationMessageCopyWith(
          NotificationMessage value, $Res Function(NotificationMessage) then) =
      _$NotificationMessageCopyWithImpl<$Res, NotificationMessage>;
  @useResult
  $Res call(
      {int id,
      int userId,
      String channel,
      String title,
      String message,
      String status,
      DateTime? readAt,
      DateTime createdAt});
}

/// @nodoc
class _$NotificationMessageCopyWithImpl<$Res, $Val extends NotificationMessage>
    implements $NotificationMessageCopyWith<$Res> {
  _$NotificationMessageCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? channel = null,
    Object? title = null,
    Object? message = null,
    Object? status = null,
    Object? readAt = freezed,
    Object? createdAt = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      channel: null == channel
          ? _value.channel
          : channel // ignore: cast_nullable_to_non_nullable
              as String,
      title: null == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String,
      message: null == message
          ? _value.message
          : message // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      readAt: freezed == readAt
          ? _value.readAt
          : readAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$NotificationMessageImplCopyWith<$Res>
    implements $NotificationMessageCopyWith<$Res> {
  factory _$$NotificationMessageImplCopyWith(_$NotificationMessageImpl value,
          $Res Function(_$NotificationMessageImpl) then) =
      __$$NotificationMessageImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int userId,
      String channel,
      String title,
      String message,
      String status,
      DateTime? readAt,
      DateTime createdAt});
}

/// @nodoc
class __$$NotificationMessageImplCopyWithImpl<$Res>
    extends _$NotificationMessageCopyWithImpl<$Res, _$NotificationMessageImpl>
    implements _$$NotificationMessageImplCopyWith<$Res> {
  __$$NotificationMessageImplCopyWithImpl(_$NotificationMessageImpl _value,
      $Res Function(_$NotificationMessageImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? channel = null,
    Object? title = null,
    Object? message = null,
    Object? status = null,
    Object? readAt = freezed,
    Object? createdAt = null,
  }) {
    return _then(_$NotificationMessageImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      channel: null == channel
          ? _value.channel
          : channel // ignore: cast_nullable_to_non_nullable
              as String,
      title: null == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String,
      message: null == message
          ? _value.message
          : message // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      readAt: freezed == readAt
          ? _value.readAt
          : readAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$NotificationMessageImpl implements _NotificationMessage {
  const _$NotificationMessageImpl(
      {required this.id,
      required this.userId,
      required this.channel,
      required this.title,
      required this.message,
      this.status = 'pending',
      this.readAt,
      required this.createdAt});

  factory _$NotificationMessageImpl.fromJson(Map<String, dynamic> json) =>
      _$$NotificationMessageImplFromJson(json);

  @override
  final int id;
  @override
  final int userId;
  @override
  final String channel;
  @override
  final String title;
  @override
  final String message;
  @override
  @JsonKey()
  final String status;
  @override
  final DateTime? readAt;
  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'NotificationMessage(id: $id, userId: $userId, channel: $channel, title: $title, message: $message, status: $status, readAt: $readAt, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$NotificationMessageImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.channel, channel) || other.channel == channel) &&
            (identical(other.title, title) || other.title == title) &&
            (identical(other.message, message) || other.message == message) &&
            (identical(other.status, status) || other.status == status) &&
            (identical(other.readAt, readAt) || other.readAt == readAt) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, id, userId, channel, title,
      message, status, readAt, createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$NotificationMessageImplCopyWith<_$NotificationMessageImpl> get copyWith =>
      __$$NotificationMessageImplCopyWithImpl<_$NotificationMessageImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$NotificationMessageImplToJson(
      this,
    );
  }
}

abstract class _NotificationMessage implements NotificationMessage {
  const factory _NotificationMessage(
      {required final int id,
      required final int userId,
      required final String channel,
      required final String title,
      required final String message,
      final String status,
      final DateTime? readAt,
      required final DateTime createdAt}) = _$NotificationMessageImpl;

  factory _NotificationMessage.fromJson(Map<String, dynamic> json) =
      _$NotificationMessageImpl.fromJson;

  @override
  int get id;
  @override
  int get userId;
  @override
  String get channel;
  @override
  String get title;
  @override
  String get message;
  @override
  String get status;
  @override
  DateTime? get readAt;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$NotificationMessageImplCopyWith<_$NotificationMessageImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

WebhookEndpoint _$WebhookEndpointFromJson(Map<String, dynamic> json) {
  return _WebhookEndpoint.fromJson(json);
}

/// @nodoc
mixin _$WebhookEndpoint {
  int get id => throw _privateConstructorUsedError;
  String get name => throw _privateConstructorUsedError;
  String get url => throw _privateConstructorUsedError;
  List<String> get events => throw _privateConstructorUsedError;
  bool get isActive => throw _privateConstructorUsedError;
  DateTime? get lastTriggeredAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $WebhookEndpointCopyWith<WebhookEndpoint> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $WebhookEndpointCopyWith<$Res> {
  factory $WebhookEndpointCopyWith(
          WebhookEndpoint value, $Res Function(WebhookEndpoint) then) =
      _$WebhookEndpointCopyWithImpl<$Res, WebhookEndpoint>;
  @useResult
  $Res call(
      {int id,
      String name,
      String url,
      List<String> events,
      bool isActive,
      DateTime? lastTriggeredAt});
}

/// @nodoc
class _$WebhookEndpointCopyWithImpl<$Res, $Val extends WebhookEndpoint>
    implements $WebhookEndpointCopyWith<$Res> {
  _$WebhookEndpointCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? url = null,
    Object? events = null,
    Object? isActive = null,
    Object? lastTriggeredAt = freezed,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      name: null == name
          ? _value.name
          : name // ignore: cast_nullable_to_non_nullable
              as String,
      url: null == url
          ? _value.url
          : url // ignore: cast_nullable_to_non_nullable
              as String,
      events: null == events
          ? _value.events
          : events // ignore: cast_nullable_to_non_nullable
              as List<String>,
      isActive: null == isActive
          ? _value.isActive
          : isActive // ignore: cast_nullable_to_non_nullable
              as bool,
      lastTriggeredAt: freezed == lastTriggeredAt
          ? _value.lastTriggeredAt
          : lastTriggeredAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$WebhookEndpointImplCopyWith<$Res>
    implements $WebhookEndpointCopyWith<$Res> {
  factory _$$WebhookEndpointImplCopyWith(_$WebhookEndpointImpl value,
          $Res Function(_$WebhookEndpointImpl) then) =
      __$$WebhookEndpointImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String name,
      String url,
      List<String> events,
      bool isActive,
      DateTime? lastTriggeredAt});
}

/// @nodoc
class __$$WebhookEndpointImplCopyWithImpl<$Res>
    extends _$WebhookEndpointCopyWithImpl<$Res, _$WebhookEndpointImpl>
    implements _$$WebhookEndpointImplCopyWith<$Res> {
  __$$WebhookEndpointImplCopyWithImpl(
      _$WebhookEndpointImpl _value, $Res Function(_$WebhookEndpointImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? url = null,
    Object? events = null,
    Object? isActive = null,
    Object? lastTriggeredAt = freezed,
  }) {
    return _then(_$WebhookEndpointImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      name: null == name
          ? _value.name
          : name // ignore: cast_nullable_to_non_nullable
              as String,
      url: null == url
          ? _value.url
          : url // ignore: cast_nullable_to_non_nullable
              as String,
      events: null == events
          ? _value._events
          : events // ignore: cast_nullable_to_non_nullable
              as List<String>,
      isActive: null == isActive
          ? _value.isActive
          : isActive // ignore: cast_nullable_to_non_nullable
              as bool,
      lastTriggeredAt: freezed == lastTriggeredAt
          ? _value.lastTriggeredAt
          : lastTriggeredAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$WebhookEndpointImpl implements _WebhookEndpoint {
  const _$WebhookEndpointImpl(
      {required this.id,
      required this.name,
      required this.url,
      required final List<String> events,
      this.isActive = true,
      this.lastTriggeredAt})
      : _events = events;

  factory _$WebhookEndpointImpl.fromJson(Map<String, dynamic> json) =>
      _$$WebhookEndpointImplFromJson(json);

  @override
  final int id;
  @override
  final String name;
  @override
  final String url;
  final List<String> _events;
  @override
  List<String> get events {
    if (_events is EqualUnmodifiableListView) return _events;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_events);
  }

  @override
  @JsonKey()
  final bool isActive;
  @override
  final DateTime? lastTriggeredAt;

  @override
  String toString() {
    return 'WebhookEndpoint(id: $id, name: $name, url: $url, events: $events, isActive: $isActive, lastTriggeredAt: $lastTriggeredAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$WebhookEndpointImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.url, url) || other.url == url) &&
            const DeepCollectionEquality().equals(other._events, _events) &&
            (identical(other.isActive, isActive) ||
                other.isActive == isActive) &&
            (identical(other.lastTriggeredAt, lastTriggeredAt) ||
                other.lastTriggeredAt == lastTriggeredAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, id, name, url,
      const DeepCollectionEquality().hash(_events), isActive, lastTriggeredAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$WebhookEndpointImplCopyWith<_$WebhookEndpointImpl> get copyWith =>
      __$$WebhookEndpointImplCopyWithImpl<_$WebhookEndpointImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$WebhookEndpointImplToJson(
      this,
    );
  }
}

abstract class _WebhookEndpoint implements WebhookEndpoint {
  const factory _WebhookEndpoint(
      {required final int id,
      required final String name,
      required final String url,
      required final List<String> events,
      final bool isActive,
      final DateTime? lastTriggeredAt}) = _$WebhookEndpointImpl;

  factory _WebhookEndpoint.fromJson(Map<String, dynamic> json) =
      _$WebhookEndpointImpl.fromJson;

  @override
  int get id;
  @override
  String get name;
  @override
  String get url;
  @override
  List<String> get events;
  @override
  bool get isActive;
  @override
  DateTime? get lastTriggeredAt;
  @override
  @JsonKey(ignore: true)
  _$$WebhookEndpointImplCopyWith<_$WebhookEndpointImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

APIKeyInfo _$APIKeyInfoFromJson(Map<String, dynamic> json) {
  return _APIKeyInfo.fromJson(json);
}

/// @nodoc
mixin _$APIKeyInfo {
  int get keyId => throw _privateConstructorUsedError;
  String get key => throw _privateConstructorUsedError;
  String get name => throw _privateConstructorUsedError;
  List<String> get permissions => throw _privateConstructorUsedError;
  bool get isActive => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $APIKeyInfoCopyWith<APIKeyInfo> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $APIKeyInfoCopyWith<$Res> {
  factory $APIKeyInfoCopyWith(
          APIKeyInfo value, $Res Function(APIKeyInfo) then) =
      _$APIKeyInfoCopyWithImpl<$Res, APIKeyInfo>;
  @useResult
  $Res call(
      {int keyId,
      String key,
      String name,
      List<String> permissions,
      bool isActive});
}

/// @nodoc
class _$APIKeyInfoCopyWithImpl<$Res, $Val extends APIKeyInfo>
    implements $APIKeyInfoCopyWith<$Res> {
  _$APIKeyInfoCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? keyId = null,
    Object? key = null,
    Object? name = null,
    Object? permissions = null,
    Object? isActive = null,
  }) {
    return _then(_value.copyWith(
      keyId: null == keyId
          ? _value.keyId
          : keyId // ignore: cast_nullable_to_non_nullable
              as int,
      key: null == key
          ? _value.key
          : key // ignore: cast_nullable_to_non_nullable
              as String,
      name: null == name
          ? _value.name
          : name // ignore: cast_nullable_to_non_nullable
              as String,
      permissions: null == permissions
          ? _value.permissions
          : permissions // ignore: cast_nullable_to_non_nullable
              as List<String>,
      isActive: null == isActive
          ? _value.isActive
          : isActive // ignore: cast_nullable_to_non_nullable
              as bool,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$APIKeyInfoImplCopyWith<$Res>
    implements $APIKeyInfoCopyWith<$Res> {
  factory _$$APIKeyInfoImplCopyWith(
          _$APIKeyInfoImpl value, $Res Function(_$APIKeyInfoImpl) then) =
      __$$APIKeyInfoImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int keyId,
      String key,
      String name,
      List<String> permissions,
      bool isActive});
}

/// @nodoc
class __$$APIKeyInfoImplCopyWithImpl<$Res>
    extends _$APIKeyInfoCopyWithImpl<$Res, _$APIKeyInfoImpl>
    implements _$$APIKeyInfoImplCopyWith<$Res> {
  __$$APIKeyInfoImplCopyWithImpl(
      _$APIKeyInfoImpl _value, $Res Function(_$APIKeyInfoImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? keyId = null,
    Object? key = null,
    Object? name = null,
    Object? permissions = null,
    Object? isActive = null,
  }) {
    return _then(_$APIKeyInfoImpl(
      keyId: null == keyId
          ? _value.keyId
          : keyId // ignore: cast_nullable_to_non_nullable
              as int,
      key: null == key
          ? _value.key
          : key // ignore: cast_nullable_to_non_nullable
              as String,
      name: null == name
          ? _value.name
          : name // ignore: cast_nullable_to_non_nullable
              as String,
      permissions: null == permissions
          ? _value._permissions
          : permissions // ignore: cast_nullable_to_non_nullable
              as List<String>,
      isActive: null == isActive
          ? _value.isActive
          : isActive // ignore: cast_nullable_to_non_nullable
              as bool,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$APIKeyInfoImpl implements _APIKeyInfo {
  const _$APIKeyInfoImpl(
      {required this.keyId,
      required this.key,
      required this.name,
      required final List<String> permissions,
      this.isActive = true})
      : _permissions = permissions;

  factory _$APIKeyInfoImpl.fromJson(Map<String, dynamic> json) =>
      _$$APIKeyInfoImplFromJson(json);

  @override
  final int keyId;
  @override
  final String key;
  @override
  final String name;
  final List<String> _permissions;
  @override
  List<String> get permissions {
    if (_permissions is EqualUnmodifiableListView) return _permissions;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_permissions);
  }

  @override
  @JsonKey()
  final bool isActive;

  @override
  String toString() {
    return 'APIKeyInfo(keyId: $keyId, key: $key, name: $name, permissions: $permissions, isActive: $isActive)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$APIKeyInfoImpl &&
            (identical(other.keyId, keyId) || other.keyId == keyId) &&
            (identical(other.key, key) || other.key == key) &&
            (identical(other.name, name) || other.name == name) &&
            const DeepCollectionEquality()
                .equals(other._permissions, _permissions) &&
            (identical(other.isActive, isActive) ||
                other.isActive == isActive));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, keyId, key, name,
      const DeepCollectionEquality().hash(_permissions), isActive);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$APIKeyInfoImplCopyWith<_$APIKeyInfoImpl> get copyWith =>
      __$$APIKeyInfoImplCopyWithImpl<_$APIKeyInfoImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$APIKeyInfoImplToJson(
      this,
    );
  }
}

abstract class _APIKeyInfo implements APIKeyInfo {
  const factory _APIKeyInfo(
      {required final int keyId,
      required final String key,
      required final String name,
      required final List<String> permissions,
      final bool isActive}) = _$APIKeyInfoImpl;

  factory _APIKeyInfo.fromJson(Map<String, dynamic> json) =
      _$APIKeyInfoImpl.fromJson;

  @override
  int get keyId;
  @override
  String get key;
  @override
  String get name;
  @override
  List<String> get permissions;
  @override
  bool get isActive;
  @override
  @JsonKey(ignore: true)
  _$$APIKeyInfoImplCopyWith<_$APIKeyInfoImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

PersonalizationProfile _$PersonalizationProfileFromJson(
    Map<String, dynamic> json) {
  return _PersonalizationProfile.fromJson(json);
}

/// @nodoc
mixin _$PersonalizationProfile {
  int get id => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  String get readingLevel => throw _privateConstructorUsedError;
  Map<String, dynamic> get contentTypePreferences =>
      throw _privateConstructorUsedError;
  List<int> get authorPreferences => throw _privateConstructorUsedError;
  List<String> get keywordInterests => throw _privateConstructorUsedError;
  int get readingTimePref => throw _privateConstructorUsedError;
  String get timezone => throw _privateConstructorUsedError;
  double get personalizationScore => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $PersonalizationProfileCopyWith<PersonalizationProfile> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $PersonalizationProfileCopyWith<$Res> {
  factory $PersonalizationProfileCopyWith(PersonalizationProfile value,
          $Res Function(PersonalizationProfile) then) =
      _$PersonalizationProfileCopyWithImpl<$Res, PersonalizationProfile>;
  @useResult
  $Res call(
      {int id,
      int userId,
      String readingLevel,
      Map<String, dynamic> contentTypePreferences,
      List<int> authorPreferences,
      List<String> keywordInterests,
      int readingTimePref,
      String timezone,
      double personalizationScore});
}

/// @nodoc
class _$PersonalizationProfileCopyWithImpl<$Res,
        $Val extends PersonalizationProfile>
    implements $PersonalizationProfileCopyWith<$Res> {
  _$PersonalizationProfileCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? readingLevel = null,
    Object? contentTypePreferences = null,
    Object? authorPreferences = null,
    Object? keywordInterests = null,
    Object? readingTimePref = null,
    Object? timezone = null,
    Object? personalizationScore = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      readingLevel: null == readingLevel
          ? _value.readingLevel
          : readingLevel // ignore: cast_nullable_to_non_nullable
              as String,
      contentTypePreferences: null == contentTypePreferences
          ? _value.contentTypePreferences
          : contentTypePreferences // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      authorPreferences: null == authorPreferences
          ? _value.authorPreferences
          : authorPreferences // ignore: cast_nullable_to_non_nullable
              as List<int>,
      keywordInterests: null == keywordInterests
          ? _value.keywordInterests
          : keywordInterests // ignore: cast_nullable_to_non_nullable
              as List<String>,
      readingTimePref: null == readingTimePref
          ? _value.readingTimePref
          : readingTimePref // ignore: cast_nullable_to_non_nullable
              as int,
      timezone: null == timezone
          ? _value.timezone
          : timezone // ignore: cast_nullable_to_non_nullable
              as String,
      personalizationScore: null == personalizationScore
          ? _value.personalizationScore
          : personalizationScore // ignore: cast_nullable_to_non_nullable
              as double,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$PersonalizationProfileImplCopyWith<$Res>
    implements $PersonalizationProfileCopyWith<$Res> {
  factory _$$PersonalizationProfileImplCopyWith(
          _$PersonalizationProfileImpl value,
          $Res Function(_$PersonalizationProfileImpl) then) =
      __$$PersonalizationProfileImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int userId,
      String readingLevel,
      Map<String, dynamic> contentTypePreferences,
      List<int> authorPreferences,
      List<String> keywordInterests,
      int readingTimePref,
      String timezone,
      double personalizationScore});
}

/// @nodoc
class __$$PersonalizationProfileImplCopyWithImpl<$Res>
    extends _$PersonalizationProfileCopyWithImpl<$Res,
        _$PersonalizationProfileImpl>
    implements _$$PersonalizationProfileImplCopyWith<$Res> {
  __$$PersonalizationProfileImplCopyWithImpl(
      _$PersonalizationProfileImpl _value,
      $Res Function(_$PersonalizationProfileImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? readingLevel = null,
    Object? contentTypePreferences = null,
    Object? authorPreferences = null,
    Object? keywordInterests = null,
    Object? readingTimePref = null,
    Object? timezone = null,
    Object? personalizationScore = null,
  }) {
    return _then(_$PersonalizationProfileImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      readingLevel: null == readingLevel
          ? _value.readingLevel
          : readingLevel // ignore: cast_nullable_to_non_nullable
              as String,
      contentTypePreferences: null == contentTypePreferences
          ? _value._contentTypePreferences
          : contentTypePreferences // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      authorPreferences: null == authorPreferences
          ? _value._authorPreferences
          : authorPreferences // ignore: cast_nullable_to_non_nullable
              as List<int>,
      keywordInterests: null == keywordInterests
          ? _value._keywordInterests
          : keywordInterests // ignore: cast_nullable_to_non_nullable
              as List<String>,
      readingTimePref: null == readingTimePref
          ? _value.readingTimePref
          : readingTimePref // ignore: cast_nullable_to_non_nullable
              as int,
      timezone: null == timezone
          ? _value.timezone
          : timezone // ignore: cast_nullable_to_non_nullable
              as String,
      personalizationScore: null == personalizationScore
          ? _value.personalizationScore
          : personalizationScore // ignore: cast_nullable_to_non_nullable
              as double,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$PersonalizationProfileImpl implements _PersonalizationProfile {
  const _$PersonalizationProfileImpl(
      {required this.id,
      required this.userId,
      this.readingLevel = 'intermediate',
      final Map<String, dynamic> contentTypePreferences = const {},
      final List<int> authorPreferences = const [],
      final List<String> keywordInterests = const [],
      this.readingTimePref = 0,
      this.timezone = 'UTC',
      this.personalizationScore = 0.0})
      : _contentTypePreferences = contentTypePreferences,
        _authorPreferences = authorPreferences,
        _keywordInterests = keywordInterests;

  factory _$PersonalizationProfileImpl.fromJson(Map<String, dynamic> json) =>
      _$$PersonalizationProfileImplFromJson(json);

  @override
  final int id;
  @override
  final int userId;
  @override
  @JsonKey()
  final String readingLevel;
  final Map<String, dynamic> _contentTypePreferences;
  @override
  @JsonKey()
  Map<String, dynamic> get contentTypePreferences {
    if (_contentTypePreferences is EqualUnmodifiableMapView)
      return _contentTypePreferences;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(_contentTypePreferences);
  }

  final List<int> _authorPreferences;
  @override
  @JsonKey()
  List<int> get authorPreferences {
    if (_authorPreferences is EqualUnmodifiableListView)
      return _authorPreferences;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_authorPreferences);
  }

  final List<String> _keywordInterests;
  @override
  @JsonKey()
  List<String> get keywordInterests {
    if (_keywordInterests is EqualUnmodifiableListView)
      return _keywordInterests;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_keywordInterests);
  }

  @override
  @JsonKey()
  final int readingTimePref;
  @override
  @JsonKey()
  final String timezone;
  @override
  @JsonKey()
  final double personalizationScore;

  @override
  String toString() {
    return 'PersonalizationProfile(id: $id, userId: $userId, readingLevel: $readingLevel, contentTypePreferences: $contentTypePreferences, authorPreferences: $authorPreferences, keywordInterests: $keywordInterests, readingTimePref: $readingTimePref, timezone: $timezone, personalizationScore: $personalizationScore)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$PersonalizationProfileImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.readingLevel, readingLevel) ||
                other.readingLevel == readingLevel) &&
            const DeepCollectionEquality().equals(
                other._contentTypePreferences, _contentTypePreferences) &&
            const DeepCollectionEquality()
                .equals(other._authorPreferences, _authorPreferences) &&
            const DeepCollectionEquality()
                .equals(other._keywordInterests, _keywordInterests) &&
            (identical(other.readingTimePref, readingTimePref) ||
                other.readingTimePref == readingTimePref) &&
            (identical(other.timezone, timezone) ||
                other.timezone == timezone) &&
            (identical(other.personalizationScore, personalizationScore) ||
                other.personalizationScore == personalizationScore));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      userId,
      readingLevel,
      const DeepCollectionEquality().hash(_contentTypePreferences),
      const DeepCollectionEquality().hash(_authorPreferences),
      const DeepCollectionEquality().hash(_keywordInterests),
      readingTimePref,
      timezone,
      personalizationScore);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$PersonalizationProfileImplCopyWith<_$PersonalizationProfileImpl>
      get copyWith => __$$PersonalizationProfileImplCopyWithImpl<
          _$PersonalizationProfileImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$PersonalizationProfileImplToJson(
      this,
    );
  }
}

abstract class _PersonalizationProfile implements PersonalizationProfile {
  const factory _PersonalizationProfile(
      {required final int id,
      required final int userId,
      final String readingLevel,
      final Map<String, dynamic> contentTypePreferences,
      final List<int> authorPreferences,
      final List<String> keywordInterests,
      final int readingTimePref,
      final String timezone,
      final double personalizationScore}) = _$PersonalizationProfileImpl;

  factory _PersonalizationProfile.fromJson(Map<String, dynamic> json) =
      _$PersonalizationProfileImpl.fromJson;

  @override
  int get id;
  @override
  int get userId;
  @override
  String get readingLevel;
  @override
  Map<String, dynamic> get contentTypePreferences;
  @override
  List<int> get authorPreferences;
  @override
  List<String> get keywordInterests;
  @override
  int get readingTimePref;
  @override
  String get timezone;
  @override
  double get personalizationScore;
  @override
  @JsonKey(ignore: true)
  _$$PersonalizationProfileImplCopyWith<_$PersonalizationProfileImpl>
      get copyWith => throw _privateConstructorUsedError;
}

SubscriberAnalytics _$SubscriberAnalyticsFromJson(Map<String, dynamic> json) {
  return _SubscriberAnalytics.fromJson(json);
}

/// @nodoc
mixin _$SubscriberAnalytics {
  int get subscriberId => throw _privateConstructorUsedError;
  DateTime get date => throw _privateConstructorUsedError;
  bool get dailyActive => throw _privateConstructorUsedError;
  int get articlesRead => throw _privateConstructorUsedError;
  int get sessionCount => throw _privateConstructorUsedError;
  double get avgSessionTime => throw _privateConstructorUsedError;
  double get engagementScore => throw _privateConstructorUsedError;
  double get retentionScore => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $SubscriberAnalyticsCopyWith<SubscriberAnalytics> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $SubscriberAnalyticsCopyWith<$Res> {
  factory $SubscriberAnalyticsCopyWith(
          SubscriberAnalytics value, $Res Function(SubscriberAnalytics) then) =
      _$SubscriberAnalyticsCopyWithImpl<$Res, SubscriberAnalytics>;
  @useResult
  $Res call(
      {int subscriberId,
      DateTime date,
      bool dailyActive,
      int articlesRead,
      int sessionCount,
      double avgSessionTime,
      double engagementScore,
      double retentionScore});
}

/// @nodoc
class _$SubscriberAnalyticsCopyWithImpl<$Res, $Val extends SubscriberAnalytics>
    implements $SubscriberAnalyticsCopyWith<$Res> {
  _$SubscriberAnalyticsCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? subscriberId = null,
    Object? date = null,
    Object? dailyActive = null,
    Object? articlesRead = null,
    Object? sessionCount = null,
    Object? avgSessionTime = null,
    Object? engagementScore = null,
    Object? retentionScore = null,
  }) {
    return _then(_value.copyWith(
      subscriberId: null == subscriberId
          ? _value.subscriberId
          : subscriberId // ignore: cast_nullable_to_non_nullable
              as int,
      date: null == date
          ? _value.date
          : date // ignore: cast_nullable_to_non_nullable
              as DateTime,
      dailyActive: null == dailyActive
          ? _value.dailyActive
          : dailyActive // ignore: cast_nullable_to_non_nullable
              as bool,
      articlesRead: null == articlesRead
          ? _value.articlesRead
          : articlesRead // ignore: cast_nullable_to_non_nullable
              as int,
      sessionCount: null == sessionCount
          ? _value.sessionCount
          : sessionCount // ignore: cast_nullable_to_non_nullable
              as int,
      avgSessionTime: null == avgSessionTime
          ? _value.avgSessionTime
          : avgSessionTime // ignore: cast_nullable_to_non_nullable
              as double,
      engagementScore: null == engagementScore
          ? _value.engagementScore
          : engagementScore // ignore: cast_nullable_to_non_nullable
              as double,
      retentionScore: null == retentionScore
          ? _value.retentionScore
          : retentionScore // ignore: cast_nullable_to_non_nullable
              as double,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$SubscriberAnalyticsImplCopyWith<$Res>
    implements $SubscriberAnalyticsCopyWith<$Res> {
  factory _$$SubscriberAnalyticsImplCopyWith(_$SubscriberAnalyticsImpl value,
          $Res Function(_$SubscriberAnalyticsImpl) then) =
      __$$SubscriberAnalyticsImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int subscriberId,
      DateTime date,
      bool dailyActive,
      int articlesRead,
      int sessionCount,
      double avgSessionTime,
      double engagementScore,
      double retentionScore});
}

/// @nodoc
class __$$SubscriberAnalyticsImplCopyWithImpl<$Res>
    extends _$SubscriberAnalyticsCopyWithImpl<$Res, _$SubscriberAnalyticsImpl>
    implements _$$SubscriberAnalyticsImplCopyWith<$Res> {
  __$$SubscriberAnalyticsImplCopyWithImpl(_$SubscriberAnalyticsImpl _value,
      $Res Function(_$SubscriberAnalyticsImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? subscriberId = null,
    Object? date = null,
    Object? dailyActive = null,
    Object? articlesRead = null,
    Object? sessionCount = null,
    Object? avgSessionTime = null,
    Object? engagementScore = null,
    Object? retentionScore = null,
  }) {
    return _then(_$SubscriberAnalyticsImpl(
      subscriberId: null == subscriberId
          ? _value.subscriberId
          : subscriberId // ignore: cast_nullable_to_non_nullable
              as int,
      date: null == date
          ? _value.date
          : date // ignore: cast_nullable_to_non_nullable
              as DateTime,
      dailyActive: null == dailyActive
          ? _value.dailyActive
          : dailyActive // ignore: cast_nullable_to_non_nullable
              as bool,
      articlesRead: null == articlesRead
          ? _value.articlesRead
          : articlesRead // ignore: cast_nullable_to_non_nullable
              as int,
      sessionCount: null == sessionCount
          ? _value.sessionCount
          : sessionCount // ignore: cast_nullable_to_non_nullable
              as int,
      avgSessionTime: null == avgSessionTime
          ? _value.avgSessionTime
          : avgSessionTime // ignore: cast_nullable_to_non_nullable
              as double,
      engagementScore: null == engagementScore
          ? _value.engagementScore
          : engagementScore // ignore: cast_nullable_to_non_nullable
              as double,
      retentionScore: null == retentionScore
          ? _value.retentionScore
          : retentionScore // ignore: cast_nullable_to_non_nullable
              as double,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$SubscriberAnalyticsImpl implements _SubscriberAnalytics {
  const _$SubscriberAnalyticsImpl(
      {required this.subscriberId,
      required this.date,
      this.dailyActive = false,
      this.articlesRead = 0,
      this.sessionCount = 0,
      this.avgSessionTime = 0.0,
      this.engagementScore = 0.0,
      this.retentionScore = 0.0});

  factory _$SubscriberAnalyticsImpl.fromJson(Map<String, dynamic> json) =>
      _$$SubscriberAnalyticsImplFromJson(json);

  @override
  final int subscriberId;
  @override
  final DateTime date;
  @override
  @JsonKey()
  final bool dailyActive;
  @override
  @JsonKey()
  final int articlesRead;
  @override
  @JsonKey()
  final int sessionCount;
  @override
  @JsonKey()
  final double avgSessionTime;
  @override
  @JsonKey()
  final double engagementScore;
  @override
  @JsonKey()
  final double retentionScore;

  @override
  String toString() {
    return 'SubscriberAnalytics(subscriberId: $subscriberId, date: $date, dailyActive: $dailyActive, articlesRead: $articlesRead, sessionCount: $sessionCount, avgSessionTime: $avgSessionTime, engagementScore: $engagementScore, retentionScore: $retentionScore)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$SubscriberAnalyticsImpl &&
            (identical(other.subscriberId, subscriberId) ||
                other.subscriberId == subscriberId) &&
            (identical(other.date, date) || other.date == date) &&
            (identical(other.dailyActive, dailyActive) ||
                other.dailyActive == dailyActive) &&
            (identical(other.articlesRead, articlesRead) ||
                other.articlesRead == articlesRead) &&
            (identical(other.sessionCount, sessionCount) ||
                other.sessionCount == sessionCount) &&
            (identical(other.avgSessionTime, avgSessionTime) ||
                other.avgSessionTime == avgSessionTime) &&
            (identical(other.engagementScore, engagementScore) ||
                other.engagementScore == engagementScore) &&
            (identical(other.retentionScore, retentionScore) ||
                other.retentionScore == retentionScore));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      subscriberId,
      date,
      dailyActive,
      articlesRead,
      sessionCount,
      avgSessionTime,
      engagementScore,
      retentionScore);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$SubscriberAnalyticsImplCopyWith<_$SubscriberAnalyticsImpl> get copyWith =>
      __$$SubscriberAnalyticsImplCopyWithImpl<_$SubscriberAnalyticsImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$SubscriberAnalyticsImplToJson(
      this,
    );
  }
}

abstract class _SubscriberAnalytics implements SubscriberAnalytics {
  const factory _SubscriberAnalytics(
      {required final int subscriberId,
      required final DateTime date,
      final bool dailyActive,
      final int articlesRead,
      final int sessionCount,
      final double avgSessionTime,
      final double engagementScore,
      final double retentionScore}) = _$SubscriberAnalyticsImpl;

  factory _SubscriberAnalytics.fromJson(Map<String, dynamic> json) =
      _$SubscriberAnalyticsImpl.fromJson;

  @override
  int get subscriberId;
  @override
  DateTime get date;
  @override
  bool get dailyActive;
  @override
  int get articlesRead;
  @override
  int get sessionCount;
  @override
  double get avgSessionTime;
  @override
  double get engagementScore;
  @override
  double get retentionScore;
  @override
  @JsonKey(ignore: true)
  _$$SubscriberAnalyticsImplCopyWith<_$SubscriberAnalyticsImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

CampaignPerformance _$CampaignPerformanceFromJson(Map<String, dynamic> json) {
  return _CampaignPerformance.fromJson(json);
}

/// @nodoc
mixin _$CampaignPerformance {
  int get campaignId => throw _privateConstructorUsedError;
  String get campaignName => throw _privateConstructorUsedError;
  int get recipientCount => throw _privateConstructorUsedError;
  int get sentCount => throw _privateConstructorUsedError;
  int get openCount => throw _privateConstructorUsedError;
  int get clickCount => throw _privateConstructorUsedError;
  double get openRate => throw _privateConstructorUsedError;
  double get clickRate => throw _privateConstructorUsedError;
  DateTime get sentAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $CampaignPerformanceCopyWith<CampaignPerformance> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $CampaignPerformanceCopyWith<$Res> {
  factory $CampaignPerformanceCopyWith(
          CampaignPerformance value, $Res Function(CampaignPerformance) then) =
      _$CampaignPerformanceCopyWithImpl<$Res, CampaignPerformance>;
  @useResult
  $Res call(
      {int campaignId,
      String campaignName,
      int recipientCount,
      int sentCount,
      int openCount,
      int clickCount,
      double openRate,
      double clickRate,
      DateTime sentAt});
}

/// @nodoc
class _$CampaignPerformanceCopyWithImpl<$Res, $Val extends CampaignPerformance>
    implements $CampaignPerformanceCopyWith<$Res> {
  _$CampaignPerformanceCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? campaignId = null,
    Object? campaignName = null,
    Object? recipientCount = null,
    Object? sentCount = null,
    Object? openCount = null,
    Object? clickCount = null,
    Object? openRate = null,
    Object? clickRate = null,
    Object? sentAt = null,
  }) {
    return _then(_value.copyWith(
      campaignId: null == campaignId
          ? _value.campaignId
          : campaignId // ignore: cast_nullable_to_non_nullable
              as int,
      campaignName: null == campaignName
          ? _value.campaignName
          : campaignName // ignore: cast_nullable_to_non_nullable
              as String,
      recipientCount: null == recipientCount
          ? _value.recipientCount
          : recipientCount // ignore: cast_nullable_to_non_nullable
              as int,
      sentCount: null == sentCount
          ? _value.sentCount
          : sentCount // ignore: cast_nullable_to_non_nullable
              as int,
      openCount: null == openCount
          ? _value.openCount
          : openCount // ignore: cast_nullable_to_non_nullable
              as int,
      clickCount: null == clickCount
          ? _value.clickCount
          : clickCount // ignore: cast_nullable_to_non_nullable
              as int,
      openRate: null == openRate
          ? _value.openRate
          : openRate // ignore: cast_nullable_to_non_nullable
              as double,
      clickRate: null == clickRate
          ? _value.clickRate
          : clickRate // ignore: cast_nullable_to_non_nullable
              as double,
      sentAt: null == sentAt
          ? _value.sentAt
          : sentAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$CampaignPerformanceImplCopyWith<$Res>
    implements $CampaignPerformanceCopyWith<$Res> {
  factory _$$CampaignPerformanceImplCopyWith(_$CampaignPerformanceImpl value,
          $Res Function(_$CampaignPerformanceImpl) then) =
      __$$CampaignPerformanceImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int campaignId,
      String campaignName,
      int recipientCount,
      int sentCount,
      int openCount,
      int clickCount,
      double openRate,
      double clickRate,
      DateTime sentAt});
}

/// @nodoc
class __$$CampaignPerformanceImplCopyWithImpl<$Res>
    extends _$CampaignPerformanceCopyWithImpl<$Res, _$CampaignPerformanceImpl>
    implements _$$CampaignPerformanceImplCopyWith<$Res> {
  __$$CampaignPerformanceImplCopyWithImpl(_$CampaignPerformanceImpl _value,
      $Res Function(_$CampaignPerformanceImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? campaignId = null,
    Object? campaignName = null,
    Object? recipientCount = null,
    Object? sentCount = null,
    Object? openCount = null,
    Object? clickCount = null,
    Object? openRate = null,
    Object? clickRate = null,
    Object? sentAt = null,
  }) {
    return _then(_$CampaignPerformanceImpl(
      campaignId: null == campaignId
          ? _value.campaignId
          : campaignId // ignore: cast_nullable_to_non_nullable
              as int,
      campaignName: null == campaignName
          ? _value.campaignName
          : campaignName // ignore: cast_nullable_to_non_nullable
              as String,
      recipientCount: null == recipientCount
          ? _value.recipientCount
          : recipientCount // ignore: cast_nullable_to_non_nullable
              as int,
      sentCount: null == sentCount
          ? _value.sentCount
          : sentCount // ignore: cast_nullable_to_non_nullable
              as int,
      openCount: null == openCount
          ? _value.openCount
          : openCount // ignore: cast_nullable_to_non_nullable
              as int,
      clickCount: null == clickCount
          ? _value.clickCount
          : clickCount // ignore: cast_nullable_to_non_nullable
              as int,
      openRate: null == openRate
          ? _value.openRate
          : openRate // ignore: cast_nullable_to_non_nullable
              as double,
      clickRate: null == clickRate
          ? _value.clickRate
          : clickRate // ignore: cast_nullable_to_non_nullable
              as double,
      sentAt: null == sentAt
          ? _value.sentAt
          : sentAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$CampaignPerformanceImpl implements _CampaignPerformance {
  const _$CampaignPerformanceImpl(
      {required this.campaignId,
      required this.campaignName,
      required this.recipientCount,
      required this.sentCount,
      required this.openCount,
      required this.clickCount,
      this.openRate = 0,
      this.clickRate = 0,
      required this.sentAt});

  factory _$CampaignPerformanceImpl.fromJson(Map<String, dynamic> json) =>
      _$$CampaignPerformanceImplFromJson(json);

  @override
  final int campaignId;
  @override
  final String campaignName;
  @override
  final int recipientCount;
  @override
  final int sentCount;
  @override
  final int openCount;
  @override
  final int clickCount;
  @override
  @JsonKey()
  final double openRate;
  @override
  @JsonKey()
  final double clickRate;
  @override
  final DateTime sentAt;

  @override
  String toString() {
    return 'CampaignPerformance(campaignId: $campaignId, campaignName: $campaignName, recipientCount: $recipientCount, sentCount: $sentCount, openCount: $openCount, clickCount: $clickCount, openRate: $openRate, clickRate: $clickRate, sentAt: $sentAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$CampaignPerformanceImpl &&
            (identical(other.campaignId, campaignId) ||
                other.campaignId == campaignId) &&
            (identical(other.campaignName, campaignName) ||
                other.campaignName == campaignName) &&
            (identical(other.recipientCount, recipientCount) ||
                other.recipientCount == recipientCount) &&
            (identical(other.sentCount, sentCount) ||
                other.sentCount == sentCount) &&
            (identical(other.openCount, openCount) ||
                other.openCount == openCount) &&
            (identical(other.clickCount, clickCount) ||
                other.clickCount == clickCount) &&
            (identical(other.openRate, openRate) ||
                other.openRate == openRate) &&
            (identical(other.clickRate, clickRate) ||
                other.clickRate == clickRate) &&
            (identical(other.sentAt, sentAt) || other.sentAt == sentAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      campaignId,
      campaignName,
      recipientCount,
      sentCount,
      openCount,
      clickCount,
      openRate,
      clickRate,
      sentAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$CampaignPerformanceImplCopyWith<_$CampaignPerformanceImpl> get copyWith =>
      __$$CampaignPerformanceImplCopyWithImpl<_$CampaignPerformanceImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$CampaignPerformanceImplToJson(
      this,
    );
  }
}

abstract class _CampaignPerformance implements CampaignPerformance {
  const factory _CampaignPerformance(
      {required final int campaignId,
      required final String campaignName,
      required final int recipientCount,
      required final int sentCount,
      required final int openCount,
      required final int clickCount,
      final double openRate,
      final double clickRate,
      required final DateTime sentAt}) = _$CampaignPerformanceImpl;

  factory _CampaignPerformance.fromJson(Map<String, dynamic> json) =
      _$CampaignPerformanceImpl.fromJson;

  @override
  int get campaignId;
  @override
  String get campaignName;
  @override
  int get recipientCount;
  @override
  int get sentCount;
  @override
  int get openCount;
  @override
  int get clickCount;
  @override
  double get openRate;
  @override
  double get clickRate;
  @override
  DateTime get sentAt;
  @override
  @JsonKey(ignore: true)
  _$$CampaignPerformanceImplCopyWith<_$CampaignPerformanceImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

SegmentMetrics _$SegmentMetricsFromJson(Map<String, dynamic> json) {
  return _SegmentMetrics.fromJson(json);
}

/// @nodoc
mixin _$SegmentMetrics {
  int get segmentId => throw _privateConstructorUsedError;
  String get segmentName => throw _privateConstructorUsedError;
  int get userCount => throw _privateConstructorUsedError;
  double get avgEngagement => throw _privateConstructorUsedError;
  double get churnRisk => throw _privateConstructorUsedError;
  int get activeUsers => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $SegmentMetricsCopyWith<SegmentMetrics> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $SegmentMetricsCopyWith<$Res> {
  factory $SegmentMetricsCopyWith(
          SegmentMetrics value, $Res Function(SegmentMetrics) then) =
      _$SegmentMetricsCopyWithImpl<$Res, SegmentMetrics>;
  @useResult
  $Res call(
      {int segmentId,
      String segmentName,
      int userCount,
      double avgEngagement,
      double churnRisk,
      int activeUsers});
}

/// @nodoc
class _$SegmentMetricsCopyWithImpl<$Res, $Val extends SegmentMetrics>
    implements $SegmentMetricsCopyWith<$Res> {
  _$SegmentMetricsCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? segmentId = null,
    Object? segmentName = null,
    Object? userCount = null,
    Object? avgEngagement = null,
    Object? churnRisk = null,
    Object? activeUsers = null,
  }) {
    return _then(_value.copyWith(
      segmentId: null == segmentId
          ? _value.segmentId
          : segmentId // ignore: cast_nullable_to_non_nullable
              as int,
      segmentName: null == segmentName
          ? _value.segmentName
          : segmentName // ignore: cast_nullable_to_non_nullable
              as String,
      userCount: null == userCount
          ? _value.userCount
          : userCount // ignore: cast_nullable_to_non_nullable
              as int,
      avgEngagement: null == avgEngagement
          ? _value.avgEngagement
          : avgEngagement // ignore: cast_nullable_to_non_nullable
              as double,
      churnRisk: null == churnRisk
          ? _value.churnRisk
          : churnRisk // ignore: cast_nullable_to_non_nullable
              as double,
      activeUsers: null == activeUsers
          ? _value.activeUsers
          : activeUsers // ignore: cast_nullable_to_non_nullable
              as int,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$SegmentMetricsImplCopyWith<$Res>
    implements $SegmentMetricsCopyWith<$Res> {
  factory _$$SegmentMetricsImplCopyWith(_$SegmentMetricsImpl value,
          $Res Function(_$SegmentMetricsImpl) then) =
      __$$SegmentMetricsImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int segmentId,
      String segmentName,
      int userCount,
      double avgEngagement,
      double churnRisk,
      int activeUsers});
}

/// @nodoc
class __$$SegmentMetricsImplCopyWithImpl<$Res>
    extends _$SegmentMetricsCopyWithImpl<$Res, _$SegmentMetricsImpl>
    implements _$$SegmentMetricsImplCopyWith<$Res> {
  __$$SegmentMetricsImplCopyWithImpl(
      _$SegmentMetricsImpl _value, $Res Function(_$SegmentMetricsImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? segmentId = null,
    Object? segmentName = null,
    Object? userCount = null,
    Object? avgEngagement = null,
    Object? churnRisk = null,
    Object? activeUsers = null,
  }) {
    return _then(_$SegmentMetricsImpl(
      segmentId: null == segmentId
          ? _value.segmentId
          : segmentId // ignore: cast_nullable_to_non_nullable
              as int,
      segmentName: null == segmentName
          ? _value.segmentName
          : segmentName // ignore: cast_nullable_to_non_nullable
              as String,
      userCount: null == userCount
          ? _value.userCount
          : userCount // ignore: cast_nullable_to_non_nullable
              as int,
      avgEngagement: null == avgEngagement
          ? _value.avgEngagement
          : avgEngagement // ignore: cast_nullable_to_non_nullable
              as double,
      churnRisk: null == churnRisk
          ? _value.churnRisk
          : churnRisk // ignore: cast_nullable_to_non_nullable
              as double,
      activeUsers: null == activeUsers
          ? _value.activeUsers
          : activeUsers // ignore: cast_nullable_to_non_nullable
              as int,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$SegmentMetricsImpl implements _SegmentMetrics {
  const _$SegmentMetricsImpl(
      {required this.segmentId,
      required this.segmentName,
      required this.userCount,
      this.avgEngagement = 0,
      this.churnRisk = 0.0,
      this.activeUsers = 0});

  factory _$SegmentMetricsImpl.fromJson(Map<String, dynamic> json) =>
      _$$SegmentMetricsImplFromJson(json);

  @override
  final int segmentId;
  @override
  final String segmentName;
  @override
  final int userCount;
  @override
  @JsonKey()
  final double avgEngagement;
  @override
  @JsonKey()
  final double churnRisk;
  @override
  @JsonKey()
  final int activeUsers;

  @override
  String toString() {
    return 'SegmentMetrics(segmentId: $segmentId, segmentName: $segmentName, userCount: $userCount, avgEngagement: $avgEngagement, churnRisk: $churnRisk, activeUsers: $activeUsers)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$SegmentMetricsImpl &&
            (identical(other.segmentId, segmentId) ||
                other.segmentId == segmentId) &&
            (identical(other.segmentName, segmentName) ||
                other.segmentName == segmentName) &&
            (identical(other.userCount, userCount) ||
                other.userCount == userCount) &&
            (identical(other.avgEngagement, avgEngagement) ||
                other.avgEngagement == avgEngagement) &&
            (identical(other.churnRisk, churnRisk) ||
                other.churnRisk == churnRisk) &&
            (identical(other.activeUsers, activeUsers) ||
                other.activeUsers == activeUsers));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, segmentId, segmentName,
      userCount, avgEngagement, churnRisk, activeUsers);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$SegmentMetricsImplCopyWith<_$SegmentMetricsImpl> get copyWith =>
      __$$SegmentMetricsImplCopyWithImpl<_$SegmentMetricsImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$SegmentMetricsImplToJson(
      this,
    );
  }
}

abstract class _SegmentMetrics implements SegmentMetrics {
  const factory _SegmentMetrics(
      {required final int segmentId,
      required final String segmentName,
      required final int userCount,
      final double avgEngagement,
      final double churnRisk,
      final int activeUsers}) = _$SegmentMetricsImpl;

  factory _SegmentMetrics.fromJson(Map<String, dynamic> json) =
      _$SegmentMetricsImpl.fromJson;

  @override
  int get segmentId;
  @override
  String get segmentName;
  @override
  int get userCount;
  @override
  double get avgEngagement;
  @override
  double get churnRisk;
  @override
  int get activeUsers;
  @override
  @JsonKey(ignore: true)
  _$$SegmentMetricsImplCopyWith<_$SegmentMetricsImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

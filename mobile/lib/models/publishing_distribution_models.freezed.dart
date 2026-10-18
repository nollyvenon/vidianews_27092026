// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'publishing_distribution_models.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
    'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models');

PublishingJob _$PublishingJobFromJson(Map<String, dynamic> json) {
  return _PublishingJob.fromJson(json);
}

/// @nodoc
mixin _$PublishingJob {
  int get id => throw _privateConstructorUsedError;
  String get title => throw _privateConstructorUsedError;
  String get status => throw _privateConstructorUsedError;
  DateTime get scheduledPublishTime => throw _privateConstructorUsedError;
  DateTime? get actualPublishTime => throw _privateConstructorUsedError;
  List<String> get distributionChannels => throw _privateConstructorUsedError;
  bool get autoPromote => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $PublishingJobCopyWith<PublishingJob> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $PublishingJobCopyWith<$Res> {
  factory $PublishingJobCopyWith(
          PublishingJob value, $Res Function(PublishingJob) then) =
      _$PublishingJobCopyWithImpl<$Res, PublishingJob>;
  @useResult
  $Res call(
      {int id,
      String title,
      String status,
      DateTime scheduledPublishTime,
      DateTime? actualPublishTime,
      List<String> distributionChannels,
      bool autoPromote});
}

/// @nodoc
class _$PublishingJobCopyWithImpl<$Res, $Val extends PublishingJob>
    implements $PublishingJobCopyWith<$Res> {
  _$PublishingJobCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? title = null,
    Object? status = null,
    Object? scheduledPublishTime = null,
    Object? actualPublishTime = freezed,
    Object? distributionChannels = null,
    Object? autoPromote = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      title: null == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      scheduledPublishTime: null == scheduledPublishTime
          ? _value.scheduledPublishTime
          : scheduledPublishTime // ignore: cast_nullable_to_non_nullable
              as DateTime,
      actualPublishTime: freezed == actualPublishTime
          ? _value.actualPublishTime
          : actualPublishTime // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      distributionChannels: null == distributionChannels
          ? _value.distributionChannels
          : distributionChannels // ignore: cast_nullable_to_non_nullable
              as List<String>,
      autoPromote: null == autoPromote
          ? _value.autoPromote
          : autoPromote // ignore: cast_nullable_to_non_nullable
              as bool,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$PublishingJobImplCopyWith<$Res>
    implements $PublishingJobCopyWith<$Res> {
  factory _$$PublishingJobImplCopyWith(
          _$PublishingJobImpl value, $Res Function(_$PublishingJobImpl) then) =
      __$$PublishingJobImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String title,
      String status,
      DateTime scheduledPublishTime,
      DateTime? actualPublishTime,
      List<String> distributionChannels,
      bool autoPromote});
}

/// @nodoc
class __$$PublishingJobImplCopyWithImpl<$Res>
    extends _$PublishingJobCopyWithImpl<$Res, _$PublishingJobImpl>
    implements _$$PublishingJobImplCopyWith<$Res> {
  __$$PublishingJobImplCopyWithImpl(
      _$PublishingJobImpl _value, $Res Function(_$PublishingJobImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? title = null,
    Object? status = null,
    Object? scheduledPublishTime = null,
    Object? actualPublishTime = freezed,
    Object? distributionChannels = null,
    Object? autoPromote = null,
  }) {
    return _then(_$PublishingJobImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      title: null == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      scheduledPublishTime: null == scheduledPublishTime
          ? _value.scheduledPublishTime
          : scheduledPublishTime // ignore: cast_nullable_to_non_nullable
              as DateTime,
      actualPublishTime: freezed == actualPublishTime
          ? _value.actualPublishTime
          : actualPublishTime // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      distributionChannels: null == distributionChannels
          ? _value._distributionChannels
          : distributionChannels // ignore: cast_nullable_to_non_nullable
              as List<String>,
      autoPromote: null == autoPromote
          ? _value.autoPromote
          : autoPromote // ignore: cast_nullable_to_non_nullable
              as bool,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$PublishingJobImpl implements _PublishingJob {
  const _$PublishingJobImpl(
      {required this.id,
      required this.title,
      required this.status,
      required this.scheduledPublishTime,
      this.actualPublishTime,
      required final List<String> distributionChannels,
      this.autoPromote = false})
      : _distributionChannels = distributionChannels;

  factory _$PublishingJobImpl.fromJson(Map<String, dynamic> json) =>
      _$$PublishingJobImplFromJson(json);

  @override
  final int id;
  @override
  final String title;
  @override
  final String status;
  @override
  final DateTime scheduledPublishTime;
  @override
  final DateTime? actualPublishTime;
  final List<String> _distributionChannels;
  @override
  List<String> get distributionChannels {
    if (_distributionChannels is EqualUnmodifiableListView)
      return _distributionChannels;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_distributionChannels);
  }

  @override
  @JsonKey()
  final bool autoPromote;

  @override
  String toString() {
    return 'PublishingJob(id: $id, title: $title, status: $status, scheduledPublishTime: $scheduledPublishTime, actualPublishTime: $actualPublishTime, distributionChannels: $distributionChannels, autoPromote: $autoPromote)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$PublishingJobImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.title, title) || other.title == title) &&
            (identical(other.status, status) || other.status == status) &&
            (identical(other.scheduledPublishTime, scheduledPublishTime) ||
                other.scheduledPublishTime == scheduledPublishTime) &&
            (identical(other.actualPublishTime, actualPublishTime) ||
                other.actualPublishTime == actualPublishTime) &&
            const DeepCollectionEquality()
                .equals(other._distributionChannels, _distributionChannels) &&
            (identical(other.autoPromote, autoPromote) ||
                other.autoPromote == autoPromote));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      title,
      status,
      scheduledPublishTime,
      actualPublishTime,
      const DeepCollectionEquality().hash(_distributionChannels),
      autoPromote);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$PublishingJobImplCopyWith<_$PublishingJobImpl> get copyWith =>
      __$$PublishingJobImplCopyWithImpl<_$PublishingJobImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$PublishingJobImplToJson(
      this,
    );
  }
}

abstract class _PublishingJob implements PublishingJob {
  const factory _PublishingJob(
      {required final int id,
      required final String title,
      required final String status,
      required final DateTime scheduledPublishTime,
      final DateTime? actualPublishTime,
      required final List<String> distributionChannels,
      final bool autoPromote}) = _$PublishingJobImpl;

  factory _PublishingJob.fromJson(Map<String, dynamic> json) =
      _$PublishingJobImpl.fromJson;

  @override
  int get id;
  @override
  String get title;
  @override
  String get status;
  @override
  DateTime get scheduledPublishTime;
  @override
  DateTime? get actualPublishTime;
  @override
  List<String> get distributionChannels;
  @override
  bool get autoPromote;
  @override
  @JsonKey(ignore: true)
  _$$PublishingJobImplCopyWith<_$PublishingJobImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

EngagementMetric _$EngagementMetricFromJson(Map<String, dynamic> json) {
  return _EngagementMetric.fromJson(json);
}

/// @nodoc
mixin _$EngagementMetric {
  int get id => throw _privateConstructorUsedError;
  int get contentId => throw _privateConstructorUsedError;
  int get views => throw _privateConstructorUsedError;
  int get clicks => throw _privateConstructorUsedError;
  int get shares => throw _privateConstructorUsedError;
  double get ctr => throw _privateConstructorUsedError;
  double get engagementRate => throw _privateConstructorUsedError;
  double get shareRate => throw _privateConstructorUsedError;
  double get conversionRate => throw _privateConstructorUsedError;
  double get engagementScore => throw _privateConstructorUsedError;
  DateTime get recordedAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $EngagementMetricCopyWith<EngagementMetric> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $EngagementMetricCopyWith<$Res> {
  factory $EngagementMetricCopyWith(
          EngagementMetric value, $Res Function(EngagementMetric) then) =
      _$EngagementMetricCopyWithImpl<$Res, EngagementMetric>;
  @useResult
  $Res call(
      {int id,
      int contentId,
      int views,
      int clicks,
      int shares,
      double ctr,
      double engagementRate,
      double shareRate,
      double conversionRate,
      double engagementScore,
      DateTime recordedAt});
}

/// @nodoc
class _$EngagementMetricCopyWithImpl<$Res, $Val extends EngagementMetric>
    implements $EngagementMetricCopyWith<$Res> {
  _$EngagementMetricCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? contentId = null,
    Object? views = null,
    Object? clicks = null,
    Object? shares = null,
    Object? ctr = null,
    Object? engagementRate = null,
    Object? shareRate = null,
    Object? conversionRate = null,
    Object? engagementScore = null,
    Object? recordedAt = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      contentId: null == contentId
          ? _value.contentId
          : contentId // ignore: cast_nullable_to_non_nullable
              as int,
      views: null == views
          ? _value.views
          : views // ignore: cast_nullable_to_non_nullable
              as int,
      clicks: null == clicks
          ? _value.clicks
          : clicks // ignore: cast_nullable_to_non_nullable
              as int,
      shares: null == shares
          ? _value.shares
          : shares // ignore: cast_nullable_to_non_nullable
              as int,
      ctr: null == ctr
          ? _value.ctr
          : ctr // ignore: cast_nullable_to_non_nullable
              as double,
      engagementRate: null == engagementRate
          ? _value.engagementRate
          : engagementRate // ignore: cast_nullable_to_non_nullable
              as double,
      shareRate: null == shareRate
          ? _value.shareRate
          : shareRate // ignore: cast_nullable_to_non_nullable
              as double,
      conversionRate: null == conversionRate
          ? _value.conversionRate
          : conversionRate // ignore: cast_nullable_to_non_nullable
              as double,
      engagementScore: null == engagementScore
          ? _value.engagementScore
          : engagementScore // ignore: cast_nullable_to_non_nullable
              as double,
      recordedAt: null == recordedAt
          ? _value.recordedAt
          : recordedAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$EngagementMetricImplCopyWith<$Res>
    implements $EngagementMetricCopyWith<$Res> {
  factory _$$EngagementMetricImplCopyWith(_$EngagementMetricImpl value,
          $Res Function(_$EngagementMetricImpl) then) =
      __$$EngagementMetricImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int contentId,
      int views,
      int clicks,
      int shares,
      double ctr,
      double engagementRate,
      double shareRate,
      double conversionRate,
      double engagementScore,
      DateTime recordedAt});
}

/// @nodoc
class __$$EngagementMetricImplCopyWithImpl<$Res>
    extends _$EngagementMetricCopyWithImpl<$Res, _$EngagementMetricImpl>
    implements _$$EngagementMetricImplCopyWith<$Res> {
  __$$EngagementMetricImplCopyWithImpl(_$EngagementMetricImpl _value,
      $Res Function(_$EngagementMetricImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? contentId = null,
    Object? views = null,
    Object? clicks = null,
    Object? shares = null,
    Object? ctr = null,
    Object? engagementRate = null,
    Object? shareRate = null,
    Object? conversionRate = null,
    Object? engagementScore = null,
    Object? recordedAt = null,
  }) {
    return _then(_$EngagementMetricImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      contentId: null == contentId
          ? _value.contentId
          : contentId // ignore: cast_nullable_to_non_nullable
              as int,
      views: null == views
          ? _value.views
          : views // ignore: cast_nullable_to_non_nullable
              as int,
      clicks: null == clicks
          ? _value.clicks
          : clicks // ignore: cast_nullable_to_non_nullable
              as int,
      shares: null == shares
          ? _value.shares
          : shares // ignore: cast_nullable_to_non_nullable
              as int,
      ctr: null == ctr
          ? _value.ctr
          : ctr // ignore: cast_nullable_to_non_nullable
              as double,
      engagementRate: null == engagementRate
          ? _value.engagementRate
          : engagementRate // ignore: cast_nullable_to_non_nullable
              as double,
      shareRate: null == shareRate
          ? _value.shareRate
          : shareRate // ignore: cast_nullable_to_non_nullable
              as double,
      conversionRate: null == conversionRate
          ? _value.conversionRate
          : conversionRate // ignore: cast_nullable_to_non_nullable
              as double,
      engagementScore: null == engagementScore
          ? _value.engagementScore
          : engagementScore // ignore: cast_nullable_to_non_nullable
              as double,
      recordedAt: null == recordedAt
          ? _value.recordedAt
          : recordedAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$EngagementMetricImpl implements _EngagementMetric {
  const _$EngagementMetricImpl(
      {required this.id,
      required this.contentId,
      required this.views,
      required this.clicks,
      required this.shares,
      required this.ctr,
      this.engagementRate = 0,
      this.shareRate = 0,
      this.conversionRate = 0,
      this.engagementScore = 0,
      required this.recordedAt});

  factory _$EngagementMetricImpl.fromJson(Map<String, dynamic> json) =>
      _$$EngagementMetricImplFromJson(json);

  @override
  final int id;
  @override
  final int contentId;
  @override
  final int views;
  @override
  final int clicks;
  @override
  final int shares;
  @override
  final double ctr;
  @override
  @JsonKey()
  final double engagementRate;
  @override
  @JsonKey()
  final double shareRate;
  @override
  @JsonKey()
  final double conversionRate;
  @override
  @JsonKey()
  final double engagementScore;
  @override
  final DateTime recordedAt;

  @override
  String toString() {
    return 'EngagementMetric(id: $id, contentId: $contentId, views: $views, clicks: $clicks, shares: $shares, ctr: $ctr, engagementRate: $engagementRate, shareRate: $shareRate, conversionRate: $conversionRate, engagementScore: $engagementScore, recordedAt: $recordedAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$EngagementMetricImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.contentId, contentId) ||
                other.contentId == contentId) &&
            (identical(other.views, views) || other.views == views) &&
            (identical(other.clicks, clicks) || other.clicks == clicks) &&
            (identical(other.shares, shares) || other.shares == shares) &&
            (identical(other.ctr, ctr) || other.ctr == ctr) &&
            (identical(other.engagementRate, engagementRate) ||
                other.engagementRate == engagementRate) &&
            (identical(other.shareRate, shareRate) ||
                other.shareRate == shareRate) &&
            (identical(other.conversionRate, conversionRate) ||
                other.conversionRate == conversionRate) &&
            (identical(other.engagementScore, engagementScore) ||
                other.engagementScore == engagementScore) &&
            (identical(other.recordedAt, recordedAt) ||
                other.recordedAt == recordedAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      contentId,
      views,
      clicks,
      shares,
      ctr,
      engagementRate,
      shareRate,
      conversionRate,
      engagementScore,
      recordedAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$EngagementMetricImplCopyWith<_$EngagementMetricImpl> get copyWith =>
      __$$EngagementMetricImplCopyWithImpl<_$EngagementMetricImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$EngagementMetricImplToJson(
      this,
    );
  }
}

abstract class _EngagementMetric implements EngagementMetric {
  const factory _EngagementMetric(
      {required final int id,
      required final int contentId,
      required final int views,
      required final int clicks,
      required final int shares,
      required final double ctr,
      final double engagementRate,
      final double shareRate,
      final double conversionRate,
      final double engagementScore,
      required final DateTime recordedAt}) = _$EngagementMetricImpl;

  factory _EngagementMetric.fromJson(Map<String, dynamic> json) =
      _$EngagementMetricImpl.fromJson;

  @override
  int get id;
  @override
  int get contentId;
  @override
  int get views;
  @override
  int get clicks;
  @override
  int get shares;
  @override
  double get ctr;
  @override
  double get engagementRate;
  @override
  double get shareRate;
  @override
  double get conversionRate;
  @override
  double get engagementScore;
  @override
  DateTime get recordedAt;
  @override
  @JsonKey(ignore: true)
  _$$EngagementMetricImplCopyWith<_$EngagementMetricImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

ABTestCampaign _$ABTestCampaignFromJson(Map<String, dynamic> json) {
  return _ABTestCampaign.fromJson(json);
}

/// @nodoc
mixin _$ABTestCampaign {
  int get id => throw _privateConstructorUsedError;
  String get name => throw _privateConstructorUsedError;
  String get testMetric => throw _privateConstructorUsedError;
  String get hypothesis => throw _privateConstructorUsedError;
  String get status => throw _privateConstructorUsedError;
  DateTime? get startDate => throw _privateConstructorUsedError;
  DateTime? get endDate => throw _privateConstructorUsedError;
  double get statisticalSignificance => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $ABTestCampaignCopyWith<ABTestCampaign> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $ABTestCampaignCopyWith<$Res> {
  factory $ABTestCampaignCopyWith(
          ABTestCampaign value, $Res Function(ABTestCampaign) then) =
      _$ABTestCampaignCopyWithImpl<$Res, ABTestCampaign>;
  @useResult
  $Res call(
      {int id,
      String name,
      String testMetric,
      String hypothesis,
      String status,
      DateTime? startDate,
      DateTime? endDate,
      double statisticalSignificance});
}

/// @nodoc
class _$ABTestCampaignCopyWithImpl<$Res, $Val extends ABTestCampaign>
    implements $ABTestCampaignCopyWith<$Res> {
  _$ABTestCampaignCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? testMetric = null,
    Object? hypothesis = null,
    Object? status = null,
    Object? startDate = freezed,
    Object? endDate = freezed,
    Object? statisticalSignificance = null,
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
      testMetric: null == testMetric
          ? _value.testMetric
          : testMetric // ignore: cast_nullable_to_non_nullable
              as String,
      hypothesis: null == hypothesis
          ? _value.hypothesis
          : hypothesis // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      startDate: freezed == startDate
          ? _value.startDate
          : startDate // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      endDate: freezed == endDate
          ? _value.endDate
          : endDate // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      statisticalSignificance: null == statisticalSignificance
          ? _value.statisticalSignificance
          : statisticalSignificance // ignore: cast_nullable_to_non_nullable
              as double,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$ABTestCampaignImplCopyWith<$Res>
    implements $ABTestCampaignCopyWith<$Res> {
  factory _$$ABTestCampaignImplCopyWith(_$ABTestCampaignImpl value,
          $Res Function(_$ABTestCampaignImpl) then) =
      __$$ABTestCampaignImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String name,
      String testMetric,
      String hypothesis,
      String status,
      DateTime? startDate,
      DateTime? endDate,
      double statisticalSignificance});
}

/// @nodoc
class __$$ABTestCampaignImplCopyWithImpl<$Res>
    extends _$ABTestCampaignCopyWithImpl<$Res, _$ABTestCampaignImpl>
    implements _$$ABTestCampaignImplCopyWith<$Res> {
  __$$ABTestCampaignImplCopyWithImpl(
      _$ABTestCampaignImpl _value, $Res Function(_$ABTestCampaignImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? testMetric = null,
    Object? hypothesis = null,
    Object? status = null,
    Object? startDate = freezed,
    Object? endDate = freezed,
    Object? statisticalSignificance = null,
  }) {
    return _then(_$ABTestCampaignImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      name: null == name
          ? _value.name
          : name // ignore: cast_nullable_to_non_nullable
              as String,
      testMetric: null == testMetric
          ? _value.testMetric
          : testMetric // ignore: cast_nullable_to_non_nullable
              as String,
      hypothesis: null == hypothesis
          ? _value.hypothesis
          : hypothesis // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      startDate: freezed == startDate
          ? _value.startDate
          : startDate // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      endDate: freezed == endDate
          ? _value.endDate
          : endDate // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      statisticalSignificance: null == statisticalSignificance
          ? _value.statisticalSignificance
          : statisticalSignificance // ignore: cast_nullable_to_non_nullable
              as double,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$ABTestCampaignImpl implements _ABTestCampaign {
  const _$ABTestCampaignImpl(
      {required this.id,
      required this.name,
      required this.testMetric,
      required this.hypothesis,
      required this.status,
      this.startDate,
      this.endDate,
      this.statisticalSignificance = 0});

  factory _$ABTestCampaignImpl.fromJson(Map<String, dynamic> json) =>
      _$$ABTestCampaignImplFromJson(json);

  @override
  final int id;
  @override
  final String name;
  @override
  final String testMetric;
  @override
  final String hypothesis;
  @override
  final String status;
  @override
  final DateTime? startDate;
  @override
  final DateTime? endDate;
  @override
  @JsonKey()
  final double statisticalSignificance;

  @override
  String toString() {
    return 'ABTestCampaign(id: $id, name: $name, testMetric: $testMetric, hypothesis: $hypothesis, status: $status, startDate: $startDate, endDate: $endDate, statisticalSignificance: $statisticalSignificance)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$ABTestCampaignImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.testMetric, testMetric) ||
                other.testMetric == testMetric) &&
            (identical(other.hypothesis, hypothesis) ||
                other.hypothesis == hypothesis) &&
            (identical(other.status, status) || other.status == status) &&
            (identical(other.startDate, startDate) ||
                other.startDate == startDate) &&
            (identical(other.endDate, endDate) || other.endDate == endDate) &&
            (identical(
                    other.statisticalSignificance, statisticalSignificance) ||
                other.statisticalSignificance == statisticalSignificance));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, id, name, testMetric, hypothesis,
      status, startDate, endDate, statisticalSignificance);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$ABTestCampaignImplCopyWith<_$ABTestCampaignImpl> get copyWith =>
      __$$ABTestCampaignImplCopyWithImpl<_$ABTestCampaignImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$ABTestCampaignImplToJson(
      this,
    );
  }
}

abstract class _ABTestCampaign implements ABTestCampaign {
  const factory _ABTestCampaign(
      {required final int id,
      required final String name,
      required final String testMetric,
      required final String hypothesis,
      required final String status,
      final DateTime? startDate,
      final DateTime? endDate,
      final double statisticalSignificance}) = _$ABTestCampaignImpl;

  factory _ABTestCampaign.fromJson(Map<String, dynamic> json) =
      _$ABTestCampaignImpl.fromJson;

  @override
  int get id;
  @override
  String get name;
  @override
  String get testMetric;
  @override
  String get hypothesis;
  @override
  String get status;
  @override
  DateTime? get startDate;
  @override
  DateTime? get endDate;
  @override
  double get statisticalSignificance;
  @override
  @JsonKey(ignore: true)
  _$$ABTestCampaignImplCopyWith<_$ABTestCampaignImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

ABTestVariant _$ABTestVariantFromJson(Map<String, dynamic> json) {
  return _ABTestVariant.fromJson(json);
}

/// @nodoc
mixin _$ABTestVariant {
  int get id => throw _privateConstructorUsedError;
  int get campaignId => throw _privateConstructorUsedError;
  String get variantName => throw _privateConstructorUsedError;
  int get conversions => throw _privateConstructorUsedError;
  int get impressions => throw _privateConstructorUsedError;
  double get conversionRate => throw _privateConstructorUsedError;
  double get ctr => throw _privateConstructorUsedError;
  bool? get isWinner => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $ABTestVariantCopyWith<ABTestVariant> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $ABTestVariantCopyWith<$Res> {
  factory $ABTestVariantCopyWith(
          ABTestVariant value, $Res Function(ABTestVariant) then) =
      _$ABTestVariantCopyWithImpl<$Res, ABTestVariant>;
  @useResult
  $Res call(
      {int id,
      int campaignId,
      String variantName,
      int conversions,
      int impressions,
      double conversionRate,
      double ctr,
      bool? isWinner});
}

/// @nodoc
class _$ABTestVariantCopyWithImpl<$Res, $Val extends ABTestVariant>
    implements $ABTestVariantCopyWith<$Res> {
  _$ABTestVariantCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? campaignId = null,
    Object? variantName = null,
    Object? conversions = null,
    Object? impressions = null,
    Object? conversionRate = null,
    Object? ctr = null,
    Object? isWinner = freezed,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      campaignId: null == campaignId
          ? _value.campaignId
          : campaignId // ignore: cast_nullable_to_non_nullable
              as int,
      variantName: null == variantName
          ? _value.variantName
          : variantName // ignore: cast_nullable_to_non_nullable
              as String,
      conversions: null == conversions
          ? _value.conversions
          : conversions // ignore: cast_nullable_to_non_nullable
              as int,
      impressions: null == impressions
          ? _value.impressions
          : impressions // ignore: cast_nullable_to_non_nullable
              as int,
      conversionRate: null == conversionRate
          ? _value.conversionRate
          : conversionRate // ignore: cast_nullable_to_non_nullable
              as double,
      ctr: null == ctr
          ? _value.ctr
          : ctr // ignore: cast_nullable_to_non_nullable
              as double,
      isWinner: freezed == isWinner
          ? _value.isWinner
          : isWinner // ignore: cast_nullable_to_non_nullable
              as bool?,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$ABTestVariantImplCopyWith<$Res>
    implements $ABTestVariantCopyWith<$Res> {
  factory _$$ABTestVariantImplCopyWith(
          _$ABTestVariantImpl value, $Res Function(_$ABTestVariantImpl) then) =
      __$$ABTestVariantImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int campaignId,
      String variantName,
      int conversions,
      int impressions,
      double conversionRate,
      double ctr,
      bool? isWinner});
}

/// @nodoc
class __$$ABTestVariantImplCopyWithImpl<$Res>
    extends _$ABTestVariantCopyWithImpl<$Res, _$ABTestVariantImpl>
    implements _$$ABTestVariantImplCopyWith<$Res> {
  __$$ABTestVariantImplCopyWithImpl(
      _$ABTestVariantImpl _value, $Res Function(_$ABTestVariantImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? campaignId = null,
    Object? variantName = null,
    Object? conversions = null,
    Object? impressions = null,
    Object? conversionRate = null,
    Object? ctr = null,
    Object? isWinner = freezed,
  }) {
    return _then(_$ABTestVariantImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      campaignId: null == campaignId
          ? _value.campaignId
          : campaignId // ignore: cast_nullable_to_non_nullable
              as int,
      variantName: null == variantName
          ? _value.variantName
          : variantName // ignore: cast_nullable_to_non_nullable
              as String,
      conversions: null == conversions
          ? _value.conversions
          : conversions // ignore: cast_nullable_to_non_nullable
              as int,
      impressions: null == impressions
          ? _value.impressions
          : impressions // ignore: cast_nullable_to_non_nullable
              as int,
      conversionRate: null == conversionRate
          ? _value.conversionRate
          : conversionRate // ignore: cast_nullable_to_non_nullable
              as double,
      ctr: null == ctr
          ? _value.ctr
          : ctr // ignore: cast_nullable_to_non_nullable
              as double,
      isWinner: freezed == isWinner
          ? _value.isWinner
          : isWinner // ignore: cast_nullable_to_non_nullable
              as bool?,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$ABTestVariantImpl implements _ABTestVariant {
  const _$ABTestVariantImpl(
      {required this.id,
      required this.campaignId,
      required this.variantName,
      this.conversions = 0,
      this.impressions = 0,
      this.conversionRate = 0,
      this.ctr = 0,
      this.isWinner});

  factory _$ABTestVariantImpl.fromJson(Map<String, dynamic> json) =>
      _$$ABTestVariantImplFromJson(json);

  @override
  final int id;
  @override
  final int campaignId;
  @override
  final String variantName;
  @override
  @JsonKey()
  final int conversions;
  @override
  @JsonKey()
  final int impressions;
  @override
  @JsonKey()
  final double conversionRate;
  @override
  @JsonKey()
  final double ctr;
  @override
  final bool? isWinner;

  @override
  String toString() {
    return 'ABTestVariant(id: $id, campaignId: $campaignId, variantName: $variantName, conversions: $conversions, impressions: $impressions, conversionRate: $conversionRate, ctr: $ctr, isWinner: $isWinner)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$ABTestVariantImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.campaignId, campaignId) ||
                other.campaignId == campaignId) &&
            (identical(other.variantName, variantName) ||
                other.variantName == variantName) &&
            (identical(other.conversions, conversions) ||
                other.conversions == conversions) &&
            (identical(other.impressions, impressions) ||
                other.impressions == impressions) &&
            (identical(other.conversionRate, conversionRate) ||
                other.conversionRate == conversionRate) &&
            (identical(other.ctr, ctr) || other.ctr == ctr) &&
            (identical(other.isWinner, isWinner) ||
                other.isWinner == isWinner));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, id, campaignId, variantName,
      conversions, impressions, conversionRate, ctr, isWinner);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$ABTestVariantImplCopyWith<_$ABTestVariantImpl> get copyWith =>
      __$$ABTestVariantImplCopyWithImpl<_$ABTestVariantImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$ABTestVariantImplToJson(
      this,
    );
  }
}

abstract class _ABTestVariant implements ABTestVariant {
  const factory _ABTestVariant(
      {required final int id,
      required final int campaignId,
      required final String variantName,
      final int conversions,
      final int impressions,
      final double conversionRate,
      final double ctr,
      final bool? isWinner}) = _$ABTestVariantImpl;

  factory _ABTestVariant.fromJson(Map<String, dynamic> json) =
      _$ABTestVariantImpl.fromJson;

  @override
  int get id;
  @override
  int get campaignId;
  @override
  String get variantName;
  @override
  int get conversions;
  @override
  int get impressions;
  @override
  double get conversionRate;
  @override
  double get ctr;
  @override
  bool? get isWinner;
  @override
  @JsonKey(ignore: true)
  _$$ABTestVariantImplCopyWith<_$ABTestVariantImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

RecommendedContent _$RecommendedContentFromJson(Map<String, dynamic> json) {
  return _RecommendedContent.fromJson(json);
}

/// @nodoc
mixin _$RecommendedContent {
  int get contentId => throw _privateConstructorUsedError;
  String get title => throw _privateConstructorUsedError;
  double get matchScore => throw _privateConstructorUsedError;
  String get contentType => throw _privateConstructorUsedError;
  List<String>? get tags => throw _privateConstructorUsedError;
  DateTime? get publishedAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $RecommendedContentCopyWith<RecommendedContent> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $RecommendedContentCopyWith<$Res> {
  factory $RecommendedContentCopyWith(
          RecommendedContent value, $Res Function(RecommendedContent) then) =
      _$RecommendedContentCopyWithImpl<$Res, RecommendedContent>;
  @useResult
  $Res call(
      {int contentId,
      String title,
      double matchScore,
      String contentType,
      List<String>? tags,
      DateTime? publishedAt});
}

/// @nodoc
class _$RecommendedContentCopyWithImpl<$Res, $Val extends RecommendedContent>
    implements $RecommendedContentCopyWith<$Res> {
  _$RecommendedContentCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? contentId = null,
    Object? title = null,
    Object? matchScore = null,
    Object? contentType = null,
    Object? tags = freezed,
    Object? publishedAt = freezed,
  }) {
    return _then(_value.copyWith(
      contentId: null == contentId
          ? _value.contentId
          : contentId // ignore: cast_nullable_to_non_nullable
              as int,
      title: null == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String,
      matchScore: null == matchScore
          ? _value.matchScore
          : matchScore // ignore: cast_nullable_to_non_nullable
              as double,
      contentType: null == contentType
          ? _value.contentType
          : contentType // ignore: cast_nullable_to_non_nullable
              as String,
      tags: freezed == tags
          ? _value.tags
          : tags // ignore: cast_nullable_to_non_nullable
              as List<String>?,
      publishedAt: freezed == publishedAt
          ? _value.publishedAt
          : publishedAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$RecommendedContentImplCopyWith<$Res>
    implements $RecommendedContentCopyWith<$Res> {
  factory _$$RecommendedContentImplCopyWith(_$RecommendedContentImpl value,
          $Res Function(_$RecommendedContentImpl) then) =
      __$$RecommendedContentImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int contentId,
      String title,
      double matchScore,
      String contentType,
      List<String>? tags,
      DateTime? publishedAt});
}

/// @nodoc
class __$$RecommendedContentImplCopyWithImpl<$Res>
    extends _$RecommendedContentCopyWithImpl<$Res, _$RecommendedContentImpl>
    implements _$$RecommendedContentImplCopyWith<$Res> {
  __$$RecommendedContentImplCopyWithImpl(_$RecommendedContentImpl _value,
      $Res Function(_$RecommendedContentImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? contentId = null,
    Object? title = null,
    Object? matchScore = null,
    Object? contentType = null,
    Object? tags = freezed,
    Object? publishedAt = freezed,
  }) {
    return _then(_$RecommendedContentImpl(
      contentId: null == contentId
          ? _value.contentId
          : contentId // ignore: cast_nullable_to_non_nullable
              as int,
      title: null == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String,
      matchScore: null == matchScore
          ? _value.matchScore
          : matchScore // ignore: cast_nullable_to_non_nullable
              as double,
      contentType: null == contentType
          ? _value.contentType
          : contentType // ignore: cast_nullable_to_non_nullable
              as String,
      tags: freezed == tags
          ? _value._tags
          : tags // ignore: cast_nullable_to_non_nullable
              as List<String>?,
      publishedAt: freezed == publishedAt
          ? _value.publishedAt
          : publishedAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$RecommendedContentImpl implements _RecommendedContent {
  const _$RecommendedContentImpl(
      {required this.contentId,
      required this.title,
      required this.matchScore,
      this.contentType = 'content',
      final List<String>? tags,
      this.publishedAt})
      : _tags = tags;

  factory _$RecommendedContentImpl.fromJson(Map<String, dynamic> json) =>
      _$$RecommendedContentImplFromJson(json);

  @override
  final int contentId;
  @override
  final String title;
  @override
  final double matchScore;
  @override
  @JsonKey()
  final String contentType;
  final List<String>? _tags;
  @override
  List<String>? get tags {
    final value = _tags;
    if (value == null) return null;
    if (_tags is EqualUnmodifiableListView) return _tags;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(value);
  }

  @override
  final DateTime? publishedAt;

  @override
  String toString() {
    return 'RecommendedContent(contentId: $contentId, title: $title, matchScore: $matchScore, contentType: $contentType, tags: $tags, publishedAt: $publishedAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$RecommendedContentImpl &&
            (identical(other.contentId, contentId) ||
                other.contentId == contentId) &&
            (identical(other.title, title) || other.title == title) &&
            (identical(other.matchScore, matchScore) ||
                other.matchScore == matchScore) &&
            (identical(other.contentType, contentType) ||
                other.contentType == contentType) &&
            const DeepCollectionEquality().equals(other._tags, _tags) &&
            (identical(other.publishedAt, publishedAt) ||
                other.publishedAt == publishedAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, contentId, title, matchScore,
      contentType, const DeepCollectionEquality().hash(_tags), publishedAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$RecommendedContentImplCopyWith<_$RecommendedContentImpl> get copyWith =>
      __$$RecommendedContentImplCopyWithImpl<_$RecommendedContentImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$RecommendedContentImplToJson(
      this,
    );
  }
}

abstract class _RecommendedContent implements RecommendedContent {
  const factory _RecommendedContent(
      {required final int contentId,
      required final String title,
      required final double matchScore,
      final String contentType,
      final List<String>? tags,
      final DateTime? publishedAt}) = _$RecommendedContentImpl;

  factory _RecommendedContent.fromJson(Map<String, dynamic> json) =
      _$RecommendedContentImpl.fromJson;

  @override
  int get contentId;
  @override
  String get title;
  @override
  double get matchScore;
  @override
  String get contentType;
  @override
  List<String>? get tags;
  @override
  DateTime? get publishedAt;
  @override
  @JsonKey(ignore: true)
  _$$RecommendedContentImplCopyWith<_$RecommendedContentImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

UserPreference _$UserPreferenceFromJson(Map<String, dynamic> json) {
  return _UserPreference.fromJson(json);
}

/// @nodoc
mixin _$UserPreference {
  int get id => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  String get category => throw _privateConstructorUsedError;
  double get preferenceScore => throw _privateConstructorUsedError;
  int get interactionCount => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $UserPreferenceCopyWith<UserPreference> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $UserPreferenceCopyWith<$Res> {
  factory $UserPreferenceCopyWith(
          UserPreference value, $Res Function(UserPreference) then) =
      _$UserPreferenceCopyWithImpl<$Res, UserPreference>;
  @useResult
  $Res call(
      {int id,
      int userId,
      String category,
      double preferenceScore,
      int interactionCount});
}

/// @nodoc
class _$UserPreferenceCopyWithImpl<$Res, $Val extends UserPreference>
    implements $UserPreferenceCopyWith<$Res> {
  _$UserPreferenceCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? category = null,
    Object? preferenceScore = null,
    Object? interactionCount = null,
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
      category: null == category
          ? _value.category
          : category // ignore: cast_nullable_to_non_nullable
              as String,
      preferenceScore: null == preferenceScore
          ? _value.preferenceScore
          : preferenceScore // ignore: cast_nullable_to_non_nullable
              as double,
      interactionCount: null == interactionCount
          ? _value.interactionCount
          : interactionCount // ignore: cast_nullable_to_non_nullable
              as int,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$UserPreferenceImplCopyWith<$Res>
    implements $UserPreferenceCopyWith<$Res> {
  factory _$$UserPreferenceImplCopyWith(_$UserPreferenceImpl value,
          $Res Function(_$UserPreferenceImpl) then) =
      __$$UserPreferenceImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int userId,
      String category,
      double preferenceScore,
      int interactionCount});
}

/// @nodoc
class __$$UserPreferenceImplCopyWithImpl<$Res>
    extends _$UserPreferenceCopyWithImpl<$Res, _$UserPreferenceImpl>
    implements _$$UserPreferenceImplCopyWith<$Res> {
  __$$UserPreferenceImplCopyWithImpl(
      _$UserPreferenceImpl _value, $Res Function(_$UserPreferenceImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? category = null,
    Object? preferenceScore = null,
    Object? interactionCount = null,
  }) {
    return _then(_$UserPreferenceImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      category: null == category
          ? _value.category
          : category // ignore: cast_nullable_to_non_nullable
              as String,
      preferenceScore: null == preferenceScore
          ? _value.preferenceScore
          : preferenceScore // ignore: cast_nullable_to_non_nullable
              as double,
      interactionCount: null == interactionCount
          ? _value.interactionCount
          : interactionCount // ignore: cast_nullable_to_non_nullable
              as int,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$UserPreferenceImpl implements _UserPreference {
  const _$UserPreferenceImpl(
      {required this.id,
      required this.userId,
      required this.category,
      required this.preferenceScore,
      this.interactionCount = 0});

  factory _$UserPreferenceImpl.fromJson(Map<String, dynamic> json) =>
      _$$UserPreferenceImplFromJson(json);

  @override
  final int id;
  @override
  final int userId;
  @override
  final String category;
  @override
  final double preferenceScore;
  @override
  @JsonKey()
  final int interactionCount;

  @override
  String toString() {
    return 'UserPreference(id: $id, userId: $userId, category: $category, preferenceScore: $preferenceScore, interactionCount: $interactionCount)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$UserPreferenceImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.category, category) ||
                other.category == category) &&
            (identical(other.preferenceScore, preferenceScore) ||
                other.preferenceScore == preferenceScore) &&
            (identical(other.interactionCount, interactionCount) ||
                other.interactionCount == interactionCount));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType, id, userId, category, preferenceScore, interactionCount);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$UserPreferenceImplCopyWith<_$UserPreferenceImpl> get copyWith =>
      __$$UserPreferenceImplCopyWithImpl<_$UserPreferenceImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$UserPreferenceImplToJson(
      this,
    );
  }
}

abstract class _UserPreference implements UserPreference {
  const factory _UserPreference(
      {required final int id,
      required final int userId,
      required final String category,
      required final double preferenceScore,
      final int interactionCount}) = _$UserPreferenceImpl;

  factory _UserPreference.fromJson(Map<String, dynamic> json) =
      _$UserPreferenceImpl.fromJson;

  @override
  int get id;
  @override
  int get userId;
  @override
  String get category;
  @override
  double get preferenceScore;
  @override
  int get interactionCount;
  @override
  @JsonKey(ignore: true)
  _$$UserPreferenceImplCopyWith<_$UserPreferenceImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

DistributionChannel _$DistributionChannelFromJson(Map<String, dynamic> json) {
  return _DistributionChannel.fromJson(json);
}

/// @nodoc
mixin _$DistributionChannel {
  int get id => throw _privateConstructorUsedError;
  String get channelName => throw _privateConstructorUsedError;
  String get status => throw _privateConstructorUsedError;
  int get reach => throw _privateConstructorUsedError;
  double get engagementRate => throw _privateConstructorUsedError;
  int get impressions => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $DistributionChannelCopyWith<DistributionChannel> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $DistributionChannelCopyWith<$Res> {
  factory $DistributionChannelCopyWith(
          DistributionChannel value, $Res Function(DistributionChannel) then) =
      _$DistributionChannelCopyWithImpl<$Res, DistributionChannel>;
  @useResult
  $Res call(
      {int id,
      String channelName,
      String status,
      int reach,
      double engagementRate,
      int impressions});
}

/// @nodoc
class _$DistributionChannelCopyWithImpl<$Res, $Val extends DistributionChannel>
    implements $DistributionChannelCopyWith<$Res> {
  _$DistributionChannelCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? channelName = null,
    Object? status = null,
    Object? reach = null,
    Object? engagementRate = null,
    Object? impressions = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      channelName: null == channelName
          ? _value.channelName
          : channelName // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      reach: null == reach
          ? _value.reach
          : reach // ignore: cast_nullable_to_non_nullable
              as int,
      engagementRate: null == engagementRate
          ? _value.engagementRate
          : engagementRate // ignore: cast_nullable_to_non_nullable
              as double,
      impressions: null == impressions
          ? _value.impressions
          : impressions // ignore: cast_nullable_to_non_nullable
              as int,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$DistributionChannelImplCopyWith<$Res>
    implements $DistributionChannelCopyWith<$Res> {
  factory _$$DistributionChannelImplCopyWith(_$DistributionChannelImpl value,
          $Res Function(_$DistributionChannelImpl) then) =
      __$$DistributionChannelImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String channelName,
      String status,
      int reach,
      double engagementRate,
      int impressions});
}

/// @nodoc
class __$$DistributionChannelImplCopyWithImpl<$Res>
    extends _$DistributionChannelCopyWithImpl<$Res, _$DistributionChannelImpl>
    implements _$$DistributionChannelImplCopyWith<$Res> {
  __$$DistributionChannelImplCopyWithImpl(_$DistributionChannelImpl _value,
      $Res Function(_$DistributionChannelImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? channelName = null,
    Object? status = null,
    Object? reach = null,
    Object? engagementRate = null,
    Object? impressions = null,
  }) {
    return _then(_$DistributionChannelImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      channelName: null == channelName
          ? _value.channelName
          : channelName // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      reach: null == reach
          ? _value.reach
          : reach // ignore: cast_nullable_to_non_nullable
              as int,
      engagementRate: null == engagementRate
          ? _value.engagementRate
          : engagementRate // ignore: cast_nullable_to_non_nullable
              as double,
      impressions: null == impressions
          ? _value.impressions
          : impressions // ignore: cast_nullable_to_non_nullable
              as int,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$DistributionChannelImpl implements _DistributionChannel {
  const _$DistributionChannelImpl(
      {required this.id,
      required this.channelName,
      required this.status,
      this.reach = 0,
      this.engagementRate = 0,
      this.impressions = 0});

  factory _$DistributionChannelImpl.fromJson(Map<String, dynamic> json) =>
      _$$DistributionChannelImplFromJson(json);

  @override
  final int id;
  @override
  final String channelName;
  @override
  final String status;
  @override
  @JsonKey()
  final int reach;
  @override
  @JsonKey()
  final double engagementRate;
  @override
  @JsonKey()
  final int impressions;

  @override
  String toString() {
    return 'DistributionChannel(id: $id, channelName: $channelName, status: $status, reach: $reach, engagementRate: $engagementRate, impressions: $impressions)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$DistributionChannelImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.channelName, channelName) ||
                other.channelName == channelName) &&
            (identical(other.status, status) || other.status == status) &&
            (identical(other.reach, reach) || other.reach == reach) &&
            (identical(other.engagementRate, engagementRate) ||
                other.engagementRate == engagementRate) &&
            (identical(other.impressions, impressions) ||
                other.impressions == impressions));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType, id, channelName, status, reach, engagementRate, impressions);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$DistributionChannelImplCopyWith<_$DistributionChannelImpl> get copyWith =>
      __$$DistributionChannelImplCopyWithImpl<_$DistributionChannelImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$DistributionChannelImplToJson(
      this,
    );
  }
}

abstract class _DistributionChannel implements DistributionChannel {
  const factory _DistributionChannel(
      {required final int id,
      required final String channelName,
      required final String status,
      final int reach,
      final double engagementRate,
      final int impressions}) = _$DistributionChannelImpl;

  factory _DistributionChannel.fromJson(Map<String, dynamic> json) =
      _$DistributionChannelImpl.fromJson;

  @override
  int get id;
  @override
  String get channelName;
  @override
  String get status;
  @override
  int get reach;
  @override
  double get engagementRate;
  @override
  int get impressions;
  @override
  @JsonKey(ignore: true)
  _$$DistributionChannelImplCopyWith<_$DistributionChannelImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

SyndicationPartner _$SyndicationPartnerFromJson(Map<String, dynamic> json) {
  return _SyndicationPartner.fromJson(json);
}

/// @nodoc
mixin _$SyndicationPartner {
  int get id => throw _privateConstructorUsedError;
  String get partnerName => throw _privateConstructorUsedError;
  int get articlesSyndicated => throw _privateConstructorUsedError;
  int get totalReach => throw _privateConstructorUsedError;
  DateTime? get lastSyndicationDate => throw _privateConstructorUsedError;
  String get status => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $SyndicationPartnerCopyWith<SyndicationPartner> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $SyndicationPartnerCopyWith<$Res> {
  factory $SyndicationPartnerCopyWith(
          SyndicationPartner value, $Res Function(SyndicationPartner) then) =
      _$SyndicationPartnerCopyWithImpl<$Res, SyndicationPartner>;
  @useResult
  $Res call(
      {int id,
      String partnerName,
      int articlesSyndicated,
      int totalReach,
      DateTime? lastSyndicationDate,
      String status});
}

/// @nodoc
class _$SyndicationPartnerCopyWithImpl<$Res, $Val extends SyndicationPartner>
    implements $SyndicationPartnerCopyWith<$Res> {
  _$SyndicationPartnerCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? partnerName = null,
    Object? articlesSyndicated = null,
    Object? totalReach = null,
    Object? lastSyndicationDate = freezed,
    Object? status = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      partnerName: null == partnerName
          ? _value.partnerName
          : partnerName // ignore: cast_nullable_to_non_nullable
              as String,
      articlesSyndicated: null == articlesSyndicated
          ? _value.articlesSyndicated
          : articlesSyndicated // ignore: cast_nullable_to_non_nullable
              as int,
      totalReach: null == totalReach
          ? _value.totalReach
          : totalReach // ignore: cast_nullable_to_non_nullable
              as int,
      lastSyndicationDate: freezed == lastSyndicationDate
          ? _value.lastSyndicationDate
          : lastSyndicationDate // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$SyndicationPartnerImplCopyWith<$Res>
    implements $SyndicationPartnerCopyWith<$Res> {
  factory _$$SyndicationPartnerImplCopyWith(_$SyndicationPartnerImpl value,
          $Res Function(_$SyndicationPartnerImpl) then) =
      __$$SyndicationPartnerImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String partnerName,
      int articlesSyndicated,
      int totalReach,
      DateTime? lastSyndicationDate,
      String status});
}

/// @nodoc
class __$$SyndicationPartnerImplCopyWithImpl<$Res>
    extends _$SyndicationPartnerCopyWithImpl<$Res, _$SyndicationPartnerImpl>
    implements _$$SyndicationPartnerImplCopyWith<$Res> {
  __$$SyndicationPartnerImplCopyWithImpl(_$SyndicationPartnerImpl _value,
      $Res Function(_$SyndicationPartnerImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? partnerName = null,
    Object? articlesSyndicated = null,
    Object? totalReach = null,
    Object? lastSyndicationDate = freezed,
    Object? status = null,
  }) {
    return _then(_$SyndicationPartnerImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      partnerName: null == partnerName
          ? _value.partnerName
          : partnerName // ignore: cast_nullable_to_non_nullable
              as String,
      articlesSyndicated: null == articlesSyndicated
          ? _value.articlesSyndicated
          : articlesSyndicated // ignore: cast_nullable_to_non_nullable
              as int,
      totalReach: null == totalReach
          ? _value.totalReach
          : totalReach // ignore: cast_nullable_to_non_nullable
              as int,
      lastSyndicationDate: freezed == lastSyndicationDate
          ? _value.lastSyndicationDate
          : lastSyndicationDate // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$SyndicationPartnerImpl implements _SyndicationPartner {
  const _$SyndicationPartnerImpl(
      {required this.id,
      required this.partnerName,
      this.articlesSyndicated = 0,
      this.totalReach = 0,
      this.lastSyndicationDate,
      this.status = 'active'});

  factory _$SyndicationPartnerImpl.fromJson(Map<String, dynamic> json) =>
      _$$SyndicationPartnerImplFromJson(json);

  @override
  final int id;
  @override
  final String partnerName;
  @override
  @JsonKey()
  final int articlesSyndicated;
  @override
  @JsonKey()
  final int totalReach;
  @override
  final DateTime? lastSyndicationDate;
  @override
  @JsonKey()
  final String status;

  @override
  String toString() {
    return 'SyndicationPartner(id: $id, partnerName: $partnerName, articlesSyndicated: $articlesSyndicated, totalReach: $totalReach, lastSyndicationDate: $lastSyndicationDate, status: $status)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$SyndicationPartnerImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.partnerName, partnerName) ||
                other.partnerName == partnerName) &&
            (identical(other.articlesSyndicated, articlesSyndicated) ||
                other.articlesSyndicated == articlesSyndicated) &&
            (identical(other.totalReach, totalReach) ||
                other.totalReach == totalReach) &&
            (identical(other.lastSyndicationDate, lastSyndicationDate) ||
                other.lastSyndicationDate == lastSyndicationDate) &&
            (identical(other.status, status) || other.status == status));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, id, partnerName,
      articlesSyndicated, totalReach, lastSyndicationDate, status);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$SyndicationPartnerImplCopyWith<_$SyndicationPartnerImpl> get copyWith =>
      __$$SyndicationPartnerImplCopyWithImpl<_$SyndicationPartnerImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$SyndicationPartnerImplToJson(
      this,
    );
  }
}

abstract class _SyndicationPartner implements SyndicationPartner {
  const factory _SyndicationPartner(
      {required final int id,
      required final String partnerName,
      final int articlesSyndicated,
      final int totalReach,
      final DateTime? lastSyndicationDate,
      final String status}) = _$SyndicationPartnerImpl;

  factory _SyndicationPartner.fromJson(Map<String, dynamic> json) =
      _$SyndicationPartnerImpl.fromJson;

  @override
  int get id;
  @override
  String get partnerName;
  @override
  int get articlesSyndicated;
  @override
  int get totalReach;
  @override
  DateTime? get lastSyndicationDate;
  @override
  String get status;
  @override
  @JsonKey(ignore: true)
  _$$SyndicationPartnerImplCopyWith<_$SyndicationPartnerImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

AnalyticsSnapshot _$AnalyticsSnapshotFromJson(Map<String, dynamic> json) {
  return _AnalyticsSnapshot.fromJson(json);
}

/// @nodoc
mixin _$AnalyticsSnapshot {
  int get contentId => throw _privateConstructorUsedError;
  int get views => throw _privateConstructorUsedError;
  int get clicks => throw _privateConstructorUsedError;
  int get shares => throw _privateConstructorUsedError;
  double get engagementScore => throw _privateConstructorUsedError;
  double get trend => throw _privateConstructorUsedError;
  DateTime get timestamp => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $AnalyticsSnapshotCopyWith<AnalyticsSnapshot> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $AnalyticsSnapshotCopyWith<$Res> {
  factory $AnalyticsSnapshotCopyWith(
          AnalyticsSnapshot value, $Res Function(AnalyticsSnapshot) then) =
      _$AnalyticsSnapshotCopyWithImpl<$Res, AnalyticsSnapshot>;
  @useResult
  $Res call(
      {int contentId,
      int views,
      int clicks,
      int shares,
      double engagementScore,
      double trend,
      DateTime timestamp});
}

/// @nodoc
class _$AnalyticsSnapshotCopyWithImpl<$Res, $Val extends AnalyticsSnapshot>
    implements $AnalyticsSnapshotCopyWith<$Res> {
  _$AnalyticsSnapshotCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? contentId = null,
    Object? views = null,
    Object? clicks = null,
    Object? shares = null,
    Object? engagementScore = null,
    Object? trend = null,
    Object? timestamp = null,
  }) {
    return _then(_value.copyWith(
      contentId: null == contentId
          ? _value.contentId
          : contentId // ignore: cast_nullable_to_non_nullable
              as int,
      views: null == views
          ? _value.views
          : views // ignore: cast_nullable_to_non_nullable
              as int,
      clicks: null == clicks
          ? _value.clicks
          : clicks // ignore: cast_nullable_to_non_nullable
              as int,
      shares: null == shares
          ? _value.shares
          : shares // ignore: cast_nullable_to_non_nullable
              as int,
      engagementScore: null == engagementScore
          ? _value.engagementScore
          : engagementScore // ignore: cast_nullable_to_non_nullable
              as double,
      trend: null == trend
          ? _value.trend
          : trend // ignore: cast_nullable_to_non_nullable
              as double,
      timestamp: null == timestamp
          ? _value.timestamp
          : timestamp // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$AnalyticsSnapshotImplCopyWith<$Res>
    implements $AnalyticsSnapshotCopyWith<$Res> {
  factory _$$AnalyticsSnapshotImplCopyWith(_$AnalyticsSnapshotImpl value,
          $Res Function(_$AnalyticsSnapshotImpl) then) =
      __$$AnalyticsSnapshotImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int contentId,
      int views,
      int clicks,
      int shares,
      double engagementScore,
      double trend,
      DateTime timestamp});
}

/// @nodoc
class __$$AnalyticsSnapshotImplCopyWithImpl<$Res>
    extends _$AnalyticsSnapshotCopyWithImpl<$Res, _$AnalyticsSnapshotImpl>
    implements _$$AnalyticsSnapshotImplCopyWith<$Res> {
  __$$AnalyticsSnapshotImplCopyWithImpl(_$AnalyticsSnapshotImpl _value,
      $Res Function(_$AnalyticsSnapshotImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? contentId = null,
    Object? views = null,
    Object? clicks = null,
    Object? shares = null,
    Object? engagementScore = null,
    Object? trend = null,
    Object? timestamp = null,
  }) {
    return _then(_$AnalyticsSnapshotImpl(
      contentId: null == contentId
          ? _value.contentId
          : contentId // ignore: cast_nullable_to_non_nullable
              as int,
      views: null == views
          ? _value.views
          : views // ignore: cast_nullable_to_non_nullable
              as int,
      clicks: null == clicks
          ? _value.clicks
          : clicks // ignore: cast_nullable_to_non_nullable
              as int,
      shares: null == shares
          ? _value.shares
          : shares // ignore: cast_nullable_to_non_nullable
              as int,
      engagementScore: null == engagementScore
          ? _value.engagementScore
          : engagementScore // ignore: cast_nullable_to_non_nullable
              as double,
      trend: null == trend
          ? _value.trend
          : trend // ignore: cast_nullable_to_non_nullable
              as double,
      timestamp: null == timestamp
          ? _value.timestamp
          : timestamp // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$AnalyticsSnapshotImpl implements _AnalyticsSnapshot {
  const _$AnalyticsSnapshotImpl(
      {required this.contentId,
      required this.views,
      required this.clicks,
      required this.shares,
      required this.engagementScore,
      this.trend = 0,
      required this.timestamp});

  factory _$AnalyticsSnapshotImpl.fromJson(Map<String, dynamic> json) =>
      _$$AnalyticsSnapshotImplFromJson(json);

  @override
  final int contentId;
  @override
  final int views;
  @override
  final int clicks;
  @override
  final int shares;
  @override
  final double engagementScore;
  @override
  @JsonKey()
  final double trend;
  @override
  final DateTime timestamp;

  @override
  String toString() {
    return 'AnalyticsSnapshot(contentId: $contentId, views: $views, clicks: $clicks, shares: $shares, engagementScore: $engagementScore, trend: $trend, timestamp: $timestamp)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$AnalyticsSnapshotImpl &&
            (identical(other.contentId, contentId) ||
                other.contentId == contentId) &&
            (identical(other.views, views) || other.views == views) &&
            (identical(other.clicks, clicks) || other.clicks == clicks) &&
            (identical(other.shares, shares) || other.shares == shares) &&
            (identical(other.engagementScore, engagementScore) ||
                other.engagementScore == engagementScore) &&
            (identical(other.trend, trend) || other.trend == trend) &&
            (identical(other.timestamp, timestamp) ||
                other.timestamp == timestamp));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, contentId, views, clicks, shares,
      engagementScore, trend, timestamp);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$AnalyticsSnapshotImplCopyWith<_$AnalyticsSnapshotImpl> get copyWith =>
      __$$AnalyticsSnapshotImplCopyWithImpl<_$AnalyticsSnapshotImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$AnalyticsSnapshotImplToJson(
      this,
    );
  }
}

abstract class _AnalyticsSnapshot implements AnalyticsSnapshot {
  const factory _AnalyticsSnapshot(
      {required final int contentId,
      required final int views,
      required final int clicks,
      required final int shares,
      required final double engagementScore,
      final double trend,
      required final DateTime timestamp}) = _$AnalyticsSnapshotImpl;

  factory _AnalyticsSnapshot.fromJson(Map<String, dynamic> json) =
      _$AnalyticsSnapshotImpl.fromJson;

  @override
  int get contentId;
  @override
  int get views;
  @override
  int get clicks;
  @override
  int get shares;
  @override
  double get engagementScore;
  @override
  double get trend;
  @override
  DateTime get timestamp;
  @override
  @JsonKey(ignore: true)
  _$$AnalyticsSnapshotImplCopyWith<_$AnalyticsSnapshotImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

RecommendationPerformance _$RecommendationPerformanceFromJson(
    Map<String, dynamic> json) {
  return _RecommendationPerformance.fromJson(json);
}

/// @nodoc
mixin _$RecommendationPerformance {
  int get totalRecommendations => throw _privateConstructorUsedError;
  int get clicks => throw _privateConstructorUsedError;
  int get conversions => throw _privateConstructorUsedError;
  double get clickThroughRate => throw _privateConstructorUsedError;
  double get conversionRate => throw _privateConstructorUsedError;
  double get avgReadTime => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $RecommendationPerformanceCopyWith<RecommendationPerformance> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $RecommendationPerformanceCopyWith<$Res> {
  factory $RecommendationPerformanceCopyWith(RecommendationPerformance value,
          $Res Function(RecommendationPerformance) then) =
      _$RecommendationPerformanceCopyWithImpl<$Res, RecommendationPerformance>;
  @useResult
  $Res call(
      {int totalRecommendations,
      int clicks,
      int conversions,
      double clickThroughRate,
      double conversionRate,
      double avgReadTime});
}

/// @nodoc
class _$RecommendationPerformanceCopyWithImpl<$Res,
        $Val extends RecommendationPerformance>
    implements $RecommendationPerformanceCopyWith<$Res> {
  _$RecommendationPerformanceCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? totalRecommendations = null,
    Object? clicks = null,
    Object? conversions = null,
    Object? clickThroughRate = null,
    Object? conversionRate = null,
    Object? avgReadTime = null,
  }) {
    return _then(_value.copyWith(
      totalRecommendations: null == totalRecommendations
          ? _value.totalRecommendations
          : totalRecommendations // ignore: cast_nullable_to_non_nullable
              as int,
      clicks: null == clicks
          ? _value.clicks
          : clicks // ignore: cast_nullable_to_non_nullable
              as int,
      conversions: null == conversions
          ? _value.conversions
          : conversions // ignore: cast_nullable_to_non_nullable
              as int,
      clickThroughRate: null == clickThroughRate
          ? _value.clickThroughRate
          : clickThroughRate // ignore: cast_nullable_to_non_nullable
              as double,
      conversionRate: null == conversionRate
          ? _value.conversionRate
          : conversionRate // ignore: cast_nullable_to_non_nullable
              as double,
      avgReadTime: null == avgReadTime
          ? _value.avgReadTime
          : avgReadTime // ignore: cast_nullable_to_non_nullable
              as double,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$RecommendationPerformanceImplCopyWith<$Res>
    implements $RecommendationPerformanceCopyWith<$Res> {
  factory _$$RecommendationPerformanceImplCopyWith(
          _$RecommendationPerformanceImpl value,
          $Res Function(_$RecommendationPerformanceImpl) then) =
      __$$RecommendationPerformanceImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int totalRecommendations,
      int clicks,
      int conversions,
      double clickThroughRate,
      double conversionRate,
      double avgReadTime});
}

/// @nodoc
class __$$RecommendationPerformanceImplCopyWithImpl<$Res>
    extends _$RecommendationPerformanceCopyWithImpl<$Res,
        _$RecommendationPerformanceImpl>
    implements _$$RecommendationPerformanceImplCopyWith<$Res> {
  __$$RecommendationPerformanceImplCopyWithImpl(
      _$RecommendationPerformanceImpl _value,
      $Res Function(_$RecommendationPerformanceImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? totalRecommendations = null,
    Object? clicks = null,
    Object? conversions = null,
    Object? clickThroughRate = null,
    Object? conversionRate = null,
    Object? avgReadTime = null,
  }) {
    return _then(_$RecommendationPerformanceImpl(
      totalRecommendations: null == totalRecommendations
          ? _value.totalRecommendations
          : totalRecommendations // ignore: cast_nullable_to_non_nullable
              as int,
      clicks: null == clicks
          ? _value.clicks
          : clicks // ignore: cast_nullable_to_non_nullable
              as int,
      conversions: null == conversions
          ? _value.conversions
          : conversions // ignore: cast_nullable_to_non_nullable
              as int,
      clickThroughRate: null == clickThroughRate
          ? _value.clickThroughRate
          : clickThroughRate // ignore: cast_nullable_to_non_nullable
              as double,
      conversionRate: null == conversionRate
          ? _value.conversionRate
          : conversionRate // ignore: cast_nullable_to_non_nullable
              as double,
      avgReadTime: null == avgReadTime
          ? _value.avgReadTime
          : avgReadTime // ignore: cast_nullable_to_non_nullable
              as double,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$RecommendationPerformanceImpl implements _RecommendationPerformance {
  const _$RecommendationPerformanceImpl(
      {required this.totalRecommendations,
      required this.clicks,
      required this.conversions,
      this.clickThroughRate = 0,
      this.conversionRate = 0,
      this.avgReadTime = 0});

  factory _$RecommendationPerformanceImpl.fromJson(Map<String, dynamic> json) =>
      _$$RecommendationPerformanceImplFromJson(json);

  @override
  final int totalRecommendations;
  @override
  final int clicks;
  @override
  final int conversions;
  @override
  @JsonKey()
  final double clickThroughRate;
  @override
  @JsonKey()
  final double conversionRate;
  @override
  @JsonKey()
  final double avgReadTime;

  @override
  String toString() {
    return 'RecommendationPerformance(totalRecommendations: $totalRecommendations, clicks: $clicks, conversions: $conversions, clickThroughRate: $clickThroughRate, conversionRate: $conversionRate, avgReadTime: $avgReadTime)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$RecommendationPerformanceImpl &&
            (identical(other.totalRecommendations, totalRecommendations) ||
                other.totalRecommendations == totalRecommendations) &&
            (identical(other.clicks, clicks) || other.clicks == clicks) &&
            (identical(other.conversions, conversions) ||
                other.conversions == conversions) &&
            (identical(other.clickThroughRate, clickThroughRate) ||
                other.clickThroughRate == clickThroughRate) &&
            (identical(other.conversionRate, conversionRate) ||
                other.conversionRate == conversionRate) &&
            (identical(other.avgReadTime, avgReadTime) ||
                other.avgReadTime == avgReadTime));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, totalRecommendations, clicks,
      conversions, clickThroughRate, conversionRate, avgReadTime);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$RecommendationPerformanceImplCopyWith<_$RecommendationPerformanceImpl>
      get copyWith => __$$RecommendationPerformanceImplCopyWithImpl<
          _$RecommendationPerformanceImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$RecommendationPerformanceImplToJson(
      this,
    );
  }
}

abstract class _RecommendationPerformance implements RecommendationPerformance {
  const factory _RecommendationPerformance(
      {required final int totalRecommendations,
      required final int clicks,
      required final int conversions,
      final double clickThroughRate,
      final double conversionRate,
      final double avgReadTime}) = _$RecommendationPerformanceImpl;

  factory _RecommendationPerformance.fromJson(Map<String, dynamic> json) =
      _$RecommendationPerformanceImpl.fromJson;

  @override
  int get totalRecommendations;
  @override
  int get clicks;
  @override
  int get conversions;
  @override
  double get clickThroughRate;
  @override
  double get conversionRate;
  @override
  double get avgReadTime;
  @override
  @JsonKey(ignore: true)
  _$$RecommendationPerformanceImplCopyWith<_$RecommendationPerformanceImpl>
      get copyWith => throw _privateConstructorUsedError;
}

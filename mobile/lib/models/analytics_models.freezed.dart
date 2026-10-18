// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'analytics_models.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
    'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models');

AnalyticsReport _$AnalyticsReportFromJson(Map<String, dynamic> json) {
  return _AnalyticsReport.fromJson(json);
}

/// @nodoc
mixin _$AnalyticsReport {
  int get id => throw _privateConstructorUsedError;
  String get name => throw _privateConstructorUsedError;
  String get reportType => throw _privateConstructorUsedError;
  DateTime get periodStart => throw _privateConstructorUsedError;
  DateTime get periodEnd => throw _privateConstructorUsedError;
  int get totalPageviews => throw _privateConstructorUsedError;
  int get totalSessions => throw _privateConstructorUsedError;
  int get uniqueVisitors => throw _privateConstructorUsedError;
  double get avgSessionDuration => throw _privateConstructorUsedError;
  double get bounceRate => throw _privateConstructorUsedError;
  double get conversionRate => throw _privateConstructorUsedError;
  double get revenue => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;
  DateTime get updatedAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $AnalyticsReportCopyWith<AnalyticsReport> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $AnalyticsReportCopyWith<$Res> {
  factory $AnalyticsReportCopyWith(
          AnalyticsReport value, $Res Function(AnalyticsReport) then) =
      _$AnalyticsReportCopyWithImpl<$Res, AnalyticsReport>;
  @useResult
  $Res call(
      {int id,
      String name,
      String reportType,
      DateTime periodStart,
      DateTime periodEnd,
      int totalPageviews,
      int totalSessions,
      int uniqueVisitors,
      double avgSessionDuration,
      double bounceRate,
      double conversionRate,
      double revenue,
      DateTime createdAt,
      DateTime updatedAt});
}

/// @nodoc
class _$AnalyticsReportCopyWithImpl<$Res, $Val extends AnalyticsReport>
    implements $AnalyticsReportCopyWith<$Res> {
  _$AnalyticsReportCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? reportType = null,
    Object? periodStart = null,
    Object? periodEnd = null,
    Object? totalPageviews = null,
    Object? totalSessions = null,
    Object? uniqueVisitors = null,
    Object? avgSessionDuration = null,
    Object? bounceRate = null,
    Object? conversionRate = null,
    Object? revenue = null,
    Object? createdAt = null,
    Object? updatedAt = null,
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
      reportType: null == reportType
          ? _value.reportType
          : reportType // ignore: cast_nullable_to_non_nullable
              as String,
      periodStart: null == periodStart
          ? _value.periodStart
          : periodStart // ignore: cast_nullable_to_non_nullable
              as DateTime,
      periodEnd: null == periodEnd
          ? _value.periodEnd
          : periodEnd // ignore: cast_nullable_to_non_nullable
              as DateTime,
      totalPageviews: null == totalPageviews
          ? _value.totalPageviews
          : totalPageviews // ignore: cast_nullable_to_non_nullable
              as int,
      totalSessions: null == totalSessions
          ? _value.totalSessions
          : totalSessions // ignore: cast_nullable_to_non_nullable
              as int,
      uniqueVisitors: null == uniqueVisitors
          ? _value.uniqueVisitors
          : uniqueVisitors // ignore: cast_nullable_to_non_nullable
              as int,
      avgSessionDuration: null == avgSessionDuration
          ? _value.avgSessionDuration
          : avgSessionDuration // ignore: cast_nullable_to_non_nullable
              as double,
      bounceRate: null == bounceRate
          ? _value.bounceRate
          : bounceRate // ignore: cast_nullable_to_non_nullable
              as double,
      conversionRate: null == conversionRate
          ? _value.conversionRate
          : conversionRate // ignore: cast_nullable_to_non_nullable
              as double,
      revenue: null == revenue
          ? _value.revenue
          : revenue // ignore: cast_nullable_to_non_nullable
              as double,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
      updatedAt: null == updatedAt
          ? _value.updatedAt
          : updatedAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$AnalyticsReportImplCopyWith<$Res>
    implements $AnalyticsReportCopyWith<$Res> {
  factory _$$AnalyticsReportImplCopyWith(_$AnalyticsReportImpl value,
          $Res Function(_$AnalyticsReportImpl) then) =
      __$$AnalyticsReportImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String name,
      String reportType,
      DateTime periodStart,
      DateTime periodEnd,
      int totalPageviews,
      int totalSessions,
      int uniqueVisitors,
      double avgSessionDuration,
      double bounceRate,
      double conversionRate,
      double revenue,
      DateTime createdAt,
      DateTime updatedAt});
}

/// @nodoc
class __$$AnalyticsReportImplCopyWithImpl<$Res>
    extends _$AnalyticsReportCopyWithImpl<$Res, _$AnalyticsReportImpl>
    implements _$$AnalyticsReportImplCopyWith<$Res> {
  __$$AnalyticsReportImplCopyWithImpl(
      _$AnalyticsReportImpl _value, $Res Function(_$AnalyticsReportImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? reportType = null,
    Object? periodStart = null,
    Object? periodEnd = null,
    Object? totalPageviews = null,
    Object? totalSessions = null,
    Object? uniqueVisitors = null,
    Object? avgSessionDuration = null,
    Object? bounceRate = null,
    Object? conversionRate = null,
    Object? revenue = null,
    Object? createdAt = null,
    Object? updatedAt = null,
  }) {
    return _then(_$AnalyticsReportImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      name: null == name
          ? _value.name
          : name // ignore: cast_nullable_to_non_nullable
              as String,
      reportType: null == reportType
          ? _value.reportType
          : reportType // ignore: cast_nullable_to_non_nullable
              as String,
      periodStart: null == periodStart
          ? _value.periodStart
          : periodStart // ignore: cast_nullable_to_non_nullable
              as DateTime,
      periodEnd: null == periodEnd
          ? _value.periodEnd
          : periodEnd // ignore: cast_nullable_to_non_nullable
              as DateTime,
      totalPageviews: null == totalPageviews
          ? _value.totalPageviews
          : totalPageviews // ignore: cast_nullable_to_non_nullable
              as int,
      totalSessions: null == totalSessions
          ? _value.totalSessions
          : totalSessions // ignore: cast_nullable_to_non_nullable
              as int,
      uniqueVisitors: null == uniqueVisitors
          ? _value.uniqueVisitors
          : uniqueVisitors // ignore: cast_nullable_to_non_nullable
              as int,
      avgSessionDuration: null == avgSessionDuration
          ? _value.avgSessionDuration
          : avgSessionDuration // ignore: cast_nullable_to_non_nullable
              as double,
      bounceRate: null == bounceRate
          ? _value.bounceRate
          : bounceRate // ignore: cast_nullable_to_non_nullable
              as double,
      conversionRate: null == conversionRate
          ? _value.conversionRate
          : conversionRate // ignore: cast_nullable_to_non_nullable
              as double,
      revenue: null == revenue
          ? _value.revenue
          : revenue // ignore: cast_nullable_to_non_nullable
              as double,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
      updatedAt: null == updatedAt
          ? _value.updatedAt
          : updatedAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$AnalyticsReportImpl implements _AnalyticsReport {
  const _$AnalyticsReportImpl(
      {required this.id,
      required this.name,
      required this.reportType,
      required this.periodStart,
      required this.periodEnd,
      required this.totalPageviews,
      required this.totalSessions,
      required this.uniqueVisitors,
      required this.avgSessionDuration,
      required this.bounceRate,
      required this.conversionRate,
      required this.revenue,
      required this.createdAt,
      required this.updatedAt});

  factory _$AnalyticsReportImpl.fromJson(Map<String, dynamic> json) =>
      _$$AnalyticsReportImplFromJson(json);

  @override
  final int id;
  @override
  final String name;
  @override
  final String reportType;
  @override
  final DateTime periodStart;
  @override
  final DateTime periodEnd;
  @override
  final int totalPageviews;
  @override
  final int totalSessions;
  @override
  final int uniqueVisitors;
  @override
  final double avgSessionDuration;
  @override
  final double bounceRate;
  @override
  final double conversionRate;
  @override
  final double revenue;
  @override
  final DateTime createdAt;
  @override
  final DateTime updatedAt;

  @override
  String toString() {
    return 'AnalyticsReport(id: $id, name: $name, reportType: $reportType, periodStart: $periodStart, periodEnd: $periodEnd, totalPageviews: $totalPageviews, totalSessions: $totalSessions, uniqueVisitors: $uniqueVisitors, avgSessionDuration: $avgSessionDuration, bounceRate: $bounceRate, conversionRate: $conversionRate, revenue: $revenue, createdAt: $createdAt, updatedAt: $updatedAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$AnalyticsReportImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.reportType, reportType) ||
                other.reportType == reportType) &&
            (identical(other.periodStart, periodStart) ||
                other.periodStart == periodStart) &&
            (identical(other.periodEnd, periodEnd) ||
                other.periodEnd == periodEnd) &&
            (identical(other.totalPageviews, totalPageviews) ||
                other.totalPageviews == totalPageviews) &&
            (identical(other.totalSessions, totalSessions) ||
                other.totalSessions == totalSessions) &&
            (identical(other.uniqueVisitors, uniqueVisitors) ||
                other.uniqueVisitors == uniqueVisitors) &&
            (identical(other.avgSessionDuration, avgSessionDuration) ||
                other.avgSessionDuration == avgSessionDuration) &&
            (identical(other.bounceRate, bounceRate) ||
                other.bounceRate == bounceRate) &&
            (identical(other.conversionRate, conversionRate) ||
                other.conversionRate == conversionRate) &&
            (identical(other.revenue, revenue) || other.revenue == revenue) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt) &&
            (identical(other.updatedAt, updatedAt) ||
                other.updatedAt == updatedAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      name,
      reportType,
      periodStart,
      periodEnd,
      totalPageviews,
      totalSessions,
      uniqueVisitors,
      avgSessionDuration,
      bounceRate,
      conversionRate,
      revenue,
      createdAt,
      updatedAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$AnalyticsReportImplCopyWith<_$AnalyticsReportImpl> get copyWith =>
      __$$AnalyticsReportImplCopyWithImpl<_$AnalyticsReportImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$AnalyticsReportImplToJson(
      this,
    );
  }
}

abstract class _AnalyticsReport implements AnalyticsReport {
  const factory _AnalyticsReport(
      {required final int id,
      required final String name,
      required final String reportType,
      required final DateTime periodStart,
      required final DateTime periodEnd,
      required final int totalPageviews,
      required final int totalSessions,
      required final int uniqueVisitors,
      required final double avgSessionDuration,
      required final double bounceRate,
      required final double conversionRate,
      required final double revenue,
      required final DateTime createdAt,
      required final DateTime updatedAt}) = _$AnalyticsReportImpl;

  factory _AnalyticsReport.fromJson(Map<String, dynamic> json) =
      _$AnalyticsReportImpl.fromJson;

  @override
  int get id;
  @override
  String get name;
  @override
  String get reportType;
  @override
  DateTime get periodStart;
  @override
  DateTime get periodEnd;
  @override
  int get totalPageviews;
  @override
  int get totalSessions;
  @override
  int get uniqueVisitors;
  @override
  double get avgSessionDuration;
  @override
  double get bounceRate;
  @override
  double get conversionRate;
  @override
  double get revenue;
  @override
  DateTime get createdAt;
  @override
  DateTime get updatedAt;
  @override
  @JsonKey(ignore: true)
  _$$AnalyticsReportImplCopyWith<_$AnalyticsReportImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

DailyAnalytics _$DailyAnalyticsFromJson(Map<String, dynamic> json) {
  return _DailyAnalytics.fromJson(json);
}

/// @nodoc
mixin _$DailyAnalytics {
  DateTime get date => throw _privateConstructorUsedError;
  int get pageviews => throw _privateConstructorUsedError;
  int get sessions => throw _privateConstructorUsedError;
  int get uniqueVisitors => throw _privateConstructorUsedError;
  double get bounceRate => throw _privateConstructorUsedError;
  double get conversionRate => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $DailyAnalyticsCopyWith<DailyAnalytics> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $DailyAnalyticsCopyWith<$Res> {
  factory $DailyAnalyticsCopyWith(
          DailyAnalytics value, $Res Function(DailyAnalytics) then) =
      _$DailyAnalyticsCopyWithImpl<$Res, DailyAnalytics>;
  @useResult
  $Res call(
      {DateTime date,
      int pageviews,
      int sessions,
      int uniqueVisitors,
      double bounceRate,
      double conversionRate});
}

/// @nodoc
class _$DailyAnalyticsCopyWithImpl<$Res, $Val extends DailyAnalytics>
    implements $DailyAnalyticsCopyWith<$Res> {
  _$DailyAnalyticsCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? date = null,
    Object? pageviews = null,
    Object? sessions = null,
    Object? uniqueVisitors = null,
    Object? bounceRate = null,
    Object? conversionRate = null,
  }) {
    return _then(_value.copyWith(
      date: null == date
          ? _value.date
          : date // ignore: cast_nullable_to_non_nullable
              as DateTime,
      pageviews: null == pageviews
          ? _value.pageviews
          : pageviews // ignore: cast_nullable_to_non_nullable
              as int,
      sessions: null == sessions
          ? _value.sessions
          : sessions // ignore: cast_nullable_to_non_nullable
              as int,
      uniqueVisitors: null == uniqueVisitors
          ? _value.uniqueVisitors
          : uniqueVisitors // ignore: cast_nullable_to_non_nullable
              as int,
      bounceRate: null == bounceRate
          ? _value.bounceRate
          : bounceRate // ignore: cast_nullable_to_non_nullable
              as double,
      conversionRate: null == conversionRate
          ? _value.conversionRate
          : conversionRate // ignore: cast_nullable_to_non_nullable
              as double,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$DailyAnalyticsImplCopyWith<$Res>
    implements $DailyAnalyticsCopyWith<$Res> {
  factory _$$DailyAnalyticsImplCopyWith(_$DailyAnalyticsImpl value,
          $Res Function(_$DailyAnalyticsImpl) then) =
      __$$DailyAnalyticsImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {DateTime date,
      int pageviews,
      int sessions,
      int uniqueVisitors,
      double bounceRate,
      double conversionRate});
}

/// @nodoc
class __$$DailyAnalyticsImplCopyWithImpl<$Res>
    extends _$DailyAnalyticsCopyWithImpl<$Res, _$DailyAnalyticsImpl>
    implements _$$DailyAnalyticsImplCopyWith<$Res> {
  __$$DailyAnalyticsImplCopyWithImpl(
      _$DailyAnalyticsImpl _value, $Res Function(_$DailyAnalyticsImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? date = null,
    Object? pageviews = null,
    Object? sessions = null,
    Object? uniqueVisitors = null,
    Object? bounceRate = null,
    Object? conversionRate = null,
  }) {
    return _then(_$DailyAnalyticsImpl(
      date: null == date
          ? _value.date
          : date // ignore: cast_nullable_to_non_nullable
              as DateTime,
      pageviews: null == pageviews
          ? _value.pageviews
          : pageviews // ignore: cast_nullable_to_non_nullable
              as int,
      sessions: null == sessions
          ? _value.sessions
          : sessions // ignore: cast_nullable_to_non_nullable
              as int,
      uniqueVisitors: null == uniqueVisitors
          ? _value.uniqueVisitors
          : uniqueVisitors // ignore: cast_nullable_to_non_nullable
              as int,
      bounceRate: null == bounceRate
          ? _value.bounceRate
          : bounceRate // ignore: cast_nullable_to_non_nullable
              as double,
      conversionRate: null == conversionRate
          ? _value.conversionRate
          : conversionRate // ignore: cast_nullable_to_non_nullable
              as double,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$DailyAnalyticsImpl implements _DailyAnalytics {
  const _$DailyAnalyticsImpl(
      {required this.date,
      required this.pageviews,
      required this.sessions,
      required this.uniqueVisitors,
      required this.bounceRate,
      required this.conversionRate});

  factory _$DailyAnalyticsImpl.fromJson(Map<String, dynamic> json) =>
      _$$DailyAnalyticsImplFromJson(json);

  @override
  final DateTime date;
  @override
  final int pageviews;
  @override
  final int sessions;
  @override
  final int uniqueVisitors;
  @override
  final double bounceRate;
  @override
  final double conversionRate;

  @override
  String toString() {
    return 'DailyAnalytics(date: $date, pageviews: $pageviews, sessions: $sessions, uniqueVisitors: $uniqueVisitors, bounceRate: $bounceRate, conversionRate: $conversionRate)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$DailyAnalyticsImpl &&
            (identical(other.date, date) || other.date == date) &&
            (identical(other.pageviews, pageviews) ||
                other.pageviews == pageviews) &&
            (identical(other.sessions, sessions) ||
                other.sessions == sessions) &&
            (identical(other.uniqueVisitors, uniqueVisitors) ||
                other.uniqueVisitors == uniqueVisitors) &&
            (identical(other.bounceRate, bounceRate) ||
                other.bounceRate == bounceRate) &&
            (identical(other.conversionRate, conversionRate) ||
                other.conversionRate == conversionRate));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, date, pageviews, sessions,
      uniqueVisitors, bounceRate, conversionRate);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$DailyAnalyticsImplCopyWith<_$DailyAnalyticsImpl> get copyWith =>
      __$$DailyAnalyticsImplCopyWithImpl<_$DailyAnalyticsImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$DailyAnalyticsImplToJson(
      this,
    );
  }
}

abstract class _DailyAnalytics implements DailyAnalytics {
  const factory _DailyAnalytics(
      {required final DateTime date,
      required final int pageviews,
      required final int sessions,
      required final int uniqueVisitors,
      required final double bounceRate,
      required final double conversionRate}) = _$DailyAnalyticsImpl;

  factory _DailyAnalytics.fromJson(Map<String, dynamic> json) =
      _$DailyAnalyticsImpl.fromJson;

  @override
  DateTime get date;
  @override
  int get pageviews;
  @override
  int get sessions;
  @override
  int get uniqueVisitors;
  @override
  double get bounceRate;
  @override
  double get conversionRate;
  @override
  @JsonKey(ignore: true)
  _$$DailyAnalyticsImplCopyWith<_$DailyAnalyticsImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

PageViewMetric _$PageViewMetricFromJson(Map<String, dynamic> json) {
  return _PageViewMetric.fromJson(json);
}

/// @nodoc
mixin _$PageViewMetric {
  int get id => throw _privateConstructorUsedError;
  int get contentId => throw _privateConstructorUsedError;
  DateTime get date => throw _privateConstructorUsedError;
  int get pageViews => throw _privateConstructorUsedError;
  int get uniqueVisitors => throw _privateConstructorUsedError;
  double get avgTimeOnPage => throw _privateConstructorUsedError;
  double get bounceRate => throw _privateConstructorUsedError;
  double get scrollDepth => throw _privateConstructorUsedError;
  int get conversionCount => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $PageViewMetricCopyWith<PageViewMetric> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $PageViewMetricCopyWith<$Res> {
  factory $PageViewMetricCopyWith(
          PageViewMetric value, $Res Function(PageViewMetric) then) =
      _$PageViewMetricCopyWithImpl<$Res, PageViewMetric>;
  @useResult
  $Res call(
      {int id,
      int contentId,
      DateTime date,
      int pageViews,
      int uniqueVisitors,
      double avgTimeOnPage,
      double bounceRate,
      double scrollDepth,
      int conversionCount});
}

/// @nodoc
class _$PageViewMetricCopyWithImpl<$Res, $Val extends PageViewMetric>
    implements $PageViewMetricCopyWith<$Res> {
  _$PageViewMetricCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? contentId = null,
    Object? date = null,
    Object? pageViews = null,
    Object? uniqueVisitors = null,
    Object? avgTimeOnPage = null,
    Object? bounceRate = null,
    Object? scrollDepth = null,
    Object? conversionCount = null,
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
      date: null == date
          ? _value.date
          : date // ignore: cast_nullable_to_non_nullable
              as DateTime,
      pageViews: null == pageViews
          ? _value.pageViews
          : pageViews // ignore: cast_nullable_to_non_nullable
              as int,
      uniqueVisitors: null == uniqueVisitors
          ? _value.uniqueVisitors
          : uniqueVisitors // ignore: cast_nullable_to_non_nullable
              as int,
      avgTimeOnPage: null == avgTimeOnPage
          ? _value.avgTimeOnPage
          : avgTimeOnPage // ignore: cast_nullable_to_non_nullable
              as double,
      bounceRate: null == bounceRate
          ? _value.bounceRate
          : bounceRate // ignore: cast_nullable_to_non_nullable
              as double,
      scrollDepth: null == scrollDepth
          ? _value.scrollDepth
          : scrollDepth // ignore: cast_nullable_to_non_nullable
              as double,
      conversionCount: null == conversionCount
          ? _value.conversionCount
          : conversionCount // ignore: cast_nullable_to_non_nullable
              as int,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$PageViewMetricImplCopyWith<$Res>
    implements $PageViewMetricCopyWith<$Res> {
  factory _$$PageViewMetricImplCopyWith(_$PageViewMetricImpl value,
          $Res Function(_$PageViewMetricImpl) then) =
      __$$PageViewMetricImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int contentId,
      DateTime date,
      int pageViews,
      int uniqueVisitors,
      double avgTimeOnPage,
      double bounceRate,
      double scrollDepth,
      int conversionCount});
}

/// @nodoc
class __$$PageViewMetricImplCopyWithImpl<$Res>
    extends _$PageViewMetricCopyWithImpl<$Res, _$PageViewMetricImpl>
    implements _$$PageViewMetricImplCopyWith<$Res> {
  __$$PageViewMetricImplCopyWithImpl(
      _$PageViewMetricImpl _value, $Res Function(_$PageViewMetricImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? contentId = null,
    Object? date = null,
    Object? pageViews = null,
    Object? uniqueVisitors = null,
    Object? avgTimeOnPage = null,
    Object? bounceRate = null,
    Object? scrollDepth = null,
    Object? conversionCount = null,
  }) {
    return _then(_$PageViewMetricImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      contentId: null == contentId
          ? _value.contentId
          : contentId // ignore: cast_nullable_to_non_nullable
              as int,
      date: null == date
          ? _value.date
          : date // ignore: cast_nullable_to_non_nullable
              as DateTime,
      pageViews: null == pageViews
          ? _value.pageViews
          : pageViews // ignore: cast_nullable_to_non_nullable
              as int,
      uniqueVisitors: null == uniqueVisitors
          ? _value.uniqueVisitors
          : uniqueVisitors // ignore: cast_nullable_to_non_nullable
              as int,
      avgTimeOnPage: null == avgTimeOnPage
          ? _value.avgTimeOnPage
          : avgTimeOnPage // ignore: cast_nullable_to_non_nullable
              as double,
      bounceRate: null == bounceRate
          ? _value.bounceRate
          : bounceRate // ignore: cast_nullable_to_non_nullable
              as double,
      scrollDepth: null == scrollDepth
          ? _value.scrollDepth
          : scrollDepth // ignore: cast_nullable_to_non_nullable
              as double,
      conversionCount: null == conversionCount
          ? _value.conversionCount
          : conversionCount // ignore: cast_nullable_to_non_nullable
              as int,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$PageViewMetricImpl implements _PageViewMetric {
  const _$PageViewMetricImpl(
      {required this.id,
      required this.contentId,
      required this.date,
      required this.pageViews,
      required this.uniqueVisitors,
      required this.avgTimeOnPage,
      required this.bounceRate,
      required this.scrollDepth,
      required this.conversionCount});

  factory _$PageViewMetricImpl.fromJson(Map<String, dynamic> json) =>
      _$$PageViewMetricImplFromJson(json);

  @override
  final int id;
  @override
  final int contentId;
  @override
  final DateTime date;
  @override
  final int pageViews;
  @override
  final int uniqueVisitors;
  @override
  final double avgTimeOnPage;
  @override
  final double bounceRate;
  @override
  final double scrollDepth;
  @override
  final int conversionCount;

  @override
  String toString() {
    return 'PageViewMetric(id: $id, contentId: $contentId, date: $date, pageViews: $pageViews, uniqueVisitors: $uniqueVisitors, avgTimeOnPage: $avgTimeOnPage, bounceRate: $bounceRate, scrollDepth: $scrollDepth, conversionCount: $conversionCount)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$PageViewMetricImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.contentId, contentId) ||
                other.contentId == contentId) &&
            (identical(other.date, date) || other.date == date) &&
            (identical(other.pageViews, pageViews) ||
                other.pageViews == pageViews) &&
            (identical(other.uniqueVisitors, uniqueVisitors) ||
                other.uniqueVisitors == uniqueVisitors) &&
            (identical(other.avgTimeOnPage, avgTimeOnPage) ||
                other.avgTimeOnPage == avgTimeOnPage) &&
            (identical(other.bounceRate, bounceRate) ||
                other.bounceRate == bounceRate) &&
            (identical(other.scrollDepth, scrollDepth) ||
                other.scrollDepth == scrollDepth) &&
            (identical(other.conversionCount, conversionCount) ||
                other.conversionCount == conversionCount));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, id, contentId, date, pageViews,
      uniqueVisitors, avgTimeOnPage, bounceRate, scrollDepth, conversionCount);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$PageViewMetricImplCopyWith<_$PageViewMetricImpl> get copyWith =>
      __$$PageViewMetricImplCopyWithImpl<_$PageViewMetricImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$PageViewMetricImplToJson(
      this,
    );
  }
}

abstract class _PageViewMetric implements PageViewMetric {
  const factory _PageViewMetric(
      {required final int id,
      required final int contentId,
      required final DateTime date,
      required final int pageViews,
      required final int uniqueVisitors,
      required final double avgTimeOnPage,
      required final double bounceRate,
      required final double scrollDepth,
      required final int conversionCount}) = _$PageViewMetricImpl;

  factory _PageViewMetric.fromJson(Map<String, dynamic> json) =
      _$PageViewMetricImpl.fromJson;

  @override
  int get id;
  @override
  int get contentId;
  @override
  DateTime get date;
  @override
  int get pageViews;
  @override
  int get uniqueVisitors;
  @override
  double get avgTimeOnPage;
  @override
  double get bounceRate;
  @override
  double get scrollDepth;
  @override
  int get conversionCount;
  @override
  @JsonKey(ignore: true)
  _$$PageViewMetricImplCopyWith<_$PageViewMetricImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

TopContent _$TopContentFromJson(Map<String, dynamic> json) {
  return _TopContent.fromJson(json);
}

/// @nodoc
mixin _$TopContent {
  int get contentId => throw _privateConstructorUsedError;
  int get pageviews => throw _privateConstructorUsedError;
  int get uniqueVisitors => throw _privateConstructorUsedError;
  double get avgTimeOnPage => throw _privateConstructorUsedError;
  int get conversionCount => throw _privateConstructorUsedError;
  String? get title => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $TopContentCopyWith<TopContent> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $TopContentCopyWith<$Res> {
  factory $TopContentCopyWith(
          TopContent value, $Res Function(TopContent) then) =
      _$TopContentCopyWithImpl<$Res, TopContent>;
  @useResult
  $Res call(
      {int contentId,
      int pageviews,
      int uniqueVisitors,
      double avgTimeOnPage,
      int conversionCount,
      String? title});
}

/// @nodoc
class _$TopContentCopyWithImpl<$Res, $Val extends TopContent>
    implements $TopContentCopyWith<$Res> {
  _$TopContentCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? contentId = null,
    Object? pageviews = null,
    Object? uniqueVisitors = null,
    Object? avgTimeOnPage = null,
    Object? conversionCount = null,
    Object? title = freezed,
  }) {
    return _then(_value.copyWith(
      contentId: null == contentId
          ? _value.contentId
          : contentId // ignore: cast_nullable_to_non_nullable
              as int,
      pageviews: null == pageviews
          ? _value.pageviews
          : pageviews // ignore: cast_nullable_to_non_nullable
              as int,
      uniqueVisitors: null == uniqueVisitors
          ? _value.uniqueVisitors
          : uniqueVisitors // ignore: cast_nullable_to_non_nullable
              as int,
      avgTimeOnPage: null == avgTimeOnPage
          ? _value.avgTimeOnPage
          : avgTimeOnPage // ignore: cast_nullable_to_non_nullable
              as double,
      conversionCount: null == conversionCount
          ? _value.conversionCount
          : conversionCount // ignore: cast_nullable_to_non_nullable
              as int,
      title: freezed == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String?,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$TopContentImplCopyWith<$Res>
    implements $TopContentCopyWith<$Res> {
  factory _$$TopContentImplCopyWith(
          _$TopContentImpl value, $Res Function(_$TopContentImpl) then) =
      __$$TopContentImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int contentId,
      int pageviews,
      int uniqueVisitors,
      double avgTimeOnPage,
      int conversionCount,
      String? title});
}

/// @nodoc
class __$$TopContentImplCopyWithImpl<$Res>
    extends _$TopContentCopyWithImpl<$Res, _$TopContentImpl>
    implements _$$TopContentImplCopyWith<$Res> {
  __$$TopContentImplCopyWithImpl(
      _$TopContentImpl _value, $Res Function(_$TopContentImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? contentId = null,
    Object? pageviews = null,
    Object? uniqueVisitors = null,
    Object? avgTimeOnPage = null,
    Object? conversionCount = null,
    Object? title = freezed,
  }) {
    return _then(_$TopContentImpl(
      contentId: null == contentId
          ? _value.contentId
          : contentId // ignore: cast_nullable_to_non_nullable
              as int,
      pageviews: null == pageviews
          ? _value.pageviews
          : pageviews // ignore: cast_nullable_to_non_nullable
              as int,
      uniqueVisitors: null == uniqueVisitors
          ? _value.uniqueVisitors
          : uniqueVisitors // ignore: cast_nullable_to_non_nullable
              as int,
      avgTimeOnPage: null == avgTimeOnPage
          ? _value.avgTimeOnPage
          : avgTimeOnPage // ignore: cast_nullable_to_non_nullable
              as double,
      conversionCount: null == conversionCount
          ? _value.conversionCount
          : conversionCount // ignore: cast_nullable_to_non_nullable
              as int,
      title: freezed == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String?,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$TopContentImpl implements _TopContent {
  const _$TopContentImpl(
      {required this.contentId,
      required this.pageviews,
      required this.uniqueVisitors,
      required this.avgTimeOnPage,
      required this.conversionCount,
      required this.title});

  factory _$TopContentImpl.fromJson(Map<String, dynamic> json) =>
      _$$TopContentImplFromJson(json);

  @override
  final int contentId;
  @override
  final int pageviews;
  @override
  final int uniqueVisitors;
  @override
  final double avgTimeOnPage;
  @override
  final int conversionCount;
  @override
  final String? title;

  @override
  String toString() {
    return 'TopContent(contentId: $contentId, pageviews: $pageviews, uniqueVisitors: $uniqueVisitors, avgTimeOnPage: $avgTimeOnPage, conversionCount: $conversionCount, title: $title)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$TopContentImpl &&
            (identical(other.contentId, contentId) ||
                other.contentId == contentId) &&
            (identical(other.pageviews, pageviews) ||
                other.pageviews == pageviews) &&
            (identical(other.uniqueVisitors, uniqueVisitors) ||
                other.uniqueVisitors == uniqueVisitors) &&
            (identical(other.avgTimeOnPage, avgTimeOnPage) ||
                other.avgTimeOnPage == avgTimeOnPage) &&
            (identical(other.conversionCount, conversionCount) ||
                other.conversionCount == conversionCount) &&
            (identical(other.title, title) || other.title == title));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, contentId, pageviews,
      uniqueVisitors, avgTimeOnPage, conversionCount, title);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$TopContentImplCopyWith<_$TopContentImpl> get copyWith =>
      __$$TopContentImplCopyWithImpl<_$TopContentImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$TopContentImplToJson(
      this,
    );
  }
}

abstract class _TopContent implements TopContent {
  const factory _TopContent(
      {required final int contentId,
      required final int pageviews,
      required final int uniqueVisitors,
      required final double avgTimeOnPage,
      required final int conversionCount,
      required final String? title}) = _$TopContentImpl;

  factory _TopContent.fromJson(Map<String, dynamic> json) =
      _$TopContentImpl.fromJson;

  @override
  int get contentId;
  @override
  int get pageviews;
  @override
  int get uniqueVisitors;
  @override
  double get avgTimeOnPage;
  @override
  int get conversionCount;
  @override
  String? get title;
  @override
  @JsonKey(ignore: true)
  _$$TopContentImplCopyWith<_$TopContentImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

UserEvent _$UserEventFromJson(Map<String, dynamic> json) {
  return _UserEvent.fromJson(json);
}

/// @nodoc
mixin _$UserEvent {
  int get id => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  int? get contentId => throw _privateConstructorUsedError;
  String get eventType => throw _privateConstructorUsedError;
  Map<String, dynamic> get eventData => throw _privateConstructorUsedError;
  String? get pageUrl => throw _privateConstructorUsedError;
  String? get referrer => throw _privateConstructorUsedError;
  String? get deviceType => throw _privateConstructorUsedError;
  String? get browser => throw _privateConstructorUsedError;
  String? get os => throw _privateConstructorUsedError;
  DateTime get timestamp => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $UserEventCopyWith<UserEvent> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $UserEventCopyWith<$Res> {
  factory $UserEventCopyWith(UserEvent value, $Res Function(UserEvent) then) =
      _$UserEventCopyWithImpl<$Res, UserEvent>;
  @useResult
  $Res call(
      {int id,
      int userId,
      int? contentId,
      String eventType,
      Map<String, dynamic> eventData,
      String? pageUrl,
      String? referrer,
      String? deviceType,
      String? browser,
      String? os,
      DateTime timestamp});
}

/// @nodoc
class _$UserEventCopyWithImpl<$Res, $Val extends UserEvent>
    implements $UserEventCopyWith<$Res> {
  _$UserEventCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? contentId = freezed,
    Object? eventType = null,
    Object? eventData = null,
    Object? pageUrl = freezed,
    Object? referrer = freezed,
    Object? deviceType = freezed,
    Object? browser = freezed,
    Object? os = freezed,
    Object? timestamp = null,
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
      contentId: freezed == contentId
          ? _value.contentId
          : contentId // ignore: cast_nullable_to_non_nullable
              as int?,
      eventType: null == eventType
          ? _value.eventType
          : eventType // ignore: cast_nullable_to_non_nullable
              as String,
      eventData: null == eventData
          ? _value.eventData
          : eventData // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      pageUrl: freezed == pageUrl
          ? _value.pageUrl
          : pageUrl // ignore: cast_nullable_to_non_nullable
              as String?,
      referrer: freezed == referrer
          ? _value.referrer
          : referrer // ignore: cast_nullable_to_non_nullable
              as String?,
      deviceType: freezed == deviceType
          ? _value.deviceType
          : deviceType // ignore: cast_nullable_to_non_nullable
              as String?,
      browser: freezed == browser
          ? _value.browser
          : browser // ignore: cast_nullable_to_non_nullable
              as String?,
      os: freezed == os
          ? _value.os
          : os // ignore: cast_nullable_to_non_nullable
              as String?,
      timestamp: null == timestamp
          ? _value.timestamp
          : timestamp // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$UserEventImplCopyWith<$Res>
    implements $UserEventCopyWith<$Res> {
  factory _$$UserEventImplCopyWith(
          _$UserEventImpl value, $Res Function(_$UserEventImpl) then) =
      __$$UserEventImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int userId,
      int? contentId,
      String eventType,
      Map<String, dynamic> eventData,
      String? pageUrl,
      String? referrer,
      String? deviceType,
      String? browser,
      String? os,
      DateTime timestamp});
}

/// @nodoc
class __$$UserEventImplCopyWithImpl<$Res>
    extends _$UserEventCopyWithImpl<$Res, _$UserEventImpl>
    implements _$$UserEventImplCopyWith<$Res> {
  __$$UserEventImplCopyWithImpl(
      _$UserEventImpl _value, $Res Function(_$UserEventImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? contentId = freezed,
    Object? eventType = null,
    Object? eventData = null,
    Object? pageUrl = freezed,
    Object? referrer = freezed,
    Object? deviceType = freezed,
    Object? browser = freezed,
    Object? os = freezed,
    Object? timestamp = null,
  }) {
    return _then(_$UserEventImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      contentId: freezed == contentId
          ? _value.contentId
          : contentId // ignore: cast_nullable_to_non_nullable
              as int?,
      eventType: null == eventType
          ? _value.eventType
          : eventType // ignore: cast_nullable_to_non_nullable
              as String,
      eventData: null == eventData
          ? _value._eventData
          : eventData // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      pageUrl: freezed == pageUrl
          ? _value.pageUrl
          : pageUrl // ignore: cast_nullable_to_non_nullable
              as String?,
      referrer: freezed == referrer
          ? _value.referrer
          : referrer // ignore: cast_nullable_to_non_nullable
              as String?,
      deviceType: freezed == deviceType
          ? _value.deviceType
          : deviceType // ignore: cast_nullable_to_non_nullable
              as String?,
      browser: freezed == browser
          ? _value.browser
          : browser // ignore: cast_nullable_to_non_nullable
              as String?,
      os: freezed == os
          ? _value.os
          : os // ignore: cast_nullable_to_non_nullable
              as String?,
      timestamp: null == timestamp
          ? _value.timestamp
          : timestamp // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$UserEventImpl implements _UserEvent {
  const _$UserEventImpl(
      {required this.id,
      required this.userId,
      required this.contentId,
      required this.eventType,
      required final Map<String, dynamic> eventData,
      required this.pageUrl,
      required this.referrer,
      required this.deviceType,
      required this.browser,
      required this.os,
      required this.timestamp})
      : _eventData = eventData;

  factory _$UserEventImpl.fromJson(Map<String, dynamic> json) =>
      _$$UserEventImplFromJson(json);

  @override
  final int id;
  @override
  final int userId;
  @override
  final int? contentId;
  @override
  final String eventType;
  final Map<String, dynamic> _eventData;
  @override
  Map<String, dynamic> get eventData {
    if (_eventData is EqualUnmodifiableMapView) return _eventData;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(_eventData);
  }

  @override
  final String? pageUrl;
  @override
  final String? referrer;
  @override
  final String? deviceType;
  @override
  final String? browser;
  @override
  final String? os;
  @override
  final DateTime timestamp;

  @override
  String toString() {
    return 'UserEvent(id: $id, userId: $userId, contentId: $contentId, eventType: $eventType, eventData: $eventData, pageUrl: $pageUrl, referrer: $referrer, deviceType: $deviceType, browser: $browser, os: $os, timestamp: $timestamp)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$UserEventImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.contentId, contentId) ||
                other.contentId == contentId) &&
            (identical(other.eventType, eventType) ||
                other.eventType == eventType) &&
            const DeepCollectionEquality()
                .equals(other._eventData, _eventData) &&
            (identical(other.pageUrl, pageUrl) || other.pageUrl == pageUrl) &&
            (identical(other.referrer, referrer) ||
                other.referrer == referrer) &&
            (identical(other.deviceType, deviceType) ||
                other.deviceType == deviceType) &&
            (identical(other.browser, browser) || other.browser == browser) &&
            (identical(other.os, os) || other.os == os) &&
            (identical(other.timestamp, timestamp) ||
                other.timestamp == timestamp));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      userId,
      contentId,
      eventType,
      const DeepCollectionEquality().hash(_eventData),
      pageUrl,
      referrer,
      deviceType,
      browser,
      os,
      timestamp);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$UserEventImplCopyWith<_$UserEventImpl> get copyWith =>
      __$$UserEventImplCopyWithImpl<_$UserEventImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$UserEventImplToJson(
      this,
    );
  }
}

abstract class _UserEvent implements UserEvent {
  const factory _UserEvent(
      {required final int id,
      required final int userId,
      required final int? contentId,
      required final String eventType,
      required final Map<String, dynamic> eventData,
      required final String? pageUrl,
      required final String? referrer,
      required final String? deviceType,
      required final String? browser,
      required final String? os,
      required final DateTime timestamp}) = _$UserEventImpl;

  factory _UserEvent.fromJson(Map<String, dynamic> json) =
      _$UserEventImpl.fromJson;

  @override
  int get id;
  @override
  int get userId;
  @override
  int? get contentId;
  @override
  String get eventType;
  @override
  Map<String, dynamic> get eventData;
  @override
  String? get pageUrl;
  @override
  String? get referrer;
  @override
  String? get deviceType;
  @override
  String? get browser;
  @override
  String? get os;
  @override
  DateTime get timestamp;
  @override
  @JsonKey(ignore: true)
  _$$UserEventImplCopyWith<_$UserEventImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

UserBehaviorSummary _$UserBehaviorSummaryFromJson(Map<String, dynamic> json) {
  return _UserBehaviorSummary.fromJson(json);
}

/// @nodoc
mixin _$UserBehaviorSummary {
  int get userId => throw _privateConstructorUsedError;
  int get totalEvents => throw _privateConstructorUsedError;
  Map<String, int> get eventBreakdown => throw _privateConstructorUsedError;
  DateTime? get lastEvent => throw _privateConstructorUsedError;
  String? get mostCommonEvent => throw _privateConstructorUsedError;
  double? get engagementScore => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $UserBehaviorSummaryCopyWith<UserBehaviorSummary> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $UserBehaviorSummaryCopyWith<$Res> {
  factory $UserBehaviorSummaryCopyWith(
          UserBehaviorSummary value, $Res Function(UserBehaviorSummary) then) =
      _$UserBehaviorSummaryCopyWithImpl<$Res, UserBehaviorSummary>;
  @useResult
  $Res call(
      {int userId,
      int totalEvents,
      Map<String, int> eventBreakdown,
      DateTime? lastEvent,
      String? mostCommonEvent,
      double? engagementScore});
}

/// @nodoc
class _$UserBehaviorSummaryCopyWithImpl<$Res, $Val extends UserBehaviorSummary>
    implements $UserBehaviorSummaryCopyWith<$Res> {
  _$UserBehaviorSummaryCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? userId = null,
    Object? totalEvents = null,
    Object? eventBreakdown = null,
    Object? lastEvent = freezed,
    Object? mostCommonEvent = freezed,
    Object? engagementScore = freezed,
  }) {
    return _then(_value.copyWith(
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      totalEvents: null == totalEvents
          ? _value.totalEvents
          : totalEvents // ignore: cast_nullable_to_non_nullable
              as int,
      eventBreakdown: null == eventBreakdown
          ? _value.eventBreakdown
          : eventBreakdown // ignore: cast_nullable_to_non_nullable
              as Map<String, int>,
      lastEvent: freezed == lastEvent
          ? _value.lastEvent
          : lastEvent // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      mostCommonEvent: freezed == mostCommonEvent
          ? _value.mostCommonEvent
          : mostCommonEvent // ignore: cast_nullable_to_non_nullable
              as String?,
      engagementScore: freezed == engagementScore
          ? _value.engagementScore
          : engagementScore // ignore: cast_nullable_to_non_nullable
              as double?,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$UserBehaviorSummaryImplCopyWith<$Res>
    implements $UserBehaviorSummaryCopyWith<$Res> {
  factory _$$UserBehaviorSummaryImplCopyWith(_$UserBehaviorSummaryImpl value,
          $Res Function(_$UserBehaviorSummaryImpl) then) =
      __$$UserBehaviorSummaryImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int userId,
      int totalEvents,
      Map<String, int> eventBreakdown,
      DateTime? lastEvent,
      String? mostCommonEvent,
      double? engagementScore});
}

/// @nodoc
class __$$UserBehaviorSummaryImplCopyWithImpl<$Res>
    extends _$UserBehaviorSummaryCopyWithImpl<$Res, _$UserBehaviorSummaryImpl>
    implements _$$UserBehaviorSummaryImplCopyWith<$Res> {
  __$$UserBehaviorSummaryImplCopyWithImpl(_$UserBehaviorSummaryImpl _value,
      $Res Function(_$UserBehaviorSummaryImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? userId = null,
    Object? totalEvents = null,
    Object? eventBreakdown = null,
    Object? lastEvent = freezed,
    Object? mostCommonEvent = freezed,
    Object? engagementScore = freezed,
  }) {
    return _then(_$UserBehaviorSummaryImpl(
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      totalEvents: null == totalEvents
          ? _value.totalEvents
          : totalEvents // ignore: cast_nullable_to_non_nullable
              as int,
      eventBreakdown: null == eventBreakdown
          ? _value._eventBreakdown
          : eventBreakdown // ignore: cast_nullable_to_non_nullable
              as Map<String, int>,
      lastEvent: freezed == lastEvent
          ? _value.lastEvent
          : lastEvent // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      mostCommonEvent: freezed == mostCommonEvent
          ? _value.mostCommonEvent
          : mostCommonEvent // ignore: cast_nullable_to_non_nullable
              as String?,
      engagementScore: freezed == engagementScore
          ? _value.engagementScore
          : engagementScore // ignore: cast_nullable_to_non_nullable
              as double?,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$UserBehaviorSummaryImpl implements _UserBehaviorSummary {
  const _$UserBehaviorSummaryImpl(
      {required this.userId,
      required this.totalEvents,
      required final Map<String, int> eventBreakdown,
      required this.lastEvent,
      required this.mostCommonEvent,
      required this.engagementScore})
      : _eventBreakdown = eventBreakdown;

  factory _$UserBehaviorSummaryImpl.fromJson(Map<String, dynamic> json) =>
      _$$UserBehaviorSummaryImplFromJson(json);

  @override
  final int userId;
  @override
  final int totalEvents;
  final Map<String, int> _eventBreakdown;
  @override
  Map<String, int> get eventBreakdown {
    if (_eventBreakdown is EqualUnmodifiableMapView) return _eventBreakdown;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(_eventBreakdown);
  }

  @override
  final DateTime? lastEvent;
  @override
  final String? mostCommonEvent;
  @override
  final double? engagementScore;

  @override
  String toString() {
    return 'UserBehaviorSummary(userId: $userId, totalEvents: $totalEvents, eventBreakdown: $eventBreakdown, lastEvent: $lastEvent, mostCommonEvent: $mostCommonEvent, engagementScore: $engagementScore)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$UserBehaviorSummaryImpl &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.totalEvents, totalEvents) ||
                other.totalEvents == totalEvents) &&
            const DeepCollectionEquality()
                .equals(other._eventBreakdown, _eventBreakdown) &&
            (identical(other.lastEvent, lastEvent) ||
                other.lastEvent == lastEvent) &&
            (identical(other.mostCommonEvent, mostCommonEvent) ||
                other.mostCommonEvent == mostCommonEvent) &&
            (identical(other.engagementScore, engagementScore) ||
                other.engagementScore == engagementScore));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      userId,
      totalEvents,
      const DeepCollectionEquality().hash(_eventBreakdown),
      lastEvent,
      mostCommonEvent,
      engagementScore);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$UserBehaviorSummaryImplCopyWith<_$UserBehaviorSummaryImpl> get copyWith =>
      __$$UserBehaviorSummaryImplCopyWithImpl<_$UserBehaviorSummaryImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$UserBehaviorSummaryImplToJson(
      this,
    );
  }
}

abstract class _UserBehaviorSummary implements UserBehaviorSummary {
  const factory _UserBehaviorSummary(
      {required final int userId,
      required final int totalEvents,
      required final Map<String, int> eventBreakdown,
      required final DateTime? lastEvent,
      required final String? mostCommonEvent,
      required final double? engagementScore}) = _$UserBehaviorSummaryImpl;

  factory _UserBehaviorSummary.fromJson(Map<String, dynamic> json) =
      _$UserBehaviorSummaryImpl.fromJson;

  @override
  int get userId;
  @override
  int get totalEvents;
  @override
  Map<String, int> get eventBreakdown;
  @override
  DateTime? get lastEvent;
  @override
  String? get mostCommonEvent;
  @override
  double? get engagementScore;
  @override
  @JsonKey(ignore: true)
  _$$UserBehaviorSummaryImplCopyWith<_$UserBehaviorSummaryImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

HeatmapData _$HeatmapDataFromJson(Map<String, dynamic> json) {
  return _HeatmapData.fromJson(json);
}

/// @nodoc
mixin _$HeatmapData {
  int get id => throw _privateConstructorUsedError;
  int get contentId => throw _privateConstructorUsedError;
  Map<String, dynamic> get heatmapJson => throw _privateConstructorUsedError;
  Map<String, dynamic> get scrollDepthPercentiles =>
      throw _privateConstructorUsedError;
  Map<String, dynamic> get clickZones => throw _privateConstructorUsedError;
  double get exitRate => throw _privateConstructorUsedError;
  DateTime get lastUpdated => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $HeatmapDataCopyWith<HeatmapData> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $HeatmapDataCopyWith<$Res> {
  factory $HeatmapDataCopyWith(
          HeatmapData value, $Res Function(HeatmapData) then) =
      _$HeatmapDataCopyWithImpl<$Res, HeatmapData>;
  @useResult
  $Res call(
      {int id,
      int contentId,
      Map<String, dynamic> heatmapJson,
      Map<String, dynamic> scrollDepthPercentiles,
      Map<String, dynamic> clickZones,
      double exitRate,
      DateTime lastUpdated});
}

/// @nodoc
class _$HeatmapDataCopyWithImpl<$Res, $Val extends HeatmapData>
    implements $HeatmapDataCopyWith<$Res> {
  _$HeatmapDataCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? contentId = null,
    Object? heatmapJson = null,
    Object? scrollDepthPercentiles = null,
    Object? clickZones = null,
    Object? exitRate = null,
    Object? lastUpdated = null,
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
      heatmapJson: null == heatmapJson
          ? _value.heatmapJson
          : heatmapJson // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      scrollDepthPercentiles: null == scrollDepthPercentiles
          ? _value.scrollDepthPercentiles
          : scrollDepthPercentiles // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      clickZones: null == clickZones
          ? _value.clickZones
          : clickZones // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      exitRate: null == exitRate
          ? _value.exitRate
          : exitRate // ignore: cast_nullable_to_non_nullable
              as double,
      lastUpdated: null == lastUpdated
          ? _value.lastUpdated
          : lastUpdated // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$HeatmapDataImplCopyWith<$Res>
    implements $HeatmapDataCopyWith<$Res> {
  factory _$$HeatmapDataImplCopyWith(
          _$HeatmapDataImpl value, $Res Function(_$HeatmapDataImpl) then) =
      __$$HeatmapDataImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int contentId,
      Map<String, dynamic> heatmapJson,
      Map<String, dynamic> scrollDepthPercentiles,
      Map<String, dynamic> clickZones,
      double exitRate,
      DateTime lastUpdated});
}

/// @nodoc
class __$$HeatmapDataImplCopyWithImpl<$Res>
    extends _$HeatmapDataCopyWithImpl<$Res, _$HeatmapDataImpl>
    implements _$$HeatmapDataImplCopyWith<$Res> {
  __$$HeatmapDataImplCopyWithImpl(
      _$HeatmapDataImpl _value, $Res Function(_$HeatmapDataImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? contentId = null,
    Object? heatmapJson = null,
    Object? scrollDepthPercentiles = null,
    Object? clickZones = null,
    Object? exitRate = null,
    Object? lastUpdated = null,
  }) {
    return _then(_$HeatmapDataImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      contentId: null == contentId
          ? _value.contentId
          : contentId // ignore: cast_nullable_to_non_nullable
              as int,
      heatmapJson: null == heatmapJson
          ? _value._heatmapJson
          : heatmapJson // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      scrollDepthPercentiles: null == scrollDepthPercentiles
          ? _value._scrollDepthPercentiles
          : scrollDepthPercentiles // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      clickZones: null == clickZones
          ? _value._clickZones
          : clickZones // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      exitRate: null == exitRate
          ? _value.exitRate
          : exitRate // ignore: cast_nullable_to_non_nullable
              as double,
      lastUpdated: null == lastUpdated
          ? _value.lastUpdated
          : lastUpdated // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$HeatmapDataImpl implements _HeatmapData {
  const _$HeatmapDataImpl(
      {required this.id,
      required this.contentId,
      required final Map<String, dynamic> heatmapJson,
      required final Map<String, dynamic> scrollDepthPercentiles,
      required final Map<String, dynamic> clickZones,
      required this.exitRate,
      required this.lastUpdated})
      : _heatmapJson = heatmapJson,
        _scrollDepthPercentiles = scrollDepthPercentiles,
        _clickZones = clickZones;

  factory _$HeatmapDataImpl.fromJson(Map<String, dynamic> json) =>
      _$$HeatmapDataImplFromJson(json);

  @override
  final int id;
  @override
  final int contentId;
  final Map<String, dynamic> _heatmapJson;
  @override
  Map<String, dynamic> get heatmapJson {
    if (_heatmapJson is EqualUnmodifiableMapView) return _heatmapJson;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(_heatmapJson);
  }

  final Map<String, dynamic> _scrollDepthPercentiles;
  @override
  Map<String, dynamic> get scrollDepthPercentiles {
    if (_scrollDepthPercentiles is EqualUnmodifiableMapView)
      return _scrollDepthPercentiles;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(_scrollDepthPercentiles);
  }

  final Map<String, dynamic> _clickZones;
  @override
  Map<String, dynamic> get clickZones {
    if (_clickZones is EqualUnmodifiableMapView) return _clickZones;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(_clickZones);
  }

  @override
  final double exitRate;
  @override
  final DateTime lastUpdated;

  @override
  String toString() {
    return 'HeatmapData(id: $id, contentId: $contentId, heatmapJson: $heatmapJson, scrollDepthPercentiles: $scrollDepthPercentiles, clickZones: $clickZones, exitRate: $exitRate, lastUpdated: $lastUpdated)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$HeatmapDataImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.contentId, contentId) ||
                other.contentId == contentId) &&
            const DeepCollectionEquality()
                .equals(other._heatmapJson, _heatmapJson) &&
            const DeepCollectionEquality().equals(
                other._scrollDepthPercentiles, _scrollDepthPercentiles) &&
            const DeepCollectionEquality()
                .equals(other._clickZones, _clickZones) &&
            (identical(other.exitRate, exitRate) ||
                other.exitRate == exitRate) &&
            (identical(other.lastUpdated, lastUpdated) ||
                other.lastUpdated == lastUpdated));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      contentId,
      const DeepCollectionEquality().hash(_heatmapJson),
      const DeepCollectionEquality().hash(_scrollDepthPercentiles),
      const DeepCollectionEquality().hash(_clickZones),
      exitRate,
      lastUpdated);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$HeatmapDataImplCopyWith<_$HeatmapDataImpl> get copyWith =>
      __$$HeatmapDataImplCopyWithImpl<_$HeatmapDataImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$HeatmapDataImplToJson(
      this,
    );
  }
}

abstract class _HeatmapData implements HeatmapData {
  const factory _HeatmapData(
      {required final int id,
      required final int contentId,
      required final Map<String, dynamic> heatmapJson,
      required final Map<String, dynamic> scrollDepthPercentiles,
      required final Map<String, dynamic> clickZones,
      required final double exitRate,
      required final DateTime lastUpdated}) = _$HeatmapDataImpl;

  factory _HeatmapData.fromJson(Map<String, dynamic> json) =
      _$HeatmapDataImpl.fromJson;

  @override
  int get id;
  @override
  int get contentId;
  @override
  Map<String, dynamic> get heatmapJson;
  @override
  Map<String, dynamic> get scrollDepthPercentiles;
  @override
  Map<String, dynamic> get clickZones;
  @override
  double get exitRate;
  @override
  DateTime get lastUpdated;
  @override
  @JsonKey(ignore: true)
  _$$HeatmapDataImplCopyWith<_$HeatmapDataImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

SearchIndexEntry _$SearchIndexEntryFromJson(Map<String, dynamic> json) {
  return _SearchIndexEntry.fromJson(json);
}

/// @nodoc
mixin _$SearchIndexEntry {
  int get id => throw _privateConstructorUsedError;
  int get contentId => throw _privateConstructorUsedError;
  String get title => throw _privateConstructorUsedError;
  String? get summary => throw _privateConstructorUsedError;
  String get status => throw _privateConstructorUsedError;
  DateTime? get indexedAt => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $SearchIndexEntryCopyWith<SearchIndexEntry> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $SearchIndexEntryCopyWith<$Res> {
  factory $SearchIndexEntryCopyWith(
          SearchIndexEntry value, $Res Function(SearchIndexEntry) then) =
      _$SearchIndexEntryCopyWithImpl<$Res, SearchIndexEntry>;
  @useResult
  $Res call(
      {int id,
      int contentId,
      String title,
      String? summary,
      String status,
      DateTime? indexedAt,
      DateTime createdAt});
}

/// @nodoc
class _$SearchIndexEntryCopyWithImpl<$Res, $Val extends SearchIndexEntry>
    implements $SearchIndexEntryCopyWith<$Res> {
  _$SearchIndexEntryCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? contentId = null,
    Object? title = null,
    Object? summary = freezed,
    Object? status = null,
    Object? indexedAt = freezed,
    Object? createdAt = null,
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
      title: null == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String,
      summary: freezed == summary
          ? _value.summary
          : summary // ignore: cast_nullable_to_non_nullable
              as String?,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      indexedAt: freezed == indexedAt
          ? _value.indexedAt
          : indexedAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$SearchIndexEntryImplCopyWith<$Res>
    implements $SearchIndexEntryCopyWith<$Res> {
  factory _$$SearchIndexEntryImplCopyWith(_$SearchIndexEntryImpl value,
          $Res Function(_$SearchIndexEntryImpl) then) =
      __$$SearchIndexEntryImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int contentId,
      String title,
      String? summary,
      String status,
      DateTime? indexedAt,
      DateTime createdAt});
}

/// @nodoc
class __$$SearchIndexEntryImplCopyWithImpl<$Res>
    extends _$SearchIndexEntryCopyWithImpl<$Res, _$SearchIndexEntryImpl>
    implements _$$SearchIndexEntryImplCopyWith<$Res> {
  __$$SearchIndexEntryImplCopyWithImpl(_$SearchIndexEntryImpl _value,
      $Res Function(_$SearchIndexEntryImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? contentId = null,
    Object? title = null,
    Object? summary = freezed,
    Object? status = null,
    Object? indexedAt = freezed,
    Object? createdAt = null,
  }) {
    return _then(_$SearchIndexEntryImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      contentId: null == contentId
          ? _value.contentId
          : contentId // ignore: cast_nullable_to_non_nullable
              as int,
      title: null == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String,
      summary: freezed == summary
          ? _value.summary
          : summary // ignore: cast_nullable_to_non_nullable
              as String?,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      indexedAt: freezed == indexedAt
          ? _value.indexedAt
          : indexedAt // ignore: cast_nullable_to_non_nullable
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
class _$SearchIndexEntryImpl implements _SearchIndexEntry {
  const _$SearchIndexEntryImpl(
      {required this.id,
      required this.contentId,
      required this.title,
      required this.summary,
      required this.status,
      required this.indexedAt,
      required this.createdAt});

  factory _$SearchIndexEntryImpl.fromJson(Map<String, dynamic> json) =>
      _$$SearchIndexEntryImplFromJson(json);

  @override
  final int id;
  @override
  final int contentId;
  @override
  final String title;
  @override
  final String? summary;
  @override
  final String status;
  @override
  final DateTime? indexedAt;
  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'SearchIndexEntry(id: $id, contentId: $contentId, title: $title, summary: $summary, status: $status, indexedAt: $indexedAt, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$SearchIndexEntryImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.contentId, contentId) ||
                other.contentId == contentId) &&
            (identical(other.title, title) || other.title == title) &&
            (identical(other.summary, summary) || other.summary == summary) &&
            (identical(other.status, status) || other.status == status) &&
            (identical(other.indexedAt, indexedAt) ||
                other.indexedAt == indexedAt) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType, id, contentId, title, summary, status, indexedAt, createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$SearchIndexEntryImplCopyWith<_$SearchIndexEntryImpl> get copyWith =>
      __$$SearchIndexEntryImplCopyWithImpl<_$SearchIndexEntryImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$SearchIndexEntryImplToJson(
      this,
    );
  }
}

abstract class _SearchIndexEntry implements SearchIndexEntry {
  const factory _SearchIndexEntry(
      {required final int id,
      required final int contentId,
      required final String title,
      required final String? summary,
      required final String status,
      required final DateTime? indexedAt,
      required final DateTime createdAt}) = _$SearchIndexEntryImpl;

  factory _SearchIndexEntry.fromJson(Map<String, dynamic> json) =
      _$SearchIndexEntryImpl.fromJson;

  @override
  int get id;
  @override
  int get contentId;
  @override
  String get title;
  @override
  String? get summary;
  @override
  String get status;
  @override
  DateTime? get indexedAt;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$SearchIndexEntryImplCopyWith<_$SearchIndexEntryImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

SearchResult _$SearchResultFromJson(Map<String, dynamic> json) {
  return _SearchResult.fromJson(json);
}

/// @nodoc
mixin _$SearchResult {
  int get contentId => throw _privateConstructorUsedError;
  String get title => throw _privateConstructorUsedError;
  String? get summary => throw _privateConstructorUsedError;
  double get relevanceScore => throw _privateConstructorUsedError;
  List<String> get tags => throw _privateConstructorUsedError;
  List<String> get categories => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $SearchResultCopyWith<SearchResult> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $SearchResultCopyWith<$Res> {
  factory $SearchResultCopyWith(
          SearchResult value, $Res Function(SearchResult) then) =
      _$SearchResultCopyWithImpl<$Res, SearchResult>;
  @useResult
  $Res call(
      {int contentId,
      String title,
      String? summary,
      double relevanceScore,
      List<String> tags,
      List<String> categories});
}

/// @nodoc
class _$SearchResultCopyWithImpl<$Res, $Val extends SearchResult>
    implements $SearchResultCopyWith<$Res> {
  _$SearchResultCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? contentId = null,
    Object? title = null,
    Object? summary = freezed,
    Object? relevanceScore = null,
    Object? tags = null,
    Object? categories = null,
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
      summary: freezed == summary
          ? _value.summary
          : summary // ignore: cast_nullable_to_non_nullable
              as String?,
      relevanceScore: null == relevanceScore
          ? _value.relevanceScore
          : relevanceScore // ignore: cast_nullable_to_non_nullable
              as double,
      tags: null == tags
          ? _value.tags
          : tags // ignore: cast_nullable_to_non_nullable
              as List<String>,
      categories: null == categories
          ? _value.categories
          : categories // ignore: cast_nullable_to_non_nullable
              as List<String>,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$SearchResultImplCopyWith<$Res>
    implements $SearchResultCopyWith<$Res> {
  factory _$$SearchResultImplCopyWith(
          _$SearchResultImpl value, $Res Function(_$SearchResultImpl) then) =
      __$$SearchResultImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int contentId,
      String title,
      String? summary,
      double relevanceScore,
      List<String> tags,
      List<String> categories});
}

/// @nodoc
class __$$SearchResultImplCopyWithImpl<$Res>
    extends _$SearchResultCopyWithImpl<$Res, _$SearchResultImpl>
    implements _$$SearchResultImplCopyWith<$Res> {
  __$$SearchResultImplCopyWithImpl(
      _$SearchResultImpl _value, $Res Function(_$SearchResultImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? contentId = null,
    Object? title = null,
    Object? summary = freezed,
    Object? relevanceScore = null,
    Object? tags = null,
    Object? categories = null,
  }) {
    return _then(_$SearchResultImpl(
      contentId: null == contentId
          ? _value.contentId
          : contentId // ignore: cast_nullable_to_non_nullable
              as int,
      title: null == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String,
      summary: freezed == summary
          ? _value.summary
          : summary // ignore: cast_nullable_to_non_nullable
              as String?,
      relevanceScore: null == relevanceScore
          ? _value.relevanceScore
          : relevanceScore // ignore: cast_nullable_to_non_nullable
              as double,
      tags: null == tags
          ? _value._tags
          : tags // ignore: cast_nullable_to_non_nullable
              as List<String>,
      categories: null == categories
          ? _value._categories
          : categories // ignore: cast_nullable_to_non_nullable
              as List<String>,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$SearchResultImpl implements _SearchResult {
  const _$SearchResultImpl(
      {required this.contentId,
      required this.title,
      required this.summary,
      required this.relevanceScore,
      required final List<String> tags,
      required final List<String> categories})
      : _tags = tags,
        _categories = categories;

  factory _$SearchResultImpl.fromJson(Map<String, dynamic> json) =>
      _$$SearchResultImplFromJson(json);

  @override
  final int contentId;
  @override
  final String title;
  @override
  final String? summary;
  @override
  final double relevanceScore;
  final List<String> _tags;
  @override
  List<String> get tags {
    if (_tags is EqualUnmodifiableListView) return _tags;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_tags);
  }

  final List<String> _categories;
  @override
  List<String> get categories {
    if (_categories is EqualUnmodifiableListView) return _categories;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_categories);
  }

  @override
  String toString() {
    return 'SearchResult(contentId: $contentId, title: $title, summary: $summary, relevanceScore: $relevanceScore, tags: $tags, categories: $categories)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$SearchResultImpl &&
            (identical(other.contentId, contentId) ||
                other.contentId == contentId) &&
            (identical(other.title, title) || other.title == title) &&
            (identical(other.summary, summary) || other.summary == summary) &&
            (identical(other.relevanceScore, relevanceScore) ||
                other.relevanceScore == relevanceScore) &&
            const DeepCollectionEquality().equals(other._tags, _tags) &&
            const DeepCollectionEquality()
                .equals(other._categories, _categories));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      contentId,
      title,
      summary,
      relevanceScore,
      const DeepCollectionEquality().hash(_tags),
      const DeepCollectionEquality().hash(_categories));

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$SearchResultImplCopyWith<_$SearchResultImpl> get copyWith =>
      __$$SearchResultImplCopyWithImpl<_$SearchResultImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$SearchResultImplToJson(
      this,
    );
  }
}

abstract class _SearchResult implements SearchResult {
  const factory _SearchResult(
      {required final int contentId,
      required final String title,
      required final String? summary,
      required final double relevanceScore,
      required final List<String> tags,
      required final List<String> categories}) = _$SearchResultImpl;

  factory _SearchResult.fromJson(Map<String, dynamic> json) =
      _$SearchResultImpl.fromJson;

  @override
  int get contentId;
  @override
  String get title;
  @override
  String? get summary;
  @override
  double get relevanceScore;
  @override
  List<String> get tags;
  @override
  List<String> get categories;
  @override
  @JsonKey(ignore: true)
  _$$SearchResultImplCopyWith<_$SearchResultImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

TrendingSearch _$TrendingSearchFromJson(Map<String, dynamic> json) {
  return _TrendingSearch.fromJson(json);
}

/// @nodoc
mixin _$TrendingSearch {
  String get query => throw _privateConstructorUsedError;
  int get count => throw _privateConstructorUsedError;
  int get resultCountAvg => throw _privateConstructorUsedError;
  double get clickThroughRate => throw _privateConstructorUsedError;
  int? get lastSearched => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $TrendingSearchCopyWith<TrendingSearch> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $TrendingSearchCopyWith<$Res> {
  factory $TrendingSearchCopyWith(
          TrendingSearch value, $Res Function(TrendingSearch) then) =
      _$TrendingSearchCopyWithImpl<$Res, TrendingSearch>;
  @useResult
  $Res call(
      {String query,
      int count,
      int resultCountAvg,
      double clickThroughRate,
      int? lastSearched});
}

/// @nodoc
class _$TrendingSearchCopyWithImpl<$Res, $Val extends TrendingSearch>
    implements $TrendingSearchCopyWith<$Res> {
  _$TrendingSearchCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? query = null,
    Object? count = null,
    Object? resultCountAvg = null,
    Object? clickThroughRate = null,
    Object? lastSearched = freezed,
  }) {
    return _then(_value.copyWith(
      query: null == query
          ? _value.query
          : query // ignore: cast_nullable_to_non_nullable
              as String,
      count: null == count
          ? _value.count
          : count // ignore: cast_nullable_to_non_nullable
              as int,
      resultCountAvg: null == resultCountAvg
          ? _value.resultCountAvg
          : resultCountAvg // ignore: cast_nullable_to_non_nullable
              as int,
      clickThroughRate: null == clickThroughRate
          ? _value.clickThroughRate
          : clickThroughRate // ignore: cast_nullable_to_non_nullable
              as double,
      lastSearched: freezed == lastSearched
          ? _value.lastSearched
          : lastSearched // ignore: cast_nullable_to_non_nullable
              as int?,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$TrendingSearchImplCopyWith<$Res>
    implements $TrendingSearchCopyWith<$Res> {
  factory _$$TrendingSearchImplCopyWith(_$TrendingSearchImpl value,
          $Res Function(_$TrendingSearchImpl) then) =
      __$$TrendingSearchImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {String query,
      int count,
      int resultCountAvg,
      double clickThroughRate,
      int? lastSearched});
}

/// @nodoc
class __$$TrendingSearchImplCopyWithImpl<$Res>
    extends _$TrendingSearchCopyWithImpl<$Res, _$TrendingSearchImpl>
    implements _$$TrendingSearchImplCopyWith<$Res> {
  __$$TrendingSearchImplCopyWithImpl(
      _$TrendingSearchImpl _value, $Res Function(_$TrendingSearchImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? query = null,
    Object? count = null,
    Object? resultCountAvg = null,
    Object? clickThroughRate = null,
    Object? lastSearched = freezed,
  }) {
    return _then(_$TrendingSearchImpl(
      query: null == query
          ? _value.query
          : query // ignore: cast_nullable_to_non_nullable
              as String,
      count: null == count
          ? _value.count
          : count // ignore: cast_nullable_to_non_nullable
              as int,
      resultCountAvg: null == resultCountAvg
          ? _value.resultCountAvg
          : resultCountAvg // ignore: cast_nullable_to_non_nullable
              as int,
      clickThroughRate: null == clickThroughRate
          ? _value.clickThroughRate
          : clickThroughRate // ignore: cast_nullable_to_non_nullable
              as double,
      lastSearched: freezed == lastSearched
          ? _value.lastSearched
          : lastSearched // ignore: cast_nullable_to_non_nullable
              as int?,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$TrendingSearchImpl implements _TrendingSearch {
  const _$TrendingSearchImpl(
      {required this.query,
      required this.count,
      required this.resultCountAvg,
      required this.clickThroughRate,
      required this.lastSearched});

  factory _$TrendingSearchImpl.fromJson(Map<String, dynamic> json) =>
      _$$TrendingSearchImplFromJson(json);

  @override
  final String query;
  @override
  final int count;
  @override
  final int resultCountAvg;
  @override
  final double clickThroughRate;
  @override
  final int? lastSearched;

  @override
  String toString() {
    return 'TrendingSearch(query: $query, count: $count, resultCountAvg: $resultCountAvg, clickThroughRate: $clickThroughRate, lastSearched: $lastSearched)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$TrendingSearchImpl &&
            (identical(other.query, query) || other.query == query) &&
            (identical(other.count, count) || other.count == count) &&
            (identical(other.resultCountAvg, resultCountAvg) ||
                other.resultCountAvg == resultCountAvg) &&
            (identical(other.clickThroughRate, clickThroughRate) ||
                other.clickThroughRate == clickThroughRate) &&
            (identical(other.lastSearched, lastSearched) ||
                other.lastSearched == lastSearched));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, query, count, resultCountAvg,
      clickThroughRate, lastSearched);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$TrendingSearchImplCopyWith<_$TrendingSearchImpl> get copyWith =>
      __$$TrendingSearchImplCopyWithImpl<_$TrendingSearchImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$TrendingSearchImplToJson(
      this,
    );
  }
}

abstract class _TrendingSearch implements TrendingSearch {
  const factory _TrendingSearch(
      {required final String query,
      required final int count,
      required final int resultCountAvg,
      required final double clickThroughRate,
      required final int? lastSearched}) = _$TrendingSearchImpl;

  factory _TrendingSearch.fromJson(Map<String, dynamic> json) =
      _$TrendingSearchImpl.fromJson;

  @override
  String get query;
  @override
  int get count;
  @override
  int get resultCountAvg;
  @override
  double get clickThroughRate;
  @override
  int? get lastSearched;
  @override
  @JsonKey(ignore: true)
  _$$TrendingSearchImplCopyWith<_$TrendingSearchImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

CacheEntry _$CacheEntryFromJson(Map<String, dynamic> json) {
  return _CacheEntry.fromJson(json);
}

/// @nodoc
mixin _$CacheEntry {
  int get id => throw _privateConstructorUsedError;
  String get key => throw _privateConstructorUsedError;
  String get value => throw _privateConstructorUsedError;
  String get cacheLevel => throw _privateConstructorUsedError;
  int get ttlSeconds => throw _privateConstructorUsedError;
  int get hits => throw _privateConstructorUsedError;
  DateTime get lastAccessed => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $CacheEntryCopyWith<CacheEntry> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $CacheEntryCopyWith<$Res> {
  factory $CacheEntryCopyWith(
          CacheEntry value, $Res Function(CacheEntry) then) =
      _$CacheEntryCopyWithImpl<$Res, CacheEntry>;
  @useResult
  $Res call(
      {int id,
      String key,
      String value,
      String cacheLevel,
      int ttlSeconds,
      int hits,
      DateTime lastAccessed,
      DateTime createdAt});
}

/// @nodoc
class _$CacheEntryCopyWithImpl<$Res, $Val extends CacheEntry>
    implements $CacheEntryCopyWith<$Res> {
  _$CacheEntryCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? key = null,
    Object? value = null,
    Object? cacheLevel = null,
    Object? ttlSeconds = null,
    Object? hits = null,
    Object? lastAccessed = null,
    Object? createdAt = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      key: null == key
          ? _value.key
          : key // ignore: cast_nullable_to_non_nullable
              as String,
      value: null == value
          ? _value.value
          : value // ignore: cast_nullable_to_non_nullable
              as String,
      cacheLevel: null == cacheLevel
          ? _value.cacheLevel
          : cacheLevel // ignore: cast_nullable_to_non_nullable
              as String,
      ttlSeconds: null == ttlSeconds
          ? _value.ttlSeconds
          : ttlSeconds // ignore: cast_nullable_to_non_nullable
              as int,
      hits: null == hits
          ? _value.hits
          : hits // ignore: cast_nullable_to_non_nullable
              as int,
      lastAccessed: null == lastAccessed
          ? _value.lastAccessed
          : lastAccessed // ignore: cast_nullable_to_non_nullable
              as DateTime,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$CacheEntryImplCopyWith<$Res>
    implements $CacheEntryCopyWith<$Res> {
  factory _$$CacheEntryImplCopyWith(
          _$CacheEntryImpl value, $Res Function(_$CacheEntryImpl) then) =
      __$$CacheEntryImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String key,
      String value,
      String cacheLevel,
      int ttlSeconds,
      int hits,
      DateTime lastAccessed,
      DateTime createdAt});
}

/// @nodoc
class __$$CacheEntryImplCopyWithImpl<$Res>
    extends _$CacheEntryCopyWithImpl<$Res, _$CacheEntryImpl>
    implements _$$CacheEntryImplCopyWith<$Res> {
  __$$CacheEntryImplCopyWithImpl(
      _$CacheEntryImpl _value, $Res Function(_$CacheEntryImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? key = null,
    Object? value = null,
    Object? cacheLevel = null,
    Object? ttlSeconds = null,
    Object? hits = null,
    Object? lastAccessed = null,
    Object? createdAt = null,
  }) {
    return _then(_$CacheEntryImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      key: null == key
          ? _value.key
          : key // ignore: cast_nullable_to_non_nullable
              as String,
      value: null == value
          ? _value.value
          : value // ignore: cast_nullable_to_non_nullable
              as String,
      cacheLevel: null == cacheLevel
          ? _value.cacheLevel
          : cacheLevel // ignore: cast_nullable_to_non_nullable
              as String,
      ttlSeconds: null == ttlSeconds
          ? _value.ttlSeconds
          : ttlSeconds // ignore: cast_nullable_to_non_nullable
              as int,
      hits: null == hits
          ? _value.hits
          : hits // ignore: cast_nullable_to_non_nullable
              as int,
      lastAccessed: null == lastAccessed
          ? _value.lastAccessed
          : lastAccessed // ignore: cast_nullable_to_non_nullable
              as DateTime,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$CacheEntryImpl implements _CacheEntry {
  const _$CacheEntryImpl(
      {required this.id,
      required this.key,
      required this.value,
      required this.cacheLevel,
      required this.ttlSeconds,
      required this.hits,
      required this.lastAccessed,
      required this.createdAt});

  factory _$CacheEntryImpl.fromJson(Map<String, dynamic> json) =>
      _$$CacheEntryImplFromJson(json);

  @override
  final int id;
  @override
  final String key;
  @override
  final String value;
  @override
  final String cacheLevel;
  @override
  final int ttlSeconds;
  @override
  final int hits;
  @override
  final DateTime lastAccessed;
  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'CacheEntry(id: $id, key: $key, value: $value, cacheLevel: $cacheLevel, ttlSeconds: $ttlSeconds, hits: $hits, lastAccessed: $lastAccessed, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$CacheEntryImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.key, key) || other.key == key) &&
            (identical(other.value, value) || other.value == value) &&
            (identical(other.cacheLevel, cacheLevel) ||
                other.cacheLevel == cacheLevel) &&
            (identical(other.ttlSeconds, ttlSeconds) ||
                other.ttlSeconds == ttlSeconds) &&
            (identical(other.hits, hits) || other.hits == hits) &&
            (identical(other.lastAccessed, lastAccessed) ||
                other.lastAccessed == lastAccessed) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, id, key, value, cacheLevel,
      ttlSeconds, hits, lastAccessed, createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$CacheEntryImplCopyWith<_$CacheEntryImpl> get copyWith =>
      __$$CacheEntryImplCopyWithImpl<_$CacheEntryImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$CacheEntryImplToJson(
      this,
    );
  }
}

abstract class _CacheEntry implements CacheEntry {
  const factory _CacheEntry(
      {required final int id,
      required final String key,
      required final String value,
      required final String cacheLevel,
      required final int ttlSeconds,
      required final int hits,
      required final DateTime lastAccessed,
      required final DateTime createdAt}) = _$CacheEntryImpl;

  factory _CacheEntry.fromJson(Map<String, dynamic> json) =
      _$CacheEntryImpl.fromJson;

  @override
  int get id;
  @override
  String get key;
  @override
  String get value;
  @override
  String get cacheLevel;
  @override
  int get ttlSeconds;
  @override
  int get hits;
  @override
  DateTime get lastAccessed;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$CacheEntryImplCopyWith<_$CacheEntryImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

CacheStats _$CacheStatsFromJson(Map<String, dynamic> json) {
  return _CacheStats.fromJson(json);
}

/// @nodoc
mixin _$CacheStats {
  int get totalEntries => throw _privateConstructorUsedError;
  int get hotEntries => throw _privateConstructorUsedError;
  int get warmEntries => throw _privateConstructorUsedError;
  int get coldEntries => throw _privateConstructorUsedError;
  int get totalHits => throw _privateConstructorUsedError;
  double get avgHitsPerEntry => throw _privateConstructorUsedError;
  double get hitRate => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $CacheStatsCopyWith<CacheStats> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $CacheStatsCopyWith<$Res> {
  factory $CacheStatsCopyWith(
          CacheStats value, $Res Function(CacheStats) then) =
      _$CacheStatsCopyWithImpl<$Res, CacheStats>;
  @useResult
  $Res call(
      {int totalEntries,
      int hotEntries,
      int warmEntries,
      int coldEntries,
      int totalHits,
      double avgHitsPerEntry,
      double hitRate});
}

/// @nodoc
class _$CacheStatsCopyWithImpl<$Res, $Val extends CacheStats>
    implements $CacheStatsCopyWith<$Res> {
  _$CacheStatsCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? totalEntries = null,
    Object? hotEntries = null,
    Object? warmEntries = null,
    Object? coldEntries = null,
    Object? totalHits = null,
    Object? avgHitsPerEntry = null,
    Object? hitRate = null,
  }) {
    return _then(_value.copyWith(
      totalEntries: null == totalEntries
          ? _value.totalEntries
          : totalEntries // ignore: cast_nullable_to_non_nullable
              as int,
      hotEntries: null == hotEntries
          ? _value.hotEntries
          : hotEntries // ignore: cast_nullable_to_non_nullable
              as int,
      warmEntries: null == warmEntries
          ? _value.warmEntries
          : warmEntries // ignore: cast_nullable_to_non_nullable
              as int,
      coldEntries: null == coldEntries
          ? _value.coldEntries
          : coldEntries // ignore: cast_nullable_to_non_nullable
              as int,
      totalHits: null == totalHits
          ? _value.totalHits
          : totalHits // ignore: cast_nullable_to_non_nullable
              as int,
      avgHitsPerEntry: null == avgHitsPerEntry
          ? _value.avgHitsPerEntry
          : avgHitsPerEntry // ignore: cast_nullable_to_non_nullable
              as double,
      hitRate: null == hitRate
          ? _value.hitRate
          : hitRate // ignore: cast_nullable_to_non_nullable
              as double,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$CacheStatsImplCopyWith<$Res>
    implements $CacheStatsCopyWith<$Res> {
  factory _$$CacheStatsImplCopyWith(
          _$CacheStatsImpl value, $Res Function(_$CacheStatsImpl) then) =
      __$$CacheStatsImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int totalEntries,
      int hotEntries,
      int warmEntries,
      int coldEntries,
      int totalHits,
      double avgHitsPerEntry,
      double hitRate});
}

/// @nodoc
class __$$CacheStatsImplCopyWithImpl<$Res>
    extends _$CacheStatsCopyWithImpl<$Res, _$CacheStatsImpl>
    implements _$$CacheStatsImplCopyWith<$Res> {
  __$$CacheStatsImplCopyWithImpl(
      _$CacheStatsImpl _value, $Res Function(_$CacheStatsImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? totalEntries = null,
    Object? hotEntries = null,
    Object? warmEntries = null,
    Object? coldEntries = null,
    Object? totalHits = null,
    Object? avgHitsPerEntry = null,
    Object? hitRate = null,
  }) {
    return _then(_$CacheStatsImpl(
      totalEntries: null == totalEntries
          ? _value.totalEntries
          : totalEntries // ignore: cast_nullable_to_non_nullable
              as int,
      hotEntries: null == hotEntries
          ? _value.hotEntries
          : hotEntries // ignore: cast_nullable_to_non_nullable
              as int,
      warmEntries: null == warmEntries
          ? _value.warmEntries
          : warmEntries // ignore: cast_nullable_to_non_nullable
              as int,
      coldEntries: null == coldEntries
          ? _value.coldEntries
          : coldEntries // ignore: cast_nullable_to_non_nullable
              as int,
      totalHits: null == totalHits
          ? _value.totalHits
          : totalHits // ignore: cast_nullable_to_non_nullable
              as int,
      avgHitsPerEntry: null == avgHitsPerEntry
          ? _value.avgHitsPerEntry
          : avgHitsPerEntry // ignore: cast_nullable_to_non_nullable
              as double,
      hitRate: null == hitRate
          ? _value.hitRate
          : hitRate // ignore: cast_nullable_to_non_nullable
              as double,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$CacheStatsImpl implements _CacheStats {
  const _$CacheStatsImpl(
      {required this.totalEntries,
      required this.hotEntries,
      required this.warmEntries,
      required this.coldEntries,
      required this.totalHits,
      required this.avgHitsPerEntry,
      required this.hitRate});

  factory _$CacheStatsImpl.fromJson(Map<String, dynamic> json) =>
      _$$CacheStatsImplFromJson(json);

  @override
  final int totalEntries;
  @override
  final int hotEntries;
  @override
  final int warmEntries;
  @override
  final int coldEntries;
  @override
  final int totalHits;
  @override
  final double avgHitsPerEntry;
  @override
  final double hitRate;

  @override
  String toString() {
    return 'CacheStats(totalEntries: $totalEntries, hotEntries: $hotEntries, warmEntries: $warmEntries, coldEntries: $coldEntries, totalHits: $totalHits, avgHitsPerEntry: $avgHitsPerEntry, hitRate: $hitRate)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$CacheStatsImpl &&
            (identical(other.totalEntries, totalEntries) ||
                other.totalEntries == totalEntries) &&
            (identical(other.hotEntries, hotEntries) ||
                other.hotEntries == hotEntries) &&
            (identical(other.warmEntries, warmEntries) ||
                other.warmEntries == warmEntries) &&
            (identical(other.coldEntries, coldEntries) ||
                other.coldEntries == coldEntries) &&
            (identical(other.totalHits, totalHits) ||
                other.totalHits == totalHits) &&
            (identical(other.avgHitsPerEntry, avgHitsPerEntry) ||
                other.avgHitsPerEntry == avgHitsPerEntry) &&
            (identical(other.hitRate, hitRate) || other.hitRate == hitRate));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, totalEntries, hotEntries,
      warmEntries, coldEntries, totalHits, avgHitsPerEntry, hitRate);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$CacheStatsImplCopyWith<_$CacheStatsImpl> get copyWith =>
      __$$CacheStatsImplCopyWithImpl<_$CacheStatsImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$CacheStatsImplToJson(
      this,
    );
  }
}

abstract class _CacheStats implements CacheStats {
  const factory _CacheStats(
      {required final int totalEntries,
      required final int hotEntries,
      required final int warmEntries,
      required final int coldEntries,
      required final int totalHits,
      required final double avgHitsPerEntry,
      required final double hitRate}) = _$CacheStatsImpl;

  factory _CacheStats.fromJson(Map<String, dynamic> json) =
      _$CacheStatsImpl.fromJson;

  @override
  int get totalEntries;
  @override
  int get hotEntries;
  @override
  int get warmEntries;
  @override
  int get coldEntries;
  @override
  int get totalHits;
  @override
  double get avgHitsPerEntry;
  @override
  double get hitRate;
  @override
  @JsonKey(ignore: true)
  _$$CacheStatsImplCopyWith<_$CacheStatsImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

PerformanceMetric _$PerformanceMetricFromJson(Map<String, dynamic> json) {
  return _PerformanceMetric.fromJson(json);
}

/// @nodoc
mixin _$PerformanceMetric {
  int get id => throw _privateConstructorUsedError;
  String get endpoint => throw _privateConstructorUsedError;
  String get method => throw _privateConstructorUsedError;
  int get responseTimeMs => throw _privateConstructorUsedError;
  int get statusCode => throw _privateConstructorUsedError;
  int get requestSize => throw _privateConstructorUsedError;
  int get responseSize => throw _privateConstructorUsedError;
  DateTime get timestamp => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $PerformanceMetricCopyWith<PerformanceMetric> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $PerformanceMetricCopyWith<$Res> {
  factory $PerformanceMetricCopyWith(
          PerformanceMetric value, $Res Function(PerformanceMetric) then) =
      _$PerformanceMetricCopyWithImpl<$Res, PerformanceMetric>;
  @useResult
  $Res call(
      {int id,
      String endpoint,
      String method,
      int responseTimeMs,
      int statusCode,
      int requestSize,
      int responseSize,
      DateTime timestamp});
}

/// @nodoc
class _$PerformanceMetricCopyWithImpl<$Res, $Val extends PerformanceMetric>
    implements $PerformanceMetricCopyWith<$Res> {
  _$PerformanceMetricCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? endpoint = null,
    Object? method = null,
    Object? responseTimeMs = null,
    Object? statusCode = null,
    Object? requestSize = null,
    Object? responseSize = null,
    Object? timestamp = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      endpoint: null == endpoint
          ? _value.endpoint
          : endpoint // ignore: cast_nullable_to_non_nullable
              as String,
      method: null == method
          ? _value.method
          : method // ignore: cast_nullable_to_non_nullable
              as String,
      responseTimeMs: null == responseTimeMs
          ? _value.responseTimeMs
          : responseTimeMs // ignore: cast_nullable_to_non_nullable
              as int,
      statusCode: null == statusCode
          ? _value.statusCode
          : statusCode // ignore: cast_nullable_to_non_nullable
              as int,
      requestSize: null == requestSize
          ? _value.requestSize
          : requestSize // ignore: cast_nullable_to_non_nullable
              as int,
      responseSize: null == responseSize
          ? _value.responseSize
          : responseSize // ignore: cast_nullable_to_non_nullable
              as int,
      timestamp: null == timestamp
          ? _value.timestamp
          : timestamp // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$PerformanceMetricImplCopyWith<$Res>
    implements $PerformanceMetricCopyWith<$Res> {
  factory _$$PerformanceMetricImplCopyWith(_$PerformanceMetricImpl value,
          $Res Function(_$PerformanceMetricImpl) then) =
      __$$PerformanceMetricImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String endpoint,
      String method,
      int responseTimeMs,
      int statusCode,
      int requestSize,
      int responseSize,
      DateTime timestamp});
}

/// @nodoc
class __$$PerformanceMetricImplCopyWithImpl<$Res>
    extends _$PerformanceMetricCopyWithImpl<$Res, _$PerformanceMetricImpl>
    implements _$$PerformanceMetricImplCopyWith<$Res> {
  __$$PerformanceMetricImplCopyWithImpl(_$PerformanceMetricImpl _value,
      $Res Function(_$PerformanceMetricImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? endpoint = null,
    Object? method = null,
    Object? responseTimeMs = null,
    Object? statusCode = null,
    Object? requestSize = null,
    Object? responseSize = null,
    Object? timestamp = null,
  }) {
    return _then(_$PerformanceMetricImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      endpoint: null == endpoint
          ? _value.endpoint
          : endpoint // ignore: cast_nullable_to_non_nullable
              as String,
      method: null == method
          ? _value.method
          : method // ignore: cast_nullable_to_non_nullable
              as String,
      responseTimeMs: null == responseTimeMs
          ? _value.responseTimeMs
          : responseTimeMs // ignore: cast_nullable_to_non_nullable
              as int,
      statusCode: null == statusCode
          ? _value.statusCode
          : statusCode // ignore: cast_nullable_to_non_nullable
              as int,
      requestSize: null == requestSize
          ? _value.requestSize
          : requestSize // ignore: cast_nullable_to_non_nullable
              as int,
      responseSize: null == responseSize
          ? _value.responseSize
          : responseSize // ignore: cast_nullable_to_non_nullable
              as int,
      timestamp: null == timestamp
          ? _value.timestamp
          : timestamp // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$PerformanceMetricImpl implements _PerformanceMetric {
  const _$PerformanceMetricImpl(
      {required this.id,
      required this.endpoint,
      required this.method,
      required this.responseTimeMs,
      required this.statusCode,
      required this.requestSize,
      required this.responseSize,
      required this.timestamp});

  factory _$PerformanceMetricImpl.fromJson(Map<String, dynamic> json) =>
      _$$PerformanceMetricImplFromJson(json);

  @override
  final int id;
  @override
  final String endpoint;
  @override
  final String method;
  @override
  final int responseTimeMs;
  @override
  final int statusCode;
  @override
  final int requestSize;
  @override
  final int responseSize;
  @override
  final DateTime timestamp;

  @override
  String toString() {
    return 'PerformanceMetric(id: $id, endpoint: $endpoint, method: $method, responseTimeMs: $responseTimeMs, statusCode: $statusCode, requestSize: $requestSize, responseSize: $responseSize, timestamp: $timestamp)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$PerformanceMetricImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.endpoint, endpoint) ||
                other.endpoint == endpoint) &&
            (identical(other.method, method) || other.method == method) &&
            (identical(other.responseTimeMs, responseTimeMs) ||
                other.responseTimeMs == responseTimeMs) &&
            (identical(other.statusCode, statusCode) ||
                other.statusCode == statusCode) &&
            (identical(other.requestSize, requestSize) ||
                other.requestSize == requestSize) &&
            (identical(other.responseSize, responseSize) ||
                other.responseSize == responseSize) &&
            (identical(other.timestamp, timestamp) ||
                other.timestamp == timestamp));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, id, endpoint, method,
      responseTimeMs, statusCode, requestSize, responseSize, timestamp);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$PerformanceMetricImplCopyWith<_$PerformanceMetricImpl> get copyWith =>
      __$$PerformanceMetricImplCopyWithImpl<_$PerformanceMetricImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$PerformanceMetricImplToJson(
      this,
    );
  }
}

abstract class _PerformanceMetric implements PerformanceMetric {
  const factory _PerformanceMetric(
      {required final int id,
      required final String endpoint,
      required final String method,
      required final int responseTimeMs,
      required final int statusCode,
      required final int requestSize,
      required final int responseSize,
      required final DateTime timestamp}) = _$PerformanceMetricImpl;

  factory _PerformanceMetric.fromJson(Map<String, dynamic> json) =
      _$PerformanceMetricImpl.fromJson;

  @override
  int get id;
  @override
  String get endpoint;
  @override
  String get method;
  @override
  int get responseTimeMs;
  @override
  int get statusCode;
  @override
  int get requestSize;
  @override
  int get responseSize;
  @override
  DateTime get timestamp;
  @override
  @JsonKey(ignore: true)
  _$$PerformanceMetricImplCopyWith<_$PerformanceMetricImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

EndpointStats _$EndpointStatsFromJson(Map<String, dynamic> json) {
  return _EndpointStats.fromJson(json);
}

/// @nodoc
mixin _$EndpointStats {
  String get endpoint => throw _privateConstructorUsedError;
  String get method => throw _privateConstructorUsedError;
  int get requestCount => throw _privateConstructorUsedError;
  double get avgResponseTimeMs => throw _privateConstructorUsedError;
  double get p95ResponseTimeMs => throw _privateConstructorUsedError;
  double get p99ResponseTimeMs => throw _privateConstructorUsedError;
  double get errorRate => throw _privateConstructorUsedError;
  Map<String, int> get statusBreakdown => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $EndpointStatsCopyWith<EndpointStats> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $EndpointStatsCopyWith<$Res> {
  factory $EndpointStatsCopyWith(
          EndpointStats value, $Res Function(EndpointStats) then) =
      _$EndpointStatsCopyWithImpl<$Res, EndpointStats>;
  @useResult
  $Res call(
      {String endpoint,
      String method,
      int requestCount,
      double avgResponseTimeMs,
      double p95ResponseTimeMs,
      double p99ResponseTimeMs,
      double errorRate,
      Map<String, int> statusBreakdown});
}

/// @nodoc
class _$EndpointStatsCopyWithImpl<$Res, $Val extends EndpointStats>
    implements $EndpointStatsCopyWith<$Res> {
  _$EndpointStatsCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? endpoint = null,
    Object? method = null,
    Object? requestCount = null,
    Object? avgResponseTimeMs = null,
    Object? p95ResponseTimeMs = null,
    Object? p99ResponseTimeMs = null,
    Object? errorRate = null,
    Object? statusBreakdown = null,
  }) {
    return _then(_value.copyWith(
      endpoint: null == endpoint
          ? _value.endpoint
          : endpoint // ignore: cast_nullable_to_non_nullable
              as String,
      method: null == method
          ? _value.method
          : method // ignore: cast_nullable_to_non_nullable
              as String,
      requestCount: null == requestCount
          ? _value.requestCount
          : requestCount // ignore: cast_nullable_to_non_nullable
              as int,
      avgResponseTimeMs: null == avgResponseTimeMs
          ? _value.avgResponseTimeMs
          : avgResponseTimeMs // ignore: cast_nullable_to_non_nullable
              as double,
      p95ResponseTimeMs: null == p95ResponseTimeMs
          ? _value.p95ResponseTimeMs
          : p95ResponseTimeMs // ignore: cast_nullable_to_non_nullable
              as double,
      p99ResponseTimeMs: null == p99ResponseTimeMs
          ? _value.p99ResponseTimeMs
          : p99ResponseTimeMs // ignore: cast_nullable_to_non_nullable
              as double,
      errorRate: null == errorRate
          ? _value.errorRate
          : errorRate // ignore: cast_nullable_to_non_nullable
              as double,
      statusBreakdown: null == statusBreakdown
          ? _value.statusBreakdown
          : statusBreakdown // ignore: cast_nullable_to_non_nullable
              as Map<String, int>,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$EndpointStatsImplCopyWith<$Res>
    implements $EndpointStatsCopyWith<$Res> {
  factory _$$EndpointStatsImplCopyWith(
          _$EndpointStatsImpl value, $Res Function(_$EndpointStatsImpl) then) =
      __$$EndpointStatsImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {String endpoint,
      String method,
      int requestCount,
      double avgResponseTimeMs,
      double p95ResponseTimeMs,
      double p99ResponseTimeMs,
      double errorRate,
      Map<String, int> statusBreakdown});
}

/// @nodoc
class __$$EndpointStatsImplCopyWithImpl<$Res>
    extends _$EndpointStatsCopyWithImpl<$Res, _$EndpointStatsImpl>
    implements _$$EndpointStatsImplCopyWith<$Res> {
  __$$EndpointStatsImplCopyWithImpl(
      _$EndpointStatsImpl _value, $Res Function(_$EndpointStatsImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? endpoint = null,
    Object? method = null,
    Object? requestCount = null,
    Object? avgResponseTimeMs = null,
    Object? p95ResponseTimeMs = null,
    Object? p99ResponseTimeMs = null,
    Object? errorRate = null,
    Object? statusBreakdown = null,
  }) {
    return _then(_$EndpointStatsImpl(
      endpoint: null == endpoint
          ? _value.endpoint
          : endpoint // ignore: cast_nullable_to_non_nullable
              as String,
      method: null == method
          ? _value.method
          : method // ignore: cast_nullable_to_non_nullable
              as String,
      requestCount: null == requestCount
          ? _value.requestCount
          : requestCount // ignore: cast_nullable_to_non_nullable
              as int,
      avgResponseTimeMs: null == avgResponseTimeMs
          ? _value.avgResponseTimeMs
          : avgResponseTimeMs // ignore: cast_nullable_to_non_nullable
              as double,
      p95ResponseTimeMs: null == p95ResponseTimeMs
          ? _value.p95ResponseTimeMs
          : p95ResponseTimeMs // ignore: cast_nullable_to_non_nullable
              as double,
      p99ResponseTimeMs: null == p99ResponseTimeMs
          ? _value.p99ResponseTimeMs
          : p99ResponseTimeMs // ignore: cast_nullable_to_non_nullable
              as double,
      errorRate: null == errorRate
          ? _value.errorRate
          : errorRate // ignore: cast_nullable_to_non_nullable
              as double,
      statusBreakdown: null == statusBreakdown
          ? _value._statusBreakdown
          : statusBreakdown // ignore: cast_nullable_to_non_nullable
              as Map<String, int>,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$EndpointStatsImpl implements _EndpointStats {
  const _$EndpointStatsImpl(
      {required this.endpoint,
      required this.method,
      required this.requestCount,
      required this.avgResponseTimeMs,
      required this.p95ResponseTimeMs,
      required this.p99ResponseTimeMs,
      required this.errorRate,
      required final Map<String, int> statusBreakdown})
      : _statusBreakdown = statusBreakdown;

  factory _$EndpointStatsImpl.fromJson(Map<String, dynamic> json) =>
      _$$EndpointStatsImplFromJson(json);

  @override
  final String endpoint;
  @override
  final String method;
  @override
  final int requestCount;
  @override
  final double avgResponseTimeMs;
  @override
  final double p95ResponseTimeMs;
  @override
  final double p99ResponseTimeMs;
  @override
  final double errorRate;
  final Map<String, int> _statusBreakdown;
  @override
  Map<String, int> get statusBreakdown {
    if (_statusBreakdown is EqualUnmodifiableMapView) return _statusBreakdown;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(_statusBreakdown);
  }

  @override
  String toString() {
    return 'EndpointStats(endpoint: $endpoint, method: $method, requestCount: $requestCount, avgResponseTimeMs: $avgResponseTimeMs, p95ResponseTimeMs: $p95ResponseTimeMs, p99ResponseTimeMs: $p99ResponseTimeMs, errorRate: $errorRate, statusBreakdown: $statusBreakdown)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$EndpointStatsImpl &&
            (identical(other.endpoint, endpoint) ||
                other.endpoint == endpoint) &&
            (identical(other.method, method) || other.method == method) &&
            (identical(other.requestCount, requestCount) ||
                other.requestCount == requestCount) &&
            (identical(other.avgResponseTimeMs, avgResponseTimeMs) ||
                other.avgResponseTimeMs == avgResponseTimeMs) &&
            (identical(other.p95ResponseTimeMs, p95ResponseTimeMs) ||
                other.p95ResponseTimeMs == p95ResponseTimeMs) &&
            (identical(other.p99ResponseTimeMs, p99ResponseTimeMs) ||
                other.p99ResponseTimeMs == p99ResponseTimeMs) &&
            (identical(other.errorRate, errorRate) ||
                other.errorRate == errorRate) &&
            const DeepCollectionEquality()
                .equals(other._statusBreakdown, _statusBreakdown));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      endpoint,
      method,
      requestCount,
      avgResponseTimeMs,
      p95ResponseTimeMs,
      p99ResponseTimeMs,
      errorRate,
      const DeepCollectionEquality().hash(_statusBreakdown));

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$EndpointStatsImplCopyWith<_$EndpointStatsImpl> get copyWith =>
      __$$EndpointStatsImplCopyWithImpl<_$EndpointStatsImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$EndpointStatsImplToJson(
      this,
    );
  }
}

abstract class _EndpointStats implements EndpointStats {
  const factory _EndpointStats(
      {required final String endpoint,
      required final String method,
      required final int requestCount,
      required final double avgResponseTimeMs,
      required final double p95ResponseTimeMs,
      required final double p99ResponseTimeMs,
      required final double errorRate,
      required final Map<String, int> statusBreakdown}) = _$EndpointStatsImpl;

  factory _EndpointStats.fromJson(Map<String, dynamic> json) =
      _$EndpointStatsImpl.fromJson;

  @override
  String get endpoint;
  @override
  String get method;
  @override
  int get requestCount;
  @override
  double get avgResponseTimeMs;
  @override
  double get p95ResponseTimeMs;
  @override
  double get p99ResponseTimeMs;
  @override
  double get errorRate;
  @override
  Map<String, int> get statusBreakdown;
  @override
  @JsonKey(ignore: true)
  _$$EndpointStatsImplCopyWith<_$EndpointStatsImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

AdminAction _$AdminActionFromJson(Map<String, dynamic> json) {
  return _AdminAction.fromJson(json);
}

/// @nodoc
mixin _$AdminAction {
  int get id => throw _privateConstructorUsedError;
  int get adminId => throw _privateConstructorUsedError;
  String get action => throw _privateConstructorUsedError;
  String get resourceType => throw _privateConstructorUsedError;
  int? get resourceId => throw _privateConstructorUsedError;
  Map<String, dynamic> get changes => throw _privateConstructorUsedError;
  String? get ipAddress => throw _privateConstructorUsedError;
  DateTime get timestamp => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $AdminActionCopyWith<AdminAction> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $AdminActionCopyWith<$Res> {
  factory $AdminActionCopyWith(
          AdminAction value, $Res Function(AdminAction) then) =
      _$AdminActionCopyWithImpl<$Res, AdminAction>;
  @useResult
  $Res call(
      {int id,
      int adminId,
      String action,
      String resourceType,
      int? resourceId,
      Map<String, dynamic> changes,
      String? ipAddress,
      DateTime timestamp});
}

/// @nodoc
class _$AdminActionCopyWithImpl<$Res, $Val extends AdminAction>
    implements $AdminActionCopyWith<$Res> {
  _$AdminActionCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? adminId = null,
    Object? action = null,
    Object? resourceType = null,
    Object? resourceId = freezed,
    Object? changes = null,
    Object? ipAddress = freezed,
    Object? timestamp = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      adminId: null == adminId
          ? _value.adminId
          : adminId // ignore: cast_nullable_to_non_nullable
              as int,
      action: null == action
          ? _value.action
          : action // ignore: cast_nullable_to_non_nullable
              as String,
      resourceType: null == resourceType
          ? _value.resourceType
          : resourceType // ignore: cast_nullable_to_non_nullable
              as String,
      resourceId: freezed == resourceId
          ? _value.resourceId
          : resourceId // ignore: cast_nullable_to_non_nullable
              as int?,
      changes: null == changes
          ? _value.changes
          : changes // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      ipAddress: freezed == ipAddress
          ? _value.ipAddress
          : ipAddress // ignore: cast_nullable_to_non_nullable
              as String?,
      timestamp: null == timestamp
          ? _value.timestamp
          : timestamp // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$AdminActionImplCopyWith<$Res>
    implements $AdminActionCopyWith<$Res> {
  factory _$$AdminActionImplCopyWith(
          _$AdminActionImpl value, $Res Function(_$AdminActionImpl) then) =
      __$$AdminActionImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int adminId,
      String action,
      String resourceType,
      int? resourceId,
      Map<String, dynamic> changes,
      String? ipAddress,
      DateTime timestamp});
}

/// @nodoc
class __$$AdminActionImplCopyWithImpl<$Res>
    extends _$AdminActionCopyWithImpl<$Res, _$AdminActionImpl>
    implements _$$AdminActionImplCopyWith<$Res> {
  __$$AdminActionImplCopyWithImpl(
      _$AdminActionImpl _value, $Res Function(_$AdminActionImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? adminId = null,
    Object? action = null,
    Object? resourceType = null,
    Object? resourceId = freezed,
    Object? changes = null,
    Object? ipAddress = freezed,
    Object? timestamp = null,
  }) {
    return _then(_$AdminActionImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      adminId: null == adminId
          ? _value.adminId
          : adminId // ignore: cast_nullable_to_non_nullable
              as int,
      action: null == action
          ? _value.action
          : action // ignore: cast_nullable_to_non_nullable
              as String,
      resourceType: null == resourceType
          ? _value.resourceType
          : resourceType // ignore: cast_nullable_to_non_nullable
              as String,
      resourceId: freezed == resourceId
          ? _value.resourceId
          : resourceId // ignore: cast_nullable_to_non_nullable
              as int?,
      changes: null == changes
          ? _value._changes
          : changes // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      ipAddress: freezed == ipAddress
          ? _value.ipAddress
          : ipAddress // ignore: cast_nullable_to_non_nullable
              as String?,
      timestamp: null == timestamp
          ? _value.timestamp
          : timestamp // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$AdminActionImpl implements _AdminAction {
  const _$AdminActionImpl(
      {required this.id,
      required this.adminId,
      required this.action,
      required this.resourceType,
      required this.resourceId,
      required final Map<String, dynamic> changes,
      required this.ipAddress,
      required this.timestamp})
      : _changes = changes;

  factory _$AdminActionImpl.fromJson(Map<String, dynamic> json) =>
      _$$AdminActionImplFromJson(json);

  @override
  final int id;
  @override
  final int adminId;
  @override
  final String action;
  @override
  final String resourceType;
  @override
  final int? resourceId;
  final Map<String, dynamic> _changes;
  @override
  Map<String, dynamic> get changes {
    if (_changes is EqualUnmodifiableMapView) return _changes;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(_changes);
  }

  @override
  final String? ipAddress;
  @override
  final DateTime timestamp;

  @override
  String toString() {
    return 'AdminAction(id: $id, adminId: $adminId, action: $action, resourceType: $resourceType, resourceId: $resourceId, changes: $changes, ipAddress: $ipAddress, timestamp: $timestamp)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$AdminActionImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.adminId, adminId) || other.adminId == adminId) &&
            (identical(other.action, action) || other.action == action) &&
            (identical(other.resourceType, resourceType) ||
                other.resourceType == resourceType) &&
            (identical(other.resourceId, resourceId) ||
                other.resourceId == resourceId) &&
            const DeepCollectionEquality().equals(other._changes, _changes) &&
            (identical(other.ipAddress, ipAddress) ||
                other.ipAddress == ipAddress) &&
            (identical(other.timestamp, timestamp) ||
                other.timestamp == timestamp));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      adminId,
      action,
      resourceType,
      resourceId,
      const DeepCollectionEquality().hash(_changes),
      ipAddress,
      timestamp);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$AdminActionImplCopyWith<_$AdminActionImpl> get copyWith =>
      __$$AdminActionImplCopyWithImpl<_$AdminActionImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$AdminActionImplToJson(
      this,
    );
  }
}

abstract class _AdminAction implements AdminAction {
  const factory _AdminAction(
      {required final int id,
      required final int adminId,
      required final String action,
      required final String resourceType,
      required final int? resourceId,
      required final Map<String, dynamic> changes,
      required final String? ipAddress,
      required final DateTime timestamp}) = _$AdminActionImpl;

  factory _AdminAction.fromJson(Map<String, dynamic> json) =
      _$AdminActionImpl.fromJson;

  @override
  int get id;
  @override
  int get adminId;
  @override
  String get action;
  @override
  String get resourceType;
  @override
  int? get resourceId;
  @override
  Map<String, dynamic> get changes;
  @override
  String? get ipAddress;
  @override
  DateTime get timestamp;
  @override
  @JsonKey(ignore: true)
  _$$AdminActionImplCopyWith<_$AdminActionImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

AuditLog _$AuditLogFromJson(Map<String, dynamic> json) {
  return _AuditLog.fromJson(json);
}

/// @nodoc
mixin _$AuditLog {
  int get id => throw _privateConstructorUsedError;
  int get adminId => throw _privateConstructorUsedError;
  String get action => throw _privateConstructorUsedError;
  String get resourceType => throw _privateConstructorUsedError;
  int? get resourceId => throw _privateConstructorUsedError;
  Map<String, dynamic> get changes => throw _privateConstructorUsedError;
  DateTime get timestamp => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $AuditLogCopyWith<AuditLog> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $AuditLogCopyWith<$Res> {
  factory $AuditLogCopyWith(AuditLog value, $Res Function(AuditLog) then) =
      _$AuditLogCopyWithImpl<$Res, AuditLog>;
  @useResult
  $Res call(
      {int id,
      int adminId,
      String action,
      String resourceType,
      int? resourceId,
      Map<String, dynamic> changes,
      DateTime timestamp});
}

/// @nodoc
class _$AuditLogCopyWithImpl<$Res, $Val extends AuditLog>
    implements $AuditLogCopyWith<$Res> {
  _$AuditLogCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? adminId = null,
    Object? action = null,
    Object? resourceType = null,
    Object? resourceId = freezed,
    Object? changes = null,
    Object? timestamp = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      adminId: null == adminId
          ? _value.adminId
          : adminId // ignore: cast_nullable_to_non_nullable
              as int,
      action: null == action
          ? _value.action
          : action // ignore: cast_nullable_to_non_nullable
              as String,
      resourceType: null == resourceType
          ? _value.resourceType
          : resourceType // ignore: cast_nullable_to_non_nullable
              as String,
      resourceId: freezed == resourceId
          ? _value.resourceId
          : resourceId // ignore: cast_nullable_to_non_nullable
              as int?,
      changes: null == changes
          ? _value.changes
          : changes // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      timestamp: null == timestamp
          ? _value.timestamp
          : timestamp // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$AuditLogImplCopyWith<$Res>
    implements $AuditLogCopyWith<$Res> {
  factory _$$AuditLogImplCopyWith(
          _$AuditLogImpl value, $Res Function(_$AuditLogImpl) then) =
      __$$AuditLogImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int adminId,
      String action,
      String resourceType,
      int? resourceId,
      Map<String, dynamic> changes,
      DateTime timestamp});
}

/// @nodoc
class __$$AuditLogImplCopyWithImpl<$Res>
    extends _$AuditLogCopyWithImpl<$Res, _$AuditLogImpl>
    implements _$$AuditLogImplCopyWith<$Res> {
  __$$AuditLogImplCopyWithImpl(
      _$AuditLogImpl _value, $Res Function(_$AuditLogImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? adminId = null,
    Object? action = null,
    Object? resourceType = null,
    Object? resourceId = freezed,
    Object? changes = null,
    Object? timestamp = null,
  }) {
    return _then(_$AuditLogImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      adminId: null == adminId
          ? _value.adminId
          : adminId // ignore: cast_nullable_to_non_nullable
              as int,
      action: null == action
          ? _value.action
          : action // ignore: cast_nullable_to_non_nullable
              as String,
      resourceType: null == resourceType
          ? _value.resourceType
          : resourceType // ignore: cast_nullable_to_non_nullable
              as String,
      resourceId: freezed == resourceId
          ? _value.resourceId
          : resourceId // ignore: cast_nullable_to_non_nullable
              as int?,
      changes: null == changes
          ? _value._changes
          : changes // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      timestamp: null == timestamp
          ? _value.timestamp
          : timestamp // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$AuditLogImpl implements _AuditLog {
  const _$AuditLogImpl(
      {required this.id,
      required this.adminId,
      required this.action,
      required this.resourceType,
      required this.resourceId,
      required final Map<String, dynamic> changes,
      required this.timestamp})
      : _changes = changes;

  factory _$AuditLogImpl.fromJson(Map<String, dynamic> json) =>
      _$$AuditLogImplFromJson(json);

  @override
  final int id;
  @override
  final int adminId;
  @override
  final String action;
  @override
  final String resourceType;
  @override
  final int? resourceId;
  final Map<String, dynamic> _changes;
  @override
  Map<String, dynamic> get changes {
    if (_changes is EqualUnmodifiableMapView) return _changes;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(_changes);
  }

  @override
  final DateTime timestamp;

  @override
  String toString() {
    return 'AuditLog(id: $id, adminId: $adminId, action: $action, resourceType: $resourceType, resourceId: $resourceId, changes: $changes, timestamp: $timestamp)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$AuditLogImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.adminId, adminId) || other.adminId == adminId) &&
            (identical(other.action, action) || other.action == action) &&
            (identical(other.resourceType, resourceType) ||
                other.resourceType == resourceType) &&
            (identical(other.resourceId, resourceId) ||
                other.resourceId == resourceId) &&
            const DeepCollectionEquality().equals(other._changes, _changes) &&
            (identical(other.timestamp, timestamp) ||
                other.timestamp == timestamp));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      adminId,
      action,
      resourceType,
      resourceId,
      const DeepCollectionEquality().hash(_changes),
      timestamp);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$AuditLogImplCopyWith<_$AuditLogImpl> get copyWith =>
      __$$AuditLogImplCopyWithImpl<_$AuditLogImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$AuditLogImplToJson(
      this,
    );
  }
}

abstract class _AuditLog implements AuditLog {
  const factory _AuditLog(
      {required final int id,
      required final int adminId,
      required final String action,
      required final String resourceType,
      required final int? resourceId,
      required final Map<String, dynamic> changes,
      required final DateTime timestamp}) = _$AuditLogImpl;

  factory _AuditLog.fromJson(Map<String, dynamic> json) =
      _$AuditLogImpl.fromJson;

  @override
  int get id;
  @override
  int get adminId;
  @override
  String get action;
  @override
  String get resourceType;
  @override
  int? get resourceId;
  @override
  Map<String, dynamic> get changes;
  @override
  DateTime get timestamp;
  @override
  @JsonKey(ignore: true)
  _$$AuditLogImplCopyWith<_$AuditLogImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

HealthCheckResult _$HealthCheckResultFromJson(Map<String, dynamic> json) {
  return _HealthCheckResult.fromJson(json);
}

/// @nodoc
mixin _$HealthCheckResult {
  String get serviceName => throw _privateConstructorUsedError;
  String get status => throw _privateConstructorUsedError;
  int? get responseTimeMs => throw _privateConstructorUsedError;
  double get uptimePercentage => throw _privateConstructorUsedError;
  int get errorCount => throw _privateConstructorUsedError;
  DateTime get lastCheck => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $HealthCheckResultCopyWith<HealthCheckResult> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $HealthCheckResultCopyWith<$Res> {
  factory $HealthCheckResultCopyWith(
          HealthCheckResult value, $Res Function(HealthCheckResult) then) =
      _$HealthCheckResultCopyWithImpl<$Res, HealthCheckResult>;
  @useResult
  $Res call(
      {String serviceName,
      String status,
      int? responseTimeMs,
      double uptimePercentage,
      int errorCount,
      DateTime lastCheck});
}

/// @nodoc
class _$HealthCheckResultCopyWithImpl<$Res, $Val extends HealthCheckResult>
    implements $HealthCheckResultCopyWith<$Res> {
  _$HealthCheckResultCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? serviceName = null,
    Object? status = null,
    Object? responseTimeMs = freezed,
    Object? uptimePercentage = null,
    Object? errorCount = null,
    Object? lastCheck = null,
  }) {
    return _then(_value.copyWith(
      serviceName: null == serviceName
          ? _value.serviceName
          : serviceName // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      responseTimeMs: freezed == responseTimeMs
          ? _value.responseTimeMs
          : responseTimeMs // ignore: cast_nullable_to_non_nullable
              as int?,
      uptimePercentage: null == uptimePercentage
          ? _value.uptimePercentage
          : uptimePercentage // ignore: cast_nullable_to_non_nullable
              as double,
      errorCount: null == errorCount
          ? _value.errorCount
          : errorCount // ignore: cast_nullable_to_non_nullable
              as int,
      lastCheck: null == lastCheck
          ? _value.lastCheck
          : lastCheck // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$HealthCheckResultImplCopyWith<$Res>
    implements $HealthCheckResultCopyWith<$Res> {
  factory _$$HealthCheckResultImplCopyWith(_$HealthCheckResultImpl value,
          $Res Function(_$HealthCheckResultImpl) then) =
      __$$HealthCheckResultImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {String serviceName,
      String status,
      int? responseTimeMs,
      double uptimePercentage,
      int errorCount,
      DateTime lastCheck});
}

/// @nodoc
class __$$HealthCheckResultImplCopyWithImpl<$Res>
    extends _$HealthCheckResultCopyWithImpl<$Res, _$HealthCheckResultImpl>
    implements _$$HealthCheckResultImplCopyWith<$Res> {
  __$$HealthCheckResultImplCopyWithImpl(_$HealthCheckResultImpl _value,
      $Res Function(_$HealthCheckResultImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? serviceName = null,
    Object? status = null,
    Object? responseTimeMs = freezed,
    Object? uptimePercentage = null,
    Object? errorCount = null,
    Object? lastCheck = null,
  }) {
    return _then(_$HealthCheckResultImpl(
      serviceName: null == serviceName
          ? _value.serviceName
          : serviceName // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      responseTimeMs: freezed == responseTimeMs
          ? _value.responseTimeMs
          : responseTimeMs // ignore: cast_nullable_to_non_nullable
              as int?,
      uptimePercentage: null == uptimePercentage
          ? _value.uptimePercentage
          : uptimePercentage // ignore: cast_nullable_to_non_nullable
              as double,
      errorCount: null == errorCount
          ? _value.errorCount
          : errorCount // ignore: cast_nullable_to_non_nullable
              as int,
      lastCheck: null == lastCheck
          ? _value.lastCheck
          : lastCheck // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$HealthCheckResultImpl implements _HealthCheckResult {
  const _$HealthCheckResultImpl(
      {required this.serviceName,
      required this.status,
      required this.responseTimeMs,
      required this.uptimePercentage,
      required this.errorCount,
      required this.lastCheck});

  factory _$HealthCheckResultImpl.fromJson(Map<String, dynamic> json) =>
      _$$HealthCheckResultImplFromJson(json);

  @override
  final String serviceName;
  @override
  final String status;
  @override
  final int? responseTimeMs;
  @override
  final double uptimePercentage;
  @override
  final int errorCount;
  @override
  final DateTime lastCheck;

  @override
  String toString() {
    return 'HealthCheckResult(serviceName: $serviceName, status: $status, responseTimeMs: $responseTimeMs, uptimePercentage: $uptimePercentage, errorCount: $errorCount, lastCheck: $lastCheck)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$HealthCheckResultImpl &&
            (identical(other.serviceName, serviceName) ||
                other.serviceName == serviceName) &&
            (identical(other.status, status) || other.status == status) &&
            (identical(other.responseTimeMs, responseTimeMs) ||
                other.responseTimeMs == responseTimeMs) &&
            (identical(other.uptimePercentage, uptimePercentage) ||
                other.uptimePercentage == uptimePercentage) &&
            (identical(other.errorCount, errorCount) ||
                other.errorCount == errorCount) &&
            (identical(other.lastCheck, lastCheck) ||
                other.lastCheck == lastCheck));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, serviceName, status,
      responseTimeMs, uptimePercentage, errorCount, lastCheck);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$HealthCheckResultImplCopyWith<_$HealthCheckResultImpl> get copyWith =>
      __$$HealthCheckResultImplCopyWithImpl<_$HealthCheckResultImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$HealthCheckResultImplToJson(
      this,
    );
  }
}

abstract class _HealthCheckResult implements HealthCheckResult {
  const factory _HealthCheckResult(
      {required final String serviceName,
      required final String status,
      required final int? responseTimeMs,
      required final double uptimePercentage,
      required final int errorCount,
      required final DateTime lastCheck}) = _$HealthCheckResultImpl;

  factory _HealthCheckResult.fromJson(Map<String, dynamic> json) =
      _$HealthCheckResultImpl.fromJson;

  @override
  String get serviceName;
  @override
  String get status;
  @override
  int? get responseTimeMs;
  @override
  double get uptimePercentage;
  @override
  int get errorCount;
  @override
  DateTime get lastCheck;
  @override
  @JsonKey(ignore: true)
  _$$HealthCheckResultImplCopyWith<_$HealthCheckResultImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

SystemHealth _$SystemHealthFromJson(Map<String, dynamic> json) {
  return _SystemHealth.fromJson(json);
}

/// @nodoc
mixin _$SystemHealth {
  String get overallStatus => throw _privateConstructorUsedError;
  DateTime get timestamp => throw _privateConstructorUsedError;
  List<HealthCheckResult> get services => throw _privateConstructorUsedError;
  double get totalUptime => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $SystemHealthCopyWith<SystemHealth> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $SystemHealthCopyWith<$Res> {
  factory $SystemHealthCopyWith(
          SystemHealth value, $Res Function(SystemHealth) then) =
      _$SystemHealthCopyWithImpl<$Res, SystemHealth>;
  @useResult
  $Res call(
      {String overallStatus,
      DateTime timestamp,
      List<HealthCheckResult> services,
      double totalUptime});
}

/// @nodoc
class _$SystemHealthCopyWithImpl<$Res, $Val extends SystemHealth>
    implements $SystemHealthCopyWith<$Res> {
  _$SystemHealthCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? overallStatus = null,
    Object? timestamp = null,
    Object? services = null,
    Object? totalUptime = null,
  }) {
    return _then(_value.copyWith(
      overallStatus: null == overallStatus
          ? _value.overallStatus
          : overallStatus // ignore: cast_nullable_to_non_nullable
              as String,
      timestamp: null == timestamp
          ? _value.timestamp
          : timestamp // ignore: cast_nullable_to_non_nullable
              as DateTime,
      services: null == services
          ? _value.services
          : services // ignore: cast_nullable_to_non_nullable
              as List<HealthCheckResult>,
      totalUptime: null == totalUptime
          ? _value.totalUptime
          : totalUptime // ignore: cast_nullable_to_non_nullable
              as double,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$SystemHealthImplCopyWith<$Res>
    implements $SystemHealthCopyWith<$Res> {
  factory _$$SystemHealthImplCopyWith(
          _$SystemHealthImpl value, $Res Function(_$SystemHealthImpl) then) =
      __$$SystemHealthImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {String overallStatus,
      DateTime timestamp,
      List<HealthCheckResult> services,
      double totalUptime});
}

/// @nodoc
class __$$SystemHealthImplCopyWithImpl<$Res>
    extends _$SystemHealthCopyWithImpl<$Res, _$SystemHealthImpl>
    implements _$$SystemHealthImplCopyWith<$Res> {
  __$$SystemHealthImplCopyWithImpl(
      _$SystemHealthImpl _value, $Res Function(_$SystemHealthImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? overallStatus = null,
    Object? timestamp = null,
    Object? services = null,
    Object? totalUptime = null,
  }) {
    return _then(_$SystemHealthImpl(
      overallStatus: null == overallStatus
          ? _value.overallStatus
          : overallStatus // ignore: cast_nullable_to_non_nullable
              as String,
      timestamp: null == timestamp
          ? _value.timestamp
          : timestamp // ignore: cast_nullable_to_non_nullable
              as DateTime,
      services: null == services
          ? _value._services
          : services // ignore: cast_nullable_to_non_nullable
              as List<HealthCheckResult>,
      totalUptime: null == totalUptime
          ? _value.totalUptime
          : totalUptime // ignore: cast_nullable_to_non_nullable
              as double,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$SystemHealthImpl implements _SystemHealth {
  const _$SystemHealthImpl(
      {required this.overallStatus,
      required this.timestamp,
      required final List<HealthCheckResult> services,
      required this.totalUptime})
      : _services = services;

  factory _$SystemHealthImpl.fromJson(Map<String, dynamic> json) =>
      _$$SystemHealthImplFromJson(json);

  @override
  final String overallStatus;
  @override
  final DateTime timestamp;
  final List<HealthCheckResult> _services;
  @override
  List<HealthCheckResult> get services {
    if (_services is EqualUnmodifiableListView) return _services;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_services);
  }

  @override
  final double totalUptime;

  @override
  String toString() {
    return 'SystemHealth(overallStatus: $overallStatus, timestamp: $timestamp, services: $services, totalUptime: $totalUptime)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$SystemHealthImpl &&
            (identical(other.overallStatus, overallStatus) ||
                other.overallStatus == overallStatus) &&
            (identical(other.timestamp, timestamp) ||
                other.timestamp == timestamp) &&
            const DeepCollectionEquality().equals(other._services, _services) &&
            (identical(other.totalUptime, totalUptime) ||
                other.totalUptime == totalUptime));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, overallStatus, timestamp,
      const DeepCollectionEquality().hash(_services), totalUptime);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$SystemHealthImplCopyWith<_$SystemHealthImpl> get copyWith =>
      __$$SystemHealthImplCopyWithImpl<_$SystemHealthImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$SystemHealthImplToJson(
      this,
    );
  }
}

abstract class _SystemHealth implements SystemHealth {
  const factory _SystemHealth(
      {required final String overallStatus,
      required final DateTime timestamp,
      required final List<HealthCheckResult> services,
      required final double totalUptime}) = _$SystemHealthImpl;

  factory _SystemHealth.fromJson(Map<String, dynamic> json) =
      _$SystemHealthImpl.fromJson;

  @override
  String get overallStatus;
  @override
  DateTime get timestamp;
  @override
  List<HealthCheckResult> get services;
  @override
  double get totalUptime;
  @override
  @JsonKey(ignore: true)
  _$$SystemHealthImplCopyWith<_$SystemHealthImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

ConfigurationSetting _$ConfigurationSettingFromJson(Map<String, dynamic> json) {
  return _ConfigurationSetting.fromJson(json);
}

/// @nodoc
mixin _$ConfigurationSetting {
  int get id => throw _privateConstructorUsedError;
  String get key => throw _privateConstructorUsedError;
  String get value => throw _privateConstructorUsedError;
  String get settingType => throw _privateConstructorUsedError;
  String? get description => throw _privateConstructorUsedError;
  DateTime get updatedAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $ConfigurationSettingCopyWith<ConfigurationSetting> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $ConfigurationSettingCopyWith<$Res> {
  factory $ConfigurationSettingCopyWith(ConfigurationSetting value,
          $Res Function(ConfigurationSetting) then) =
      _$ConfigurationSettingCopyWithImpl<$Res, ConfigurationSetting>;
  @useResult
  $Res call(
      {int id,
      String key,
      String value,
      String settingType,
      String? description,
      DateTime updatedAt});
}

/// @nodoc
class _$ConfigurationSettingCopyWithImpl<$Res,
        $Val extends ConfigurationSetting>
    implements $ConfigurationSettingCopyWith<$Res> {
  _$ConfigurationSettingCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? key = null,
    Object? value = null,
    Object? settingType = null,
    Object? description = freezed,
    Object? updatedAt = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      key: null == key
          ? _value.key
          : key // ignore: cast_nullable_to_non_nullable
              as String,
      value: null == value
          ? _value.value
          : value // ignore: cast_nullable_to_non_nullable
              as String,
      settingType: null == settingType
          ? _value.settingType
          : settingType // ignore: cast_nullable_to_non_nullable
              as String,
      description: freezed == description
          ? _value.description
          : description // ignore: cast_nullable_to_non_nullable
              as String?,
      updatedAt: null == updatedAt
          ? _value.updatedAt
          : updatedAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$ConfigurationSettingImplCopyWith<$Res>
    implements $ConfigurationSettingCopyWith<$Res> {
  factory _$$ConfigurationSettingImplCopyWith(_$ConfigurationSettingImpl value,
          $Res Function(_$ConfigurationSettingImpl) then) =
      __$$ConfigurationSettingImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String key,
      String value,
      String settingType,
      String? description,
      DateTime updatedAt});
}

/// @nodoc
class __$$ConfigurationSettingImplCopyWithImpl<$Res>
    extends _$ConfigurationSettingCopyWithImpl<$Res, _$ConfigurationSettingImpl>
    implements _$$ConfigurationSettingImplCopyWith<$Res> {
  __$$ConfigurationSettingImplCopyWithImpl(_$ConfigurationSettingImpl _value,
      $Res Function(_$ConfigurationSettingImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? key = null,
    Object? value = null,
    Object? settingType = null,
    Object? description = freezed,
    Object? updatedAt = null,
  }) {
    return _then(_$ConfigurationSettingImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      key: null == key
          ? _value.key
          : key // ignore: cast_nullable_to_non_nullable
              as String,
      value: null == value
          ? _value.value
          : value // ignore: cast_nullable_to_non_nullable
              as String,
      settingType: null == settingType
          ? _value.settingType
          : settingType // ignore: cast_nullable_to_non_nullable
              as String,
      description: freezed == description
          ? _value.description
          : description // ignore: cast_nullable_to_non_nullable
              as String?,
      updatedAt: null == updatedAt
          ? _value.updatedAt
          : updatedAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$ConfigurationSettingImpl implements _ConfigurationSetting {
  const _$ConfigurationSettingImpl(
      {required this.id,
      required this.key,
      required this.value,
      required this.settingType,
      required this.description,
      required this.updatedAt});

  factory _$ConfigurationSettingImpl.fromJson(Map<String, dynamic> json) =>
      _$$ConfigurationSettingImplFromJson(json);

  @override
  final int id;
  @override
  final String key;
  @override
  final String value;
  @override
  final String settingType;
  @override
  final String? description;
  @override
  final DateTime updatedAt;

  @override
  String toString() {
    return 'ConfigurationSetting(id: $id, key: $key, value: $value, settingType: $settingType, description: $description, updatedAt: $updatedAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$ConfigurationSettingImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.key, key) || other.key == key) &&
            (identical(other.value, value) || other.value == value) &&
            (identical(other.settingType, settingType) ||
                other.settingType == settingType) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.updatedAt, updatedAt) ||
                other.updatedAt == updatedAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType, id, key, value, settingType, description, updatedAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$ConfigurationSettingImplCopyWith<_$ConfigurationSettingImpl>
      get copyWith =>
          __$$ConfigurationSettingImplCopyWithImpl<_$ConfigurationSettingImpl>(
              this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$ConfigurationSettingImplToJson(
      this,
    );
  }
}

abstract class _ConfigurationSetting implements ConfigurationSetting {
  const factory _ConfigurationSetting(
      {required final int id,
      required final String key,
      required final String value,
      required final String settingType,
      required final String? description,
      required final DateTime updatedAt}) = _$ConfigurationSettingImpl;

  factory _ConfigurationSetting.fromJson(Map<String, dynamic> json) =
      _$ConfigurationSettingImpl.fromJson;

  @override
  int get id;
  @override
  String get key;
  @override
  String get value;
  @override
  String get settingType;
  @override
  String? get description;
  @override
  DateTime get updatedAt;
  @override
  @JsonKey(ignore: true)
  _$$ConfigurationSettingImplCopyWith<_$ConfigurationSettingImpl>
      get copyWith => throw _privateConstructorUsedError;
}

FeatureFlag _$FeatureFlagFromJson(Map<String, dynamic> json) {
  return _FeatureFlag.fromJson(json);
}

/// @nodoc
mixin _$FeatureFlag {
  int get id => throw _privateConstructorUsedError;
  String get name => throw _privateConstructorUsedError;
  String? get description => throw _privateConstructorUsedError;
  bool get enabled => throw _privateConstructorUsedError;
  int get rolloutPercentage => throw _privateConstructorUsedError;
  List<String> get targetSegments => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;
  DateTime get updatedAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $FeatureFlagCopyWith<FeatureFlag> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $FeatureFlagCopyWith<$Res> {
  factory $FeatureFlagCopyWith(
          FeatureFlag value, $Res Function(FeatureFlag) then) =
      _$FeatureFlagCopyWithImpl<$Res, FeatureFlag>;
  @useResult
  $Res call(
      {int id,
      String name,
      String? description,
      bool enabled,
      int rolloutPercentage,
      List<String> targetSegments,
      DateTime createdAt,
      DateTime updatedAt});
}

/// @nodoc
class _$FeatureFlagCopyWithImpl<$Res, $Val extends FeatureFlag>
    implements $FeatureFlagCopyWith<$Res> {
  _$FeatureFlagCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? description = freezed,
    Object? enabled = null,
    Object? rolloutPercentage = null,
    Object? targetSegments = null,
    Object? createdAt = null,
    Object? updatedAt = null,
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
      description: freezed == description
          ? _value.description
          : description // ignore: cast_nullable_to_non_nullable
              as String?,
      enabled: null == enabled
          ? _value.enabled
          : enabled // ignore: cast_nullable_to_non_nullable
              as bool,
      rolloutPercentage: null == rolloutPercentage
          ? _value.rolloutPercentage
          : rolloutPercentage // ignore: cast_nullable_to_non_nullable
              as int,
      targetSegments: null == targetSegments
          ? _value.targetSegments
          : targetSegments // ignore: cast_nullable_to_non_nullable
              as List<String>,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
      updatedAt: null == updatedAt
          ? _value.updatedAt
          : updatedAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$FeatureFlagImplCopyWith<$Res>
    implements $FeatureFlagCopyWith<$Res> {
  factory _$$FeatureFlagImplCopyWith(
          _$FeatureFlagImpl value, $Res Function(_$FeatureFlagImpl) then) =
      __$$FeatureFlagImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String name,
      String? description,
      bool enabled,
      int rolloutPercentage,
      List<String> targetSegments,
      DateTime createdAt,
      DateTime updatedAt});
}

/// @nodoc
class __$$FeatureFlagImplCopyWithImpl<$Res>
    extends _$FeatureFlagCopyWithImpl<$Res, _$FeatureFlagImpl>
    implements _$$FeatureFlagImplCopyWith<$Res> {
  __$$FeatureFlagImplCopyWithImpl(
      _$FeatureFlagImpl _value, $Res Function(_$FeatureFlagImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? description = freezed,
    Object? enabled = null,
    Object? rolloutPercentage = null,
    Object? targetSegments = null,
    Object? createdAt = null,
    Object? updatedAt = null,
  }) {
    return _then(_$FeatureFlagImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      name: null == name
          ? _value.name
          : name // ignore: cast_nullable_to_non_nullable
              as String,
      description: freezed == description
          ? _value.description
          : description // ignore: cast_nullable_to_non_nullable
              as String?,
      enabled: null == enabled
          ? _value.enabled
          : enabled // ignore: cast_nullable_to_non_nullable
              as bool,
      rolloutPercentage: null == rolloutPercentage
          ? _value.rolloutPercentage
          : rolloutPercentage // ignore: cast_nullable_to_non_nullable
              as int,
      targetSegments: null == targetSegments
          ? _value._targetSegments
          : targetSegments // ignore: cast_nullable_to_non_nullable
              as List<String>,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
      updatedAt: null == updatedAt
          ? _value.updatedAt
          : updatedAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$FeatureFlagImpl implements _FeatureFlag {
  const _$FeatureFlagImpl(
      {required this.id,
      required this.name,
      required this.description,
      required this.enabled,
      required this.rolloutPercentage,
      required final List<String> targetSegments,
      required this.createdAt,
      required this.updatedAt})
      : _targetSegments = targetSegments;

  factory _$FeatureFlagImpl.fromJson(Map<String, dynamic> json) =>
      _$$FeatureFlagImplFromJson(json);

  @override
  final int id;
  @override
  final String name;
  @override
  final String? description;
  @override
  final bool enabled;
  @override
  final int rolloutPercentage;
  final List<String> _targetSegments;
  @override
  List<String> get targetSegments {
    if (_targetSegments is EqualUnmodifiableListView) return _targetSegments;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_targetSegments);
  }

  @override
  final DateTime createdAt;
  @override
  final DateTime updatedAt;

  @override
  String toString() {
    return 'FeatureFlag(id: $id, name: $name, description: $description, enabled: $enabled, rolloutPercentage: $rolloutPercentage, targetSegments: $targetSegments, createdAt: $createdAt, updatedAt: $updatedAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$FeatureFlagImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.enabled, enabled) || other.enabled == enabled) &&
            (identical(other.rolloutPercentage, rolloutPercentage) ||
                other.rolloutPercentage == rolloutPercentage) &&
            const DeepCollectionEquality()
                .equals(other._targetSegments, _targetSegments) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt) &&
            (identical(other.updatedAt, updatedAt) ||
                other.updatedAt == updatedAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      name,
      description,
      enabled,
      rolloutPercentage,
      const DeepCollectionEquality().hash(_targetSegments),
      createdAt,
      updatedAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$FeatureFlagImplCopyWith<_$FeatureFlagImpl> get copyWith =>
      __$$FeatureFlagImplCopyWithImpl<_$FeatureFlagImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$FeatureFlagImplToJson(
      this,
    );
  }
}

abstract class _FeatureFlag implements FeatureFlag {
  const factory _FeatureFlag(
      {required final int id,
      required final String name,
      required final String? description,
      required final bool enabled,
      required final int rolloutPercentage,
      required final List<String> targetSegments,
      required final DateTime createdAt,
      required final DateTime updatedAt}) = _$FeatureFlagImpl;

  factory _FeatureFlag.fromJson(Map<String, dynamic> json) =
      _$FeatureFlagImpl.fromJson;

  @override
  int get id;
  @override
  String get name;
  @override
  String? get description;
  @override
  bool get enabled;
  @override
  int get rolloutPercentage;
  @override
  List<String> get targetSegments;
  @override
  DateTime get createdAt;
  @override
  DateTime get updatedAt;
  @override
  @JsonKey(ignore: true)
  _$$FeatureFlagImplCopyWith<_$FeatureFlagImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

PerformanceSummary _$PerformanceSummaryFromJson(Map<String, dynamic> json) {
  return _PerformanceSummary.fromJson(json);
}

/// @nodoc
mixin _$PerformanceSummary {
  double get avgResponseTimeMs => throw _privateConstructorUsedError;
  double get p95ResponseTimeMs => throw _privateConstructorUsedError;
  double get p99ResponseTimeMs => throw _privateConstructorUsedError;
  int get totalRequests => throw _privateConstructorUsedError;
  double get errorRate => throw _privateConstructorUsedError;
  int get uptime => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $PerformanceSummaryCopyWith<PerformanceSummary> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $PerformanceSummaryCopyWith<$Res> {
  factory $PerformanceSummaryCopyWith(
          PerformanceSummary value, $Res Function(PerformanceSummary) then) =
      _$PerformanceSummaryCopyWithImpl<$Res, PerformanceSummary>;
  @useResult
  $Res call(
      {double avgResponseTimeMs,
      double p95ResponseTimeMs,
      double p99ResponseTimeMs,
      int totalRequests,
      double errorRate,
      int uptime});
}

/// @nodoc
class _$PerformanceSummaryCopyWithImpl<$Res, $Val extends PerformanceSummary>
    implements $PerformanceSummaryCopyWith<$Res> {
  _$PerformanceSummaryCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? avgResponseTimeMs = null,
    Object? p95ResponseTimeMs = null,
    Object? p99ResponseTimeMs = null,
    Object? totalRequests = null,
    Object? errorRate = null,
    Object? uptime = null,
  }) {
    return _then(_value.copyWith(
      avgResponseTimeMs: null == avgResponseTimeMs
          ? _value.avgResponseTimeMs
          : avgResponseTimeMs // ignore: cast_nullable_to_non_nullable
              as double,
      p95ResponseTimeMs: null == p95ResponseTimeMs
          ? _value.p95ResponseTimeMs
          : p95ResponseTimeMs // ignore: cast_nullable_to_non_nullable
              as double,
      p99ResponseTimeMs: null == p99ResponseTimeMs
          ? _value.p99ResponseTimeMs
          : p99ResponseTimeMs // ignore: cast_nullable_to_non_nullable
              as double,
      totalRequests: null == totalRequests
          ? _value.totalRequests
          : totalRequests // ignore: cast_nullable_to_non_nullable
              as int,
      errorRate: null == errorRate
          ? _value.errorRate
          : errorRate // ignore: cast_nullable_to_non_nullable
              as double,
      uptime: null == uptime
          ? _value.uptime
          : uptime // ignore: cast_nullable_to_non_nullable
              as int,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$PerformanceSummaryImplCopyWith<$Res>
    implements $PerformanceSummaryCopyWith<$Res> {
  factory _$$PerformanceSummaryImplCopyWith(_$PerformanceSummaryImpl value,
          $Res Function(_$PerformanceSummaryImpl) then) =
      __$$PerformanceSummaryImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {double avgResponseTimeMs,
      double p95ResponseTimeMs,
      double p99ResponseTimeMs,
      int totalRequests,
      double errorRate,
      int uptime});
}

/// @nodoc
class __$$PerformanceSummaryImplCopyWithImpl<$Res>
    extends _$PerformanceSummaryCopyWithImpl<$Res, _$PerformanceSummaryImpl>
    implements _$$PerformanceSummaryImplCopyWith<$Res> {
  __$$PerformanceSummaryImplCopyWithImpl(_$PerformanceSummaryImpl _value,
      $Res Function(_$PerformanceSummaryImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? avgResponseTimeMs = null,
    Object? p95ResponseTimeMs = null,
    Object? p99ResponseTimeMs = null,
    Object? totalRequests = null,
    Object? errorRate = null,
    Object? uptime = null,
  }) {
    return _then(_$PerformanceSummaryImpl(
      avgResponseTimeMs: null == avgResponseTimeMs
          ? _value.avgResponseTimeMs
          : avgResponseTimeMs // ignore: cast_nullable_to_non_nullable
              as double,
      p95ResponseTimeMs: null == p95ResponseTimeMs
          ? _value.p95ResponseTimeMs
          : p95ResponseTimeMs // ignore: cast_nullable_to_non_nullable
              as double,
      p99ResponseTimeMs: null == p99ResponseTimeMs
          ? _value.p99ResponseTimeMs
          : p99ResponseTimeMs // ignore: cast_nullable_to_non_nullable
              as double,
      totalRequests: null == totalRequests
          ? _value.totalRequests
          : totalRequests // ignore: cast_nullable_to_non_nullable
              as int,
      errorRate: null == errorRate
          ? _value.errorRate
          : errorRate // ignore: cast_nullable_to_non_nullable
              as double,
      uptime: null == uptime
          ? _value.uptime
          : uptime // ignore: cast_nullable_to_non_nullable
              as int,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$PerformanceSummaryImpl implements _PerformanceSummary {
  const _$PerformanceSummaryImpl(
      {required this.avgResponseTimeMs,
      required this.p95ResponseTimeMs,
      required this.p99ResponseTimeMs,
      required this.totalRequests,
      required this.errorRate,
      required this.uptime});

  factory _$PerformanceSummaryImpl.fromJson(Map<String, dynamic> json) =>
      _$$PerformanceSummaryImplFromJson(json);

  @override
  final double avgResponseTimeMs;
  @override
  final double p95ResponseTimeMs;
  @override
  final double p99ResponseTimeMs;
  @override
  final int totalRequests;
  @override
  final double errorRate;
  @override
  final int uptime;

  @override
  String toString() {
    return 'PerformanceSummary(avgResponseTimeMs: $avgResponseTimeMs, p95ResponseTimeMs: $p95ResponseTimeMs, p99ResponseTimeMs: $p99ResponseTimeMs, totalRequests: $totalRequests, errorRate: $errorRate, uptime: $uptime)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$PerformanceSummaryImpl &&
            (identical(other.avgResponseTimeMs, avgResponseTimeMs) ||
                other.avgResponseTimeMs == avgResponseTimeMs) &&
            (identical(other.p95ResponseTimeMs, p95ResponseTimeMs) ||
                other.p95ResponseTimeMs == p95ResponseTimeMs) &&
            (identical(other.p99ResponseTimeMs, p99ResponseTimeMs) ||
                other.p99ResponseTimeMs == p99ResponseTimeMs) &&
            (identical(other.totalRequests, totalRequests) ||
                other.totalRequests == totalRequests) &&
            (identical(other.errorRate, errorRate) ||
                other.errorRate == errorRate) &&
            (identical(other.uptime, uptime) || other.uptime == uptime));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, avgResponseTimeMs,
      p95ResponseTimeMs, p99ResponseTimeMs, totalRequests, errorRate, uptime);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$PerformanceSummaryImplCopyWith<_$PerformanceSummaryImpl> get copyWith =>
      __$$PerformanceSummaryImplCopyWithImpl<_$PerformanceSummaryImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$PerformanceSummaryImplToJson(
      this,
    );
  }
}

abstract class _PerformanceSummary implements PerformanceSummary {
  const factory _PerformanceSummary(
      {required final double avgResponseTimeMs,
      required final double p95ResponseTimeMs,
      required final double p99ResponseTimeMs,
      required final int totalRequests,
      required final double errorRate,
      required final int uptime}) = _$PerformanceSummaryImpl;

  factory _PerformanceSummary.fromJson(Map<String, dynamic> json) =
      _$PerformanceSummaryImpl.fromJson;

  @override
  double get avgResponseTimeMs;
  @override
  double get p95ResponseTimeMs;
  @override
  double get p99ResponseTimeMs;
  @override
  int get totalRequests;
  @override
  double get errorRate;
  @override
  int get uptime;
  @override
  @JsonKey(ignore: true)
  _$$PerformanceSummaryImplCopyWith<_$PerformanceSummaryImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

SearchQuery _$SearchQueryFromJson(Map<String, dynamic> json) {
  return _SearchQuery.fromJson(json);
}

/// @nodoc
mixin _$SearchQuery {
  int get id => throw _privateConstructorUsedError;
  int? get userId => throw _privateConstructorUsedError;
  String get query => throw _privateConstructorUsedError;
  int get resultCount => throw _privateConstructorUsedError;
  int? get clickedResult => throw _privateConstructorUsedError;
  int get searchTimeMs => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $SearchQueryCopyWith<SearchQuery> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $SearchQueryCopyWith<$Res> {
  factory $SearchQueryCopyWith(
          SearchQuery value, $Res Function(SearchQuery) then) =
      _$SearchQueryCopyWithImpl<$Res, SearchQuery>;
  @useResult
  $Res call(
      {int id,
      int? userId,
      String query,
      int resultCount,
      int? clickedResult,
      int searchTimeMs,
      DateTime createdAt});
}

/// @nodoc
class _$SearchQueryCopyWithImpl<$Res, $Val extends SearchQuery>
    implements $SearchQueryCopyWith<$Res> {
  _$SearchQueryCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = freezed,
    Object? query = null,
    Object? resultCount = null,
    Object? clickedResult = freezed,
    Object? searchTimeMs = null,
    Object? createdAt = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: freezed == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int?,
      query: null == query
          ? _value.query
          : query // ignore: cast_nullable_to_non_nullable
              as String,
      resultCount: null == resultCount
          ? _value.resultCount
          : resultCount // ignore: cast_nullable_to_non_nullable
              as int,
      clickedResult: freezed == clickedResult
          ? _value.clickedResult
          : clickedResult // ignore: cast_nullable_to_non_nullable
              as int?,
      searchTimeMs: null == searchTimeMs
          ? _value.searchTimeMs
          : searchTimeMs // ignore: cast_nullable_to_non_nullable
              as int,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$SearchQueryImplCopyWith<$Res>
    implements $SearchQueryCopyWith<$Res> {
  factory _$$SearchQueryImplCopyWith(
          _$SearchQueryImpl value, $Res Function(_$SearchQueryImpl) then) =
      __$$SearchQueryImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int? userId,
      String query,
      int resultCount,
      int? clickedResult,
      int searchTimeMs,
      DateTime createdAt});
}

/// @nodoc
class __$$SearchQueryImplCopyWithImpl<$Res>
    extends _$SearchQueryCopyWithImpl<$Res, _$SearchQueryImpl>
    implements _$$SearchQueryImplCopyWith<$Res> {
  __$$SearchQueryImplCopyWithImpl(
      _$SearchQueryImpl _value, $Res Function(_$SearchQueryImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = freezed,
    Object? query = null,
    Object? resultCount = null,
    Object? clickedResult = freezed,
    Object? searchTimeMs = null,
    Object? createdAt = null,
  }) {
    return _then(_$SearchQueryImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: freezed == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int?,
      query: null == query
          ? _value.query
          : query // ignore: cast_nullable_to_non_nullable
              as String,
      resultCount: null == resultCount
          ? _value.resultCount
          : resultCount // ignore: cast_nullable_to_non_nullable
              as int,
      clickedResult: freezed == clickedResult
          ? _value.clickedResult
          : clickedResult // ignore: cast_nullable_to_non_nullable
              as int?,
      searchTimeMs: null == searchTimeMs
          ? _value.searchTimeMs
          : searchTimeMs // ignore: cast_nullable_to_non_nullable
              as int,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$SearchQueryImpl implements _SearchQuery {
  const _$SearchQueryImpl(
      {required this.id,
      required this.userId,
      required this.query,
      required this.resultCount,
      required this.clickedResult,
      required this.searchTimeMs,
      required this.createdAt});

  factory _$SearchQueryImpl.fromJson(Map<String, dynamic> json) =>
      _$$SearchQueryImplFromJson(json);

  @override
  final int id;
  @override
  final int? userId;
  @override
  final String query;
  @override
  final int resultCount;
  @override
  final int? clickedResult;
  @override
  final int searchTimeMs;
  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'SearchQuery(id: $id, userId: $userId, query: $query, resultCount: $resultCount, clickedResult: $clickedResult, searchTimeMs: $searchTimeMs, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$SearchQueryImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.query, query) || other.query == query) &&
            (identical(other.resultCount, resultCount) ||
                other.resultCount == resultCount) &&
            (identical(other.clickedResult, clickedResult) ||
                other.clickedResult == clickedResult) &&
            (identical(other.searchTimeMs, searchTimeMs) ||
                other.searchTimeMs == searchTimeMs) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, id, userId, query, resultCount,
      clickedResult, searchTimeMs, createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$SearchQueryImplCopyWith<_$SearchQueryImpl> get copyWith =>
      __$$SearchQueryImplCopyWithImpl<_$SearchQueryImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$SearchQueryImplToJson(
      this,
    );
  }
}

abstract class _SearchQuery implements SearchQuery {
  const factory _SearchQuery(
      {required final int id,
      required final int? userId,
      required final String query,
      required final int resultCount,
      required final int? clickedResult,
      required final int searchTimeMs,
      required final DateTime createdAt}) = _$SearchQueryImpl;

  factory _SearchQuery.fromJson(Map<String, dynamic> json) =
      _$SearchQueryImpl.fromJson;

  @override
  int get id;
  @override
  int? get userId;
  @override
  String get query;
  @override
  int get resultCount;
  @override
  int? get clickedResult;
  @override
  int get searchTimeMs;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$SearchQueryImplCopyWith<_$SearchQueryImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

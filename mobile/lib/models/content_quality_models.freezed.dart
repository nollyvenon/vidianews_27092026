// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'content_quality_models.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
    'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models');

CalendarEvent _$CalendarEventFromJson(Map<String, dynamic> json) {
  return _CalendarEvent.fromJson(json);
}

/// @nodoc
mixin _$CalendarEvent {
  int get id => throw _privateConstructorUsedError;
  String get eventType => throw _privateConstructorUsedError;
  String get title => throw _privateConstructorUsedError;
  DateTime get scheduledFor => throw _privateConstructorUsedError;
  DateTime? get aiRecommendedTime => throw _privateConstructorUsedError;
  double get aiConfidenceScore => throw _privateConstructorUsedError;
  int? get predictedReach => throw _privateConstructorUsedError;
  int? get predictedEngagement => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $CalendarEventCopyWith<CalendarEvent> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $CalendarEventCopyWith<$Res> {
  factory $CalendarEventCopyWith(
          CalendarEvent value, $Res Function(CalendarEvent) then) =
      _$CalendarEventCopyWithImpl<$Res, CalendarEvent>;
  @useResult
  $Res call(
      {int id,
      String eventType,
      String title,
      DateTime scheduledFor,
      DateTime? aiRecommendedTime,
      double aiConfidenceScore,
      int? predictedReach,
      int? predictedEngagement});
}

/// @nodoc
class _$CalendarEventCopyWithImpl<$Res, $Val extends CalendarEvent>
    implements $CalendarEventCopyWith<$Res> {
  _$CalendarEventCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? eventType = null,
    Object? title = null,
    Object? scheduledFor = null,
    Object? aiRecommendedTime = freezed,
    Object? aiConfidenceScore = null,
    Object? predictedReach = freezed,
    Object? predictedEngagement = freezed,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      eventType: null == eventType
          ? _value.eventType
          : eventType // ignore: cast_nullable_to_non_nullable
              as String,
      title: null == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String,
      scheduledFor: null == scheduledFor
          ? _value.scheduledFor
          : scheduledFor // ignore: cast_nullable_to_non_nullable
              as DateTime,
      aiRecommendedTime: freezed == aiRecommendedTime
          ? _value.aiRecommendedTime
          : aiRecommendedTime // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      aiConfidenceScore: null == aiConfidenceScore
          ? _value.aiConfidenceScore
          : aiConfidenceScore // ignore: cast_nullable_to_non_nullable
              as double,
      predictedReach: freezed == predictedReach
          ? _value.predictedReach
          : predictedReach // ignore: cast_nullable_to_non_nullable
              as int?,
      predictedEngagement: freezed == predictedEngagement
          ? _value.predictedEngagement
          : predictedEngagement // ignore: cast_nullable_to_non_nullable
              as int?,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$CalendarEventImplCopyWith<$Res>
    implements $CalendarEventCopyWith<$Res> {
  factory _$$CalendarEventImplCopyWith(
          _$CalendarEventImpl value, $Res Function(_$CalendarEventImpl) then) =
      __$$CalendarEventImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String eventType,
      String title,
      DateTime scheduledFor,
      DateTime? aiRecommendedTime,
      double aiConfidenceScore,
      int? predictedReach,
      int? predictedEngagement});
}

/// @nodoc
class __$$CalendarEventImplCopyWithImpl<$Res>
    extends _$CalendarEventCopyWithImpl<$Res, _$CalendarEventImpl>
    implements _$$CalendarEventImplCopyWith<$Res> {
  __$$CalendarEventImplCopyWithImpl(
      _$CalendarEventImpl _value, $Res Function(_$CalendarEventImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? eventType = null,
    Object? title = null,
    Object? scheduledFor = null,
    Object? aiRecommendedTime = freezed,
    Object? aiConfidenceScore = null,
    Object? predictedReach = freezed,
    Object? predictedEngagement = freezed,
  }) {
    return _then(_$CalendarEventImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      eventType: null == eventType
          ? _value.eventType
          : eventType // ignore: cast_nullable_to_non_nullable
              as String,
      title: null == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String,
      scheduledFor: null == scheduledFor
          ? _value.scheduledFor
          : scheduledFor // ignore: cast_nullable_to_non_nullable
              as DateTime,
      aiRecommendedTime: freezed == aiRecommendedTime
          ? _value.aiRecommendedTime
          : aiRecommendedTime // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      aiConfidenceScore: null == aiConfidenceScore
          ? _value.aiConfidenceScore
          : aiConfidenceScore // ignore: cast_nullable_to_non_nullable
              as double,
      predictedReach: freezed == predictedReach
          ? _value.predictedReach
          : predictedReach // ignore: cast_nullable_to_non_nullable
              as int?,
      predictedEngagement: freezed == predictedEngagement
          ? _value.predictedEngagement
          : predictedEngagement // ignore: cast_nullable_to_non_nullable
              as int?,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$CalendarEventImpl implements _CalendarEvent {
  const _$CalendarEventImpl(
      {required this.id,
      required this.eventType,
      required this.title,
      required this.scheduledFor,
      this.aiRecommendedTime,
      required this.aiConfidenceScore,
      this.predictedReach,
      this.predictedEngagement});

  factory _$CalendarEventImpl.fromJson(Map<String, dynamic> json) =>
      _$$CalendarEventImplFromJson(json);

  @override
  final int id;
  @override
  final String eventType;
  @override
  final String title;
  @override
  final DateTime scheduledFor;
  @override
  final DateTime? aiRecommendedTime;
  @override
  final double aiConfidenceScore;
  @override
  final int? predictedReach;
  @override
  final int? predictedEngagement;

  @override
  String toString() {
    return 'CalendarEvent(id: $id, eventType: $eventType, title: $title, scheduledFor: $scheduledFor, aiRecommendedTime: $aiRecommendedTime, aiConfidenceScore: $aiConfidenceScore, predictedReach: $predictedReach, predictedEngagement: $predictedEngagement)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$CalendarEventImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.eventType, eventType) ||
                other.eventType == eventType) &&
            (identical(other.title, title) || other.title == title) &&
            (identical(other.scheduledFor, scheduledFor) ||
                other.scheduledFor == scheduledFor) &&
            (identical(other.aiRecommendedTime, aiRecommendedTime) ||
                other.aiRecommendedTime == aiRecommendedTime) &&
            (identical(other.aiConfidenceScore, aiConfidenceScore) ||
                other.aiConfidenceScore == aiConfidenceScore) &&
            (identical(other.predictedReach, predictedReach) ||
                other.predictedReach == predictedReach) &&
            (identical(other.predictedEngagement, predictedEngagement) ||
                other.predictedEngagement == predictedEngagement));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      eventType,
      title,
      scheduledFor,
      aiRecommendedTime,
      aiConfidenceScore,
      predictedReach,
      predictedEngagement);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$CalendarEventImplCopyWith<_$CalendarEventImpl> get copyWith =>
      __$$CalendarEventImplCopyWithImpl<_$CalendarEventImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$CalendarEventImplToJson(
      this,
    );
  }
}

abstract class _CalendarEvent implements CalendarEvent {
  const factory _CalendarEvent(
      {required final int id,
      required final String eventType,
      required final String title,
      required final DateTime scheduledFor,
      final DateTime? aiRecommendedTime,
      required final double aiConfidenceScore,
      final int? predictedReach,
      final int? predictedEngagement}) = _$CalendarEventImpl;

  factory _CalendarEvent.fromJson(Map<String, dynamic> json) =
      _$CalendarEventImpl.fromJson;

  @override
  int get id;
  @override
  String get eventType;
  @override
  String get title;
  @override
  DateTime get scheduledFor;
  @override
  DateTime? get aiRecommendedTime;
  @override
  double get aiConfidenceScore;
  @override
  int? get predictedReach;
  @override
  int? get predictedEngagement;
  @override
  @JsonKey(ignore: true)
  _$$CalendarEventImplCopyWith<_$CalendarEventImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

CalendarResponse _$CalendarResponseFromJson(Map<String, dynamic> json) {
  return _CalendarResponse.fromJson(json);
}

/// @nodoc
mixin _$CalendarResponse {
  List<CalendarEvent> get events => throw _privateConstructorUsedError;
  int get totalCount => throw _privateConstructorUsedError;
  double get averageConfidence => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $CalendarResponseCopyWith<CalendarResponse> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $CalendarResponseCopyWith<$Res> {
  factory $CalendarResponseCopyWith(
          CalendarResponse value, $Res Function(CalendarResponse) then) =
      _$CalendarResponseCopyWithImpl<$Res, CalendarResponse>;
  @useResult
  $Res call(
      {List<CalendarEvent> events, int totalCount, double averageConfidence});
}

/// @nodoc
class _$CalendarResponseCopyWithImpl<$Res, $Val extends CalendarResponse>
    implements $CalendarResponseCopyWith<$Res> {
  _$CalendarResponseCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? events = null,
    Object? totalCount = null,
    Object? averageConfidence = null,
  }) {
    return _then(_value.copyWith(
      events: null == events
          ? _value.events
          : events // ignore: cast_nullable_to_non_nullable
              as List<CalendarEvent>,
      totalCount: null == totalCount
          ? _value.totalCount
          : totalCount // ignore: cast_nullable_to_non_nullable
              as int,
      averageConfidence: null == averageConfidence
          ? _value.averageConfidence
          : averageConfidence // ignore: cast_nullable_to_non_nullable
              as double,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$CalendarResponseImplCopyWith<$Res>
    implements $CalendarResponseCopyWith<$Res> {
  factory _$$CalendarResponseImplCopyWith(_$CalendarResponseImpl value,
          $Res Function(_$CalendarResponseImpl) then) =
      __$$CalendarResponseImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {List<CalendarEvent> events, int totalCount, double averageConfidence});
}

/// @nodoc
class __$$CalendarResponseImplCopyWithImpl<$Res>
    extends _$CalendarResponseCopyWithImpl<$Res, _$CalendarResponseImpl>
    implements _$$CalendarResponseImplCopyWith<$Res> {
  __$$CalendarResponseImplCopyWithImpl(_$CalendarResponseImpl _value,
      $Res Function(_$CalendarResponseImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? events = null,
    Object? totalCount = null,
    Object? averageConfidence = null,
  }) {
    return _then(_$CalendarResponseImpl(
      events: null == events
          ? _value._events
          : events // ignore: cast_nullable_to_non_nullable
              as List<CalendarEvent>,
      totalCount: null == totalCount
          ? _value.totalCount
          : totalCount // ignore: cast_nullable_to_non_nullable
              as int,
      averageConfidence: null == averageConfidence
          ? _value.averageConfidence
          : averageConfidence // ignore: cast_nullable_to_non_nullable
              as double,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$CalendarResponseImpl implements _CalendarResponse {
  const _$CalendarResponseImpl(
      {required final List<CalendarEvent> events,
      required this.totalCount,
      required this.averageConfidence})
      : _events = events;

  factory _$CalendarResponseImpl.fromJson(Map<String, dynamic> json) =>
      _$$CalendarResponseImplFromJson(json);

  final List<CalendarEvent> _events;
  @override
  List<CalendarEvent> get events {
    if (_events is EqualUnmodifiableListView) return _events;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_events);
  }

  @override
  final int totalCount;
  @override
  final double averageConfidence;

  @override
  String toString() {
    return 'CalendarResponse(events: $events, totalCount: $totalCount, averageConfidence: $averageConfidence)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$CalendarResponseImpl &&
            const DeepCollectionEquality().equals(other._events, _events) &&
            (identical(other.totalCount, totalCount) ||
                other.totalCount == totalCount) &&
            (identical(other.averageConfidence, averageConfidence) ||
                other.averageConfidence == averageConfidence));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      const DeepCollectionEquality().hash(_events),
      totalCount,
      averageConfidence);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$CalendarResponseImplCopyWith<_$CalendarResponseImpl> get copyWith =>
      __$$CalendarResponseImplCopyWithImpl<_$CalendarResponseImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$CalendarResponseImplToJson(
      this,
    );
  }
}

abstract class _CalendarResponse implements CalendarResponse {
  const factory _CalendarResponse(
      {required final List<CalendarEvent> events,
      required final int totalCount,
      required final double averageConfidence}) = _$CalendarResponseImpl;

  factory _CalendarResponse.fromJson(Map<String, dynamic> json) =
      _$CalendarResponseImpl.fromJson;

  @override
  List<CalendarEvent> get events;
  @override
  int get totalCount;
  @override
  double get averageConfidence;
  @override
  @JsonKey(ignore: true)
  _$$CalendarResponseImplCopyWith<_$CalendarResponseImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

ProofreadingIssue _$ProofreadingIssueFromJson(Map<String, dynamic> json) {
  return _ProofreadingIssue.fromJson(json);
}

/// @nodoc
mixin _$ProofreadingIssue {
  int get id => throw _privateConstructorUsedError;
  String get issueType => throw _privateConstructorUsedError;
  String get severity => throw _privateConstructorUsedError;
  String get text => throw _privateConstructorUsedError;
  String get suggestion => throw _privateConstructorUsedError;
  int get position => throw _privateConstructorUsedError;
  int get length => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $ProofreadingIssueCopyWith<ProofreadingIssue> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $ProofreadingIssueCopyWith<$Res> {
  factory $ProofreadingIssueCopyWith(
          ProofreadingIssue value, $Res Function(ProofreadingIssue) then) =
      _$ProofreadingIssueCopyWithImpl<$Res, ProofreadingIssue>;
  @useResult
  $Res call(
      {int id,
      String issueType,
      String severity,
      String text,
      String suggestion,
      int position,
      int length});
}

/// @nodoc
class _$ProofreadingIssueCopyWithImpl<$Res, $Val extends ProofreadingIssue>
    implements $ProofreadingIssueCopyWith<$Res> {
  _$ProofreadingIssueCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? issueType = null,
    Object? severity = null,
    Object? text = null,
    Object? suggestion = null,
    Object? position = null,
    Object? length = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      issueType: null == issueType
          ? _value.issueType
          : issueType // ignore: cast_nullable_to_non_nullable
              as String,
      severity: null == severity
          ? _value.severity
          : severity // ignore: cast_nullable_to_non_nullable
              as String,
      text: null == text
          ? _value.text
          : text // ignore: cast_nullable_to_non_nullable
              as String,
      suggestion: null == suggestion
          ? _value.suggestion
          : suggestion // ignore: cast_nullable_to_non_nullable
              as String,
      position: null == position
          ? _value.position
          : position // ignore: cast_nullable_to_non_nullable
              as int,
      length: null == length
          ? _value.length
          : length // ignore: cast_nullable_to_non_nullable
              as int,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$ProofreadingIssueImplCopyWith<$Res>
    implements $ProofreadingIssueCopyWith<$Res> {
  factory _$$ProofreadingIssueImplCopyWith(_$ProofreadingIssueImpl value,
          $Res Function(_$ProofreadingIssueImpl) then) =
      __$$ProofreadingIssueImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String issueType,
      String severity,
      String text,
      String suggestion,
      int position,
      int length});
}

/// @nodoc
class __$$ProofreadingIssueImplCopyWithImpl<$Res>
    extends _$ProofreadingIssueCopyWithImpl<$Res, _$ProofreadingIssueImpl>
    implements _$$ProofreadingIssueImplCopyWith<$Res> {
  __$$ProofreadingIssueImplCopyWithImpl(_$ProofreadingIssueImpl _value,
      $Res Function(_$ProofreadingIssueImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? issueType = null,
    Object? severity = null,
    Object? text = null,
    Object? suggestion = null,
    Object? position = null,
    Object? length = null,
  }) {
    return _then(_$ProofreadingIssueImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      issueType: null == issueType
          ? _value.issueType
          : issueType // ignore: cast_nullable_to_non_nullable
              as String,
      severity: null == severity
          ? _value.severity
          : severity // ignore: cast_nullable_to_non_nullable
              as String,
      text: null == text
          ? _value.text
          : text // ignore: cast_nullable_to_non_nullable
              as String,
      suggestion: null == suggestion
          ? _value.suggestion
          : suggestion // ignore: cast_nullable_to_non_nullable
              as String,
      position: null == position
          ? _value.position
          : position // ignore: cast_nullable_to_non_nullable
              as int,
      length: null == length
          ? _value.length
          : length // ignore: cast_nullable_to_non_nullable
              as int,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$ProofreadingIssueImpl implements _ProofreadingIssue {
  const _$ProofreadingIssueImpl(
      {required this.id,
      required this.issueType,
      required this.severity,
      required this.text,
      required this.suggestion,
      required this.position,
      required this.length});

  factory _$ProofreadingIssueImpl.fromJson(Map<String, dynamic> json) =>
      _$$ProofreadingIssueImplFromJson(json);

  @override
  final int id;
  @override
  final String issueType;
  @override
  final String severity;
  @override
  final String text;
  @override
  final String suggestion;
  @override
  final int position;
  @override
  final int length;

  @override
  String toString() {
    return 'ProofreadingIssue(id: $id, issueType: $issueType, severity: $severity, text: $text, suggestion: $suggestion, position: $position, length: $length)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$ProofreadingIssueImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.issueType, issueType) ||
                other.issueType == issueType) &&
            (identical(other.severity, severity) ||
                other.severity == severity) &&
            (identical(other.text, text) || other.text == text) &&
            (identical(other.suggestion, suggestion) ||
                other.suggestion == suggestion) &&
            (identical(other.position, position) ||
                other.position == position) &&
            (identical(other.length, length) || other.length == length));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType, id, issueType, severity, text, suggestion, position, length);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$ProofreadingIssueImplCopyWith<_$ProofreadingIssueImpl> get copyWith =>
      __$$ProofreadingIssueImplCopyWithImpl<_$ProofreadingIssueImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$ProofreadingIssueImplToJson(
      this,
    );
  }
}

abstract class _ProofreadingIssue implements ProofreadingIssue {
  const factory _ProofreadingIssue(
      {required final int id,
      required final String issueType,
      required final String severity,
      required final String text,
      required final String suggestion,
      required final int position,
      required final int length}) = _$ProofreadingIssueImpl;

  factory _ProofreadingIssue.fromJson(Map<String, dynamic> json) =
      _$ProofreadingIssueImpl.fromJson;

  @override
  int get id;
  @override
  String get issueType;
  @override
  String get severity;
  @override
  String get text;
  @override
  String get suggestion;
  @override
  int get position;
  @override
  int get length;
  @override
  @JsonKey(ignore: true)
  _$$ProofreadingIssueImplCopyWith<_$ProofreadingIssueImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

ProofreadingResult _$ProofreadingResultFromJson(Map<String, dynamic> json) {
  return _ProofreadingResult.fromJson(json);
}

/// @nodoc
mixin _$ProofreadingResult {
  int get id => throw _privateConstructorUsedError;
  double get qualityScore => throw _privateConstructorUsedError;
  String get overallRating => throw _privateConstructorUsedError;
  int get totalIssues => throw _privateConstructorUsedError;
  int get grammarIssues => throw _privateConstructorUsedError;
  int get spellingIssues => throw _privateConstructorUsedError;
  int get punctuationIssues => throw _privateConstructorUsedError;
  int get styleIssues => throw _privateConstructorUsedError;
  List<ProofreadingIssue>? get issues => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $ProofreadingResultCopyWith<ProofreadingResult> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $ProofreadingResultCopyWith<$Res> {
  factory $ProofreadingResultCopyWith(
          ProofreadingResult value, $Res Function(ProofreadingResult) then) =
      _$ProofreadingResultCopyWithImpl<$Res, ProofreadingResult>;
  @useResult
  $Res call(
      {int id,
      double qualityScore,
      String overallRating,
      int totalIssues,
      int grammarIssues,
      int spellingIssues,
      int punctuationIssues,
      int styleIssues,
      List<ProofreadingIssue>? issues});
}

/// @nodoc
class _$ProofreadingResultCopyWithImpl<$Res, $Val extends ProofreadingResult>
    implements $ProofreadingResultCopyWith<$Res> {
  _$ProofreadingResultCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? qualityScore = null,
    Object? overallRating = null,
    Object? totalIssues = null,
    Object? grammarIssues = null,
    Object? spellingIssues = null,
    Object? punctuationIssues = null,
    Object? styleIssues = null,
    Object? issues = freezed,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      qualityScore: null == qualityScore
          ? _value.qualityScore
          : qualityScore // ignore: cast_nullable_to_non_nullable
              as double,
      overallRating: null == overallRating
          ? _value.overallRating
          : overallRating // ignore: cast_nullable_to_non_nullable
              as String,
      totalIssues: null == totalIssues
          ? _value.totalIssues
          : totalIssues // ignore: cast_nullable_to_non_nullable
              as int,
      grammarIssues: null == grammarIssues
          ? _value.grammarIssues
          : grammarIssues // ignore: cast_nullable_to_non_nullable
              as int,
      spellingIssues: null == spellingIssues
          ? _value.spellingIssues
          : spellingIssues // ignore: cast_nullable_to_non_nullable
              as int,
      punctuationIssues: null == punctuationIssues
          ? _value.punctuationIssues
          : punctuationIssues // ignore: cast_nullable_to_non_nullable
              as int,
      styleIssues: null == styleIssues
          ? _value.styleIssues
          : styleIssues // ignore: cast_nullable_to_non_nullable
              as int,
      issues: freezed == issues
          ? _value.issues
          : issues // ignore: cast_nullable_to_non_nullable
              as List<ProofreadingIssue>?,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$ProofreadingResultImplCopyWith<$Res>
    implements $ProofreadingResultCopyWith<$Res> {
  factory _$$ProofreadingResultImplCopyWith(_$ProofreadingResultImpl value,
          $Res Function(_$ProofreadingResultImpl) then) =
      __$$ProofreadingResultImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      double qualityScore,
      String overallRating,
      int totalIssues,
      int grammarIssues,
      int spellingIssues,
      int punctuationIssues,
      int styleIssues,
      List<ProofreadingIssue>? issues});
}

/// @nodoc
class __$$ProofreadingResultImplCopyWithImpl<$Res>
    extends _$ProofreadingResultCopyWithImpl<$Res, _$ProofreadingResultImpl>
    implements _$$ProofreadingResultImplCopyWith<$Res> {
  __$$ProofreadingResultImplCopyWithImpl(_$ProofreadingResultImpl _value,
      $Res Function(_$ProofreadingResultImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? qualityScore = null,
    Object? overallRating = null,
    Object? totalIssues = null,
    Object? grammarIssues = null,
    Object? spellingIssues = null,
    Object? punctuationIssues = null,
    Object? styleIssues = null,
    Object? issues = freezed,
  }) {
    return _then(_$ProofreadingResultImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      qualityScore: null == qualityScore
          ? _value.qualityScore
          : qualityScore // ignore: cast_nullable_to_non_nullable
              as double,
      overallRating: null == overallRating
          ? _value.overallRating
          : overallRating // ignore: cast_nullable_to_non_nullable
              as String,
      totalIssues: null == totalIssues
          ? _value.totalIssues
          : totalIssues // ignore: cast_nullable_to_non_nullable
              as int,
      grammarIssues: null == grammarIssues
          ? _value.grammarIssues
          : grammarIssues // ignore: cast_nullable_to_non_nullable
              as int,
      spellingIssues: null == spellingIssues
          ? _value.spellingIssues
          : spellingIssues // ignore: cast_nullable_to_non_nullable
              as int,
      punctuationIssues: null == punctuationIssues
          ? _value.punctuationIssues
          : punctuationIssues // ignore: cast_nullable_to_non_nullable
              as int,
      styleIssues: null == styleIssues
          ? _value.styleIssues
          : styleIssues // ignore: cast_nullable_to_non_nullable
              as int,
      issues: freezed == issues
          ? _value._issues
          : issues // ignore: cast_nullable_to_non_nullable
              as List<ProofreadingIssue>?,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$ProofreadingResultImpl implements _ProofreadingResult {
  const _$ProofreadingResultImpl(
      {required this.id,
      required this.qualityScore,
      required this.overallRating,
      required this.totalIssues,
      required this.grammarIssues,
      required this.spellingIssues,
      required this.punctuationIssues,
      required this.styleIssues,
      final List<ProofreadingIssue>? issues})
      : _issues = issues;

  factory _$ProofreadingResultImpl.fromJson(Map<String, dynamic> json) =>
      _$$ProofreadingResultImplFromJson(json);

  @override
  final int id;
  @override
  final double qualityScore;
  @override
  final String overallRating;
  @override
  final int totalIssues;
  @override
  final int grammarIssues;
  @override
  final int spellingIssues;
  @override
  final int punctuationIssues;
  @override
  final int styleIssues;
  final List<ProofreadingIssue>? _issues;
  @override
  List<ProofreadingIssue>? get issues {
    final value = _issues;
    if (value == null) return null;
    if (_issues is EqualUnmodifiableListView) return _issues;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(value);
  }

  @override
  String toString() {
    return 'ProofreadingResult(id: $id, qualityScore: $qualityScore, overallRating: $overallRating, totalIssues: $totalIssues, grammarIssues: $grammarIssues, spellingIssues: $spellingIssues, punctuationIssues: $punctuationIssues, styleIssues: $styleIssues, issues: $issues)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$ProofreadingResultImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.qualityScore, qualityScore) ||
                other.qualityScore == qualityScore) &&
            (identical(other.overallRating, overallRating) ||
                other.overallRating == overallRating) &&
            (identical(other.totalIssues, totalIssues) ||
                other.totalIssues == totalIssues) &&
            (identical(other.grammarIssues, grammarIssues) ||
                other.grammarIssues == grammarIssues) &&
            (identical(other.spellingIssues, spellingIssues) ||
                other.spellingIssues == spellingIssues) &&
            (identical(other.punctuationIssues, punctuationIssues) ||
                other.punctuationIssues == punctuationIssues) &&
            (identical(other.styleIssues, styleIssues) ||
                other.styleIssues == styleIssues) &&
            const DeepCollectionEquality().equals(other._issues, _issues));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      qualityScore,
      overallRating,
      totalIssues,
      grammarIssues,
      spellingIssues,
      punctuationIssues,
      styleIssues,
      const DeepCollectionEquality().hash(_issues));

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$ProofreadingResultImplCopyWith<_$ProofreadingResultImpl> get copyWith =>
      __$$ProofreadingResultImplCopyWithImpl<_$ProofreadingResultImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$ProofreadingResultImplToJson(
      this,
    );
  }
}

abstract class _ProofreadingResult implements ProofreadingResult {
  const factory _ProofreadingResult(
      {required final int id,
      required final double qualityScore,
      required final String overallRating,
      required final int totalIssues,
      required final int grammarIssues,
      required final int spellingIssues,
      required final int punctuationIssues,
      required final int styleIssues,
      final List<ProofreadingIssue>? issues}) = _$ProofreadingResultImpl;

  factory _ProofreadingResult.fromJson(Map<String, dynamic> json) =
      _$ProofreadingResultImpl.fromJson;

  @override
  int get id;
  @override
  double get qualityScore;
  @override
  String get overallRating;
  @override
  int get totalIssues;
  @override
  int get grammarIssues;
  @override
  int get spellingIssues;
  @override
  int get punctuationIssues;
  @override
  int get styleIssues;
  @override
  List<ProofreadingIssue>? get issues;
  @override
  @JsonKey(ignore: true)
  _$$ProofreadingResultImplCopyWith<_$ProofreadingResultImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

Source _$SourceFromJson(Map<String, dynamic> json) {
  return _Source.fromJson(json);
}

/// @nodoc
mixin _$Source {
  String get url => throw _privateConstructorUsedError;
  double get similarityPercent => throw _privateConstructorUsedError;
  String get matchedText => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $SourceCopyWith<Source> get copyWith => throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $SourceCopyWith<$Res> {
  factory $SourceCopyWith(Source value, $Res Function(Source) then) =
      _$SourceCopyWithImpl<$Res, Source>;
  @useResult
  $Res call({String url, double similarityPercent, String matchedText});
}

/// @nodoc
class _$SourceCopyWithImpl<$Res, $Val extends Source>
    implements $SourceCopyWith<$Res> {
  _$SourceCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? url = null,
    Object? similarityPercent = null,
    Object? matchedText = null,
  }) {
    return _then(_value.copyWith(
      url: null == url
          ? _value.url
          : url // ignore: cast_nullable_to_non_nullable
              as String,
      similarityPercent: null == similarityPercent
          ? _value.similarityPercent
          : similarityPercent // ignore: cast_nullable_to_non_nullable
              as double,
      matchedText: null == matchedText
          ? _value.matchedText
          : matchedText // ignore: cast_nullable_to_non_nullable
              as String,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$SourceImplCopyWith<$Res> implements $SourceCopyWith<$Res> {
  factory _$$SourceImplCopyWith(
          _$SourceImpl value, $Res Function(_$SourceImpl) then) =
      __$$SourceImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({String url, double similarityPercent, String matchedText});
}

/// @nodoc
class __$$SourceImplCopyWithImpl<$Res>
    extends _$SourceCopyWithImpl<$Res, _$SourceImpl>
    implements _$$SourceImplCopyWith<$Res> {
  __$$SourceImplCopyWithImpl(
      _$SourceImpl _value, $Res Function(_$SourceImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? url = null,
    Object? similarityPercent = null,
    Object? matchedText = null,
  }) {
    return _then(_$SourceImpl(
      url: null == url
          ? _value.url
          : url // ignore: cast_nullable_to_non_nullable
              as String,
      similarityPercent: null == similarityPercent
          ? _value.similarityPercent
          : similarityPercent // ignore: cast_nullable_to_non_nullable
              as double,
      matchedText: null == matchedText
          ? _value.matchedText
          : matchedText // ignore: cast_nullable_to_non_nullable
              as String,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$SourceImpl implements _Source {
  const _$SourceImpl(
      {required this.url,
      required this.similarityPercent,
      required this.matchedText});

  factory _$SourceImpl.fromJson(Map<String, dynamic> json) =>
      _$$SourceImplFromJson(json);

  @override
  final String url;
  @override
  final double similarityPercent;
  @override
  final String matchedText;

  @override
  String toString() {
    return 'Source(url: $url, similarityPercent: $similarityPercent, matchedText: $matchedText)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$SourceImpl &&
            (identical(other.url, url) || other.url == url) &&
            (identical(other.similarityPercent, similarityPercent) ||
                other.similarityPercent == similarityPercent) &&
            (identical(other.matchedText, matchedText) ||
                other.matchedText == matchedText));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode =>
      Object.hash(runtimeType, url, similarityPercent, matchedText);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$SourceImplCopyWith<_$SourceImpl> get copyWith =>
      __$$SourceImplCopyWithImpl<_$SourceImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$SourceImplToJson(
      this,
    );
  }
}

abstract class _Source implements Source {
  const factory _Source(
      {required final String url,
      required final double similarityPercent,
      required final String matchedText}) = _$SourceImpl;

  factory _Source.fromJson(Map<String, dynamic> json) = _$SourceImpl.fromJson;

  @override
  String get url;
  @override
  double get similarityPercent;
  @override
  String get matchedText;
  @override
  @JsonKey(ignore: true)
  _$$SourceImplCopyWith<_$SourceImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

PlagiarismResult _$PlagiarismResultFromJson(Map<String, dynamic> json) {
  return _PlagiarismResult.fromJson(json);
}

/// @nodoc
mixin _$PlagiarismResult {
  int get id => throw _privateConstructorUsedError;
  double get similarityPercentage => throw _privateConstructorUsedError;
  double get originalityPercentage => throw _privateConstructorUsedError;
  String get plagiarismRisk => throw _privateConstructorUsedError;
  String get status => throw _privateConstructorUsedError;
  int get totalSourcesFound => throw _privateConstructorUsedError;
  double get aiContentPercentage => throw _privateConstructorUsedError;
  double get humanContentPercentage => throw _privateConstructorUsedError;
  List<Source> get detectedSources => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $PlagiarismResultCopyWith<PlagiarismResult> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $PlagiarismResultCopyWith<$Res> {
  factory $PlagiarismResultCopyWith(
          PlagiarismResult value, $Res Function(PlagiarismResult) then) =
      _$PlagiarismResultCopyWithImpl<$Res, PlagiarismResult>;
  @useResult
  $Res call(
      {int id,
      double similarityPercentage,
      double originalityPercentage,
      String plagiarismRisk,
      String status,
      int totalSourcesFound,
      double aiContentPercentage,
      double humanContentPercentage,
      List<Source> detectedSources});
}

/// @nodoc
class _$PlagiarismResultCopyWithImpl<$Res, $Val extends PlagiarismResult>
    implements $PlagiarismResultCopyWith<$Res> {
  _$PlagiarismResultCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? similarityPercentage = null,
    Object? originalityPercentage = null,
    Object? plagiarismRisk = null,
    Object? status = null,
    Object? totalSourcesFound = null,
    Object? aiContentPercentage = null,
    Object? humanContentPercentage = null,
    Object? detectedSources = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      similarityPercentage: null == similarityPercentage
          ? _value.similarityPercentage
          : similarityPercentage // ignore: cast_nullable_to_non_nullable
              as double,
      originalityPercentage: null == originalityPercentage
          ? _value.originalityPercentage
          : originalityPercentage // ignore: cast_nullable_to_non_nullable
              as double,
      plagiarismRisk: null == plagiarismRisk
          ? _value.plagiarismRisk
          : plagiarismRisk // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      totalSourcesFound: null == totalSourcesFound
          ? _value.totalSourcesFound
          : totalSourcesFound // ignore: cast_nullable_to_non_nullable
              as int,
      aiContentPercentage: null == aiContentPercentage
          ? _value.aiContentPercentage
          : aiContentPercentage // ignore: cast_nullable_to_non_nullable
              as double,
      humanContentPercentage: null == humanContentPercentage
          ? _value.humanContentPercentage
          : humanContentPercentage // ignore: cast_nullable_to_non_nullable
              as double,
      detectedSources: null == detectedSources
          ? _value.detectedSources
          : detectedSources // ignore: cast_nullable_to_non_nullable
              as List<Source>,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$PlagiarismResultImplCopyWith<$Res>
    implements $PlagiarismResultCopyWith<$Res> {
  factory _$$PlagiarismResultImplCopyWith(_$PlagiarismResultImpl value,
          $Res Function(_$PlagiarismResultImpl) then) =
      __$$PlagiarismResultImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      double similarityPercentage,
      double originalityPercentage,
      String plagiarismRisk,
      String status,
      int totalSourcesFound,
      double aiContentPercentage,
      double humanContentPercentage,
      List<Source> detectedSources});
}

/// @nodoc
class __$$PlagiarismResultImplCopyWithImpl<$Res>
    extends _$PlagiarismResultCopyWithImpl<$Res, _$PlagiarismResultImpl>
    implements _$$PlagiarismResultImplCopyWith<$Res> {
  __$$PlagiarismResultImplCopyWithImpl(_$PlagiarismResultImpl _value,
      $Res Function(_$PlagiarismResultImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? similarityPercentage = null,
    Object? originalityPercentage = null,
    Object? plagiarismRisk = null,
    Object? status = null,
    Object? totalSourcesFound = null,
    Object? aiContentPercentage = null,
    Object? humanContentPercentage = null,
    Object? detectedSources = null,
  }) {
    return _then(_$PlagiarismResultImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      similarityPercentage: null == similarityPercentage
          ? _value.similarityPercentage
          : similarityPercentage // ignore: cast_nullable_to_non_nullable
              as double,
      originalityPercentage: null == originalityPercentage
          ? _value.originalityPercentage
          : originalityPercentage // ignore: cast_nullable_to_non_nullable
              as double,
      plagiarismRisk: null == plagiarismRisk
          ? _value.plagiarismRisk
          : plagiarismRisk // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      totalSourcesFound: null == totalSourcesFound
          ? _value.totalSourcesFound
          : totalSourcesFound // ignore: cast_nullable_to_non_nullable
              as int,
      aiContentPercentage: null == aiContentPercentage
          ? _value.aiContentPercentage
          : aiContentPercentage // ignore: cast_nullable_to_non_nullable
              as double,
      humanContentPercentage: null == humanContentPercentage
          ? _value.humanContentPercentage
          : humanContentPercentage // ignore: cast_nullable_to_non_nullable
              as double,
      detectedSources: null == detectedSources
          ? _value._detectedSources
          : detectedSources // ignore: cast_nullable_to_non_nullable
              as List<Source>,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$PlagiarismResultImpl implements _PlagiarismResult {
  const _$PlagiarismResultImpl(
      {required this.id,
      required this.similarityPercentage,
      required this.originalityPercentage,
      required this.plagiarismRisk,
      required this.status,
      required this.totalSourcesFound,
      required this.aiContentPercentage,
      required this.humanContentPercentage,
      required final List<Source> detectedSources})
      : _detectedSources = detectedSources;

  factory _$PlagiarismResultImpl.fromJson(Map<String, dynamic> json) =>
      _$$PlagiarismResultImplFromJson(json);

  @override
  final int id;
  @override
  final double similarityPercentage;
  @override
  final double originalityPercentage;
  @override
  final String plagiarismRisk;
  @override
  final String status;
  @override
  final int totalSourcesFound;
  @override
  final double aiContentPercentage;
  @override
  final double humanContentPercentage;
  final List<Source> _detectedSources;
  @override
  List<Source> get detectedSources {
    if (_detectedSources is EqualUnmodifiableListView) return _detectedSources;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_detectedSources);
  }

  @override
  String toString() {
    return 'PlagiarismResult(id: $id, similarityPercentage: $similarityPercentage, originalityPercentage: $originalityPercentage, plagiarismRisk: $plagiarismRisk, status: $status, totalSourcesFound: $totalSourcesFound, aiContentPercentage: $aiContentPercentage, humanContentPercentage: $humanContentPercentage, detectedSources: $detectedSources)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$PlagiarismResultImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.similarityPercentage, similarityPercentage) ||
                other.similarityPercentage == similarityPercentage) &&
            (identical(other.originalityPercentage, originalityPercentage) ||
                other.originalityPercentage == originalityPercentage) &&
            (identical(other.plagiarismRisk, plagiarismRisk) ||
                other.plagiarismRisk == plagiarismRisk) &&
            (identical(other.status, status) || other.status == status) &&
            (identical(other.totalSourcesFound, totalSourcesFound) ||
                other.totalSourcesFound == totalSourcesFound) &&
            (identical(other.aiContentPercentage, aiContentPercentage) ||
                other.aiContentPercentage == aiContentPercentage) &&
            (identical(other.humanContentPercentage, humanContentPercentage) ||
                other.humanContentPercentage == humanContentPercentage) &&
            const DeepCollectionEquality()
                .equals(other._detectedSources, _detectedSources));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      similarityPercentage,
      originalityPercentage,
      plagiarismRisk,
      status,
      totalSourcesFound,
      aiContentPercentage,
      humanContentPercentage,
      const DeepCollectionEquality().hash(_detectedSources));

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$PlagiarismResultImplCopyWith<_$PlagiarismResultImpl> get copyWith =>
      __$$PlagiarismResultImplCopyWithImpl<_$PlagiarismResultImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$PlagiarismResultImplToJson(
      this,
    );
  }
}

abstract class _PlagiarismResult implements PlagiarismResult {
  const factory _PlagiarismResult(
      {required final int id,
      required final double similarityPercentage,
      required final double originalityPercentage,
      required final String plagiarismRisk,
      required final String status,
      required final int totalSourcesFound,
      required final double aiContentPercentage,
      required final double humanContentPercentage,
      required final List<Source> detectedSources}) = _$PlagiarismResultImpl;

  factory _PlagiarismResult.fromJson(Map<String, dynamic> json) =
      _$PlagiarismResultImpl.fromJson;

  @override
  int get id;
  @override
  double get similarityPercentage;
  @override
  double get originalityPercentage;
  @override
  String get plagiarismRisk;
  @override
  String get status;
  @override
  int get totalSourcesFound;
  @override
  double get aiContentPercentage;
  @override
  double get humanContentPercentage;
  @override
  List<Source> get detectedSources;
  @override
  @JsonKey(ignore: true)
  _$$PlagiarismResultImplCopyWith<_$PlagiarismResultImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

ReadabilityResult _$ReadabilityResultFromJson(Map<String, dynamic> json) {
  return _ReadabilityResult.fromJson(json);
}

/// @nodoc
mixin _$ReadabilityResult {
  int get id => throw _privateConstructorUsedError;
  int get wordCount => throw _privateConstructorUsedError;
  int get sentenceCount => throw _privateConstructorUsedError;
  int get paragraphCount => throw _privateConstructorUsedError;
  double get fleschReadingEase => throw _privateConstructorUsedError;
  double get fleschKincaidGrade => throw _privateConstructorUsedError;
  double get gunningFogIndex => throw _privateConstructorUsedError;
  double get smogIndex => throw _privateConstructorUsedError;
  String get readabilityLevel => throw _privateConstructorUsedError;
  String get targetAudienceGradeLevel => throw _privateConstructorUsedError;
  double get complexityScore => throw _privateConstructorUsedError;
  double get avgWordLength => throw _privateConstructorUsedError;
  double get avgSentenceLength => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $ReadabilityResultCopyWith<ReadabilityResult> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $ReadabilityResultCopyWith<$Res> {
  factory $ReadabilityResultCopyWith(
          ReadabilityResult value, $Res Function(ReadabilityResult) then) =
      _$ReadabilityResultCopyWithImpl<$Res, ReadabilityResult>;
  @useResult
  $Res call(
      {int id,
      int wordCount,
      int sentenceCount,
      int paragraphCount,
      double fleschReadingEase,
      double fleschKincaidGrade,
      double gunningFogIndex,
      double smogIndex,
      String readabilityLevel,
      String targetAudienceGradeLevel,
      double complexityScore,
      double avgWordLength,
      double avgSentenceLength});
}

/// @nodoc
class _$ReadabilityResultCopyWithImpl<$Res, $Val extends ReadabilityResult>
    implements $ReadabilityResultCopyWith<$Res> {
  _$ReadabilityResultCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? wordCount = null,
    Object? sentenceCount = null,
    Object? paragraphCount = null,
    Object? fleschReadingEase = null,
    Object? fleschKincaidGrade = null,
    Object? gunningFogIndex = null,
    Object? smogIndex = null,
    Object? readabilityLevel = null,
    Object? targetAudienceGradeLevel = null,
    Object? complexityScore = null,
    Object? avgWordLength = null,
    Object? avgSentenceLength = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      wordCount: null == wordCount
          ? _value.wordCount
          : wordCount // ignore: cast_nullable_to_non_nullable
              as int,
      sentenceCount: null == sentenceCount
          ? _value.sentenceCount
          : sentenceCount // ignore: cast_nullable_to_non_nullable
              as int,
      paragraphCount: null == paragraphCount
          ? _value.paragraphCount
          : paragraphCount // ignore: cast_nullable_to_non_nullable
              as int,
      fleschReadingEase: null == fleschReadingEase
          ? _value.fleschReadingEase
          : fleschReadingEase // ignore: cast_nullable_to_non_nullable
              as double,
      fleschKincaidGrade: null == fleschKincaidGrade
          ? _value.fleschKincaidGrade
          : fleschKincaidGrade // ignore: cast_nullable_to_non_nullable
              as double,
      gunningFogIndex: null == gunningFogIndex
          ? _value.gunningFogIndex
          : gunningFogIndex // ignore: cast_nullable_to_non_nullable
              as double,
      smogIndex: null == smogIndex
          ? _value.smogIndex
          : smogIndex // ignore: cast_nullable_to_non_nullable
              as double,
      readabilityLevel: null == readabilityLevel
          ? _value.readabilityLevel
          : readabilityLevel // ignore: cast_nullable_to_non_nullable
              as String,
      targetAudienceGradeLevel: null == targetAudienceGradeLevel
          ? _value.targetAudienceGradeLevel
          : targetAudienceGradeLevel // ignore: cast_nullable_to_non_nullable
              as String,
      complexityScore: null == complexityScore
          ? _value.complexityScore
          : complexityScore // ignore: cast_nullable_to_non_nullable
              as double,
      avgWordLength: null == avgWordLength
          ? _value.avgWordLength
          : avgWordLength // ignore: cast_nullable_to_non_nullable
              as double,
      avgSentenceLength: null == avgSentenceLength
          ? _value.avgSentenceLength
          : avgSentenceLength // ignore: cast_nullable_to_non_nullable
              as double,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$ReadabilityResultImplCopyWith<$Res>
    implements $ReadabilityResultCopyWith<$Res> {
  factory _$$ReadabilityResultImplCopyWith(_$ReadabilityResultImpl value,
          $Res Function(_$ReadabilityResultImpl) then) =
      __$$ReadabilityResultImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int wordCount,
      int sentenceCount,
      int paragraphCount,
      double fleschReadingEase,
      double fleschKincaidGrade,
      double gunningFogIndex,
      double smogIndex,
      String readabilityLevel,
      String targetAudienceGradeLevel,
      double complexityScore,
      double avgWordLength,
      double avgSentenceLength});
}

/// @nodoc
class __$$ReadabilityResultImplCopyWithImpl<$Res>
    extends _$ReadabilityResultCopyWithImpl<$Res, _$ReadabilityResultImpl>
    implements _$$ReadabilityResultImplCopyWith<$Res> {
  __$$ReadabilityResultImplCopyWithImpl(_$ReadabilityResultImpl _value,
      $Res Function(_$ReadabilityResultImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? wordCount = null,
    Object? sentenceCount = null,
    Object? paragraphCount = null,
    Object? fleschReadingEase = null,
    Object? fleschKincaidGrade = null,
    Object? gunningFogIndex = null,
    Object? smogIndex = null,
    Object? readabilityLevel = null,
    Object? targetAudienceGradeLevel = null,
    Object? complexityScore = null,
    Object? avgWordLength = null,
    Object? avgSentenceLength = null,
  }) {
    return _then(_$ReadabilityResultImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      wordCount: null == wordCount
          ? _value.wordCount
          : wordCount // ignore: cast_nullable_to_non_nullable
              as int,
      sentenceCount: null == sentenceCount
          ? _value.sentenceCount
          : sentenceCount // ignore: cast_nullable_to_non_nullable
              as int,
      paragraphCount: null == paragraphCount
          ? _value.paragraphCount
          : paragraphCount // ignore: cast_nullable_to_non_nullable
              as int,
      fleschReadingEase: null == fleschReadingEase
          ? _value.fleschReadingEase
          : fleschReadingEase // ignore: cast_nullable_to_non_nullable
              as double,
      fleschKincaidGrade: null == fleschKincaidGrade
          ? _value.fleschKincaidGrade
          : fleschKincaidGrade // ignore: cast_nullable_to_non_nullable
              as double,
      gunningFogIndex: null == gunningFogIndex
          ? _value.gunningFogIndex
          : gunningFogIndex // ignore: cast_nullable_to_non_nullable
              as double,
      smogIndex: null == smogIndex
          ? _value.smogIndex
          : smogIndex // ignore: cast_nullable_to_non_nullable
              as double,
      readabilityLevel: null == readabilityLevel
          ? _value.readabilityLevel
          : readabilityLevel // ignore: cast_nullable_to_non_nullable
              as String,
      targetAudienceGradeLevel: null == targetAudienceGradeLevel
          ? _value.targetAudienceGradeLevel
          : targetAudienceGradeLevel // ignore: cast_nullable_to_non_nullable
              as String,
      complexityScore: null == complexityScore
          ? _value.complexityScore
          : complexityScore // ignore: cast_nullable_to_non_nullable
              as double,
      avgWordLength: null == avgWordLength
          ? _value.avgWordLength
          : avgWordLength // ignore: cast_nullable_to_non_nullable
              as double,
      avgSentenceLength: null == avgSentenceLength
          ? _value.avgSentenceLength
          : avgSentenceLength // ignore: cast_nullable_to_non_nullable
              as double,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$ReadabilityResultImpl implements _ReadabilityResult {
  const _$ReadabilityResultImpl(
      {required this.id,
      required this.wordCount,
      required this.sentenceCount,
      required this.paragraphCount,
      required this.fleschReadingEase,
      required this.fleschKincaidGrade,
      required this.gunningFogIndex,
      required this.smogIndex,
      required this.readabilityLevel,
      required this.targetAudienceGradeLevel,
      required this.complexityScore,
      required this.avgWordLength,
      required this.avgSentenceLength});

  factory _$ReadabilityResultImpl.fromJson(Map<String, dynamic> json) =>
      _$$ReadabilityResultImplFromJson(json);

  @override
  final int id;
  @override
  final int wordCount;
  @override
  final int sentenceCount;
  @override
  final int paragraphCount;
  @override
  final double fleschReadingEase;
  @override
  final double fleschKincaidGrade;
  @override
  final double gunningFogIndex;
  @override
  final double smogIndex;
  @override
  final String readabilityLevel;
  @override
  final String targetAudienceGradeLevel;
  @override
  final double complexityScore;
  @override
  final double avgWordLength;
  @override
  final double avgSentenceLength;

  @override
  String toString() {
    return 'ReadabilityResult(id: $id, wordCount: $wordCount, sentenceCount: $sentenceCount, paragraphCount: $paragraphCount, fleschReadingEase: $fleschReadingEase, fleschKincaidGrade: $fleschKincaidGrade, gunningFogIndex: $gunningFogIndex, smogIndex: $smogIndex, readabilityLevel: $readabilityLevel, targetAudienceGradeLevel: $targetAudienceGradeLevel, complexityScore: $complexityScore, avgWordLength: $avgWordLength, avgSentenceLength: $avgSentenceLength)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$ReadabilityResultImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.wordCount, wordCount) ||
                other.wordCount == wordCount) &&
            (identical(other.sentenceCount, sentenceCount) ||
                other.sentenceCount == sentenceCount) &&
            (identical(other.paragraphCount, paragraphCount) ||
                other.paragraphCount == paragraphCount) &&
            (identical(other.fleschReadingEase, fleschReadingEase) ||
                other.fleschReadingEase == fleschReadingEase) &&
            (identical(other.fleschKincaidGrade, fleschKincaidGrade) ||
                other.fleschKincaidGrade == fleschKincaidGrade) &&
            (identical(other.gunningFogIndex, gunningFogIndex) ||
                other.gunningFogIndex == gunningFogIndex) &&
            (identical(other.smogIndex, smogIndex) ||
                other.smogIndex == smogIndex) &&
            (identical(other.readabilityLevel, readabilityLevel) ||
                other.readabilityLevel == readabilityLevel) &&
            (identical(
                    other.targetAudienceGradeLevel, targetAudienceGradeLevel) ||
                other.targetAudienceGradeLevel == targetAudienceGradeLevel) &&
            (identical(other.complexityScore, complexityScore) ||
                other.complexityScore == complexityScore) &&
            (identical(other.avgWordLength, avgWordLength) ||
                other.avgWordLength == avgWordLength) &&
            (identical(other.avgSentenceLength, avgSentenceLength) ||
                other.avgSentenceLength == avgSentenceLength));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      wordCount,
      sentenceCount,
      paragraphCount,
      fleschReadingEase,
      fleschKincaidGrade,
      gunningFogIndex,
      smogIndex,
      readabilityLevel,
      targetAudienceGradeLevel,
      complexityScore,
      avgWordLength,
      avgSentenceLength);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$ReadabilityResultImplCopyWith<_$ReadabilityResultImpl> get copyWith =>
      __$$ReadabilityResultImplCopyWithImpl<_$ReadabilityResultImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$ReadabilityResultImplToJson(
      this,
    );
  }
}

abstract class _ReadabilityResult implements ReadabilityResult {
  const factory _ReadabilityResult(
      {required final int id,
      required final int wordCount,
      required final int sentenceCount,
      required final int paragraphCount,
      required final double fleschReadingEase,
      required final double fleschKincaidGrade,
      required final double gunningFogIndex,
      required final double smogIndex,
      required final String readabilityLevel,
      required final String targetAudienceGradeLevel,
      required final double complexityScore,
      required final double avgWordLength,
      required final double avgSentenceLength}) = _$ReadabilityResultImpl;

  factory _ReadabilityResult.fromJson(Map<String, dynamic> json) =
      _$ReadabilityResultImpl.fromJson;

  @override
  int get id;
  @override
  int get wordCount;
  @override
  int get sentenceCount;
  @override
  int get paragraphCount;
  @override
  double get fleschReadingEase;
  @override
  double get fleschKincaidGrade;
  @override
  double get gunningFogIndex;
  @override
  double get smogIndex;
  @override
  String get readabilityLevel;
  @override
  String get targetAudienceGradeLevel;
  @override
  double get complexityScore;
  @override
  double get avgWordLength;
  @override
  double get avgSentenceLength;
  @override
  @JsonKey(ignore: true)
  _$$ReadabilityResultImplCopyWith<_$ReadabilityResultImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

BrandVoiceViolation _$BrandVoiceViolationFromJson(Map<String, dynamic> json) {
  return _BrandVoiceViolation.fromJson(json);
}

/// @nodoc
mixin _$BrandVoiceViolation {
  int get id => throw _privateConstructorUsedError;
  String get violationType => throw _privateConstructorUsedError;
  String get severity => throw _privateConstructorUsedError;
  String get description => throw _privateConstructorUsedError;
  String get suggestedFix => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $BrandVoiceViolationCopyWith<BrandVoiceViolation> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $BrandVoiceViolationCopyWith<$Res> {
  factory $BrandVoiceViolationCopyWith(
          BrandVoiceViolation value, $Res Function(BrandVoiceViolation) then) =
      _$BrandVoiceViolationCopyWithImpl<$Res, BrandVoiceViolation>;
  @useResult
  $Res call(
      {int id,
      String violationType,
      String severity,
      String description,
      String suggestedFix});
}

/// @nodoc
class _$BrandVoiceViolationCopyWithImpl<$Res, $Val extends BrandVoiceViolation>
    implements $BrandVoiceViolationCopyWith<$Res> {
  _$BrandVoiceViolationCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? violationType = null,
    Object? severity = null,
    Object? description = null,
    Object? suggestedFix = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      violationType: null == violationType
          ? _value.violationType
          : violationType // ignore: cast_nullable_to_non_nullable
              as String,
      severity: null == severity
          ? _value.severity
          : severity // ignore: cast_nullable_to_non_nullable
              as String,
      description: null == description
          ? _value.description
          : description // ignore: cast_nullable_to_non_nullable
              as String,
      suggestedFix: null == suggestedFix
          ? _value.suggestedFix
          : suggestedFix // ignore: cast_nullable_to_non_nullable
              as String,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$BrandVoiceViolationImplCopyWith<$Res>
    implements $BrandVoiceViolationCopyWith<$Res> {
  factory _$$BrandVoiceViolationImplCopyWith(_$BrandVoiceViolationImpl value,
          $Res Function(_$BrandVoiceViolationImpl) then) =
      __$$BrandVoiceViolationImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String violationType,
      String severity,
      String description,
      String suggestedFix});
}

/// @nodoc
class __$$BrandVoiceViolationImplCopyWithImpl<$Res>
    extends _$BrandVoiceViolationCopyWithImpl<$Res, _$BrandVoiceViolationImpl>
    implements _$$BrandVoiceViolationImplCopyWith<$Res> {
  __$$BrandVoiceViolationImplCopyWithImpl(_$BrandVoiceViolationImpl _value,
      $Res Function(_$BrandVoiceViolationImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? violationType = null,
    Object? severity = null,
    Object? description = null,
    Object? suggestedFix = null,
  }) {
    return _then(_$BrandVoiceViolationImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      violationType: null == violationType
          ? _value.violationType
          : violationType // ignore: cast_nullable_to_non_nullable
              as String,
      severity: null == severity
          ? _value.severity
          : severity // ignore: cast_nullable_to_non_nullable
              as String,
      description: null == description
          ? _value.description
          : description // ignore: cast_nullable_to_non_nullable
              as String,
      suggestedFix: null == suggestedFix
          ? _value.suggestedFix
          : suggestedFix // ignore: cast_nullable_to_non_nullable
              as String,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$BrandVoiceViolationImpl implements _BrandVoiceViolation {
  const _$BrandVoiceViolationImpl(
      {required this.id,
      required this.violationType,
      required this.severity,
      required this.description,
      required this.suggestedFix});

  factory _$BrandVoiceViolationImpl.fromJson(Map<String, dynamic> json) =>
      _$$BrandVoiceViolationImplFromJson(json);

  @override
  final int id;
  @override
  final String violationType;
  @override
  final String severity;
  @override
  final String description;
  @override
  final String suggestedFix;

  @override
  String toString() {
    return 'BrandVoiceViolation(id: $id, violationType: $violationType, severity: $severity, description: $description, suggestedFix: $suggestedFix)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$BrandVoiceViolationImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.violationType, violationType) ||
                other.violationType == violationType) &&
            (identical(other.severity, severity) ||
                other.severity == severity) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.suggestedFix, suggestedFix) ||
                other.suggestedFix == suggestedFix));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType, id, violationType, severity, description, suggestedFix);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$BrandVoiceViolationImplCopyWith<_$BrandVoiceViolationImpl> get copyWith =>
      __$$BrandVoiceViolationImplCopyWithImpl<_$BrandVoiceViolationImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$BrandVoiceViolationImplToJson(
      this,
    );
  }
}

abstract class _BrandVoiceViolation implements BrandVoiceViolation {
  const factory _BrandVoiceViolation(
      {required final int id,
      required final String violationType,
      required final String severity,
      required final String description,
      required final String suggestedFix}) = _$BrandVoiceViolationImpl;

  factory _BrandVoiceViolation.fromJson(Map<String, dynamic> json) =
      _$BrandVoiceViolationImpl.fromJson;

  @override
  int get id;
  @override
  String get violationType;
  @override
  String get severity;
  @override
  String get description;
  @override
  String get suggestedFix;
  @override
  @JsonKey(ignore: true)
  _$$BrandVoiceViolationImplCopyWith<_$BrandVoiceViolationImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

BrandVoiceResult _$BrandVoiceResultFromJson(Map<String, dynamic> json) {
  return _BrandVoiceResult.fromJson(json);
}

/// @nodoc
mixin _$BrandVoiceResult {
  int get id => throw _privateConstructorUsedError;
  double get consistencyScore => throw _privateConstructorUsedError;
  double get compliancePercentage => throw _privateConstructorUsedError;
  String get brandAlignment => throw _privateConstructorUsedError;
  int get totalViolations => throw _privateConstructorUsedError;
  int get toneViolations => throw _privateConstructorUsedError;
  int get styleViolations => throw _privateConstructorUsedError;
  int get terminologyViolations => throw _privateConstructorUsedError;
  List<BrandVoiceViolation> get violations =>
      throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $BrandVoiceResultCopyWith<BrandVoiceResult> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $BrandVoiceResultCopyWith<$Res> {
  factory $BrandVoiceResultCopyWith(
          BrandVoiceResult value, $Res Function(BrandVoiceResult) then) =
      _$BrandVoiceResultCopyWithImpl<$Res, BrandVoiceResult>;
  @useResult
  $Res call(
      {int id,
      double consistencyScore,
      double compliancePercentage,
      String brandAlignment,
      int totalViolations,
      int toneViolations,
      int styleViolations,
      int terminologyViolations,
      List<BrandVoiceViolation> violations});
}

/// @nodoc
class _$BrandVoiceResultCopyWithImpl<$Res, $Val extends BrandVoiceResult>
    implements $BrandVoiceResultCopyWith<$Res> {
  _$BrandVoiceResultCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? consistencyScore = null,
    Object? compliancePercentage = null,
    Object? brandAlignment = null,
    Object? totalViolations = null,
    Object? toneViolations = null,
    Object? styleViolations = null,
    Object? terminologyViolations = null,
    Object? violations = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      consistencyScore: null == consistencyScore
          ? _value.consistencyScore
          : consistencyScore // ignore: cast_nullable_to_non_nullable
              as double,
      compliancePercentage: null == compliancePercentage
          ? _value.compliancePercentage
          : compliancePercentage // ignore: cast_nullable_to_non_nullable
              as double,
      brandAlignment: null == brandAlignment
          ? _value.brandAlignment
          : brandAlignment // ignore: cast_nullable_to_non_nullable
              as String,
      totalViolations: null == totalViolations
          ? _value.totalViolations
          : totalViolations // ignore: cast_nullable_to_non_nullable
              as int,
      toneViolations: null == toneViolations
          ? _value.toneViolations
          : toneViolations // ignore: cast_nullable_to_non_nullable
              as int,
      styleViolations: null == styleViolations
          ? _value.styleViolations
          : styleViolations // ignore: cast_nullable_to_non_nullable
              as int,
      terminologyViolations: null == terminologyViolations
          ? _value.terminologyViolations
          : terminologyViolations // ignore: cast_nullable_to_non_nullable
              as int,
      violations: null == violations
          ? _value.violations
          : violations // ignore: cast_nullable_to_non_nullable
              as List<BrandVoiceViolation>,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$BrandVoiceResultImplCopyWith<$Res>
    implements $BrandVoiceResultCopyWith<$Res> {
  factory _$$BrandVoiceResultImplCopyWith(_$BrandVoiceResultImpl value,
          $Res Function(_$BrandVoiceResultImpl) then) =
      __$$BrandVoiceResultImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      double consistencyScore,
      double compliancePercentage,
      String brandAlignment,
      int totalViolations,
      int toneViolations,
      int styleViolations,
      int terminologyViolations,
      List<BrandVoiceViolation> violations});
}

/// @nodoc
class __$$BrandVoiceResultImplCopyWithImpl<$Res>
    extends _$BrandVoiceResultCopyWithImpl<$Res, _$BrandVoiceResultImpl>
    implements _$$BrandVoiceResultImplCopyWith<$Res> {
  __$$BrandVoiceResultImplCopyWithImpl(_$BrandVoiceResultImpl _value,
      $Res Function(_$BrandVoiceResultImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? consistencyScore = null,
    Object? compliancePercentage = null,
    Object? brandAlignment = null,
    Object? totalViolations = null,
    Object? toneViolations = null,
    Object? styleViolations = null,
    Object? terminologyViolations = null,
    Object? violations = null,
  }) {
    return _then(_$BrandVoiceResultImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      consistencyScore: null == consistencyScore
          ? _value.consistencyScore
          : consistencyScore // ignore: cast_nullable_to_non_nullable
              as double,
      compliancePercentage: null == compliancePercentage
          ? _value.compliancePercentage
          : compliancePercentage // ignore: cast_nullable_to_non_nullable
              as double,
      brandAlignment: null == brandAlignment
          ? _value.brandAlignment
          : brandAlignment // ignore: cast_nullable_to_non_nullable
              as String,
      totalViolations: null == totalViolations
          ? _value.totalViolations
          : totalViolations // ignore: cast_nullable_to_non_nullable
              as int,
      toneViolations: null == toneViolations
          ? _value.toneViolations
          : toneViolations // ignore: cast_nullable_to_non_nullable
              as int,
      styleViolations: null == styleViolations
          ? _value.styleViolations
          : styleViolations // ignore: cast_nullable_to_non_nullable
              as int,
      terminologyViolations: null == terminologyViolations
          ? _value.terminologyViolations
          : terminologyViolations // ignore: cast_nullable_to_non_nullable
              as int,
      violations: null == violations
          ? _value._violations
          : violations // ignore: cast_nullable_to_non_nullable
              as List<BrandVoiceViolation>,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$BrandVoiceResultImpl implements _BrandVoiceResult {
  const _$BrandVoiceResultImpl(
      {required this.id,
      required this.consistencyScore,
      required this.compliancePercentage,
      required this.brandAlignment,
      required this.totalViolations,
      required this.toneViolations,
      required this.styleViolations,
      required this.terminologyViolations,
      required final List<BrandVoiceViolation> violations})
      : _violations = violations;

  factory _$BrandVoiceResultImpl.fromJson(Map<String, dynamic> json) =>
      _$$BrandVoiceResultImplFromJson(json);

  @override
  final int id;
  @override
  final double consistencyScore;
  @override
  final double compliancePercentage;
  @override
  final String brandAlignment;
  @override
  final int totalViolations;
  @override
  final int toneViolations;
  @override
  final int styleViolations;
  @override
  final int terminologyViolations;
  final List<BrandVoiceViolation> _violations;
  @override
  List<BrandVoiceViolation> get violations {
    if (_violations is EqualUnmodifiableListView) return _violations;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_violations);
  }

  @override
  String toString() {
    return 'BrandVoiceResult(id: $id, consistencyScore: $consistencyScore, compliancePercentage: $compliancePercentage, brandAlignment: $brandAlignment, totalViolations: $totalViolations, toneViolations: $toneViolations, styleViolations: $styleViolations, terminologyViolations: $terminologyViolations, violations: $violations)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$BrandVoiceResultImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.consistencyScore, consistencyScore) ||
                other.consistencyScore == consistencyScore) &&
            (identical(other.compliancePercentage, compliancePercentage) ||
                other.compliancePercentage == compliancePercentage) &&
            (identical(other.brandAlignment, brandAlignment) ||
                other.brandAlignment == brandAlignment) &&
            (identical(other.totalViolations, totalViolations) ||
                other.totalViolations == totalViolations) &&
            (identical(other.toneViolations, toneViolations) ||
                other.toneViolations == toneViolations) &&
            (identical(other.styleViolations, styleViolations) ||
                other.styleViolations == styleViolations) &&
            (identical(other.terminologyViolations, terminologyViolations) ||
                other.terminologyViolations == terminologyViolations) &&
            const DeepCollectionEquality()
                .equals(other._violations, _violations));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      consistencyScore,
      compliancePercentage,
      brandAlignment,
      totalViolations,
      toneViolations,
      styleViolations,
      terminologyViolations,
      const DeepCollectionEquality().hash(_violations));

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$BrandVoiceResultImplCopyWith<_$BrandVoiceResultImpl> get copyWith =>
      __$$BrandVoiceResultImplCopyWithImpl<_$BrandVoiceResultImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$BrandVoiceResultImplToJson(
      this,
    );
  }
}

abstract class _BrandVoiceResult implements BrandVoiceResult {
  const factory _BrandVoiceResult(
          {required final int id,
          required final double consistencyScore,
          required final double compliancePercentage,
          required final String brandAlignment,
          required final int totalViolations,
          required final int toneViolations,
          required final int styleViolations,
          required final int terminologyViolations,
          required final List<BrandVoiceViolation> violations}) =
      _$BrandVoiceResultImpl;

  factory _BrandVoiceResult.fromJson(Map<String, dynamic> json) =
      _$BrandVoiceResultImpl.fromJson;

  @override
  int get id;
  @override
  double get consistencyScore;
  @override
  double get compliancePercentage;
  @override
  String get brandAlignment;
  @override
  int get totalViolations;
  @override
  int get toneViolations;
  @override
  int get styleViolations;
  @override
  int get terminologyViolations;
  @override
  List<BrandVoiceViolation> get violations;
  @override
  @JsonKey(ignore: true)
  _$$BrandVoiceResultImplCopyWith<_$BrandVoiceResultImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

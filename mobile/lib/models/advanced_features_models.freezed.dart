// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'advanced_features_models.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
    'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models');

PersonalizationProfile _$PersonalizationProfileFromJson(
    Map<String, dynamic> json) {
  return _PersonalizationProfile.fromJson(json);
}

/// @nodoc
mixin _$PersonalizationProfile {
  int get id => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  Map<String, double> get contentPreferences =>
      throw _privateConstructorUsedError;
  Map<String, double> get authorPreferences =>
      throw _privateConstructorUsedError;
  Map<String, double> get categoryWeights => throw _privateConstructorUsedError;
  String? get readingTimePreference => throw _privateConstructorUsedError;
  double get personalizationScore => throw _privateConstructorUsedError;
  DateTime get lastUpdated => throw _privateConstructorUsedError;

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
      Map<String, double> contentPreferences,
      Map<String, double> authorPreferences,
      Map<String, double> categoryWeights,
      String? readingTimePreference,
      double personalizationScore,
      DateTime lastUpdated});
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
    Object? contentPreferences = null,
    Object? authorPreferences = null,
    Object? categoryWeights = null,
    Object? readingTimePreference = freezed,
    Object? personalizationScore = null,
    Object? lastUpdated = null,
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
      contentPreferences: null == contentPreferences
          ? _value.contentPreferences
          : contentPreferences // ignore: cast_nullable_to_non_nullable
              as Map<String, double>,
      authorPreferences: null == authorPreferences
          ? _value.authorPreferences
          : authorPreferences // ignore: cast_nullable_to_non_nullable
              as Map<String, double>,
      categoryWeights: null == categoryWeights
          ? _value.categoryWeights
          : categoryWeights // ignore: cast_nullable_to_non_nullable
              as Map<String, double>,
      readingTimePreference: freezed == readingTimePreference
          ? _value.readingTimePreference
          : readingTimePreference // ignore: cast_nullable_to_non_nullable
              as String?,
      personalizationScore: null == personalizationScore
          ? _value.personalizationScore
          : personalizationScore // ignore: cast_nullable_to_non_nullable
              as double,
      lastUpdated: null == lastUpdated
          ? _value.lastUpdated
          : lastUpdated // ignore: cast_nullable_to_non_nullable
              as DateTime,
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
      Map<String, double> contentPreferences,
      Map<String, double> authorPreferences,
      Map<String, double> categoryWeights,
      String? readingTimePreference,
      double personalizationScore,
      DateTime lastUpdated});
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
    Object? contentPreferences = null,
    Object? authorPreferences = null,
    Object? categoryWeights = null,
    Object? readingTimePreference = freezed,
    Object? personalizationScore = null,
    Object? lastUpdated = null,
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
      contentPreferences: null == contentPreferences
          ? _value._contentPreferences
          : contentPreferences // ignore: cast_nullable_to_non_nullable
              as Map<String, double>,
      authorPreferences: null == authorPreferences
          ? _value._authorPreferences
          : authorPreferences // ignore: cast_nullable_to_non_nullable
              as Map<String, double>,
      categoryWeights: null == categoryWeights
          ? _value._categoryWeights
          : categoryWeights // ignore: cast_nullable_to_non_nullable
              as Map<String, double>,
      readingTimePreference: freezed == readingTimePreference
          ? _value.readingTimePreference
          : readingTimePreference // ignore: cast_nullable_to_non_nullable
              as String?,
      personalizationScore: null == personalizationScore
          ? _value.personalizationScore
          : personalizationScore // ignore: cast_nullable_to_non_nullable
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
class _$PersonalizationProfileImpl implements _PersonalizationProfile {
  const _$PersonalizationProfileImpl(
      {required this.id,
      required this.userId,
      required final Map<String, double> contentPreferences,
      required final Map<String, double> authorPreferences,
      required final Map<String, double> categoryWeights,
      this.readingTimePreference,
      required this.personalizationScore,
      required this.lastUpdated})
      : _contentPreferences = contentPreferences,
        _authorPreferences = authorPreferences,
        _categoryWeights = categoryWeights;

  factory _$PersonalizationProfileImpl.fromJson(Map<String, dynamic> json) =>
      _$$PersonalizationProfileImplFromJson(json);

  @override
  final int id;
  @override
  final int userId;
  final Map<String, double> _contentPreferences;
  @override
  Map<String, double> get contentPreferences {
    if (_contentPreferences is EqualUnmodifiableMapView)
      return _contentPreferences;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(_contentPreferences);
  }

  final Map<String, double> _authorPreferences;
  @override
  Map<String, double> get authorPreferences {
    if (_authorPreferences is EqualUnmodifiableMapView)
      return _authorPreferences;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(_authorPreferences);
  }

  final Map<String, double> _categoryWeights;
  @override
  Map<String, double> get categoryWeights {
    if (_categoryWeights is EqualUnmodifiableMapView) return _categoryWeights;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(_categoryWeights);
  }

  @override
  final String? readingTimePreference;
  @override
  final double personalizationScore;
  @override
  final DateTime lastUpdated;

  @override
  String toString() {
    return 'PersonalizationProfile(id: $id, userId: $userId, contentPreferences: $contentPreferences, authorPreferences: $authorPreferences, categoryWeights: $categoryWeights, readingTimePreference: $readingTimePreference, personalizationScore: $personalizationScore, lastUpdated: $lastUpdated)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$PersonalizationProfileImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            const DeepCollectionEquality()
                .equals(other._contentPreferences, _contentPreferences) &&
            const DeepCollectionEquality()
                .equals(other._authorPreferences, _authorPreferences) &&
            const DeepCollectionEquality()
                .equals(other._categoryWeights, _categoryWeights) &&
            (identical(other.readingTimePreference, readingTimePreference) ||
                other.readingTimePreference == readingTimePreference) &&
            (identical(other.personalizationScore, personalizationScore) ||
                other.personalizationScore == personalizationScore) &&
            (identical(other.lastUpdated, lastUpdated) ||
                other.lastUpdated == lastUpdated));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      userId,
      const DeepCollectionEquality().hash(_contentPreferences),
      const DeepCollectionEquality().hash(_authorPreferences),
      const DeepCollectionEquality().hash(_categoryWeights),
      readingTimePreference,
      personalizationScore,
      lastUpdated);

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
      required final Map<String, double> contentPreferences,
      required final Map<String, double> authorPreferences,
      required final Map<String, double> categoryWeights,
      final String? readingTimePreference,
      required final double personalizationScore,
      required final DateTime lastUpdated}) = _$PersonalizationProfileImpl;

  factory _PersonalizationProfile.fromJson(Map<String, dynamic> json) =
      _$PersonalizationProfileImpl.fromJson;

  @override
  int get id;
  @override
  int get userId;
  @override
  Map<String, double> get contentPreferences;
  @override
  Map<String, double> get authorPreferences;
  @override
  Map<String, double> get categoryWeights;
  @override
  String? get readingTimePreference;
  @override
  double get personalizationScore;
  @override
  DateTime get lastUpdated;
  @override
  @JsonKey(ignore: true)
  _$$PersonalizationProfileImplCopyWith<_$PersonalizationProfileImpl>
      get copyWith => throw _privateConstructorUsedError;
}

ContentRecommendation _$ContentRecommendationFromJson(
    Map<String, dynamic> json) {
  return _ContentRecommendation.fromJson(json);
}

/// @nodoc
mixin _$ContentRecommendation {
  int get id => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  int get contentId => throw _privateConstructorUsedError;
  String get type => throw _privateConstructorUsedError;
  double get similarityScore => throw _privateConstructorUsedError;
  double get relevanceScore => throw _privateConstructorUsedError;
  bool get clicked => throw _privateConstructorUsedError;
  bool get conversion => throw _privateConstructorUsedError;
  DateTime? get clickTimestamp => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $ContentRecommendationCopyWith<ContentRecommendation> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $ContentRecommendationCopyWith<$Res> {
  factory $ContentRecommendationCopyWith(ContentRecommendation value,
          $Res Function(ContentRecommendation) then) =
      _$ContentRecommendationCopyWithImpl<$Res, ContentRecommendation>;
  @useResult
  $Res call(
      {int id,
      int userId,
      int contentId,
      String type,
      double similarityScore,
      double relevanceScore,
      bool clicked,
      bool conversion,
      DateTime? clickTimestamp});
}

/// @nodoc
class _$ContentRecommendationCopyWithImpl<$Res,
        $Val extends ContentRecommendation>
    implements $ContentRecommendationCopyWith<$Res> {
  _$ContentRecommendationCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? contentId = null,
    Object? type = null,
    Object? similarityScore = null,
    Object? relevanceScore = null,
    Object? clicked = null,
    Object? conversion = null,
    Object? clickTimestamp = freezed,
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
      contentId: null == contentId
          ? _value.contentId
          : contentId // ignore: cast_nullable_to_non_nullable
              as int,
      type: null == type
          ? _value.type
          : type // ignore: cast_nullable_to_non_nullable
              as String,
      similarityScore: null == similarityScore
          ? _value.similarityScore
          : similarityScore // ignore: cast_nullable_to_non_nullable
              as double,
      relevanceScore: null == relevanceScore
          ? _value.relevanceScore
          : relevanceScore // ignore: cast_nullable_to_non_nullable
              as double,
      clicked: null == clicked
          ? _value.clicked
          : clicked // ignore: cast_nullable_to_non_nullable
              as bool,
      conversion: null == conversion
          ? _value.conversion
          : conversion // ignore: cast_nullable_to_non_nullable
              as bool,
      clickTimestamp: freezed == clickTimestamp
          ? _value.clickTimestamp
          : clickTimestamp // ignore: cast_nullable_to_non_nullable
              as DateTime?,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$ContentRecommendationImplCopyWith<$Res>
    implements $ContentRecommendationCopyWith<$Res> {
  factory _$$ContentRecommendationImplCopyWith(
          _$ContentRecommendationImpl value,
          $Res Function(_$ContentRecommendationImpl) then) =
      __$$ContentRecommendationImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int userId,
      int contentId,
      String type,
      double similarityScore,
      double relevanceScore,
      bool clicked,
      bool conversion,
      DateTime? clickTimestamp});
}

/// @nodoc
class __$$ContentRecommendationImplCopyWithImpl<$Res>
    extends _$ContentRecommendationCopyWithImpl<$Res,
        _$ContentRecommendationImpl>
    implements _$$ContentRecommendationImplCopyWith<$Res> {
  __$$ContentRecommendationImplCopyWithImpl(_$ContentRecommendationImpl _value,
      $Res Function(_$ContentRecommendationImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? contentId = null,
    Object? type = null,
    Object? similarityScore = null,
    Object? relevanceScore = null,
    Object? clicked = null,
    Object? conversion = null,
    Object? clickTimestamp = freezed,
  }) {
    return _then(_$ContentRecommendationImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      contentId: null == contentId
          ? _value.contentId
          : contentId // ignore: cast_nullable_to_non_nullable
              as int,
      type: null == type
          ? _value.type
          : type // ignore: cast_nullable_to_non_nullable
              as String,
      similarityScore: null == similarityScore
          ? _value.similarityScore
          : similarityScore // ignore: cast_nullable_to_non_nullable
              as double,
      relevanceScore: null == relevanceScore
          ? _value.relevanceScore
          : relevanceScore // ignore: cast_nullable_to_non_nullable
              as double,
      clicked: null == clicked
          ? _value.clicked
          : clicked // ignore: cast_nullable_to_non_nullable
              as bool,
      conversion: null == conversion
          ? _value.conversion
          : conversion // ignore: cast_nullable_to_non_nullable
              as bool,
      clickTimestamp: freezed == clickTimestamp
          ? _value.clickTimestamp
          : clickTimestamp // ignore: cast_nullable_to_non_nullable
              as DateTime?,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$ContentRecommendationImpl implements _ContentRecommendation {
  const _$ContentRecommendationImpl(
      {required this.id,
      required this.userId,
      required this.contentId,
      required this.type,
      required this.similarityScore,
      required this.relevanceScore,
      required this.clicked,
      required this.conversion,
      this.clickTimestamp});

  factory _$ContentRecommendationImpl.fromJson(Map<String, dynamic> json) =>
      _$$ContentRecommendationImplFromJson(json);

  @override
  final int id;
  @override
  final int userId;
  @override
  final int contentId;
  @override
  final String type;
  @override
  final double similarityScore;
  @override
  final double relevanceScore;
  @override
  final bool clicked;
  @override
  final bool conversion;
  @override
  final DateTime? clickTimestamp;

  @override
  String toString() {
    return 'ContentRecommendation(id: $id, userId: $userId, contentId: $contentId, type: $type, similarityScore: $similarityScore, relevanceScore: $relevanceScore, clicked: $clicked, conversion: $conversion, clickTimestamp: $clickTimestamp)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$ContentRecommendationImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.contentId, contentId) ||
                other.contentId == contentId) &&
            (identical(other.type, type) || other.type == type) &&
            (identical(other.similarityScore, similarityScore) ||
                other.similarityScore == similarityScore) &&
            (identical(other.relevanceScore, relevanceScore) ||
                other.relevanceScore == relevanceScore) &&
            (identical(other.clicked, clicked) || other.clicked == clicked) &&
            (identical(other.conversion, conversion) ||
                other.conversion == conversion) &&
            (identical(other.clickTimestamp, clickTimestamp) ||
                other.clickTimestamp == clickTimestamp));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, id, userId, contentId, type,
      similarityScore, relevanceScore, clicked, conversion, clickTimestamp);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$ContentRecommendationImplCopyWith<_$ContentRecommendationImpl>
      get copyWith => __$$ContentRecommendationImplCopyWithImpl<
          _$ContentRecommendationImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$ContentRecommendationImplToJson(
      this,
    );
  }
}

abstract class _ContentRecommendation implements ContentRecommendation {
  const factory _ContentRecommendation(
      {required final int id,
      required final int userId,
      required final int contentId,
      required final String type,
      required final double similarityScore,
      required final double relevanceScore,
      required final bool clicked,
      required final bool conversion,
      final DateTime? clickTimestamp}) = _$ContentRecommendationImpl;

  factory _ContentRecommendation.fromJson(Map<String, dynamic> json) =
      _$ContentRecommendationImpl.fromJson;

  @override
  int get id;
  @override
  int get userId;
  @override
  int get contentId;
  @override
  String get type;
  @override
  double get similarityScore;
  @override
  double get relevanceScore;
  @override
  bool get clicked;
  @override
  bool get conversion;
  @override
  DateTime? get clickTimestamp;
  @override
  @JsonKey(ignore: true)
  _$$ContentRecommendationImplCopyWith<_$ContentRecommendationImpl>
      get copyWith => throw _privateConstructorUsedError;
}

RecommendationEffectiveness _$RecommendationEffectivenessFromJson(
    Map<String, dynamic> json) {
  return _RecommendationEffectiveness.fromJson(json);
}

/// @nodoc
mixin _$RecommendationEffectiveness {
  int get totalRecommendations => throw _privateConstructorUsedError;
  int get clicks => throw _privateConstructorUsedError;
  int get conversions => throw _privateConstructorUsedError;
  double get clickThroughRate => throw _privateConstructorUsedError;
  double get conversionRate => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $RecommendationEffectivenessCopyWith<RecommendationEffectiveness>
      get copyWith => throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $RecommendationEffectivenessCopyWith<$Res> {
  factory $RecommendationEffectivenessCopyWith(
          RecommendationEffectiveness value,
          $Res Function(RecommendationEffectiveness) then) =
      _$RecommendationEffectivenessCopyWithImpl<$Res,
          RecommendationEffectiveness>;
  @useResult
  $Res call(
      {int totalRecommendations,
      int clicks,
      int conversions,
      double clickThroughRate,
      double conversionRate});
}

/// @nodoc
class _$RecommendationEffectivenessCopyWithImpl<$Res,
        $Val extends RecommendationEffectiveness>
    implements $RecommendationEffectivenessCopyWith<$Res> {
  _$RecommendationEffectivenessCopyWithImpl(this._value, this._then);

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
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$RecommendationEffectivenessImplCopyWith<$Res>
    implements $RecommendationEffectivenessCopyWith<$Res> {
  factory _$$RecommendationEffectivenessImplCopyWith(
          _$RecommendationEffectivenessImpl value,
          $Res Function(_$RecommendationEffectivenessImpl) then) =
      __$$RecommendationEffectivenessImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int totalRecommendations,
      int clicks,
      int conversions,
      double clickThroughRate,
      double conversionRate});
}

/// @nodoc
class __$$RecommendationEffectivenessImplCopyWithImpl<$Res>
    extends _$RecommendationEffectivenessCopyWithImpl<$Res,
        _$RecommendationEffectivenessImpl>
    implements _$$RecommendationEffectivenessImplCopyWith<$Res> {
  __$$RecommendationEffectivenessImplCopyWithImpl(
      _$RecommendationEffectivenessImpl _value,
      $Res Function(_$RecommendationEffectivenessImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? totalRecommendations = null,
    Object? clicks = null,
    Object? conversions = null,
    Object? clickThroughRate = null,
    Object? conversionRate = null,
  }) {
    return _then(_$RecommendationEffectivenessImpl(
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
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$RecommendationEffectivenessImpl
    implements _RecommendationEffectiveness {
  const _$RecommendationEffectivenessImpl(
      {required this.totalRecommendations,
      required this.clicks,
      required this.conversions,
      required this.clickThroughRate,
      required this.conversionRate});

  factory _$RecommendationEffectivenessImpl.fromJson(
          Map<String, dynamic> json) =>
      _$$RecommendationEffectivenessImplFromJson(json);

  @override
  final int totalRecommendations;
  @override
  final int clicks;
  @override
  final int conversions;
  @override
  final double clickThroughRate;
  @override
  final double conversionRate;

  @override
  String toString() {
    return 'RecommendationEffectiveness(totalRecommendations: $totalRecommendations, clicks: $clicks, conversions: $conversions, clickThroughRate: $clickThroughRate, conversionRate: $conversionRate)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$RecommendationEffectivenessImpl &&
            (identical(other.totalRecommendations, totalRecommendations) ||
                other.totalRecommendations == totalRecommendations) &&
            (identical(other.clicks, clicks) || other.clicks == clicks) &&
            (identical(other.conversions, conversions) ||
                other.conversions == conversions) &&
            (identical(other.clickThroughRate, clickThroughRate) ||
                other.clickThroughRate == clickThroughRate) &&
            (identical(other.conversionRate, conversionRate) ||
                other.conversionRate == conversionRate));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, totalRecommendations, clicks,
      conversions, clickThroughRate, conversionRate);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$RecommendationEffectivenessImplCopyWith<_$RecommendationEffectivenessImpl>
      get copyWith => __$$RecommendationEffectivenessImplCopyWithImpl<
          _$RecommendationEffectivenessImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$RecommendationEffectivenessImplToJson(
      this,
    );
  }
}

abstract class _RecommendationEffectiveness
    implements RecommendationEffectiveness {
  const factory _RecommendationEffectiveness(
          {required final int totalRecommendations,
          required final int clicks,
          required final int conversions,
          required final double clickThroughRate,
          required final double conversionRate}) =
      _$RecommendationEffectivenessImpl;

  factory _RecommendationEffectiveness.fromJson(Map<String, dynamic> json) =
      _$RecommendationEffectivenessImpl.fromJson;

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
  @JsonKey(ignore: true)
  _$$RecommendationEffectivenessImplCopyWith<_$RecommendationEffectivenessImpl>
      get copyWith => throw _privateConstructorUsedError;
}

RetentionMetric _$RetentionMetricFromJson(Map<String, dynamic> json) {
  return _RetentionMetric.fromJson(json);
}

/// @nodoc
mixin _$RetentionMetric {
  int get id => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  String get status => throw _privateConstructorUsedError;
  double get churnProbability => throw _privateConstructorUsedError;
  int get daysSinceActive => throw _privateConstructorUsedError;
  String? get engagementTrend => throw _privateConstructorUsedError;
  String? get retentionSegment => throw _privateConstructorUsedError;
  String? get recommendedAction => throw _privateConstructorUsedError;
  DateTime? get lastEngagement => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $RetentionMetricCopyWith<RetentionMetric> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $RetentionMetricCopyWith<$Res> {
  factory $RetentionMetricCopyWith(
          RetentionMetric value, $Res Function(RetentionMetric) then) =
      _$RetentionMetricCopyWithImpl<$Res, RetentionMetric>;
  @useResult
  $Res call(
      {int id,
      int userId,
      String status,
      double churnProbability,
      int daysSinceActive,
      String? engagementTrend,
      String? retentionSegment,
      String? recommendedAction,
      DateTime? lastEngagement});
}

/// @nodoc
class _$RetentionMetricCopyWithImpl<$Res, $Val extends RetentionMetric>
    implements $RetentionMetricCopyWith<$Res> {
  _$RetentionMetricCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? status = null,
    Object? churnProbability = null,
    Object? daysSinceActive = null,
    Object? engagementTrend = freezed,
    Object? retentionSegment = freezed,
    Object? recommendedAction = freezed,
    Object? lastEngagement = freezed,
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
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      churnProbability: null == churnProbability
          ? _value.churnProbability
          : churnProbability // ignore: cast_nullable_to_non_nullable
              as double,
      daysSinceActive: null == daysSinceActive
          ? _value.daysSinceActive
          : daysSinceActive // ignore: cast_nullable_to_non_nullable
              as int,
      engagementTrend: freezed == engagementTrend
          ? _value.engagementTrend
          : engagementTrend // ignore: cast_nullable_to_non_nullable
              as String?,
      retentionSegment: freezed == retentionSegment
          ? _value.retentionSegment
          : retentionSegment // ignore: cast_nullable_to_non_nullable
              as String?,
      recommendedAction: freezed == recommendedAction
          ? _value.recommendedAction
          : recommendedAction // ignore: cast_nullable_to_non_nullable
              as String?,
      lastEngagement: freezed == lastEngagement
          ? _value.lastEngagement
          : lastEngagement // ignore: cast_nullable_to_non_nullable
              as DateTime?,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$RetentionMetricImplCopyWith<$Res>
    implements $RetentionMetricCopyWith<$Res> {
  factory _$$RetentionMetricImplCopyWith(_$RetentionMetricImpl value,
          $Res Function(_$RetentionMetricImpl) then) =
      __$$RetentionMetricImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int userId,
      String status,
      double churnProbability,
      int daysSinceActive,
      String? engagementTrend,
      String? retentionSegment,
      String? recommendedAction,
      DateTime? lastEngagement});
}

/// @nodoc
class __$$RetentionMetricImplCopyWithImpl<$Res>
    extends _$RetentionMetricCopyWithImpl<$Res, _$RetentionMetricImpl>
    implements _$$RetentionMetricImplCopyWith<$Res> {
  __$$RetentionMetricImplCopyWithImpl(
      _$RetentionMetricImpl _value, $Res Function(_$RetentionMetricImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? status = null,
    Object? churnProbability = null,
    Object? daysSinceActive = null,
    Object? engagementTrend = freezed,
    Object? retentionSegment = freezed,
    Object? recommendedAction = freezed,
    Object? lastEngagement = freezed,
  }) {
    return _then(_$RetentionMetricImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      churnProbability: null == churnProbability
          ? _value.churnProbability
          : churnProbability // ignore: cast_nullable_to_non_nullable
              as double,
      daysSinceActive: null == daysSinceActive
          ? _value.daysSinceActive
          : daysSinceActive // ignore: cast_nullable_to_non_nullable
              as int,
      engagementTrend: freezed == engagementTrend
          ? _value.engagementTrend
          : engagementTrend // ignore: cast_nullable_to_non_nullable
              as String?,
      retentionSegment: freezed == retentionSegment
          ? _value.retentionSegment
          : retentionSegment // ignore: cast_nullable_to_non_nullable
              as String?,
      recommendedAction: freezed == recommendedAction
          ? _value.recommendedAction
          : recommendedAction // ignore: cast_nullable_to_non_nullable
              as String?,
      lastEngagement: freezed == lastEngagement
          ? _value.lastEngagement
          : lastEngagement // ignore: cast_nullable_to_non_nullable
              as DateTime?,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$RetentionMetricImpl implements _RetentionMetric {
  const _$RetentionMetricImpl(
      {required this.id,
      required this.userId,
      required this.status,
      required this.churnProbability,
      required this.daysSinceActive,
      this.engagementTrend,
      this.retentionSegment,
      this.recommendedAction,
      this.lastEngagement});

  factory _$RetentionMetricImpl.fromJson(Map<String, dynamic> json) =>
      _$$RetentionMetricImplFromJson(json);

  @override
  final int id;
  @override
  final int userId;
  @override
  final String status;
  @override
  final double churnProbability;
  @override
  final int daysSinceActive;
  @override
  final String? engagementTrend;
  @override
  final String? retentionSegment;
  @override
  final String? recommendedAction;
  @override
  final DateTime? lastEngagement;

  @override
  String toString() {
    return 'RetentionMetric(id: $id, userId: $userId, status: $status, churnProbability: $churnProbability, daysSinceActive: $daysSinceActive, engagementTrend: $engagementTrend, retentionSegment: $retentionSegment, recommendedAction: $recommendedAction, lastEngagement: $lastEngagement)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$RetentionMetricImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.status, status) || other.status == status) &&
            (identical(other.churnProbability, churnProbability) ||
                other.churnProbability == churnProbability) &&
            (identical(other.daysSinceActive, daysSinceActive) ||
                other.daysSinceActive == daysSinceActive) &&
            (identical(other.engagementTrend, engagementTrend) ||
                other.engagementTrend == engagementTrend) &&
            (identical(other.retentionSegment, retentionSegment) ||
                other.retentionSegment == retentionSegment) &&
            (identical(other.recommendedAction, recommendedAction) ||
                other.recommendedAction == recommendedAction) &&
            (identical(other.lastEngagement, lastEngagement) ||
                other.lastEngagement == lastEngagement));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      userId,
      status,
      churnProbability,
      daysSinceActive,
      engagementTrend,
      retentionSegment,
      recommendedAction,
      lastEngagement);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$RetentionMetricImplCopyWith<_$RetentionMetricImpl> get copyWith =>
      __$$RetentionMetricImplCopyWithImpl<_$RetentionMetricImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$RetentionMetricImplToJson(
      this,
    );
  }
}

abstract class _RetentionMetric implements RetentionMetric {
  const factory _RetentionMetric(
      {required final int id,
      required final int userId,
      required final String status,
      required final double churnProbability,
      required final int daysSinceActive,
      final String? engagementTrend,
      final String? retentionSegment,
      final String? recommendedAction,
      final DateTime? lastEngagement}) = _$RetentionMetricImpl;

  factory _RetentionMetric.fromJson(Map<String, dynamic> json) =
      _$RetentionMetricImpl.fromJson;

  @override
  int get id;
  @override
  int get userId;
  @override
  String get status;
  @override
  double get churnProbability;
  @override
  int get daysSinceActive;
  @override
  String? get engagementTrend;
  @override
  String? get retentionSegment;
  @override
  String? get recommendedAction;
  @override
  DateTime? get lastEngagement;
  @override
  @JsonKey(ignore: true)
  _$$RetentionMetricImplCopyWith<_$RetentionMetricImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

RetentionCampaign _$RetentionCampaignFromJson(Map<String, dynamic> json) {
  return _RetentionCampaign.fromJson(json);
}

/// @nodoc
mixin _$RetentionCampaign {
  int get id => throw _privateConstructorUsedError;
  String get name => throw _privateConstructorUsedError;
  String? get description => throw _privateConstructorUsedError;
  String get status => throw _privateConstructorUsedError;
  String get targetSegment => throw _privateConstructorUsedError;
  String? get campaignType => throw _privateConstructorUsedError;
  int get sentCount => throw _privateConstructorUsedError;
  int get convertedCount => throw _privateConstructorUsedError;
  double get roi => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $RetentionCampaignCopyWith<RetentionCampaign> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $RetentionCampaignCopyWith<$Res> {
  factory $RetentionCampaignCopyWith(
          RetentionCampaign value, $Res Function(RetentionCampaign) then) =
      _$RetentionCampaignCopyWithImpl<$Res, RetentionCampaign>;
  @useResult
  $Res call(
      {int id,
      String name,
      String? description,
      String status,
      String targetSegment,
      String? campaignType,
      int sentCount,
      int convertedCount,
      double roi});
}

/// @nodoc
class _$RetentionCampaignCopyWithImpl<$Res, $Val extends RetentionCampaign>
    implements $RetentionCampaignCopyWith<$Res> {
  _$RetentionCampaignCopyWithImpl(this._value, this._then);

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
    Object? status = null,
    Object? targetSegment = null,
    Object? campaignType = freezed,
    Object? sentCount = null,
    Object? convertedCount = null,
    Object? roi = null,
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
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      targetSegment: null == targetSegment
          ? _value.targetSegment
          : targetSegment // ignore: cast_nullable_to_non_nullable
              as String,
      campaignType: freezed == campaignType
          ? _value.campaignType
          : campaignType // ignore: cast_nullable_to_non_nullable
              as String?,
      sentCount: null == sentCount
          ? _value.sentCount
          : sentCount // ignore: cast_nullable_to_non_nullable
              as int,
      convertedCount: null == convertedCount
          ? _value.convertedCount
          : convertedCount // ignore: cast_nullable_to_non_nullable
              as int,
      roi: null == roi
          ? _value.roi
          : roi // ignore: cast_nullable_to_non_nullable
              as double,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$RetentionCampaignImplCopyWith<$Res>
    implements $RetentionCampaignCopyWith<$Res> {
  factory _$$RetentionCampaignImplCopyWith(_$RetentionCampaignImpl value,
          $Res Function(_$RetentionCampaignImpl) then) =
      __$$RetentionCampaignImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String name,
      String? description,
      String status,
      String targetSegment,
      String? campaignType,
      int sentCount,
      int convertedCount,
      double roi});
}

/// @nodoc
class __$$RetentionCampaignImplCopyWithImpl<$Res>
    extends _$RetentionCampaignCopyWithImpl<$Res, _$RetentionCampaignImpl>
    implements _$$RetentionCampaignImplCopyWith<$Res> {
  __$$RetentionCampaignImplCopyWithImpl(_$RetentionCampaignImpl _value,
      $Res Function(_$RetentionCampaignImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? description = freezed,
    Object? status = null,
    Object? targetSegment = null,
    Object? campaignType = freezed,
    Object? sentCount = null,
    Object? convertedCount = null,
    Object? roi = null,
  }) {
    return _then(_$RetentionCampaignImpl(
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
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      targetSegment: null == targetSegment
          ? _value.targetSegment
          : targetSegment // ignore: cast_nullable_to_non_nullable
              as String,
      campaignType: freezed == campaignType
          ? _value.campaignType
          : campaignType // ignore: cast_nullable_to_non_nullable
              as String?,
      sentCount: null == sentCount
          ? _value.sentCount
          : sentCount // ignore: cast_nullable_to_non_nullable
              as int,
      convertedCount: null == convertedCount
          ? _value.convertedCount
          : convertedCount // ignore: cast_nullable_to_non_nullable
              as int,
      roi: null == roi
          ? _value.roi
          : roi // ignore: cast_nullable_to_non_nullable
              as double,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$RetentionCampaignImpl implements _RetentionCampaign {
  const _$RetentionCampaignImpl(
      {required this.id,
      required this.name,
      this.description,
      required this.status,
      required this.targetSegment,
      this.campaignType,
      required this.sentCount,
      required this.convertedCount,
      required this.roi});

  factory _$RetentionCampaignImpl.fromJson(Map<String, dynamic> json) =>
      _$$RetentionCampaignImplFromJson(json);

  @override
  final int id;
  @override
  final String name;
  @override
  final String? description;
  @override
  final String status;
  @override
  final String targetSegment;
  @override
  final String? campaignType;
  @override
  final int sentCount;
  @override
  final int convertedCount;
  @override
  final double roi;

  @override
  String toString() {
    return 'RetentionCampaign(id: $id, name: $name, description: $description, status: $status, targetSegment: $targetSegment, campaignType: $campaignType, sentCount: $sentCount, convertedCount: $convertedCount, roi: $roi)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$RetentionCampaignImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.status, status) || other.status == status) &&
            (identical(other.targetSegment, targetSegment) ||
                other.targetSegment == targetSegment) &&
            (identical(other.campaignType, campaignType) ||
                other.campaignType == campaignType) &&
            (identical(other.sentCount, sentCount) ||
                other.sentCount == sentCount) &&
            (identical(other.convertedCount, convertedCount) ||
                other.convertedCount == convertedCount) &&
            (identical(other.roi, roi) || other.roi == roi));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, id, name, description, status,
      targetSegment, campaignType, sentCount, convertedCount, roi);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$RetentionCampaignImplCopyWith<_$RetentionCampaignImpl> get copyWith =>
      __$$RetentionCampaignImplCopyWithImpl<_$RetentionCampaignImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$RetentionCampaignImplToJson(
      this,
    );
  }
}

abstract class _RetentionCampaign implements RetentionCampaign {
  const factory _RetentionCampaign(
      {required final int id,
      required final String name,
      final String? description,
      required final String status,
      required final String targetSegment,
      final String? campaignType,
      required final int sentCount,
      required final int convertedCount,
      required final double roi}) = _$RetentionCampaignImpl;

  factory _RetentionCampaign.fromJson(Map<String, dynamic> json) =
      _$RetentionCampaignImpl.fromJson;

  @override
  int get id;
  @override
  String get name;
  @override
  String? get description;
  @override
  String get status;
  @override
  String get targetSegment;
  @override
  String? get campaignType;
  @override
  int get sentCount;
  @override
  int get convertedCount;
  @override
  double get roi;
  @override
  @JsonKey(ignore: true)
  _$$RetentionCampaignImplCopyWith<_$RetentionCampaignImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

ABTest _$ABTestFromJson(Map<String, dynamic> json) {
  return _ABTest.fromJson(json);
}

/// @nodoc
mixin _$ABTest {
  int get id => throw _privateConstructorUsedError;
  String get name => throw _privateConstructorUsedError;
  String? get description => throw _privateConstructorUsedError;
  String? get hypothesis => throw _privateConstructorUsedError;
  String get status => throw _privateConstructorUsedError;
  String get metricToOptimize => throw _privateConstructorUsedError;
  String get variantAName => throw _privateConstructorUsedError;
  String get variantBName => throw _privateConstructorUsedError;
  double get metricA => throw _privateConstructorUsedError;
  double get metricB => throw _privateConstructorUsedError;
  double get confidence => throw _privateConstructorUsedError;
  String? get winner => throw _privateConstructorUsedError;
  DateTime? get startDate => throw _privateConstructorUsedError;
  DateTime? get endDate => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $ABTestCopyWith<ABTest> get copyWith => throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $ABTestCopyWith<$Res> {
  factory $ABTestCopyWith(ABTest value, $Res Function(ABTest) then) =
      _$ABTestCopyWithImpl<$Res, ABTest>;
  @useResult
  $Res call(
      {int id,
      String name,
      String? description,
      String? hypothesis,
      String status,
      String metricToOptimize,
      String variantAName,
      String variantBName,
      double metricA,
      double metricB,
      double confidence,
      String? winner,
      DateTime? startDate,
      DateTime? endDate});
}

/// @nodoc
class _$ABTestCopyWithImpl<$Res, $Val extends ABTest>
    implements $ABTestCopyWith<$Res> {
  _$ABTestCopyWithImpl(this._value, this._then);

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
    Object? hypothesis = freezed,
    Object? status = null,
    Object? metricToOptimize = null,
    Object? variantAName = null,
    Object? variantBName = null,
    Object? metricA = null,
    Object? metricB = null,
    Object? confidence = null,
    Object? winner = freezed,
    Object? startDate = freezed,
    Object? endDate = freezed,
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
      hypothesis: freezed == hypothesis
          ? _value.hypothesis
          : hypothesis // ignore: cast_nullable_to_non_nullable
              as String?,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      metricToOptimize: null == metricToOptimize
          ? _value.metricToOptimize
          : metricToOptimize // ignore: cast_nullable_to_non_nullable
              as String,
      variantAName: null == variantAName
          ? _value.variantAName
          : variantAName // ignore: cast_nullable_to_non_nullable
              as String,
      variantBName: null == variantBName
          ? _value.variantBName
          : variantBName // ignore: cast_nullable_to_non_nullable
              as String,
      metricA: null == metricA
          ? _value.metricA
          : metricA // ignore: cast_nullable_to_non_nullable
              as double,
      metricB: null == metricB
          ? _value.metricB
          : metricB // ignore: cast_nullable_to_non_nullable
              as double,
      confidence: null == confidence
          ? _value.confidence
          : confidence // ignore: cast_nullable_to_non_nullable
              as double,
      winner: freezed == winner
          ? _value.winner
          : winner // ignore: cast_nullable_to_non_nullable
              as String?,
      startDate: freezed == startDate
          ? _value.startDate
          : startDate // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      endDate: freezed == endDate
          ? _value.endDate
          : endDate // ignore: cast_nullable_to_non_nullable
              as DateTime?,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$ABTestImplCopyWith<$Res> implements $ABTestCopyWith<$Res> {
  factory _$$ABTestImplCopyWith(
          _$ABTestImpl value, $Res Function(_$ABTestImpl) then) =
      __$$ABTestImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String name,
      String? description,
      String? hypothesis,
      String status,
      String metricToOptimize,
      String variantAName,
      String variantBName,
      double metricA,
      double metricB,
      double confidence,
      String? winner,
      DateTime? startDate,
      DateTime? endDate});
}

/// @nodoc
class __$$ABTestImplCopyWithImpl<$Res>
    extends _$ABTestCopyWithImpl<$Res, _$ABTestImpl>
    implements _$$ABTestImplCopyWith<$Res> {
  __$$ABTestImplCopyWithImpl(
      _$ABTestImpl _value, $Res Function(_$ABTestImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? description = freezed,
    Object? hypothesis = freezed,
    Object? status = null,
    Object? metricToOptimize = null,
    Object? variantAName = null,
    Object? variantBName = null,
    Object? metricA = null,
    Object? metricB = null,
    Object? confidence = null,
    Object? winner = freezed,
    Object? startDate = freezed,
    Object? endDate = freezed,
  }) {
    return _then(_$ABTestImpl(
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
      hypothesis: freezed == hypothesis
          ? _value.hypothesis
          : hypothesis // ignore: cast_nullable_to_non_nullable
              as String?,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      metricToOptimize: null == metricToOptimize
          ? _value.metricToOptimize
          : metricToOptimize // ignore: cast_nullable_to_non_nullable
              as String,
      variantAName: null == variantAName
          ? _value.variantAName
          : variantAName // ignore: cast_nullable_to_non_nullable
              as String,
      variantBName: null == variantBName
          ? _value.variantBName
          : variantBName // ignore: cast_nullable_to_non_nullable
              as String,
      metricA: null == metricA
          ? _value.metricA
          : metricA // ignore: cast_nullable_to_non_nullable
              as double,
      metricB: null == metricB
          ? _value.metricB
          : metricB // ignore: cast_nullable_to_non_nullable
              as double,
      confidence: null == confidence
          ? _value.confidence
          : confidence // ignore: cast_nullable_to_non_nullable
              as double,
      winner: freezed == winner
          ? _value.winner
          : winner // ignore: cast_nullable_to_non_nullable
              as String?,
      startDate: freezed == startDate
          ? _value.startDate
          : startDate // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      endDate: freezed == endDate
          ? _value.endDate
          : endDate // ignore: cast_nullable_to_non_nullable
              as DateTime?,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$ABTestImpl implements _ABTest {
  const _$ABTestImpl(
      {required this.id,
      required this.name,
      this.description,
      this.hypothesis,
      required this.status,
      required this.metricToOptimize,
      required this.variantAName,
      required this.variantBName,
      required this.metricA,
      required this.metricB,
      required this.confidence,
      this.winner,
      this.startDate,
      this.endDate});

  factory _$ABTestImpl.fromJson(Map<String, dynamic> json) =>
      _$$ABTestImplFromJson(json);

  @override
  final int id;
  @override
  final String name;
  @override
  final String? description;
  @override
  final String? hypothesis;
  @override
  final String status;
  @override
  final String metricToOptimize;
  @override
  final String variantAName;
  @override
  final String variantBName;
  @override
  final double metricA;
  @override
  final double metricB;
  @override
  final double confidence;
  @override
  final String? winner;
  @override
  final DateTime? startDate;
  @override
  final DateTime? endDate;

  @override
  String toString() {
    return 'ABTest(id: $id, name: $name, description: $description, hypothesis: $hypothesis, status: $status, metricToOptimize: $metricToOptimize, variantAName: $variantAName, variantBName: $variantBName, metricA: $metricA, metricB: $metricB, confidence: $confidence, winner: $winner, startDate: $startDate, endDate: $endDate)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$ABTestImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.hypothesis, hypothesis) ||
                other.hypothesis == hypothesis) &&
            (identical(other.status, status) || other.status == status) &&
            (identical(other.metricToOptimize, metricToOptimize) ||
                other.metricToOptimize == metricToOptimize) &&
            (identical(other.variantAName, variantAName) ||
                other.variantAName == variantAName) &&
            (identical(other.variantBName, variantBName) ||
                other.variantBName == variantBName) &&
            (identical(other.metricA, metricA) || other.metricA == metricA) &&
            (identical(other.metricB, metricB) || other.metricB == metricB) &&
            (identical(other.confidence, confidence) ||
                other.confidence == confidence) &&
            (identical(other.winner, winner) || other.winner == winner) &&
            (identical(other.startDate, startDate) ||
                other.startDate == startDate) &&
            (identical(other.endDate, endDate) || other.endDate == endDate));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      name,
      description,
      hypothesis,
      status,
      metricToOptimize,
      variantAName,
      variantBName,
      metricA,
      metricB,
      confidence,
      winner,
      startDate,
      endDate);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$ABTestImplCopyWith<_$ABTestImpl> get copyWith =>
      __$$ABTestImplCopyWithImpl<_$ABTestImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$ABTestImplToJson(
      this,
    );
  }
}

abstract class _ABTest implements ABTest {
  const factory _ABTest(
      {required final int id,
      required final String name,
      final String? description,
      final String? hypothesis,
      required final String status,
      required final String metricToOptimize,
      required final String variantAName,
      required final String variantBName,
      required final double metricA,
      required final double metricB,
      required final double confidence,
      final String? winner,
      final DateTime? startDate,
      final DateTime? endDate}) = _$ABTestImpl;

  factory _ABTest.fromJson(Map<String, dynamic> json) = _$ABTestImpl.fromJson;

  @override
  int get id;
  @override
  String get name;
  @override
  String? get description;
  @override
  String? get hypothesis;
  @override
  String get status;
  @override
  String get metricToOptimize;
  @override
  String get variantAName;
  @override
  String get variantBName;
  @override
  double get metricA;
  @override
  double get metricB;
  @override
  double get confidence;
  @override
  String? get winner;
  @override
  DateTime? get startDate;
  @override
  DateTime? get endDate;
  @override
  @JsonKey(ignore: true)
  _$$ABTestImplCopyWith<_$ABTestImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

ABTestVariant _$ABTestVariantFromJson(Map<String, dynamic> json) {
  return _ABTestVariant.fromJson(json);
}

/// @nodoc
mixin _$ABTestVariant {
  int get id => throw _privateConstructorUsedError;
  int get abTestId => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  String get variant => throw _privateConstructorUsedError;
  bool get conversion => throw _privateConstructorUsedError;
  double get metricValue => throw _privateConstructorUsedError;
  DateTime get assignedAt => throw _privateConstructorUsedError;

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
      int abTestId,
      int userId,
      String variant,
      bool conversion,
      double metricValue,
      DateTime assignedAt});
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
    Object? abTestId = null,
    Object? userId = null,
    Object? variant = null,
    Object? conversion = null,
    Object? metricValue = null,
    Object? assignedAt = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      abTestId: null == abTestId
          ? _value.abTestId
          : abTestId // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      variant: null == variant
          ? _value.variant
          : variant // ignore: cast_nullable_to_non_nullable
              as String,
      conversion: null == conversion
          ? _value.conversion
          : conversion // ignore: cast_nullable_to_non_nullable
              as bool,
      metricValue: null == metricValue
          ? _value.metricValue
          : metricValue // ignore: cast_nullable_to_non_nullable
              as double,
      assignedAt: null == assignedAt
          ? _value.assignedAt
          : assignedAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
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
      int abTestId,
      int userId,
      String variant,
      bool conversion,
      double metricValue,
      DateTime assignedAt});
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
    Object? abTestId = null,
    Object? userId = null,
    Object? variant = null,
    Object? conversion = null,
    Object? metricValue = null,
    Object? assignedAt = null,
  }) {
    return _then(_$ABTestVariantImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      abTestId: null == abTestId
          ? _value.abTestId
          : abTestId // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      variant: null == variant
          ? _value.variant
          : variant // ignore: cast_nullable_to_non_nullable
              as String,
      conversion: null == conversion
          ? _value.conversion
          : conversion // ignore: cast_nullable_to_non_nullable
              as bool,
      metricValue: null == metricValue
          ? _value.metricValue
          : metricValue // ignore: cast_nullable_to_non_nullable
              as double,
      assignedAt: null == assignedAt
          ? _value.assignedAt
          : assignedAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$ABTestVariantImpl implements _ABTestVariant {
  const _$ABTestVariantImpl(
      {required this.id,
      required this.abTestId,
      required this.userId,
      required this.variant,
      required this.conversion,
      required this.metricValue,
      required this.assignedAt});

  factory _$ABTestVariantImpl.fromJson(Map<String, dynamic> json) =>
      _$$ABTestVariantImplFromJson(json);

  @override
  final int id;
  @override
  final int abTestId;
  @override
  final int userId;
  @override
  final String variant;
  @override
  final bool conversion;
  @override
  final double metricValue;
  @override
  final DateTime assignedAt;

  @override
  String toString() {
    return 'ABTestVariant(id: $id, abTestId: $abTestId, userId: $userId, variant: $variant, conversion: $conversion, metricValue: $metricValue, assignedAt: $assignedAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$ABTestVariantImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.abTestId, abTestId) ||
                other.abTestId == abTestId) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.variant, variant) || other.variant == variant) &&
            (identical(other.conversion, conversion) ||
                other.conversion == conversion) &&
            (identical(other.metricValue, metricValue) ||
                other.metricValue == metricValue) &&
            (identical(other.assignedAt, assignedAt) ||
                other.assignedAt == assignedAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, id, abTestId, userId, variant,
      conversion, metricValue, assignedAt);

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
      required final int abTestId,
      required final int userId,
      required final String variant,
      required final bool conversion,
      required final double metricValue,
      required final DateTime assignedAt}) = _$ABTestVariantImpl;

  factory _ABTestVariant.fromJson(Map<String, dynamic> json) =
      _$ABTestVariantImpl.fromJson;

  @override
  int get id;
  @override
  int get abTestId;
  @override
  int get userId;
  @override
  String get variant;
  @override
  bool get conversion;
  @override
  double get metricValue;
  @override
  DateTime get assignedAt;
  @override
  @JsonKey(ignore: true)
  _$$ABTestVariantImplCopyWith<_$ABTestVariantImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

AnalyticsInsight _$AnalyticsInsightFromJson(Map<String, dynamic> json) {
  return _AnalyticsInsight.fromJson(json);
}

/// @nodoc
mixin _$AnalyticsInsight {
  int get id => throw _privateConstructorUsedError;
  String get type => throw _privateConstructorUsedError;
  String get title => throw _privateConstructorUsedError;
  String? get description => throw _privateConstructorUsedError;
  Map<String, dynamic> get data => throw _privateConstructorUsedError;
  String? get metricName => throw _privateConstructorUsedError;
  double? get metricValue => throw _privateConstructorUsedError;
  String? get trend => throw _privateConstructorUsedError;
  double get confidenceLevel => throw _privateConstructorUsedError;
  bool get actionable => throw _privateConstructorUsedError;
  String? get recommendedAction => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $AnalyticsInsightCopyWith<AnalyticsInsight> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $AnalyticsInsightCopyWith<$Res> {
  factory $AnalyticsInsightCopyWith(
          AnalyticsInsight value, $Res Function(AnalyticsInsight) then) =
      _$AnalyticsInsightCopyWithImpl<$Res, AnalyticsInsight>;
  @useResult
  $Res call(
      {int id,
      String type,
      String title,
      String? description,
      Map<String, dynamic> data,
      String? metricName,
      double? metricValue,
      String? trend,
      double confidenceLevel,
      bool actionable,
      String? recommendedAction,
      DateTime createdAt});
}

/// @nodoc
class _$AnalyticsInsightCopyWithImpl<$Res, $Val extends AnalyticsInsight>
    implements $AnalyticsInsightCopyWith<$Res> {
  _$AnalyticsInsightCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? type = null,
    Object? title = null,
    Object? description = freezed,
    Object? data = null,
    Object? metricName = freezed,
    Object? metricValue = freezed,
    Object? trend = freezed,
    Object? confidenceLevel = null,
    Object? actionable = null,
    Object? recommendedAction = freezed,
    Object? createdAt = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      type: null == type
          ? _value.type
          : type // ignore: cast_nullable_to_non_nullable
              as String,
      title: null == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String,
      description: freezed == description
          ? _value.description
          : description // ignore: cast_nullable_to_non_nullable
              as String?,
      data: null == data
          ? _value.data
          : data // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      metricName: freezed == metricName
          ? _value.metricName
          : metricName // ignore: cast_nullable_to_non_nullable
              as String?,
      metricValue: freezed == metricValue
          ? _value.metricValue
          : metricValue // ignore: cast_nullable_to_non_nullable
              as double?,
      trend: freezed == trend
          ? _value.trend
          : trend // ignore: cast_nullable_to_non_nullable
              as String?,
      confidenceLevel: null == confidenceLevel
          ? _value.confidenceLevel
          : confidenceLevel // ignore: cast_nullable_to_non_nullable
              as double,
      actionable: null == actionable
          ? _value.actionable
          : actionable // ignore: cast_nullable_to_non_nullable
              as bool,
      recommendedAction: freezed == recommendedAction
          ? _value.recommendedAction
          : recommendedAction // ignore: cast_nullable_to_non_nullable
              as String?,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$AnalyticsInsightImplCopyWith<$Res>
    implements $AnalyticsInsightCopyWith<$Res> {
  factory _$$AnalyticsInsightImplCopyWith(_$AnalyticsInsightImpl value,
          $Res Function(_$AnalyticsInsightImpl) then) =
      __$$AnalyticsInsightImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String type,
      String title,
      String? description,
      Map<String, dynamic> data,
      String? metricName,
      double? metricValue,
      String? trend,
      double confidenceLevel,
      bool actionable,
      String? recommendedAction,
      DateTime createdAt});
}

/// @nodoc
class __$$AnalyticsInsightImplCopyWithImpl<$Res>
    extends _$AnalyticsInsightCopyWithImpl<$Res, _$AnalyticsInsightImpl>
    implements _$$AnalyticsInsightImplCopyWith<$Res> {
  __$$AnalyticsInsightImplCopyWithImpl(_$AnalyticsInsightImpl _value,
      $Res Function(_$AnalyticsInsightImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? type = null,
    Object? title = null,
    Object? description = freezed,
    Object? data = null,
    Object? metricName = freezed,
    Object? metricValue = freezed,
    Object? trend = freezed,
    Object? confidenceLevel = null,
    Object? actionable = null,
    Object? recommendedAction = freezed,
    Object? createdAt = null,
  }) {
    return _then(_$AnalyticsInsightImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      type: null == type
          ? _value.type
          : type // ignore: cast_nullable_to_non_nullable
              as String,
      title: null == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String,
      description: freezed == description
          ? _value.description
          : description // ignore: cast_nullable_to_non_nullable
              as String?,
      data: null == data
          ? _value._data
          : data // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      metricName: freezed == metricName
          ? _value.metricName
          : metricName // ignore: cast_nullable_to_non_nullable
              as String?,
      metricValue: freezed == metricValue
          ? _value.metricValue
          : metricValue // ignore: cast_nullable_to_non_nullable
              as double?,
      trend: freezed == trend
          ? _value.trend
          : trend // ignore: cast_nullable_to_non_nullable
              as String?,
      confidenceLevel: null == confidenceLevel
          ? _value.confidenceLevel
          : confidenceLevel // ignore: cast_nullable_to_non_nullable
              as double,
      actionable: null == actionable
          ? _value.actionable
          : actionable // ignore: cast_nullable_to_non_nullable
              as bool,
      recommendedAction: freezed == recommendedAction
          ? _value.recommendedAction
          : recommendedAction // ignore: cast_nullable_to_non_nullable
              as String?,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$AnalyticsInsightImpl implements _AnalyticsInsight {
  const _$AnalyticsInsightImpl(
      {required this.id,
      required this.type,
      required this.title,
      this.description,
      required final Map<String, dynamic> data,
      this.metricName,
      this.metricValue,
      this.trend,
      required this.confidenceLevel,
      required this.actionable,
      this.recommendedAction,
      required this.createdAt})
      : _data = data;

  factory _$AnalyticsInsightImpl.fromJson(Map<String, dynamic> json) =>
      _$$AnalyticsInsightImplFromJson(json);

  @override
  final int id;
  @override
  final String type;
  @override
  final String title;
  @override
  final String? description;
  final Map<String, dynamic> _data;
  @override
  Map<String, dynamic> get data {
    if (_data is EqualUnmodifiableMapView) return _data;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(_data);
  }

  @override
  final String? metricName;
  @override
  final double? metricValue;
  @override
  final String? trend;
  @override
  final double confidenceLevel;
  @override
  final bool actionable;
  @override
  final String? recommendedAction;
  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'AnalyticsInsight(id: $id, type: $type, title: $title, description: $description, data: $data, metricName: $metricName, metricValue: $metricValue, trend: $trend, confidenceLevel: $confidenceLevel, actionable: $actionable, recommendedAction: $recommendedAction, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$AnalyticsInsightImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.type, type) || other.type == type) &&
            (identical(other.title, title) || other.title == title) &&
            (identical(other.description, description) ||
                other.description == description) &&
            const DeepCollectionEquality().equals(other._data, _data) &&
            (identical(other.metricName, metricName) ||
                other.metricName == metricName) &&
            (identical(other.metricValue, metricValue) ||
                other.metricValue == metricValue) &&
            (identical(other.trend, trend) || other.trend == trend) &&
            (identical(other.confidenceLevel, confidenceLevel) ||
                other.confidenceLevel == confidenceLevel) &&
            (identical(other.actionable, actionable) ||
                other.actionable == actionable) &&
            (identical(other.recommendedAction, recommendedAction) ||
                other.recommendedAction == recommendedAction) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      type,
      title,
      description,
      const DeepCollectionEquality().hash(_data),
      metricName,
      metricValue,
      trend,
      confidenceLevel,
      actionable,
      recommendedAction,
      createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$AnalyticsInsightImplCopyWith<_$AnalyticsInsightImpl> get copyWith =>
      __$$AnalyticsInsightImplCopyWithImpl<_$AnalyticsInsightImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$AnalyticsInsightImplToJson(
      this,
    );
  }
}

abstract class _AnalyticsInsight implements AnalyticsInsight {
  const factory _AnalyticsInsight(
      {required final int id,
      required final String type,
      required final String title,
      final String? description,
      required final Map<String, dynamic> data,
      final String? metricName,
      final double? metricValue,
      final String? trend,
      required final double confidenceLevel,
      required final bool actionable,
      final String? recommendedAction,
      required final DateTime createdAt}) = _$AnalyticsInsightImpl;

  factory _AnalyticsInsight.fromJson(Map<String, dynamic> json) =
      _$AnalyticsInsightImpl.fromJson;

  @override
  int get id;
  @override
  String get type;
  @override
  String get title;
  @override
  String? get description;
  @override
  Map<String, dynamic> get data;
  @override
  String? get metricName;
  @override
  double? get metricValue;
  @override
  String? get trend;
  @override
  double get confidenceLevel;
  @override
  bool get actionable;
  @override
  String? get recommendedAction;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$AnalyticsInsightImplCopyWith<_$AnalyticsInsightImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

UserCohort _$UserCohortFromJson(Map<String, dynamic> json) {
  return _UserCohort.fromJson(json);
}

/// @nodoc
mixin _$UserCohort {
  int get id => throw _privateConstructorUsedError;
  String get name => throw _privateConstructorUsedError;
  String? get description => throw _privateConstructorUsedError;
  String get cohortType => throw _privateConstructorUsedError;
  Map<String, dynamic> get criteria => throw _privateConstructorUsedError;
  int get userCount => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $UserCohortCopyWith<UserCohort> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $UserCohortCopyWith<$Res> {
  factory $UserCohortCopyWith(
          UserCohort value, $Res Function(UserCohort) then) =
      _$UserCohortCopyWithImpl<$Res, UserCohort>;
  @useResult
  $Res call(
      {int id,
      String name,
      String? description,
      String cohortType,
      Map<String, dynamic> criteria,
      int userCount,
      DateTime createdAt});
}

/// @nodoc
class _$UserCohortCopyWithImpl<$Res, $Val extends UserCohort>
    implements $UserCohortCopyWith<$Res> {
  _$UserCohortCopyWithImpl(this._value, this._then);

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
    Object? cohortType = null,
    Object? criteria = null,
    Object? userCount = null,
    Object? createdAt = null,
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
      cohortType: null == cohortType
          ? _value.cohortType
          : cohortType // ignore: cast_nullable_to_non_nullable
              as String,
      criteria: null == criteria
          ? _value.criteria
          : criteria // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      userCount: null == userCount
          ? _value.userCount
          : userCount // ignore: cast_nullable_to_non_nullable
              as int,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$UserCohortImplCopyWith<$Res>
    implements $UserCohortCopyWith<$Res> {
  factory _$$UserCohortImplCopyWith(
          _$UserCohortImpl value, $Res Function(_$UserCohortImpl) then) =
      __$$UserCohortImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String name,
      String? description,
      String cohortType,
      Map<String, dynamic> criteria,
      int userCount,
      DateTime createdAt});
}

/// @nodoc
class __$$UserCohortImplCopyWithImpl<$Res>
    extends _$UserCohortCopyWithImpl<$Res, _$UserCohortImpl>
    implements _$$UserCohortImplCopyWith<$Res> {
  __$$UserCohortImplCopyWithImpl(
      _$UserCohortImpl _value, $Res Function(_$UserCohortImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? description = freezed,
    Object? cohortType = null,
    Object? criteria = null,
    Object? userCount = null,
    Object? createdAt = null,
  }) {
    return _then(_$UserCohortImpl(
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
      cohortType: null == cohortType
          ? _value.cohortType
          : cohortType // ignore: cast_nullable_to_non_nullable
              as String,
      criteria: null == criteria
          ? _value._criteria
          : criteria // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      userCount: null == userCount
          ? _value.userCount
          : userCount // ignore: cast_nullable_to_non_nullable
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
class _$UserCohortImpl implements _UserCohort {
  const _$UserCohortImpl(
      {required this.id,
      required this.name,
      this.description,
      required this.cohortType,
      required final Map<String, dynamic> criteria,
      required this.userCount,
      required this.createdAt})
      : _criteria = criteria;

  factory _$UserCohortImpl.fromJson(Map<String, dynamic> json) =>
      _$$UserCohortImplFromJson(json);

  @override
  final int id;
  @override
  final String name;
  @override
  final String? description;
  @override
  final String cohortType;
  final Map<String, dynamic> _criteria;
  @override
  Map<String, dynamic> get criteria {
    if (_criteria is EqualUnmodifiableMapView) return _criteria;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(_criteria);
  }

  @override
  final int userCount;
  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'UserCohort(id: $id, name: $name, description: $description, cohortType: $cohortType, criteria: $criteria, userCount: $userCount, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$UserCohortImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.cohortType, cohortType) ||
                other.cohortType == cohortType) &&
            const DeepCollectionEquality().equals(other._criteria, _criteria) &&
            (identical(other.userCount, userCount) ||
                other.userCount == userCount) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      name,
      description,
      cohortType,
      const DeepCollectionEquality().hash(_criteria),
      userCount,
      createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$UserCohortImplCopyWith<_$UserCohortImpl> get copyWith =>
      __$$UserCohortImplCopyWithImpl<_$UserCohortImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$UserCohortImplToJson(
      this,
    );
  }
}

abstract class _UserCohort implements UserCohort {
  const factory _UserCohort(
      {required final int id,
      required final String name,
      final String? description,
      required final String cohortType,
      required final Map<String, dynamic> criteria,
      required final int userCount,
      required final DateTime createdAt}) = _$UserCohortImpl;

  factory _UserCohort.fromJson(Map<String, dynamic> json) =
      _$UserCohortImpl.fromJson;

  @override
  int get id;
  @override
  String get name;
  @override
  String? get description;
  @override
  String get cohortType;
  @override
  Map<String, dynamic> get criteria;
  @override
  int get userCount;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$UserCohortImplCopyWith<_$UserCohortImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

PredictionModel _$PredictionModelFromJson(Map<String, dynamic> json) {
  return _PredictionModel.fromJson(json);
}

/// @nodoc
mixin _$PredictionModel {
  int get id => throw _privateConstructorUsedError;
  String get name => throw _privateConstructorUsedError;
  String get modelType => throw _privateConstructorUsedError;
  String get targetMetric => throw _privateConstructorUsedError;
  double get accuracy => throw _privateConstructorUsedError;
  double get precision => throw _privateConstructorUsedError;
  double get recall => throw _privateConstructorUsedError;
  double get f1Score => throw _privateConstructorUsedError;
  double get aucScore => throw _privateConstructorUsedError;
  bool get deployed => throw _privateConstructorUsedError;
  DateTime? get lastTrained => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $PredictionModelCopyWith<PredictionModel> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $PredictionModelCopyWith<$Res> {
  factory $PredictionModelCopyWith(
          PredictionModel value, $Res Function(PredictionModel) then) =
      _$PredictionModelCopyWithImpl<$Res, PredictionModel>;
  @useResult
  $Res call(
      {int id,
      String name,
      String modelType,
      String targetMetric,
      double accuracy,
      double precision,
      double recall,
      double f1Score,
      double aucScore,
      bool deployed,
      DateTime? lastTrained});
}

/// @nodoc
class _$PredictionModelCopyWithImpl<$Res, $Val extends PredictionModel>
    implements $PredictionModelCopyWith<$Res> {
  _$PredictionModelCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? modelType = null,
    Object? targetMetric = null,
    Object? accuracy = null,
    Object? precision = null,
    Object? recall = null,
    Object? f1Score = null,
    Object? aucScore = null,
    Object? deployed = null,
    Object? lastTrained = freezed,
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
      modelType: null == modelType
          ? _value.modelType
          : modelType // ignore: cast_nullable_to_non_nullable
              as String,
      targetMetric: null == targetMetric
          ? _value.targetMetric
          : targetMetric // ignore: cast_nullable_to_non_nullable
              as String,
      accuracy: null == accuracy
          ? _value.accuracy
          : accuracy // ignore: cast_nullable_to_non_nullable
              as double,
      precision: null == precision
          ? _value.precision
          : precision // ignore: cast_nullable_to_non_nullable
              as double,
      recall: null == recall
          ? _value.recall
          : recall // ignore: cast_nullable_to_non_nullable
              as double,
      f1Score: null == f1Score
          ? _value.f1Score
          : f1Score // ignore: cast_nullable_to_non_nullable
              as double,
      aucScore: null == aucScore
          ? _value.aucScore
          : aucScore // ignore: cast_nullable_to_non_nullable
              as double,
      deployed: null == deployed
          ? _value.deployed
          : deployed // ignore: cast_nullable_to_non_nullable
              as bool,
      lastTrained: freezed == lastTrained
          ? _value.lastTrained
          : lastTrained // ignore: cast_nullable_to_non_nullable
              as DateTime?,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$PredictionModelImplCopyWith<$Res>
    implements $PredictionModelCopyWith<$Res> {
  factory _$$PredictionModelImplCopyWith(_$PredictionModelImpl value,
          $Res Function(_$PredictionModelImpl) then) =
      __$$PredictionModelImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String name,
      String modelType,
      String targetMetric,
      double accuracy,
      double precision,
      double recall,
      double f1Score,
      double aucScore,
      bool deployed,
      DateTime? lastTrained});
}

/// @nodoc
class __$$PredictionModelImplCopyWithImpl<$Res>
    extends _$PredictionModelCopyWithImpl<$Res, _$PredictionModelImpl>
    implements _$$PredictionModelImplCopyWith<$Res> {
  __$$PredictionModelImplCopyWithImpl(
      _$PredictionModelImpl _value, $Res Function(_$PredictionModelImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? modelType = null,
    Object? targetMetric = null,
    Object? accuracy = null,
    Object? precision = null,
    Object? recall = null,
    Object? f1Score = null,
    Object? aucScore = null,
    Object? deployed = null,
    Object? lastTrained = freezed,
  }) {
    return _then(_$PredictionModelImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      name: null == name
          ? _value.name
          : name // ignore: cast_nullable_to_non_nullable
              as String,
      modelType: null == modelType
          ? _value.modelType
          : modelType // ignore: cast_nullable_to_non_nullable
              as String,
      targetMetric: null == targetMetric
          ? _value.targetMetric
          : targetMetric // ignore: cast_nullable_to_non_nullable
              as String,
      accuracy: null == accuracy
          ? _value.accuracy
          : accuracy // ignore: cast_nullable_to_non_nullable
              as double,
      precision: null == precision
          ? _value.precision
          : precision // ignore: cast_nullable_to_non_nullable
              as double,
      recall: null == recall
          ? _value.recall
          : recall // ignore: cast_nullable_to_non_nullable
              as double,
      f1Score: null == f1Score
          ? _value.f1Score
          : f1Score // ignore: cast_nullable_to_non_nullable
              as double,
      aucScore: null == aucScore
          ? _value.aucScore
          : aucScore // ignore: cast_nullable_to_non_nullable
              as double,
      deployed: null == deployed
          ? _value.deployed
          : deployed // ignore: cast_nullable_to_non_nullable
              as bool,
      lastTrained: freezed == lastTrained
          ? _value.lastTrained
          : lastTrained // ignore: cast_nullable_to_non_nullable
              as DateTime?,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$PredictionModelImpl implements _PredictionModel {
  const _$PredictionModelImpl(
      {required this.id,
      required this.name,
      required this.modelType,
      required this.targetMetric,
      required this.accuracy,
      required this.precision,
      required this.recall,
      required this.f1Score,
      required this.aucScore,
      required this.deployed,
      this.lastTrained});

  factory _$PredictionModelImpl.fromJson(Map<String, dynamic> json) =>
      _$$PredictionModelImplFromJson(json);

  @override
  final int id;
  @override
  final String name;
  @override
  final String modelType;
  @override
  final String targetMetric;
  @override
  final double accuracy;
  @override
  final double precision;
  @override
  final double recall;
  @override
  final double f1Score;
  @override
  final double aucScore;
  @override
  final bool deployed;
  @override
  final DateTime? lastTrained;

  @override
  String toString() {
    return 'PredictionModel(id: $id, name: $name, modelType: $modelType, targetMetric: $targetMetric, accuracy: $accuracy, precision: $precision, recall: $recall, f1Score: $f1Score, aucScore: $aucScore, deployed: $deployed, lastTrained: $lastTrained)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$PredictionModelImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.modelType, modelType) ||
                other.modelType == modelType) &&
            (identical(other.targetMetric, targetMetric) ||
                other.targetMetric == targetMetric) &&
            (identical(other.accuracy, accuracy) ||
                other.accuracy == accuracy) &&
            (identical(other.precision, precision) ||
                other.precision == precision) &&
            (identical(other.recall, recall) || other.recall == recall) &&
            (identical(other.f1Score, f1Score) || other.f1Score == f1Score) &&
            (identical(other.aucScore, aucScore) ||
                other.aucScore == aucScore) &&
            (identical(other.deployed, deployed) ||
                other.deployed == deployed) &&
            (identical(other.lastTrained, lastTrained) ||
                other.lastTrained == lastTrained));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      name,
      modelType,
      targetMetric,
      accuracy,
      precision,
      recall,
      f1Score,
      aucScore,
      deployed,
      lastTrained);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$PredictionModelImplCopyWith<_$PredictionModelImpl> get copyWith =>
      __$$PredictionModelImplCopyWithImpl<_$PredictionModelImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$PredictionModelImplToJson(
      this,
    );
  }
}

abstract class _PredictionModel implements PredictionModel {
  const factory _PredictionModel(
      {required final int id,
      required final String name,
      required final String modelType,
      required final String targetMetric,
      required final double accuracy,
      required final double precision,
      required final double recall,
      required final double f1Score,
      required final double aucScore,
      required final bool deployed,
      final DateTime? lastTrained}) = _$PredictionModelImpl;

  factory _PredictionModel.fromJson(Map<String, dynamic> json) =
      _$PredictionModelImpl.fromJson;

  @override
  int get id;
  @override
  String get name;
  @override
  String get modelType;
  @override
  String get targetMetric;
  @override
  double get accuracy;
  @override
  double get precision;
  @override
  double get recall;
  @override
  double get f1Score;
  @override
  double get aucScore;
  @override
  bool get deployed;
  @override
  DateTime? get lastTrained;
  @override
  @JsonKey(ignore: true)
  _$$PredictionModelImplCopyWith<_$PredictionModelImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

UserPrediction _$UserPredictionFromJson(Map<String, dynamic> json) {
  return _UserPrediction.fromJson(json);
}

/// @nodoc
mixin _$UserPrediction {
  int get id => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  int get modelId => throw _privateConstructorUsedError;
  double get predictionScore => throw _privateConstructorUsedError;
  double get confidence => throw _privateConstructorUsedError;
  String? get predictedBehavior => throw _privateConstructorUsedError;
  String? get actualBehavior => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $UserPredictionCopyWith<UserPrediction> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $UserPredictionCopyWith<$Res> {
  factory $UserPredictionCopyWith(
          UserPrediction value, $Res Function(UserPrediction) then) =
      _$UserPredictionCopyWithImpl<$Res, UserPrediction>;
  @useResult
  $Res call(
      {int id,
      int userId,
      int modelId,
      double predictionScore,
      double confidence,
      String? predictedBehavior,
      String? actualBehavior,
      DateTime createdAt});
}

/// @nodoc
class _$UserPredictionCopyWithImpl<$Res, $Val extends UserPrediction>
    implements $UserPredictionCopyWith<$Res> {
  _$UserPredictionCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? modelId = null,
    Object? predictionScore = null,
    Object? confidence = null,
    Object? predictedBehavior = freezed,
    Object? actualBehavior = freezed,
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
      modelId: null == modelId
          ? _value.modelId
          : modelId // ignore: cast_nullable_to_non_nullable
              as int,
      predictionScore: null == predictionScore
          ? _value.predictionScore
          : predictionScore // ignore: cast_nullable_to_non_nullable
              as double,
      confidence: null == confidence
          ? _value.confidence
          : confidence // ignore: cast_nullable_to_non_nullable
              as double,
      predictedBehavior: freezed == predictedBehavior
          ? _value.predictedBehavior
          : predictedBehavior // ignore: cast_nullable_to_non_nullable
              as String?,
      actualBehavior: freezed == actualBehavior
          ? _value.actualBehavior
          : actualBehavior // ignore: cast_nullable_to_non_nullable
              as String?,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$UserPredictionImplCopyWith<$Res>
    implements $UserPredictionCopyWith<$Res> {
  factory _$$UserPredictionImplCopyWith(_$UserPredictionImpl value,
          $Res Function(_$UserPredictionImpl) then) =
      __$$UserPredictionImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int userId,
      int modelId,
      double predictionScore,
      double confidence,
      String? predictedBehavior,
      String? actualBehavior,
      DateTime createdAt});
}

/// @nodoc
class __$$UserPredictionImplCopyWithImpl<$Res>
    extends _$UserPredictionCopyWithImpl<$Res, _$UserPredictionImpl>
    implements _$$UserPredictionImplCopyWith<$Res> {
  __$$UserPredictionImplCopyWithImpl(
      _$UserPredictionImpl _value, $Res Function(_$UserPredictionImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? modelId = null,
    Object? predictionScore = null,
    Object? confidence = null,
    Object? predictedBehavior = freezed,
    Object? actualBehavior = freezed,
    Object? createdAt = null,
  }) {
    return _then(_$UserPredictionImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      modelId: null == modelId
          ? _value.modelId
          : modelId // ignore: cast_nullable_to_non_nullable
              as int,
      predictionScore: null == predictionScore
          ? _value.predictionScore
          : predictionScore // ignore: cast_nullable_to_non_nullable
              as double,
      confidence: null == confidence
          ? _value.confidence
          : confidence // ignore: cast_nullable_to_non_nullable
              as double,
      predictedBehavior: freezed == predictedBehavior
          ? _value.predictedBehavior
          : predictedBehavior // ignore: cast_nullable_to_non_nullable
              as String?,
      actualBehavior: freezed == actualBehavior
          ? _value.actualBehavior
          : actualBehavior // ignore: cast_nullable_to_non_nullable
              as String?,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$UserPredictionImpl implements _UserPrediction {
  const _$UserPredictionImpl(
      {required this.id,
      required this.userId,
      required this.modelId,
      required this.predictionScore,
      required this.confidence,
      this.predictedBehavior,
      this.actualBehavior,
      required this.createdAt});

  factory _$UserPredictionImpl.fromJson(Map<String, dynamic> json) =>
      _$$UserPredictionImplFromJson(json);

  @override
  final int id;
  @override
  final int userId;
  @override
  final int modelId;
  @override
  final double predictionScore;
  @override
  final double confidence;
  @override
  final String? predictedBehavior;
  @override
  final String? actualBehavior;
  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'UserPrediction(id: $id, userId: $userId, modelId: $modelId, predictionScore: $predictionScore, confidence: $confidence, predictedBehavior: $predictedBehavior, actualBehavior: $actualBehavior, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$UserPredictionImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.modelId, modelId) || other.modelId == modelId) &&
            (identical(other.predictionScore, predictionScore) ||
                other.predictionScore == predictionScore) &&
            (identical(other.confidence, confidence) ||
                other.confidence == confidence) &&
            (identical(other.predictedBehavior, predictedBehavior) ||
                other.predictedBehavior == predictedBehavior) &&
            (identical(other.actualBehavior, actualBehavior) ||
                other.actualBehavior == actualBehavior) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      userId,
      modelId,
      predictionScore,
      confidence,
      predictedBehavior,
      actualBehavior,
      createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$UserPredictionImplCopyWith<_$UserPredictionImpl> get copyWith =>
      __$$UserPredictionImplCopyWithImpl<_$UserPredictionImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$UserPredictionImplToJson(
      this,
    );
  }
}

abstract class _UserPrediction implements UserPrediction {
  const factory _UserPrediction(
      {required final int id,
      required final int userId,
      required final int modelId,
      required final double predictionScore,
      required final double confidence,
      final String? predictedBehavior,
      final String? actualBehavior,
      required final DateTime createdAt}) = _$UserPredictionImpl;

  factory _UserPrediction.fromJson(Map<String, dynamic> json) =
      _$UserPredictionImpl.fromJson;

  @override
  int get id;
  @override
  int get userId;
  @override
  int get modelId;
  @override
  double get predictionScore;
  @override
  double get confidence;
  @override
  String? get predictedBehavior;
  @override
  String? get actualBehavior;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$UserPredictionImplCopyWith<_$UserPredictionImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

RecommendationListResponse _$RecommendationListResponseFromJson(
    Map<String, dynamic> json) {
  return _RecommendationListResponse.fromJson(json);
}

/// @nodoc
mixin _$RecommendationListResponse {
  List<ContentRecommendation> get recommendations =>
      throw _privateConstructorUsedError;
  int get totalCount => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $RecommendationListResponseCopyWith<RecommendationListResponse>
      get copyWith => throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $RecommendationListResponseCopyWith<$Res> {
  factory $RecommendationListResponseCopyWith(RecommendationListResponse value,
          $Res Function(RecommendationListResponse) then) =
      _$RecommendationListResponseCopyWithImpl<$Res,
          RecommendationListResponse>;
  @useResult
  $Res call({List<ContentRecommendation> recommendations, int totalCount});
}

/// @nodoc
class _$RecommendationListResponseCopyWithImpl<$Res,
        $Val extends RecommendationListResponse>
    implements $RecommendationListResponseCopyWith<$Res> {
  _$RecommendationListResponseCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? recommendations = null,
    Object? totalCount = null,
  }) {
    return _then(_value.copyWith(
      recommendations: null == recommendations
          ? _value.recommendations
          : recommendations // ignore: cast_nullable_to_non_nullable
              as List<ContentRecommendation>,
      totalCount: null == totalCount
          ? _value.totalCount
          : totalCount // ignore: cast_nullable_to_non_nullable
              as int,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$RecommendationListResponseImplCopyWith<$Res>
    implements $RecommendationListResponseCopyWith<$Res> {
  factory _$$RecommendationListResponseImplCopyWith(
          _$RecommendationListResponseImpl value,
          $Res Function(_$RecommendationListResponseImpl) then) =
      __$$RecommendationListResponseImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({List<ContentRecommendation> recommendations, int totalCount});
}

/// @nodoc
class __$$RecommendationListResponseImplCopyWithImpl<$Res>
    extends _$RecommendationListResponseCopyWithImpl<$Res,
        _$RecommendationListResponseImpl>
    implements _$$RecommendationListResponseImplCopyWith<$Res> {
  __$$RecommendationListResponseImplCopyWithImpl(
      _$RecommendationListResponseImpl _value,
      $Res Function(_$RecommendationListResponseImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? recommendations = null,
    Object? totalCount = null,
  }) {
    return _then(_$RecommendationListResponseImpl(
      recommendations: null == recommendations
          ? _value._recommendations
          : recommendations // ignore: cast_nullable_to_non_nullable
              as List<ContentRecommendation>,
      totalCount: null == totalCount
          ? _value.totalCount
          : totalCount // ignore: cast_nullable_to_non_nullable
              as int,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$RecommendationListResponseImpl implements _RecommendationListResponse {
  const _$RecommendationListResponseImpl(
      {required final List<ContentRecommendation> recommendations,
      required this.totalCount})
      : _recommendations = recommendations;

  factory _$RecommendationListResponseImpl.fromJson(
          Map<String, dynamic> json) =>
      _$$RecommendationListResponseImplFromJson(json);

  final List<ContentRecommendation> _recommendations;
  @override
  List<ContentRecommendation> get recommendations {
    if (_recommendations is EqualUnmodifiableListView) return _recommendations;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_recommendations);
  }

  @override
  final int totalCount;

  @override
  String toString() {
    return 'RecommendationListResponse(recommendations: $recommendations, totalCount: $totalCount)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$RecommendationListResponseImpl &&
            const DeepCollectionEquality()
                .equals(other._recommendations, _recommendations) &&
            (identical(other.totalCount, totalCount) ||
                other.totalCount == totalCount));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType,
      const DeepCollectionEquality().hash(_recommendations), totalCount);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$RecommendationListResponseImplCopyWith<_$RecommendationListResponseImpl>
      get copyWith => __$$RecommendationListResponseImplCopyWithImpl<
          _$RecommendationListResponseImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$RecommendationListResponseImplToJson(
      this,
    );
  }
}

abstract class _RecommendationListResponse
    implements RecommendationListResponse {
  const factory _RecommendationListResponse(
      {required final List<ContentRecommendation> recommendations,
      required final int totalCount}) = _$RecommendationListResponseImpl;

  factory _RecommendationListResponse.fromJson(Map<String, dynamic> json) =
      _$RecommendationListResponseImpl.fromJson;

  @override
  List<ContentRecommendation> get recommendations;
  @override
  int get totalCount;
  @override
  @JsonKey(ignore: true)
  _$$RecommendationListResponseImplCopyWith<_$RecommendationListResponseImpl>
      get copyWith => throw _privateConstructorUsedError;
}

CohortMemberResponse _$CohortMemberResponseFromJson(Map<String, dynamic> json) {
  return _CohortMemberResponse.fromJson(json);
}

/// @nodoc
mixin _$CohortMemberResponse {
  int get cohortId => throw _privateConstructorUsedError;
  int get memberCount => throw _privateConstructorUsedError;
  List<int> get members => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $CohortMemberResponseCopyWith<CohortMemberResponse> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $CohortMemberResponseCopyWith<$Res> {
  factory $CohortMemberResponseCopyWith(CohortMemberResponse value,
          $Res Function(CohortMemberResponse) then) =
      _$CohortMemberResponseCopyWithImpl<$Res, CohortMemberResponse>;
  @useResult
  $Res call({int cohortId, int memberCount, List<int> members});
}

/// @nodoc
class _$CohortMemberResponseCopyWithImpl<$Res,
        $Val extends CohortMemberResponse>
    implements $CohortMemberResponseCopyWith<$Res> {
  _$CohortMemberResponseCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? cohortId = null,
    Object? memberCount = null,
    Object? members = null,
  }) {
    return _then(_value.copyWith(
      cohortId: null == cohortId
          ? _value.cohortId
          : cohortId // ignore: cast_nullable_to_non_nullable
              as int,
      memberCount: null == memberCount
          ? _value.memberCount
          : memberCount // ignore: cast_nullable_to_non_nullable
              as int,
      members: null == members
          ? _value.members
          : members // ignore: cast_nullable_to_non_nullable
              as List<int>,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$CohortMemberResponseImplCopyWith<$Res>
    implements $CohortMemberResponseCopyWith<$Res> {
  factory _$$CohortMemberResponseImplCopyWith(_$CohortMemberResponseImpl value,
          $Res Function(_$CohortMemberResponseImpl) then) =
      __$$CohortMemberResponseImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({int cohortId, int memberCount, List<int> members});
}

/// @nodoc
class __$$CohortMemberResponseImplCopyWithImpl<$Res>
    extends _$CohortMemberResponseCopyWithImpl<$Res, _$CohortMemberResponseImpl>
    implements _$$CohortMemberResponseImplCopyWith<$Res> {
  __$$CohortMemberResponseImplCopyWithImpl(_$CohortMemberResponseImpl _value,
      $Res Function(_$CohortMemberResponseImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? cohortId = null,
    Object? memberCount = null,
    Object? members = null,
  }) {
    return _then(_$CohortMemberResponseImpl(
      cohortId: null == cohortId
          ? _value.cohortId
          : cohortId // ignore: cast_nullable_to_non_nullable
              as int,
      memberCount: null == memberCount
          ? _value.memberCount
          : memberCount // ignore: cast_nullable_to_non_nullable
              as int,
      members: null == members
          ? _value._members
          : members // ignore: cast_nullable_to_non_nullable
              as List<int>,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$CohortMemberResponseImpl implements _CohortMemberResponse {
  const _$CohortMemberResponseImpl(
      {required this.cohortId,
      required this.memberCount,
      required final List<int> members})
      : _members = members;

  factory _$CohortMemberResponseImpl.fromJson(Map<String, dynamic> json) =>
      _$$CohortMemberResponseImplFromJson(json);

  @override
  final int cohortId;
  @override
  final int memberCount;
  final List<int> _members;
  @override
  List<int> get members {
    if (_members is EqualUnmodifiableListView) return _members;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_members);
  }

  @override
  String toString() {
    return 'CohortMemberResponse(cohortId: $cohortId, memberCount: $memberCount, members: $members)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$CohortMemberResponseImpl &&
            (identical(other.cohortId, cohortId) ||
                other.cohortId == cohortId) &&
            (identical(other.memberCount, memberCount) ||
                other.memberCount == memberCount) &&
            const DeepCollectionEquality().equals(other._members, _members));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, cohortId, memberCount,
      const DeepCollectionEquality().hash(_members));

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$CohortMemberResponseImplCopyWith<_$CohortMemberResponseImpl>
      get copyWith =>
          __$$CohortMemberResponseImplCopyWithImpl<_$CohortMemberResponseImpl>(
              this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$CohortMemberResponseImplToJson(
      this,
    );
  }
}

abstract class _CohortMemberResponse implements CohortMemberResponse {
  const factory _CohortMemberResponse(
      {required final int cohortId,
      required final int memberCount,
      required final List<int> members}) = _$CohortMemberResponseImpl;

  factory _CohortMemberResponse.fromJson(Map<String, dynamic> json) =
      _$CohortMemberResponseImpl.fromJson;

  @override
  int get cohortId;
  @override
  int get memberCount;
  @override
  List<int> get members;
  @override
  @JsonKey(ignore: true)
  _$$CohortMemberResponseImplCopyWith<_$CohortMemberResponseImpl>
      get copyWith => throw _privateConstructorUsedError;
}

UserPredictionListResponse _$UserPredictionListResponseFromJson(
    Map<String, dynamic> json) {
  return _UserPredictionListResponse.fromJson(json);
}

/// @nodoc
mixin _$UserPredictionListResponse {
  int get userId => throw _privateConstructorUsedError;
  List<UserPrediction> get predictions => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $UserPredictionListResponseCopyWith<UserPredictionListResponse>
      get copyWith => throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $UserPredictionListResponseCopyWith<$Res> {
  factory $UserPredictionListResponseCopyWith(UserPredictionListResponse value,
          $Res Function(UserPredictionListResponse) then) =
      _$UserPredictionListResponseCopyWithImpl<$Res,
          UserPredictionListResponse>;
  @useResult
  $Res call({int userId, List<UserPrediction> predictions});
}

/// @nodoc
class _$UserPredictionListResponseCopyWithImpl<$Res,
        $Val extends UserPredictionListResponse>
    implements $UserPredictionListResponseCopyWith<$Res> {
  _$UserPredictionListResponseCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? userId = null,
    Object? predictions = null,
  }) {
    return _then(_value.copyWith(
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      predictions: null == predictions
          ? _value.predictions
          : predictions // ignore: cast_nullable_to_non_nullable
              as List<UserPrediction>,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$UserPredictionListResponseImplCopyWith<$Res>
    implements $UserPredictionListResponseCopyWith<$Res> {
  factory _$$UserPredictionListResponseImplCopyWith(
          _$UserPredictionListResponseImpl value,
          $Res Function(_$UserPredictionListResponseImpl) then) =
      __$$UserPredictionListResponseImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({int userId, List<UserPrediction> predictions});
}

/// @nodoc
class __$$UserPredictionListResponseImplCopyWithImpl<$Res>
    extends _$UserPredictionListResponseCopyWithImpl<$Res,
        _$UserPredictionListResponseImpl>
    implements _$$UserPredictionListResponseImplCopyWith<$Res> {
  __$$UserPredictionListResponseImplCopyWithImpl(
      _$UserPredictionListResponseImpl _value,
      $Res Function(_$UserPredictionListResponseImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? userId = null,
    Object? predictions = null,
  }) {
    return _then(_$UserPredictionListResponseImpl(
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      predictions: null == predictions
          ? _value._predictions
          : predictions // ignore: cast_nullable_to_non_nullable
              as List<UserPrediction>,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$UserPredictionListResponseImpl implements _UserPredictionListResponse {
  const _$UserPredictionListResponseImpl(
      {required this.userId, required final List<UserPrediction> predictions})
      : _predictions = predictions;

  factory _$UserPredictionListResponseImpl.fromJson(
          Map<String, dynamic> json) =>
      _$$UserPredictionListResponseImplFromJson(json);

  @override
  final int userId;
  final List<UserPrediction> _predictions;
  @override
  List<UserPrediction> get predictions {
    if (_predictions is EqualUnmodifiableListView) return _predictions;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_predictions);
  }

  @override
  String toString() {
    return 'UserPredictionListResponse(userId: $userId, predictions: $predictions)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$UserPredictionListResponseImpl &&
            (identical(other.userId, userId) || other.userId == userId) &&
            const DeepCollectionEquality()
                .equals(other._predictions, _predictions));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType, userId, const DeepCollectionEquality().hash(_predictions));

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$UserPredictionListResponseImplCopyWith<_$UserPredictionListResponseImpl>
      get copyWith => __$$UserPredictionListResponseImplCopyWithImpl<
          _$UserPredictionListResponseImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$UserPredictionListResponseImplToJson(
      this,
    );
  }
}

abstract class _UserPredictionListResponse
    implements UserPredictionListResponse {
  const factory _UserPredictionListResponse(
          {required final int userId,
          required final List<UserPrediction> predictions}) =
      _$UserPredictionListResponseImpl;

  factory _UserPredictionListResponse.fromJson(Map<String, dynamic> json) =
      _$UserPredictionListResponseImpl.fromJson;

  @override
  int get userId;
  @override
  List<UserPrediction> get predictions;
  @override
  @JsonKey(ignore: true)
  _$$UserPredictionListResponseImplCopyWith<_$UserPredictionListResponseImpl>
      get copyWith => throw _privateConstructorUsedError;
}

// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'platform_completion_models.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
    'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models');

UserInteractionModel _$UserInteractionModelFromJson(Map<String, dynamic> json) {
  return _UserInteractionModel.fromJson(json);
}

/// @nodoc
mixin _$UserInteractionModel {
  int get id => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  int get contentId => throw _privateConstructorUsedError;
  String get interactionType => throw _privateConstructorUsedError;
  Map<String, dynamic> get metadata => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $UserInteractionModelCopyWith<UserInteractionModel> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $UserInteractionModelCopyWith<$Res> {
  factory $UserInteractionModelCopyWith(UserInteractionModel value,
          $Res Function(UserInteractionModel) then) =
      _$UserInteractionModelCopyWithImpl<$Res, UserInteractionModel>;
  @useResult
  $Res call(
      {int id,
      int userId,
      int contentId,
      String interactionType,
      Map<String, dynamic> metadata,
      DateTime createdAt});
}

/// @nodoc
class _$UserInteractionModelCopyWithImpl<$Res,
        $Val extends UserInteractionModel>
    implements $UserInteractionModelCopyWith<$Res> {
  _$UserInteractionModelCopyWithImpl(this._value, this._then);

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
    Object? interactionType = null,
    Object? metadata = null,
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
      contentId: null == contentId
          ? _value.contentId
          : contentId // ignore: cast_nullable_to_non_nullable
              as int,
      interactionType: null == interactionType
          ? _value.interactionType
          : interactionType // ignore: cast_nullable_to_non_nullable
              as String,
      metadata: null == metadata
          ? _value.metadata
          : metadata // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$UserInteractionModelImplCopyWith<$Res>
    implements $UserInteractionModelCopyWith<$Res> {
  factory _$$UserInteractionModelImplCopyWith(_$UserInteractionModelImpl value,
          $Res Function(_$UserInteractionModelImpl) then) =
      __$$UserInteractionModelImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int userId,
      int contentId,
      String interactionType,
      Map<String, dynamic> metadata,
      DateTime createdAt});
}

/// @nodoc
class __$$UserInteractionModelImplCopyWithImpl<$Res>
    extends _$UserInteractionModelCopyWithImpl<$Res, _$UserInteractionModelImpl>
    implements _$$UserInteractionModelImplCopyWith<$Res> {
  __$$UserInteractionModelImplCopyWithImpl(_$UserInteractionModelImpl _value,
      $Res Function(_$UserInteractionModelImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? contentId = null,
    Object? interactionType = null,
    Object? metadata = null,
    Object? createdAt = null,
  }) {
    return _then(_$UserInteractionModelImpl(
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
      interactionType: null == interactionType
          ? _value.interactionType
          : interactionType // ignore: cast_nullable_to_non_nullable
              as String,
      metadata: null == metadata
          ? _value._metadata
          : metadata // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$UserInteractionModelImpl implements _UserInteractionModel {
  const _$UserInteractionModelImpl(
      {required this.id,
      required this.userId,
      required this.contentId,
      required this.interactionType,
      required final Map<String, dynamic> metadata,
      required this.createdAt})
      : _metadata = metadata;

  factory _$UserInteractionModelImpl.fromJson(Map<String, dynamic> json) =>
      _$$UserInteractionModelImplFromJson(json);

  @override
  final int id;
  @override
  final int userId;
  @override
  final int contentId;
  @override
  final String interactionType;
  final Map<String, dynamic> _metadata;
  @override
  Map<String, dynamic> get metadata {
    if (_metadata is EqualUnmodifiableMapView) return _metadata;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(_metadata);
  }

  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'UserInteractionModel(id: $id, userId: $userId, contentId: $contentId, interactionType: $interactionType, metadata: $metadata, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$UserInteractionModelImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.contentId, contentId) ||
                other.contentId == contentId) &&
            (identical(other.interactionType, interactionType) ||
                other.interactionType == interactionType) &&
            const DeepCollectionEquality().equals(other._metadata, _metadata) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      userId,
      contentId,
      interactionType,
      const DeepCollectionEquality().hash(_metadata),
      createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$UserInteractionModelImplCopyWith<_$UserInteractionModelImpl>
      get copyWith =>
          __$$UserInteractionModelImplCopyWithImpl<_$UserInteractionModelImpl>(
              this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$UserInteractionModelImplToJson(
      this,
    );
  }
}

abstract class _UserInteractionModel implements UserInteractionModel {
  const factory _UserInteractionModel(
      {required final int id,
      required final int userId,
      required final int contentId,
      required final String interactionType,
      required final Map<String, dynamic> metadata,
      required final DateTime createdAt}) = _$UserInteractionModelImpl;

  factory _UserInteractionModel.fromJson(Map<String, dynamic> json) =
      _$UserInteractionModelImpl.fromJson;

  @override
  int get id;
  @override
  int get userId;
  @override
  int get contentId;
  @override
  String get interactionType;
  @override
  Map<String, dynamic> get metadata;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$UserInteractionModelImplCopyWith<_$UserInteractionModelImpl>
      get copyWith => throw _privateConstructorUsedError;
}

UserFollowModel _$UserFollowModelFromJson(Map<String, dynamic> json) {
  return _UserFollowModel.fromJson(json);
}

/// @nodoc
mixin _$UserFollowModel {
  int get id => throw _privateConstructorUsedError;
  int get followerId => throw _privateConstructorUsedError;
  int get followingId => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $UserFollowModelCopyWith<UserFollowModel> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $UserFollowModelCopyWith<$Res> {
  factory $UserFollowModelCopyWith(
          UserFollowModel value, $Res Function(UserFollowModel) then) =
      _$UserFollowModelCopyWithImpl<$Res, UserFollowModel>;
  @useResult
  $Res call({int id, int followerId, int followingId, DateTime createdAt});
}

/// @nodoc
class _$UserFollowModelCopyWithImpl<$Res, $Val extends UserFollowModel>
    implements $UserFollowModelCopyWith<$Res> {
  _$UserFollowModelCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? followerId = null,
    Object? followingId = null,
    Object? createdAt = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      followerId: null == followerId
          ? _value.followerId
          : followerId // ignore: cast_nullable_to_non_nullable
              as int,
      followingId: null == followingId
          ? _value.followingId
          : followingId // ignore: cast_nullable_to_non_nullable
              as int,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$UserFollowModelImplCopyWith<$Res>
    implements $UserFollowModelCopyWith<$Res> {
  factory _$$UserFollowModelImplCopyWith(_$UserFollowModelImpl value,
          $Res Function(_$UserFollowModelImpl) then) =
      __$$UserFollowModelImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({int id, int followerId, int followingId, DateTime createdAt});
}

/// @nodoc
class __$$UserFollowModelImplCopyWithImpl<$Res>
    extends _$UserFollowModelCopyWithImpl<$Res, _$UserFollowModelImpl>
    implements _$$UserFollowModelImplCopyWith<$Res> {
  __$$UserFollowModelImplCopyWithImpl(
      _$UserFollowModelImpl _value, $Res Function(_$UserFollowModelImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? followerId = null,
    Object? followingId = null,
    Object? createdAt = null,
  }) {
    return _then(_$UserFollowModelImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      followerId: null == followerId
          ? _value.followerId
          : followerId // ignore: cast_nullable_to_non_nullable
              as int,
      followingId: null == followingId
          ? _value.followingId
          : followingId // ignore: cast_nullable_to_non_nullable
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
class _$UserFollowModelImpl implements _UserFollowModel {
  const _$UserFollowModelImpl(
      {required this.id,
      required this.followerId,
      required this.followingId,
      required this.createdAt});

  factory _$UserFollowModelImpl.fromJson(Map<String, dynamic> json) =>
      _$$UserFollowModelImplFromJson(json);

  @override
  final int id;
  @override
  final int followerId;
  @override
  final int followingId;
  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'UserFollowModel(id: $id, followerId: $followerId, followingId: $followingId, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$UserFollowModelImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.followerId, followerId) ||
                other.followerId == followerId) &&
            (identical(other.followingId, followingId) ||
                other.followingId == followingId) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode =>
      Object.hash(runtimeType, id, followerId, followingId, createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$UserFollowModelImplCopyWith<_$UserFollowModelImpl> get copyWith =>
      __$$UserFollowModelImplCopyWithImpl<_$UserFollowModelImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$UserFollowModelImplToJson(
      this,
    );
  }
}

abstract class _UserFollowModel implements UserFollowModel {
  const factory _UserFollowModel(
      {required final int id,
      required final int followerId,
      required final int followingId,
      required final DateTime createdAt}) = _$UserFollowModelImpl;

  factory _UserFollowModel.fromJson(Map<String, dynamic> json) =
      _$UserFollowModelImpl.fromJson;

  @override
  int get id;
  @override
  int get followerId;
  @override
  int get followingId;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$UserFollowModelImplCopyWith<_$UserFollowModelImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

ContentCommentModel _$ContentCommentModelFromJson(Map<String, dynamic> json) {
  return _ContentCommentModel.fromJson(json);
}

/// @nodoc
mixin _$ContentCommentModel {
  int get id => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  int get contentId => throw _privateConstructorUsedError;
  String get text => throw _privateConstructorUsedError;
  int? get parentCommentId => throw _privateConstructorUsedError;
  String get status => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $ContentCommentModelCopyWith<ContentCommentModel> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $ContentCommentModelCopyWith<$Res> {
  factory $ContentCommentModelCopyWith(
          ContentCommentModel value, $Res Function(ContentCommentModel) then) =
      _$ContentCommentModelCopyWithImpl<$Res, ContentCommentModel>;
  @useResult
  $Res call(
      {int id,
      int userId,
      int contentId,
      String text,
      int? parentCommentId,
      String status,
      DateTime createdAt});
}

/// @nodoc
class _$ContentCommentModelCopyWithImpl<$Res, $Val extends ContentCommentModel>
    implements $ContentCommentModelCopyWith<$Res> {
  _$ContentCommentModelCopyWithImpl(this._value, this._then);

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
    Object? text = null,
    Object? parentCommentId = freezed,
    Object? status = null,
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
      contentId: null == contentId
          ? _value.contentId
          : contentId // ignore: cast_nullable_to_non_nullable
              as int,
      text: null == text
          ? _value.text
          : text // ignore: cast_nullable_to_non_nullable
              as String,
      parentCommentId: freezed == parentCommentId
          ? _value.parentCommentId
          : parentCommentId // ignore: cast_nullable_to_non_nullable
              as int?,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$ContentCommentModelImplCopyWith<$Res>
    implements $ContentCommentModelCopyWith<$Res> {
  factory _$$ContentCommentModelImplCopyWith(_$ContentCommentModelImpl value,
          $Res Function(_$ContentCommentModelImpl) then) =
      __$$ContentCommentModelImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int userId,
      int contentId,
      String text,
      int? parentCommentId,
      String status,
      DateTime createdAt});
}

/// @nodoc
class __$$ContentCommentModelImplCopyWithImpl<$Res>
    extends _$ContentCommentModelCopyWithImpl<$Res, _$ContentCommentModelImpl>
    implements _$$ContentCommentModelImplCopyWith<$Res> {
  __$$ContentCommentModelImplCopyWithImpl(_$ContentCommentModelImpl _value,
      $Res Function(_$ContentCommentModelImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? contentId = null,
    Object? text = null,
    Object? parentCommentId = freezed,
    Object? status = null,
    Object? createdAt = null,
  }) {
    return _then(_$ContentCommentModelImpl(
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
      text: null == text
          ? _value.text
          : text // ignore: cast_nullable_to_non_nullable
              as String,
      parentCommentId: freezed == parentCommentId
          ? _value.parentCommentId
          : parentCommentId // ignore: cast_nullable_to_non_nullable
              as int?,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$ContentCommentModelImpl implements _ContentCommentModel {
  const _$ContentCommentModelImpl(
      {required this.id,
      required this.userId,
      required this.contentId,
      required this.text,
      this.parentCommentId,
      required this.status,
      required this.createdAt});

  factory _$ContentCommentModelImpl.fromJson(Map<String, dynamic> json) =>
      _$$ContentCommentModelImplFromJson(json);

  @override
  final int id;
  @override
  final int userId;
  @override
  final int contentId;
  @override
  final String text;
  @override
  final int? parentCommentId;
  @override
  final String status;
  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'ContentCommentModel(id: $id, userId: $userId, contentId: $contentId, text: $text, parentCommentId: $parentCommentId, status: $status, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$ContentCommentModelImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.contentId, contentId) ||
                other.contentId == contentId) &&
            (identical(other.text, text) || other.text == text) &&
            (identical(other.parentCommentId, parentCommentId) ||
                other.parentCommentId == parentCommentId) &&
            (identical(other.status, status) || other.status == status) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, id, userId, contentId, text,
      parentCommentId, status, createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$ContentCommentModelImplCopyWith<_$ContentCommentModelImpl> get copyWith =>
      __$$ContentCommentModelImplCopyWithImpl<_$ContentCommentModelImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$ContentCommentModelImplToJson(
      this,
    );
  }
}

abstract class _ContentCommentModel implements ContentCommentModel {
  const factory _ContentCommentModel(
      {required final int id,
      required final int userId,
      required final int contentId,
      required final String text,
      final int? parentCommentId,
      required final String status,
      required final DateTime createdAt}) = _$ContentCommentModelImpl;

  factory _ContentCommentModel.fromJson(Map<String, dynamic> json) =
      _$ContentCommentModelImpl.fromJson;

  @override
  int get id;
  @override
  int get userId;
  @override
  int get contentId;
  @override
  String get text;
  @override
  int? get parentCommentId;
  @override
  String get status;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$ContentCommentModelImplCopyWith<_$ContentCommentModelImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

UserMessageModel _$UserMessageModelFromJson(Map<String, dynamic> json) {
  return _UserMessageModel.fromJson(json);
}

/// @nodoc
mixin _$UserMessageModel {
  int get id => throw _privateConstructorUsedError;
  int get senderId => throw _privateConstructorUsedError;
  int get recipientId => throw _privateConstructorUsedError;
  String get text => throw _privateConstructorUsedError;
  bool get read => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $UserMessageModelCopyWith<UserMessageModel> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $UserMessageModelCopyWith<$Res> {
  factory $UserMessageModelCopyWith(
          UserMessageModel value, $Res Function(UserMessageModel) then) =
      _$UserMessageModelCopyWithImpl<$Res, UserMessageModel>;
  @useResult
  $Res call(
      {int id,
      int senderId,
      int recipientId,
      String text,
      bool read,
      DateTime createdAt});
}

/// @nodoc
class _$UserMessageModelCopyWithImpl<$Res, $Val extends UserMessageModel>
    implements $UserMessageModelCopyWith<$Res> {
  _$UserMessageModelCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? senderId = null,
    Object? recipientId = null,
    Object? text = null,
    Object? read = null,
    Object? createdAt = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      senderId: null == senderId
          ? _value.senderId
          : senderId // ignore: cast_nullable_to_non_nullable
              as int,
      recipientId: null == recipientId
          ? _value.recipientId
          : recipientId // ignore: cast_nullable_to_non_nullable
              as int,
      text: null == text
          ? _value.text
          : text // ignore: cast_nullable_to_non_nullable
              as String,
      read: null == read
          ? _value.read
          : read // ignore: cast_nullable_to_non_nullable
              as bool,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$UserMessageModelImplCopyWith<$Res>
    implements $UserMessageModelCopyWith<$Res> {
  factory _$$UserMessageModelImplCopyWith(_$UserMessageModelImpl value,
          $Res Function(_$UserMessageModelImpl) then) =
      __$$UserMessageModelImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int senderId,
      int recipientId,
      String text,
      bool read,
      DateTime createdAt});
}

/// @nodoc
class __$$UserMessageModelImplCopyWithImpl<$Res>
    extends _$UserMessageModelCopyWithImpl<$Res, _$UserMessageModelImpl>
    implements _$$UserMessageModelImplCopyWith<$Res> {
  __$$UserMessageModelImplCopyWithImpl(_$UserMessageModelImpl _value,
      $Res Function(_$UserMessageModelImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? senderId = null,
    Object? recipientId = null,
    Object? text = null,
    Object? read = null,
    Object? createdAt = null,
  }) {
    return _then(_$UserMessageModelImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      senderId: null == senderId
          ? _value.senderId
          : senderId // ignore: cast_nullable_to_non_nullable
              as int,
      recipientId: null == recipientId
          ? _value.recipientId
          : recipientId // ignore: cast_nullable_to_non_nullable
              as int,
      text: null == text
          ? _value.text
          : text // ignore: cast_nullable_to_non_nullable
              as String,
      read: null == read
          ? _value.read
          : read // ignore: cast_nullable_to_non_nullable
              as bool,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$UserMessageModelImpl implements _UserMessageModel {
  const _$UserMessageModelImpl(
      {required this.id,
      required this.senderId,
      required this.recipientId,
      required this.text,
      required this.read,
      required this.createdAt});

  factory _$UserMessageModelImpl.fromJson(Map<String, dynamic> json) =>
      _$$UserMessageModelImplFromJson(json);

  @override
  final int id;
  @override
  final int senderId;
  @override
  final int recipientId;
  @override
  final String text;
  @override
  final bool read;
  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'UserMessageModel(id: $id, senderId: $senderId, recipientId: $recipientId, text: $text, read: $read, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$UserMessageModelImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.senderId, senderId) ||
                other.senderId == senderId) &&
            (identical(other.recipientId, recipientId) ||
                other.recipientId == recipientId) &&
            (identical(other.text, text) || other.text == text) &&
            (identical(other.read, read) || other.read == read) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType, id, senderId, recipientId, text, read, createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$UserMessageModelImplCopyWith<_$UserMessageModelImpl> get copyWith =>
      __$$UserMessageModelImplCopyWithImpl<_$UserMessageModelImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$UserMessageModelImplToJson(
      this,
    );
  }
}

abstract class _UserMessageModel implements UserMessageModel {
  const factory _UserMessageModel(
      {required final int id,
      required final int senderId,
      required final int recipientId,
      required final String text,
      required final bool read,
      required final DateTime createdAt}) = _$UserMessageModelImpl;

  factory _UserMessageModel.fromJson(Map<String, dynamic> json) =
      _$UserMessageModelImpl.fromJson;

  @override
  int get id;
  @override
  int get senderId;
  @override
  int get recipientId;
  @override
  String get text;
  @override
  bool get read;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$UserMessageModelImplCopyWith<_$UserMessageModelImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

SearchIndexModel _$SearchIndexModelFromJson(Map<String, dynamic> json) {
  return _SearchIndexModel.fromJson(json);
}

/// @nodoc
mixin _$SearchIndexModel {
  int get id => throw _privateConstructorUsedError;
  int get contentId => throw _privateConstructorUsedError;
  String get indexType => throw _privateConstructorUsedError;
  String get title => throw _privateConstructorUsedError;
  String get content => throw _privateConstructorUsedError;
  Map<String, dynamic> get metadata => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $SearchIndexModelCopyWith<SearchIndexModel> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $SearchIndexModelCopyWith<$Res> {
  factory $SearchIndexModelCopyWith(
          SearchIndexModel value, $Res Function(SearchIndexModel) then) =
      _$SearchIndexModelCopyWithImpl<$Res, SearchIndexModel>;
  @useResult
  $Res call(
      {int id,
      int contentId,
      String indexType,
      String title,
      String content,
      Map<String, dynamic> metadata,
      DateTime createdAt});
}

/// @nodoc
class _$SearchIndexModelCopyWithImpl<$Res, $Val extends SearchIndexModel>
    implements $SearchIndexModelCopyWith<$Res> {
  _$SearchIndexModelCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? contentId = null,
    Object? indexType = null,
    Object? title = null,
    Object? content = null,
    Object? metadata = null,
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
      indexType: null == indexType
          ? _value.indexType
          : indexType // ignore: cast_nullable_to_non_nullable
              as String,
      title: null == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String,
      content: null == content
          ? _value.content
          : content // ignore: cast_nullable_to_non_nullable
              as String,
      metadata: null == metadata
          ? _value.metadata
          : metadata // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$SearchIndexModelImplCopyWith<$Res>
    implements $SearchIndexModelCopyWith<$Res> {
  factory _$$SearchIndexModelImplCopyWith(_$SearchIndexModelImpl value,
          $Res Function(_$SearchIndexModelImpl) then) =
      __$$SearchIndexModelImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int contentId,
      String indexType,
      String title,
      String content,
      Map<String, dynamic> metadata,
      DateTime createdAt});
}

/// @nodoc
class __$$SearchIndexModelImplCopyWithImpl<$Res>
    extends _$SearchIndexModelCopyWithImpl<$Res, _$SearchIndexModelImpl>
    implements _$$SearchIndexModelImplCopyWith<$Res> {
  __$$SearchIndexModelImplCopyWithImpl(_$SearchIndexModelImpl _value,
      $Res Function(_$SearchIndexModelImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? contentId = null,
    Object? indexType = null,
    Object? title = null,
    Object? content = null,
    Object? metadata = null,
    Object? createdAt = null,
  }) {
    return _then(_$SearchIndexModelImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      contentId: null == contentId
          ? _value.contentId
          : contentId // ignore: cast_nullable_to_non_nullable
              as int,
      indexType: null == indexType
          ? _value.indexType
          : indexType // ignore: cast_nullable_to_non_nullable
              as String,
      title: null == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String,
      content: null == content
          ? _value.content
          : content // ignore: cast_nullable_to_non_nullable
              as String,
      metadata: null == metadata
          ? _value._metadata
          : metadata // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$SearchIndexModelImpl implements _SearchIndexModel {
  const _$SearchIndexModelImpl(
      {required this.id,
      required this.contentId,
      required this.indexType,
      required this.title,
      required this.content,
      required final Map<String, dynamic> metadata,
      required this.createdAt})
      : _metadata = metadata;

  factory _$SearchIndexModelImpl.fromJson(Map<String, dynamic> json) =>
      _$$SearchIndexModelImplFromJson(json);

  @override
  final int id;
  @override
  final int contentId;
  @override
  final String indexType;
  @override
  final String title;
  @override
  final String content;
  final Map<String, dynamic> _metadata;
  @override
  Map<String, dynamic> get metadata {
    if (_metadata is EqualUnmodifiableMapView) return _metadata;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(_metadata);
  }

  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'SearchIndexModel(id: $id, contentId: $contentId, indexType: $indexType, title: $title, content: $content, metadata: $metadata, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$SearchIndexModelImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.contentId, contentId) ||
                other.contentId == contentId) &&
            (identical(other.indexType, indexType) ||
                other.indexType == indexType) &&
            (identical(other.title, title) || other.title == title) &&
            (identical(other.content, content) || other.content == content) &&
            const DeepCollectionEquality().equals(other._metadata, _metadata) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, id, contentId, indexType, title,
      content, const DeepCollectionEquality().hash(_metadata), createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$SearchIndexModelImplCopyWith<_$SearchIndexModelImpl> get copyWith =>
      __$$SearchIndexModelImplCopyWithImpl<_$SearchIndexModelImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$SearchIndexModelImplToJson(
      this,
    );
  }
}

abstract class _SearchIndexModel implements SearchIndexModel {
  const factory _SearchIndexModel(
      {required final int id,
      required final int contentId,
      required final String indexType,
      required final String title,
      required final String content,
      required final Map<String, dynamic> metadata,
      required final DateTime createdAt}) = _$SearchIndexModelImpl;

  factory _SearchIndexModel.fromJson(Map<String, dynamic> json) =
      _$SearchIndexModelImpl.fromJson;

  @override
  int get id;
  @override
  int get contentId;
  @override
  String get indexType;
  @override
  String get title;
  @override
  String get content;
  @override
  Map<String, dynamic> get metadata;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$SearchIndexModelImplCopyWith<_$SearchIndexModelImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

SavedSearchModel _$SavedSearchModelFromJson(Map<String, dynamic> json) {
  return _SavedSearchModel.fromJson(json);
}

/// @nodoc
mixin _$SavedSearchModel {
  int get id => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  String get query => throw _privateConstructorUsedError;
  Map<String, dynamic> get filters => throw _privateConstructorUsedError;
  int get resultCount => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $SavedSearchModelCopyWith<SavedSearchModel> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $SavedSearchModelCopyWith<$Res> {
  factory $SavedSearchModelCopyWith(
          SavedSearchModel value, $Res Function(SavedSearchModel) then) =
      _$SavedSearchModelCopyWithImpl<$Res, SavedSearchModel>;
  @useResult
  $Res call(
      {int id,
      int userId,
      String query,
      Map<String, dynamic> filters,
      int resultCount,
      DateTime createdAt});
}

/// @nodoc
class _$SavedSearchModelCopyWithImpl<$Res, $Val extends SavedSearchModel>
    implements $SavedSearchModelCopyWith<$Res> {
  _$SavedSearchModelCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? query = null,
    Object? filters = null,
    Object? resultCount = null,
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
      query: null == query
          ? _value.query
          : query // ignore: cast_nullable_to_non_nullable
              as String,
      filters: null == filters
          ? _value.filters
          : filters // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      resultCount: null == resultCount
          ? _value.resultCount
          : resultCount // ignore: cast_nullable_to_non_nullable
              as int,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$SavedSearchModelImplCopyWith<$Res>
    implements $SavedSearchModelCopyWith<$Res> {
  factory _$$SavedSearchModelImplCopyWith(_$SavedSearchModelImpl value,
          $Res Function(_$SavedSearchModelImpl) then) =
      __$$SavedSearchModelImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int userId,
      String query,
      Map<String, dynamic> filters,
      int resultCount,
      DateTime createdAt});
}

/// @nodoc
class __$$SavedSearchModelImplCopyWithImpl<$Res>
    extends _$SavedSearchModelCopyWithImpl<$Res, _$SavedSearchModelImpl>
    implements _$$SavedSearchModelImplCopyWith<$Res> {
  __$$SavedSearchModelImplCopyWithImpl(_$SavedSearchModelImpl _value,
      $Res Function(_$SavedSearchModelImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? query = null,
    Object? filters = null,
    Object? resultCount = null,
    Object? createdAt = null,
  }) {
    return _then(_$SavedSearchModelImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      query: null == query
          ? _value.query
          : query // ignore: cast_nullable_to_non_nullable
              as String,
      filters: null == filters
          ? _value._filters
          : filters // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      resultCount: null == resultCount
          ? _value.resultCount
          : resultCount // ignore: cast_nullable_to_non_nullable
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
class _$SavedSearchModelImpl implements _SavedSearchModel {
  const _$SavedSearchModelImpl(
      {required this.id,
      required this.userId,
      required this.query,
      required final Map<String, dynamic> filters,
      required this.resultCount,
      required this.createdAt})
      : _filters = filters;

  factory _$SavedSearchModelImpl.fromJson(Map<String, dynamic> json) =>
      _$$SavedSearchModelImplFromJson(json);

  @override
  final int id;
  @override
  final int userId;
  @override
  final String query;
  final Map<String, dynamic> _filters;
  @override
  Map<String, dynamic> get filters {
    if (_filters is EqualUnmodifiableMapView) return _filters;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(_filters);
  }

  @override
  final int resultCount;
  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'SavedSearchModel(id: $id, userId: $userId, query: $query, filters: $filters, resultCount: $resultCount, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$SavedSearchModelImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.query, query) || other.query == query) &&
            const DeepCollectionEquality().equals(other._filters, _filters) &&
            (identical(other.resultCount, resultCount) ||
                other.resultCount == resultCount) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, id, userId, query,
      const DeepCollectionEquality().hash(_filters), resultCount, createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$SavedSearchModelImplCopyWith<_$SavedSearchModelImpl> get copyWith =>
      __$$SavedSearchModelImplCopyWithImpl<_$SavedSearchModelImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$SavedSearchModelImplToJson(
      this,
    );
  }
}

abstract class _SavedSearchModel implements SavedSearchModel {
  const factory _SavedSearchModel(
      {required final int id,
      required final int userId,
      required final String query,
      required final Map<String, dynamic> filters,
      required final int resultCount,
      required final DateTime createdAt}) = _$SavedSearchModelImpl;

  factory _SavedSearchModel.fromJson(Map<String, dynamic> json) =
      _$SavedSearchModelImpl.fromJson;

  @override
  int get id;
  @override
  int get userId;
  @override
  String get query;
  @override
  Map<String, dynamic> get filters;
  @override
  int get resultCount;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$SavedSearchModelImplCopyWith<_$SavedSearchModelImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

PushNotificationConfigModel _$PushNotificationConfigModelFromJson(
    Map<String, dynamic> json) {
  return _PushNotificationConfigModel.fromJson(json);
}

/// @nodoc
mixin _$PushNotificationConfigModel {
  int get id => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  String get deviceToken => throw _privateConstructorUsedError;
  String get platform => throw _privateConstructorUsedError;
  String? get deviceName => throw _privateConstructorUsedError;
  DateTime get lastActive => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $PushNotificationConfigModelCopyWith<PushNotificationConfigModel>
      get copyWith => throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $PushNotificationConfigModelCopyWith<$Res> {
  factory $PushNotificationConfigModelCopyWith(
          PushNotificationConfigModel value,
          $Res Function(PushNotificationConfigModel) then) =
      _$PushNotificationConfigModelCopyWithImpl<$Res,
          PushNotificationConfigModel>;
  @useResult
  $Res call(
      {int id,
      int userId,
      String deviceToken,
      String platform,
      String? deviceName,
      DateTime lastActive,
      DateTime createdAt});
}

/// @nodoc
class _$PushNotificationConfigModelCopyWithImpl<$Res,
        $Val extends PushNotificationConfigModel>
    implements $PushNotificationConfigModelCopyWith<$Res> {
  _$PushNotificationConfigModelCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? deviceToken = null,
    Object? platform = null,
    Object? deviceName = freezed,
    Object? lastActive = null,
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
      deviceToken: null == deviceToken
          ? _value.deviceToken
          : deviceToken // ignore: cast_nullable_to_non_nullable
              as String,
      platform: null == platform
          ? _value.platform
          : platform // ignore: cast_nullable_to_non_nullable
              as String,
      deviceName: freezed == deviceName
          ? _value.deviceName
          : deviceName // ignore: cast_nullable_to_non_nullable
              as String?,
      lastActive: null == lastActive
          ? _value.lastActive
          : lastActive // ignore: cast_nullable_to_non_nullable
              as DateTime,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$PushNotificationConfigModelImplCopyWith<$Res>
    implements $PushNotificationConfigModelCopyWith<$Res> {
  factory _$$PushNotificationConfigModelImplCopyWith(
          _$PushNotificationConfigModelImpl value,
          $Res Function(_$PushNotificationConfigModelImpl) then) =
      __$$PushNotificationConfigModelImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int userId,
      String deviceToken,
      String platform,
      String? deviceName,
      DateTime lastActive,
      DateTime createdAt});
}

/// @nodoc
class __$$PushNotificationConfigModelImplCopyWithImpl<$Res>
    extends _$PushNotificationConfigModelCopyWithImpl<$Res,
        _$PushNotificationConfigModelImpl>
    implements _$$PushNotificationConfigModelImplCopyWith<$Res> {
  __$$PushNotificationConfigModelImplCopyWithImpl(
      _$PushNotificationConfigModelImpl _value,
      $Res Function(_$PushNotificationConfigModelImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? deviceToken = null,
    Object? platform = null,
    Object? deviceName = freezed,
    Object? lastActive = null,
    Object? createdAt = null,
  }) {
    return _then(_$PushNotificationConfigModelImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      deviceToken: null == deviceToken
          ? _value.deviceToken
          : deviceToken // ignore: cast_nullable_to_non_nullable
              as String,
      platform: null == platform
          ? _value.platform
          : platform // ignore: cast_nullable_to_non_nullable
              as String,
      deviceName: freezed == deviceName
          ? _value.deviceName
          : deviceName // ignore: cast_nullable_to_non_nullable
              as String?,
      lastActive: null == lastActive
          ? _value.lastActive
          : lastActive // ignore: cast_nullable_to_non_nullable
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
class _$PushNotificationConfigModelImpl
    implements _PushNotificationConfigModel {
  const _$PushNotificationConfigModelImpl(
      {required this.id,
      required this.userId,
      required this.deviceToken,
      required this.platform,
      this.deviceName,
      required this.lastActive,
      required this.createdAt});

  factory _$PushNotificationConfigModelImpl.fromJson(
          Map<String, dynamic> json) =>
      _$$PushNotificationConfigModelImplFromJson(json);

  @override
  final int id;
  @override
  final int userId;
  @override
  final String deviceToken;
  @override
  final String platform;
  @override
  final String? deviceName;
  @override
  final DateTime lastActive;
  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'PushNotificationConfigModel(id: $id, userId: $userId, deviceToken: $deviceToken, platform: $platform, deviceName: $deviceName, lastActive: $lastActive, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$PushNotificationConfigModelImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.deviceToken, deviceToken) ||
                other.deviceToken == deviceToken) &&
            (identical(other.platform, platform) ||
                other.platform == platform) &&
            (identical(other.deviceName, deviceName) ||
                other.deviceName == deviceName) &&
            (identical(other.lastActive, lastActive) ||
                other.lastActive == lastActive) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, id, userId, deviceToken,
      platform, deviceName, lastActive, createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$PushNotificationConfigModelImplCopyWith<_$PushNotificationConfigModelImpl>
      get copyWith => __$$PushNotificationConfigModelImplCopyWithImpl<
          _$PushNotificationConfigModelImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$PushNotificationConfigModelImplToJson(
      this,
    );
  }
}

abstract class _PushNotificationConfigModel
    implements PushNotificationConfigModel {
  const factory _PushNotificationConfigModel(
      {required final int id,
      required final int userId,
      required final String deviceToken,
      required final String platform,
      final String? deviceName,
      required final DateTime lastActive,
      required final DateTime createdAt}) = _$PushNotificationConfigModelImpl;

  factory _PushNotificationConfigModel.fromJson(Map<String, dynamic> json) =
      _$PushNotificationConfigModelImpl.fromJson;

  @override
  int get id;
  @override
  int get userId;
  @override
  String get deviceToken;
  @override
  String get platform;
  @override
  String? get deviceName;
  @override
  DateTime get lastActive;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$PushNotificationConfigModelImplCopyWith<_$PushNotificationConfigModelImpl>
      get copyWith => throw _privateConstructorUsedError;
}

PushNotificationLogModel _$PushNotificationLogModelFromJson(
    Map<String, dynamic> json) {
  return _PushNotificationLogModel.fromJson(json);
}

/// @nodoc
mixin _$PushNotificationLogModel {
  int get id => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  String get notificationType => throw _privateConstructorUsedError;
  String get title => throw _privateConstructorUsedError;
  String get body => throw _privateConstructorUsedError;
  String get status => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $PushNotificationLogModelCopyWith<PushNotificationLogModel> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $PushNotificationLogModelCopyWith<$Res> {
  factory $PushNotificationLogModelCopyWith(PushNotificationLogModel value,
          $Res Function(PushNotificationLogModel) then) =
      _$PushNotificationLogModelCopyWithImpl<$Res, PushNotificationLogModel>;
  @useResult
  $Res call(
      {int id,
      int userId,
      String notificationType,
      String title,
      String body,
      String status,
      DateTime createdAt});
}

/// @nodoc
class _$PushNotificationLogModelCopyWithImpl<$Res,
        $Val extends PushNotificationLogModel>
    implements $PushNotificationLogModelCopyWith<$Res> {
  _$PushNotificationLogModelCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? notificationType = null,
    Object? title = null,
    Object? body = null,
    Object? status = null,
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
      notificationType: null == notificationType
          ? _value.notificationType
          : notificationType // ignore: cast_nullable_to_non_nullable
              as String,
      title: null == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String,
      body: null == body
          ? _value.body
          : body // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$PushNotificationLogModelImplCopyWith<$Res>
    implements $PushNotificationLogModelCopyWith<$Res> {
  factory _$$PushNotificationLogModelImplCopyWith(
          _$PushNotificationLogModelImpl value,
          $Res Function(_$PushNotificationLogModelImpl) then) =
      __$$PushNotificationLogModelImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int userId,
      String notificationType,
      String title,
      String body,
      String status,
      DateTime createdAt});
}

/// @nodoc
class __$$PushNotificationLogModelImplCopyWithImpl<$Res>
    extends _$PushNotificationLogModelCopyWithImpl<$Res,
        _$PushNotificationLogModelImpl>
    implements _$$PushNotificationLogModelImplCopyWith<$Res> {
  __$$PushNotificationLogModelImplCopyWithImpl(
      _$PushNotificationLogModelImpl _value,
      $Res Function(_$PushNotificationLogModelImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? notificationType = null,
    Object? title = null,
    Object? body = null,
    Object? status = null,
    Object? createdAt = null,
  }) {
    return _then(_$PushNotificationLogModelImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      notificationType: null == notificationType
          ? _value.notificationType
          : notificationType // ignore: cast_nullable_to_non_nullable
              as String,
      title: null == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String,
      body: null == body
          ? _value.body
          : body // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$PushNotificationLogModelImpl implements _PushNotificationLogModel {
  const _$PushNotificationLogModelImpl(
      {required this.id,
      required this.userId,
      required this.notificationType,
      required this.title,
      required this.body,
      required this.status,
      required this.createdAt});

  factory _$PushNotificationLogModelImpl.fromJson(Map<String, dynamic> json) =>
      _$$PushNotificationLogModelImplFromJson(json);

  @override
  final int id;
  @override
  final int userId;
  @override
  final String notificationType;
  @override
  final String title;
  @override
  final String body;
  @override
  final String status;
  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'PushNotificationLogModel(id: $id, userId: $userId, notificationType: $notificationType, title: $title, body: $body, status: $status, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$PushNotificationLogModelImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.notificationType, notificationType) ||
                other.notificationType == notificationType) &&
            (identical(other.title, title) || other.title == title) &&
            (identical(other.body, body) || other.body == body) &&
            (identical(other.status, status) || other.status == status) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, id, userId, notificationType,
      title, body, status, createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$PushNotificationLogModelImplCopyWith<_$PushNotificationLogModelImpl>
      get copyWith => __$$PushNotificationLogModelImplCopyWithImpl<
          _$PushNotificationLogModelImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$PushNotificationLogModelImplToJson(
      this,
    );
  }
}

abstract class _PushNotificationLogModel implements PushNotificationLogModel {
  const factory _PushNotificationLogModel(
      {required final int id,
      required final int userId,
      required final String notificationType,
      required final String title,
      required final String body,
      required final String status,
      required final DateTime createdAt}) = _$PushNotificationLogModelImpl;

  factory _PushNotificationLogModel.fromJson(Map<String, dynamic> json) =
      _$PushNotificationLogModelImpl.fromJson;

  @override
  int get id;
  @override
  int get userId;
  @override
  String get notificationType;
  @override
  String get title;
  @override
  String get body;
  @override
  String get status;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$PushNotificationLogModelImplCopyWith<_$PushNotificationLogModelImpl>
      get copyWith => throw _privateConstructorUsedError;
}

AdminUserModel _$AdminUserModelFromJson(Map<String, dynamic> json) {
  return _AdminUserModel.fromJson(json);
}

/// @nodoc
mixin _$AdminUserModel {
  int get id => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  String get role => throw _privateConstructorUsedError;
  List<String> get permissions => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $AdminUserModelCopyWith<AdminUserModel> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $AdminUserModelCopyWith<$Res> {
  factory $AdminUserModelCopyWith(
          AdminUserModel value, $Res Function(AdminUserModel) then) =
      _$AdminUserModelCopyWithImpl<$Res, AdminUserModel>;
  @useResult
  $Res call(
      {int id,
      int userId,
      String role,
      List<String> permissions,
      DateTime createdAt});
}

/// @nodoc
class _$AdminUserModelCopyWithImpl<$Res, $Val extends AdminUserModel>
    implements $AdminUserModelCopyWith<$Res> {
  _$AdminUserModelCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? role = null,
    Object? permissions = null,
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
      role: null == role
          ? _value.role
          : role // ignore: cast_nullable_to_non_nullable
              as String,
      permissions: null == permissions
          ? _value.permissions
          : permissions // ignore: cast_nullable_to_non_nullable
              as List<String>,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$AdminUserModelImplCopyWith<$Res>
    implements $AdminUserModelCopyWith<$Res> {
  factory _$$AdminUserModelImplCopyWith(_$AdminUserModelImpl value,
          $Res Function(_$AdminUserModelImpl) then) =
      __$$AdminUserModelImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int userId,
      String role,
      List<String> permissions,
      DateTime createdAt});
}

/// @nodoc
class __$$AdminUserModelImplCopyWithImpl<$Res>
    extends _$AdminUserModelCopyWithImpl<$Res, _$AdminUserModelImpl>
    implements _$$AdminUserModelImplCopyWith<$Res> {
  __$$AdminUserModelImplCopyWithImpl(
      _$AdminUserModelImpl _value, $Res Function(_$AdminUserModelImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? role = null,
    Object? permissions = null,
    Object? createdAt = null,
  }) {
    return _then(_$AdminUserModelImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      role: null == role
          ? _value.role
          : role // ignore: cast_nullable_to_non_nullable
              as String,
      permissions: null == permissions
          ? _value._permissions
          : permissions // ignore: cast_nullable_to_non_nullable
              as List<String>,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$AdminUserModelImpl implements _AdminUserModel {
  const _$AdminUserModelImpl(
      {required this.id,
      required this.userId,
      required this.role,
      required final List<String> permissions,
      required this.createdAt})
      : _permissions = permissions;

  factory _$AdminUserModelImpl.fromJson(Map<String, dynamic> json) =>
      _$$AdminUserModelImplFromJson(json);

  @override
  final int id;
  @override
  final int userId;
  @override
  final String role;
  final List<String> _permissions;
  @override
  List<String> get permissions {
    if (_permissions is EqualUnmodifiableListView) return _permissions;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_permissions);
  }

  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'AdminUserModel(id: $id, userId: $userId, role: $role, permissions: $permissions, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$AdminUserModelImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.role, role) || other.role == role) &&
            const DeepCollectionEquality()
                .equals(other._permissions, _permissions) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, id, userId, role,
      const DeepCollectionEquality().hash(_permissions), createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$AdminUserModelImplCopyWith<_$AdminUserModelImpl> get copyWith =>
      __$$AdminUserModelImplCopyWithImpl<_$AdminUserModelImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$AdminUserModelImplToJson(
      this,
    );
  }
}

abstract class _AdminUserModel implements AdminUserModel {
  const factory _AdminUserModel(
      {required final int id,
      required final int userId,
      required final String role,
      required final List<String> permissions,
      required final DateTime createdAt}) = _$AdminUserModelImpl;

  factory _AdminUserModel.fromJson(Map<String, dynamic> json) =
      _$AdminUserModelImpl.fromJson;

  @override
  int get id;
  @override
  int get userId;
  @override
  String get role;
  @override
  List<String> get permissions;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$AdminUserModelImplCopyWith<_$AdminUserModelImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

SystemNotificationModel _$SystemNotificationModelFromJson(
    Map<String, dynamic> json) {
  return _SystemNotificationModel.fromJson(json);
}

/// @nodoc
mixin _$SystemNotificationModel {
  int get id => throw _privateConstructorUsedError;
  String get title => throw _privateConstructorUsedError;
  String get message => throw _privateConstructorUsedError;
  String get notificationType => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $SystemNotificationModelCopyWith<SystemNotificationModel> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $SystemNotificationModelCopyWith<$Res> {
  factory $SystemNotificationModelCopyWith(SystemNotificationModel value,
          $Res Function(SystemNotificationModel) then) =
      _$SystemNotificationModelCopyWithImpl<$Res, SystemNotificationModel>;
  @useResult
  $Res call(
      {int id,
      String title,
      String message,
      String notificationType,
      DateTime createdAt});
}

/// @nodoc
class _$SystemNotificationModelCopyWithImpl<$Res,
        $Val extends SystemNotificationModel>
    implements $SystemNotificationModelCopyWith<$Res> {
  _$SystemNotificationModelCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? title = null,
    Object? message = null,
    Object? notificationType = null,
    Object? createdAt = null,
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
      message: null == message
          ? _value.message
          : message // ignore: cast_nullable_to_non_nullable
              as String,
      notificationType: null == notificationType
          ? _value.notificationType
          : notificationType // ignore: cast_nullable_to_non_nullable
              as String,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$SystemNotificationModelImplCopyWith<$Res>
    implements $SystemNotificationModelCopyWith<$Res> {
  factory _$$SystemNotificationModelImplCopyWith(
          _$SystemNotificationModelImpl value,
          $Res Function(_$SystemNotificationModelImpl) then) =
      __$$SystemNotificationModelImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String title,
      String message,
      String notificationType,
      DateTime createdAt});
}

/// @nodoc
class __$$SystemNotificationModelImplCopyWithImpl<$Res>
    extends _$SystemNotificationModelCopyWithImpl<$Res,
        _$SystemNotificationModelImpl>
    implements _$$SystemNotificationModelImplCopyWith<$Res> {
  __$$SystemNotificationModelImplCopyWithImpl(
      _$SystemNotificationModelImpl _value,
      $Res Function(_$SystemNotificationModelImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? title = null,
    Object? message = null,
    Object? notificationType = null,
    Object? createdAt = null,
  }) {
    return _then(_$SystemNotificationModelImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      title: null == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String,
      message: null == message
          ? _value.message
          : message // ignore: cast_nullable_to_non_nullable
              as String,
      notificationType: null == notificationType
          ? _value.notificationType
          : notificationType // ignore: cast_nullable_to_non_nullable
              as String,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$SystemNotificationModelImpl implements _SystemNotificationModel {
  const _$SystemNotificationModelImpl(
      {required this.id,
      required this.title,
      required this.message,
      required this.notificationType,
      required this.createdAt});

  factory _$SystemNotificationModelImpl.fromJson(Map<String, dynamic> json) =>
      _$$SystemNotificationModelImplFromJson(json);

  @override
  final int id;
  @override
  final String title;
  @override
  final String message;
  @override
  final String notificationType;
  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'SystemNotificationModel(id: $id, title: $title, message: $message, notificationType: $notificationType, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$SystemNotificationModelImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.title, title) || other.title == title) &&
            (identical(other.message, message) || other.message == message) &&
            (identical(other.notificationType, notificationType) ||
                other.notificationType == notificationType) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode =>
      Object.hash(runtimeType, id, title, message, notificationType, createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$SystemNotificationModelImplCopyWith<_$SystemNotificationModelImpl>
      get copyWith => __$$SystemNotificationModelImplCopyWithImpl<
          _$SystemNotificationModelImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$SystemNotificationModelImplToJson(
      this,
    );
  }
}

abstract class _SystemNotificationModel implements SystemNotificationModel {
  const factory _SystemNotificationModel(
      {required final int id,
      required final String title,
      required final String message,
      required final String notificationType,
      required final DateTime createdAt}) = _$SystemNotificationModelImpl;

  factory _SystemNotificationModel.fromJson(Map<String, dynamic> json) =
      _$SystemNotificationModelImpl.fromJson;

  @override
  int get id;
  @override
  String get title;
  @override
  String get message;
  @override
  String get notificationType;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$SystemNotificationModelImplCopyWith<_$SystemNotificationModelImpl>
      get copyWith => throw _privateConstructorUsedError;
}

PlatformStatisticModel _$PlatformStatisticModelFromJson(
    Map<String, dynamic> json) {
  return _PlatformStatisticModel.fromJson(json);
}

/// @nodoc
mixin _$PlatformStatisticModel {
  int get id => throw _privateConstructorUsedError;
  String get metricName => throw _privateConstructorUsedError;
  double get metricValue => throw _privateConstructorUsedError;
  String get metricType => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $PlatformStatisticModelCopyWith<PlatformStatisticModel> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $PlatformStatisticModelCopyWith<$Res> {
  factory $PlatformStatisticModelCopyWith(PlatformStatisticModel value,
          $Res Function(PlatformStatisticModel) then) =
      _$PlatformStatisticModelCopyWithImpl<$Res, PlatformStatisticModel>;
  @useResult
  $Res call(
      {int id,
      String metricName,
      double metricValue,
      String metricType,
      DateTime createdAt});
}

/// @nodoc
class _$PlatformStatisticModelCopyWithImpl<$Res,
        $Val extends PlatformStatisticModel>
    implements $PlatformStatisticModelCopyWith<$Res> {
  _$PlatformStatisticModelCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? metricName = null,
    Object? metricValue = null,
    Object? metricType = null,
    Object? createdAt = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      metricName: null == metricName
          ? _value.metricName
          : metricName // ignore: cast_nullable_to_non_nullable
              as String,
      metricValue: null == metricValue
          ? _value.metricValue
          : metricValue // ignore: cast_nullable_to_non_nullable
              as double,
      metricType: null == metricType
          ? _value.metricType
          : metricType // ignore: cast_nullable_to_non_nullable
              as String,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$PlatformStatisticModelImplCopyWith<$Res>
    implements $PlatformStatisticModelCopyWith<$Res> {
  factory _$$PlatformStatisticModelImplCopyWith(
          _$PlatformStatisticModelImpl value,
          $Res Function(_$PlatformStatisticModelImpl) then) =
      __$$PlatformStatisticModelImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String metricName,
      double metricValue,
      String metricType,
      DateTime createdAt});
}

/// @nodoc
class __$$PlatformStatisticModelImplCopyWithImpl<$Res>
    extends _$PlatformStatisticModelCopyWithImpl<$Res,
        _$PlatformStatisticModelImpl>
    implements _$$PlatformStatisticModelImplCopyWith<$Res> {
  __$$PlatformStatisticModelImplCopyWithImpl(
      _$PlatformStatisticModelImpl _value,
      $Res Function(_$PlatformStatisticModelImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? metricName = null,
    Object? metricValue = null,
    Object? metricType = null,
    Object? createdAt = null,
  }) {
    return _then(_$PlatformStatisticModelImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      metricName: null == metricName
          ? _value.metricName
          : metricName // ignore: cast_nullable_to_non_nullable
              as String,
      metricValue: null == metricValue
          ? _value.metricValue
          : metricValue // ignore: cast_nullable_to_non_nullable
              as double,
      metricType: null == metricType
          ? _value.metricType
          : metricType // ignore: cast_nullable_to_non_nullable
              as String,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$PlatformStatisticModelImpl implements _PlatformStatisticModel {
  const _$PlatformStatisticModelImpl(
      {required this.id,
      required this.metricName,
      required this.metricValue,
      required this.metricType,
      required this.createdAt});

  factory _$PlatformStatisticModelImpl.fromJson(Map<String, dynamic> json) =>
      _$$PlatformStatisticModelImplFromJson(json);

  @override
  final int id;
  @override
  final String metricName;
  @override
  final double metricValue;
  @override
  final String metricType;
  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'PlatformStatisticModel(id: $id, metricName: $metricName, metricValue: $metricValue, metricType: $metricType, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$PlatformStatisticModelImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.metricName, metricName) ||
                other.metricName == metricName) &&
            (identical(other.metricValue, metricValue) ||
                other.metricValue == metricValue) &&
            (identical(other.metricType, metricType) ||
                other.metricType == metricType) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType, id, metricName, metricValue, metricType, createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$PlatformStatisticModelImplCopyWith<_$PlatformStatisticModelImpl>
      get copyWith => __$$PlatformStatisticModelImplCopyWithImpl<
          _$PlatformStatisticModelImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$PlatformStatisticModelImplToJson(
      this,
    );
  }
}

abstract class _PlatformStatisticModel implements PlatformStatisticModel {
  const factory _PlatformStatisticModel(
      {required final int id,
      required final String metricName,
      required final double metricValue,
      required final String metricType,
      required final DateTime createdAt}) = _$PlatformStatisticModelImpl;

  factory _PlatformStatisticModel.fromJson(Map<String, dynamic> json) =
      _$PlatformStatisticModelImpl.fromJson;

  @override
  int get id;
  @override
  String get metricName;
  @override
  double get metricValue;
  @override
  String get metricType;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$PlatformStatisticModelImplCopyWith<_$PlatformStatisticModelImpl>
      get copyWith => throw _privateConstructorUsedError;
}

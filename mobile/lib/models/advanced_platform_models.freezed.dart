// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'advanced_platform_models.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
    'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models');

WebSocketConnection _$WebSocketConnectionFromJson(Map<String, dynamic> json) {
  return _WebSocketConnection.fromJson(json);
}

/// @nodoc
mixin _$WebSocketConnection {
  int get id => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  String get connectionId => throw _privateConstructorUsedError;
  String get status => throw _privateConstructorUsedError;
  List<String> get eventSubscriptions => throw _privateConstructorUsedError;
  String? get ipAddress => throw _privateConstructorUsedError;
  DateTime get connectedAt => throw _privateConstructorUsedError;
  DateTime? get disconnectedAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $WebSocketConnectionCopyWith<WebSocketConnection> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $WebSocketConnectionCopyWith<$Res> {
  factory $WebSocketConnectionCopyWith(
          WebSocketConnection value, $Res Function(WebSocketConnection) then) =
      _$WebSocketConnectionCopyWithImpl<$Res, WebSocketConnection>;
  @useResult
  $Res call(
      {int id,
      int userId,
      String connectionId,
      String status,
      List<String> eventSubscriptions,
      String? ipAddress,
      DateTime connectedAt,
      DateTime? disconnectedAt});
}

/// @nodoc
class _$WebSocketConnectionCopyWithImpl<$Res, $Val extends WebSocketConnection>
    implements $WebSocketConnectionCopyWith<$Res> {
  _$WebSocketConnectionCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? connectionId = null,
    Object? status = null,
    Object? eventSubscriptions = null,
    Object? ipAddress = freezed,
    Object? connectedAt = null,
    Object? disconnectedAt = freezed,
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
      connectionId: null == connectionId
          ? _value.connectionId
          : connectionId // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      eventSubscriptions: null == eventSubscriptions
          ? _value.eventSubscriptions
          : eventSubscriptions // ignore: cast_nullable_to_non_nullable
              as List<String>,
      ipAddress: freezed == ipAddress
          ? _value.ipAddress
          : ipAddress // ignore: cast_nullable_to_non_nullable
              as String?,
      connectedAt: null == connectedAt
          ? _value.connectedAt
          : connectedAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
      disconnectedAt: freezed == disconnectedAt
          ? _value.disconnectedAt
          : disconnectedAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$WebSocketConnectionImplCopyWith<$Res>
    implements $WebSocketConnectionCopyWith<$Res> {
  factory _$$WebSocketConnectionImplCopyWith(_$WebSocketConnectionImpl value,
          $Res Function(_$WebSocketConnectionImpl) then) =
      __$$WebSocketConnectionImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int userId,
      String connectionId,
      String status,
      List<String> eventSubscriptions,
      String? ipAddress,
      DateTime connectedAt,
      DateTime? disconnectedAt});
}

/// @nodoc
class __$$WebSocketConnectionImplCopyWithImpl<$Res>
    extends _$WebSocketConnectionCopyWithImpl<$Res, _$WebSocketConnectionImpl>
    implements _$$WebSocketConnectionImplCopyWith<$Res> {
  __$$WebSocketConnectionImplCopyWithImpl(_$WebSocketConnectionImpl _value,
      $Res Function(_$WebSocketConnectionImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? connectionId = null,
    Object? status = null,
    Object? eventSubscriptions = null,
    Object? ipAddress = freezed,
    Object? connectedAt = null,
    Object? disconnectedAt = freezed,
  }) {
    return _then(_$WebSocketConnectionImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      connectionId: null == connectionId
          ? _value.connectionId
          : connectionId // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      eventSubscriptions: null == eventSubscriptions
          ? _value._eventSubscriptions
          : eventSubscriptions // ignore: cast_nullable_to_non_nullable
              as List<String>,
      ipAddress: freezed == ipAddress
          ? _value.ipAddress
          : ipAddress // ignore: cast_nullable_to_non_nullable
              as String?,
      connectedAt: null == connectedAt
          ? _value.connectedAt
          : connectedAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
      disconnectedAt: freezed == disconnectedAt
          ? _value.disconnectedAt
          : disconnectedAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$WebSocketConnectionImpl implements _WebSocketConnection {
  const _$WebSocketConnectionImpl(
      {required this.id,
      required this.userId,
      required this.connectionId,
      required this.status,
      required final List<String> eventSubscriptions,
      this.ipAddress,
      required this.connectedAt,
      this.disconnectedAt})
      : _eventSubscriptions = eventSubscriptions;

  factory _$WebSocketConnectionImpl.fromJson(Map<String, dynamic> json) =>
      _$$WebSocketConnectionImplFromJson(json);

  @override
  final int id;
  @override
  final int userId;
  @override
  final String connectionId;
  @override
  final String status;
  final List<String> _eventSubscriptions;
  @override
  List<String> get eventSubscriptions {
    if (_eventSubscriptions is EqualUnmodifiableListView)
      return _eventSubscriptions;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_eventSubscriptions);
  }

  @override
  final String? ipAddress;
  @override
  final DateTime connectedAt;
  @override
  final DateTime? disconnectedAt;

  @override
  String toString() {
    return 'WebSocketConnection(id: $id, userId: $userId, connectionId: $connectionId, status: $status, eventSubscriptions: $eventSubscriptions, ipAddress: $ipAddress, connectedAt: $connectedAt, disconnectedAt: $disconnectedAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$WebSocketConnectionImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.connectionId, connectionId) ||
                other.connectionId == connectionId) &&
            (identical(other.status, status) || other.status == status) &&
            const DeepCollectionEquality()
                .equals(other._eventSubscriptions, _eventSubscriptions) &&
            (identical(other.ipAddress, ipAddress) ||
                other.ipAddress == ipAddress) &&
            (identical(other.connectedAt, connectedAt) ||
                other.connectedAt == connectedAt) &&
            (identical(other.disconnectedAt, disconnectedAt) ||
                other.disconnectedAt == disconnectedAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      userId,
      connectionId,
      status,
      const DeepCollectionEquality().hash(_eventSubscriptions),
      ipAddress,
      connectedAt,
      disconnectedAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$WebSocketConnectionImplCopyWith<_$WebSocketConnectionImpl> get copyWith =>
      __$$WebSocketConnectionImplCopyWithImpl<_$WebSocketConnectionImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$WebSocketConnectionImplToJson(
      this,
    );
  }
}

abstract class _WebSocketConnection implements WebSocketConnection {
  const factory _WebSocketConnection(
      {required final int id,
      required final int userId,
      required final String connectionId,
      required final String status,
      required final List<String> eventSubscriptions,
      final String? ipAddress,
      required final DateTime connectedAt,
      final DateTime? disconnectedAt}) = _$WebSocketConnectionImpl;

  factory _WebSocketConnection.fromJson(Map<String, dynamic> json) =
      _$WebSocketConnectionImpl.fromJson;

  @override
  int get id;
  @override
  int get userId;
  @override
  String get connectionId;
  @override
  String get status;
  @override
  List<String> get eventSubscriptions;
  @override
  String? get ipAddress;
  @override
  DateTime get connectedAt;
  @override
  DateTime? get disconnectedAt;
  @override
  @JsonKey(ignore: true)
  _$$WebSocketConnectionImplCopyWith<_$WebSocketConnectionImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

RealtimeEvent _$RealtimeEventFromJson(Map<String, dynamic> json) {
  return _RealtimeEvent.fromJson(json);
}

/// @nodoc
mixin _$RealtimeEvent {
  int get id => throw _privateConstructorUsedError;
  String get eventType => throw _privateConstructorUsedError;
  String get eventSource => throw _privateConstructorUsedError;
  List<int> get userIds => throw _privateConstructorUsedError;
  Map<String, dynamic> get payload => throw _privateConstructorUsedError;
  int get priority => throw _privateConstructorUsedError;
  String get status => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;
  DateTime? get publishedAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $RealtimeEventCopyWith<RealtimeEvent> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $RealtimeEventCopyWith<$Res> {
  factory $RealtimeEventCopyWith(
          RealtimeEvent value, $Res Function(RealtimeEvent) then) =
      _$RealtimeEventCopyWithImpl<$Res, RealtimeEvent>;
  @useResult
  $Res call(
      {int id,
      String eventType,
      String eventSource,
      List<int> userIds,
      Map<String, dynamic> payload,
      int priority,
      String status,
      DateTime createdAt,
      DateTime? publishedAt});
}

/// @nodoc
class _$RealtimeEventCopyWithImpl<$Res, $Val extends RealtimeEvent>
    implements $RealtimeEventCopyWith<$Res> {
  _$RealtimeEventCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? eventType = null,
    Object? eventSource = null,
    Object? userIds = null,
    Object? payload = null,
    Object? priority = null,
    Object? status = null,
    Object? createdAt = null,
    Object? publishedAt = freezed,
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
      eventSource: null == eventSource
          ? _value.eventSource
          : eventSource // ignore: cast_nullable_to_non_nullable
              as String,
      userIds: null == userIds
          ? _value.userIds
          : userIds // ignore: cast_nullable_to_non_nullable
              as List<int>,
      payload: null == payload
          ? _value.payload
          : payload // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      priority: null == priority
          ? _value.priority
          : priority // ignore: cast_nullable_to_non_nullable
              as int,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
      publishedAt: freezed == publishedAt
          ? _value.publishedAt
          : publishedAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$RealtimeEventImplCopyWith<$Res>
    implements $RealtimeEventCopyWith<$Res> {
  factory _$$RealtimeEventImplCopyWith(
          _$RealtimeEventImpl value, $Res Function(_$RealtimeEventImpl) then) =
      __$$RealtimeEventImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String eventType,
      String eventSource,
      List<int> userIds,
      Map<String, dynamic> payload,
      int priority,
      String status,
      DateTime createdAt,
      DateTime? publishedAt});
}

/// @nodoc
class __$$RealtimeEventImplCopyWithImpl<$Res>
    extends _$RealtimeEventCopyWithImpl<$Res, _$RealtimeEventImpl>
    implements _$$RealtimeEventImplCopyWith<$Res> {
  __$$RealtimeEventImplCopyWithImpl(
      _$RealtimeEventImpl _value, $Res Function(_$RealtimeEventImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? eventType = null,
    Object? eventSource = null,
    Object? userIds = null,
    Object? payload = null,
    Object? priority = null,
    Object? status = null,
    Object? createdAt = null,
    Object? publishedAt = freezed,
  }) {
    return _then(_$RealtimeEventImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      eventType: null == eventType
          ? _value.eventType
          : eventType // ignore: cast_nullable_to_non_nullable
              as String,
      eventSource: null == eventSource
          ? _value.eventSource
          : eventSource // ignore: cast_nullable_to_non_nullable
              as String,
      userIds: null == userIds
          ? _value._userIds
          : userIds // ignore: cast_nullable_to_non_nullable
              as List<int>,
      payload: null == payload
          ? _value._payload
          : payload // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      priority: null == priority
          ? _value.priority
          : priority // ignore: cast_nullable_to_non_nullable
              as int,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
      publishedAt: freezed == publishedAt
          ? _value.publishedAt
          : publishedAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$RealtimeEventImpl implements _RealtimeEvent {
  const _$RealtimeEventImpl(
      {required this.id,
      required this.eventType,
      required this.eventSource,
      required final List<int> userIds,
      required final Map<String, dynamic> payload,
      required this.priority,
      required this.status,
      required this.createdAt,
      this.publishedAt})
      : _userIds = userIds,
        _payload = payload;

  factory _$RealtimeEventImpl.fromJson(Map<String, dynamic> json) =>
      _$$RealtimeEventImplFromJson(json);

  @override
  final int id;
  @override
  final String eventType;
  @override
  final String eventSource;
  final List<int> _userIds;
  @override
  List<int> get userIds {
    if (_userIds is EqualUnmodifiableListView) return _userIds;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_userIds);
  }

  final Map<String, dynamic> _payload;
  @override
  Map<String, dynamic> get payload {
    if (_payload is EqualUnmodifiableMapView) return _payload;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(_payload);
  }

  @override
  final int priority;
  @override
  final String status;
  @override
  final DateTime createdAt;
  @override
  final DateTime? publishedAt;

  @override
  String toString() {
    return 'RealtimeEvent(id: $id, eventType: $eventType, eventSource: $eventSource, userIds: $userIds, payload: $payload, priority: $priority, status: $status, createdAt: $createdAt, publishedAt: $publishedAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$RealtimeEventImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.eventType, eventType) ||
                other.eventType == eventType) &&
            (identical(other.eventSource, eventSource) ||
                other.eventSource == eventSource) &&
            const DeepCollectionEquality().equals(other._userIds, _userIds) &&
            const DeepCollectionEquality().equals(other._payload, _payload) &&
            (identical(other.priority, priority) ||
                other.priority == priority) &&
            (identical(other.status, status) || other.status == status) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt) &&
            (identical(other.publishedAt, publishedAt) ||
                other.publishedAt == publishedAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      eventType,
      eventSource,
      const DeepCollectionEquality().hash(_userIds),
      const DeepCollectionEquality().hash(_payload),
      priority,
      status,
      createdAt,
      publishedAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$RealtimeEventImplCopyWith<_$RealtimeEventImpl> get copyWith =>
      __$$RealtimeEventImplCopyWithImpl<_$RealtimeEventImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$RealtimeEventImplToJson(
      this,
    );
  }
}

abstract class _RealtimeEvent implements RealtimeEvent {
  const factory _RealtimeEvent(
      {required final int id,
      required final String eventType,
      required final String eventSource,
      required final List<int> userIds,
      required final Map<String, dynamic> payload,
      required final int priority,
      required final String status,
      required final DateTime createdAt,
      final DateTime? publishedAt}) = _$RealtimeEventImpl;

  factory _RealtimeEvent.fromJson(Map<String, dynamic> json) =
      _$RealtimeEventImpl.fromJson;

  @override
  int get id;
  @override
  String get eventType;
  @override
  String get eventSource;
  @override
  List<int> get userIds;
  @override
  Map<String, dynamic> get payload;
  @override
  int get priority;
  @override
  String get status;
  @override
  DateTime get createdAt;
  @override
  DateTime? get publishedAt;
  @override
  @JsonKey(ignore: true)
  _$$RealtimeEventImplCopyWith<_$RealtimeEventImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

BackgroundJob _$BackgroundJobFromJson(Map<String, dynamic> json) {
  return _BackgroundJob.fromJson(json);
}

/// @nodoc
mixin _$BackgroundJob {
  int get id => throw _privateConstructorUsedError;
  String get jobType => throw _privateConstructorUsedError;
  String get status => throw _privateConstructorUsedError;
  int? get userId => throw _privateConstructorUsedError;
  int get priority => throw _privateConstructorUsedError;
  Map<String, dynamic> get payload => throw _privateConstructorUsedError;
  Map<String, dynamic>? get result => throw _privateConstructorUsedError;
  String? get errorMessage => throw _privateConstructorUsedError;
  int get retryCount => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;
  DateTime? get startedAt => throw _privateConstructorUsedError;
  DateTime? get completedAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $BackgroundJobCopyWith<BackgroundJob> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $BackgroundJobCopyWith<$Res> {
  factory $BackgroundJobCopyWith(
          BackgroundJob value, $Res Function(BackgroundJob) then) =
      _$BackgroundJobCopyWithImpl<$Res, BackgroundJob>;
  @useResult
  $Res call(
      {int id,
      String jobType,
      String status,
      int? userId,
      int priority,
      Map<String, dynamic> payload,
      Map<String, dynamic>? result,
      String? errorMessage,
      int retryCount,
      DateTime createdAt,
      DateTime? startedAt,
      DateTime? completedAt});
}

/// @nodoc
class _$BackgroundJobCopyWithImpl<$Res, $Val extends BackgroundJob>
    implements $BackgroundJobCopyWith<$Res> {
  _$BackgroundJobCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? jobType = null,
    Object? status = null,
    Object? userId = freezed,
    Object? priority = null,
    Object? payload = null,
    Object? result = freezed,
    Object? errorMessage = freezed,
    Object? retryCount = null,
    Object? createdAt = null,
    Object? startedAt = freezed,
    Object? completedAt = freezed,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      jobType: null == jobType
          ? _value.jobType
          : jobType // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      userId: freezed == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int?,
      priority: null == priority
          ? _value.priority
          : priority // ignore: cast_nullable_to_non_nullable
              as int,
      payload: null == payload
          ? _value.payload
          : payload // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      result: freezed == result
          ? _value.result
          : result // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>?,
      errorMessage: freezed == errorMessage
          ? _value.errorMessage
          : errorMessage // ignore: cast_nullable_to_non_nullable
              as String?,
      retryCount: null == retryCount
          ? _value.retryCount
          : retryCount // ignore: cast_nullable_to_non_nullable
              as int,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
      startedAt: freezed == startedAt
          ? _value.startedAt
          : startedAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      completedAt: freezed == completedAt
          ? _value.completedAt
          : completedAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$BackgroundJobImplCopyWith<$Res>
    implements $BackgroundJobCopyWith<$Res> {
  factory _$$BackgroundJobImplCopyWith(
          _$BackgroundJobImpl value, $Res Function(_$BackgroundJobImpl) then) =
      __$$BackgroundJobImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String jobType,
      String status,
      int? userId,
      int priority,
      Map<String, dynamic> payload,
      Map<String, dynamic>? result,
      String? errorMessage,
      int retryCount,
      DateTime createdAt,
      DateTime? startedAt,
      DateTime? completedAt});
}

/// @nodoc
class __$$BackgroundJobImplCopyWithImpl<$Res>
    extends _$BackgroundJobCopyWithImpl<$Res, _$BackgroundJobImpl>
    implements _$$BackgroundJobImplCopyWith<$Res> {
  __$$BackgroundJobImplCopyWithImpl(
      _$BackgroundJobImpl _value, $Res Function(_$BackgroundJobImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? jobType = null,
    Object? status = null,
    Object? userId = freezed,
    Object? priority = null,
    Object? payload = null,
    Object? result = freezed,
    Object? errorMessage = freezed,
    Object? retryCount = null,
    Object? createdAt = null,
    Object? startedAt = freezed,
    Object? completedAt = freezed,
  }) {
    return _then(_$BackgroundJobImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      jobType: null == jobType
          ? _value.jobType
          : jobType // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      userId: freezed == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int?,
      priority: null == priority
          ? _value.priority
          : priority // ignore: cast_nullable_to_non_nullable
              as int,
      payload: null == payload
          ? _value._payload
          : payload // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      result: freezed == result
          ? _value._result
          : result // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>?,
      errorMessage: freezed == errorMessage
          ? _value.errorMessage
          : errorMessage // ignore: cast_nullable_to_non_nullable
              as String?,
      retryCount: null == retryCount
          ? _value.retryCount
          : retryCount // ignore: cast_nullable_to_non_nullable
              as int,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
      startedAt: freezed == startedAt
          ? _value.startedAt
          : startedAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      completedAt: freezed == completedAt
          ? _value.completedAt
          : completedAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$BackgroundJobImpl implements _BackgroundJob {
  const _$BackgroundJobImpl(
      {required this.id,
      required this.jobType,
      required this.status,
      this.userId,
      required this.priority,
      required final Map<String, dynamic> payload,
      final Map<String, dynamic>? result,
      this.errorMessage,
      required this.retryCount,
      required this.createdAt,
      this.startedAt,
      this.completedAt})
      : _payload = payload,
        _result = result;

  factory _$BackgroundJobImpl.fromJson(Map<String, dynamic> json) =>
      _$$BackgroundJobImplFromJson(json);

  @override
  final int id;
  @override
  final String jobType;
  @override
  final String status;
  @override
  final int? userId;
  @override
  final int priority;
  final Map<String, dynamic> _payload;
  @override
  Map<String, dynamic> get payload {
    if (_payload is EqualUnmodifiableMapView) return _payload;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(_payload);
  }

  final Map<String, dynamic>? _result;
  @override
  Map<String, dynamic>? get result {
    final value = _result;
    if (value == null) return null;
    if (_result is EqualUnmodifiableMapView) return _result;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(value);
  }

  @override
  final String? errorMessage;
  @override
  final int retryCount;
  @override
  final DateTime createdAt;
  @override
  final DateTime? startedAt;
  @override
  final DateTime? completedAt;

  @override
  String toString() {
    return 'BackgroundJob(id: $id, jobType: $jobType, status: $status, userId: $userId, priority: $priority, payload: $payload, result: $result, errorMessage: $errorMessage, retryCount: $retryCount, createdAt: $createdAt, startedAt: $startedAt, completedAt: $completedAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$BackgroundJobImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.jobType, jobType) || other.jobType == jobType) &&
            (identical(other.status, status) || other.status == status) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.priority, priority) ||
                other.priority == priority) &&
            const DeepCollectionEquality().equals(other._payload, _payload) &&
            const DeepCollectionEquality().equals(other._result, _result) &&
            (identical(other.errorMessage, errorMessage) ||
                other.errorMessage == errorMessage) &&
            (identical(other.retryCount, retryCount) ||
                other.retryCount == retryCount) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt) &&
            (identical(other.startedAt, startedAt) ||
                other.startedAt == startedAt) &&
            (identical(other.completedAt, completedAt) ||
                other.completedAt == completedAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      jobType,
      status,
      userId,
      priority,
      const DeepCollectionEquality().hash(_payload),
      const DeepCollectionEquality().hash(_result),
      errorMessage,
      retryCount,
      createdAt,
      startedAt,
      completedAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$BackgroundJobImplCopyWith<_$BackgroundJobImpl> get copyWith =>
      __$$BackgroundJobImplCopyWithImpl<_$BackgroundJobImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$BackgroundJobImplToJson(
      this,
    );
  }
}

abstract class _BackgroundJob implements BackgroundJob {
  const factory _BackgroundJob(
      {required final int id,
      required final String jobType,
      required final String status,
      final int? userId,
      required final int priority,
      required final Map<String, dynamic> payload,
      final Map<String, dynamic>? result,
      final String? errorMessage,
      required final int retryCount,
      required final DateTime createdAt,
      final DateTime? startedAt,
      final DateTime? completedAt}) = _$BackgroundJobImpl;

  factory _BackgroundJob.fromJson(Map<String, dynamic> json) =
      _$BackgroundJobImpl.fromJson;

  @override
  int get id;
  @override
  String get jobType;
  @override
  String get status;
  @override
  int? get userId;
  @override
  int get priority;
  @override
  Map<String, dynamic> get payload;
  @override
  Map<String, dynamic>? get result;
  @override
  String? get errorMessage;
  @override
  int get retryCount;
  @override
  DateTime get createdAt;
  @override
  DateTime? get startedAt;
  @override
  DateTime? get completedAt;
  @override
  @JsonKey(ignore: true)
  _$$BackgroundJobImplCopyWith<_$BackgroundJobImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

JobSchedule _$JobScheduleFromJson(Map<String, dynamic> json) {
  return _JobSchedule.fromJson(json);
}

/// @nodoc
mixin _$JobSchedule {
  int get id => throw _privateConstructorUsedError;
  String get jobType => throw _privateConstructorUsedError;
  String get cronExpression => throw _privateConstructorUsedError;
  bool get enabled => throw _privateConstructorUsedError;
  String? get description => throw _privateConstructorUsedError;
  DateTime? get lastRun => throw _privateConstructorUsedError;
  DateTime? get nextRun => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $JobScheduleCopyWith<JobSchedule> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $JobScheduleCopyWith<$Res> {
  factory $JobScheduleCopyWith(
          JobSchedule value, $Res Function(JobSchedule) then) =
      _$JobScheduleCopyWithImpl<$Res, JobSchedule>;
  @useResult
  $Res call(
      {int id,
      String jobType,
      String cronExpression,
      bool enabled,
      String? description,
      DateTime? lastRun,
      DateTime? nextRun,
      DateTime createdAt});
}

/// @nodoc
class _$JobScheduleCopyWithImpl<$Res, $Val extends JobSchedule>
    implements $JobScheduleCopyWith<$Res> {
  _$JobScheduleCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? jobType = null,
    Object? cronExpression = null,
    Object? enabled = null,
    Object? description = freezed,
    Object? lastRun = freezed,
    Object? nextRun = freezed,
    Object? createdAt = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      jobType: null == jobType
          ? _value.jobType
          : jobType // ignore: cast_nullable_to_non_nullable
              as String,
      cronExpression: null == cronExpression
          ? _value.cronExpression
          : cronExpression // ignore: cast_nullable_to_non_nullable
              as String,
      enabled: null == enabled
          ? _value.enabled
          : enabled // ignore: cast_nullable_to_non_nullable
              as bool,
      description: freezed == description
          ? _value.description
          : description // ignore: cast_nullable_to_non_nullable
              as String?,
      lastRun: freezed == lastRun
          ? _value.lastRun
          : lastRun // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      nextRun: freezed == nextRun
          ? _value.nextRun
          : nextRun // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$JobScheduleImplCopyWith<$Res>
    implements $JobScheduleCopyWith<$Res> {
  factory _$$JobScheduleImplCopyWith(
          _$JobScheduleImpl value, $Res Function(_$JobScheduleImpl) then) =
      __$$JobScheduleImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String jobType,
      String cronExpression,
      bool enabled,
      String? description,
      DateTime? lastRun,
      DateTime? nextRun,
      DateTime createdAt});
}

/// @nodoc
class __$$JobScheduleImplCopyWithImpl<$Res>
    extends _$JobScheduleCopyWithImpl<$Res, _$JobScheduleImpl>
    implements _$$JobScheduleImplCopyWith<$Res> {
  __$$JobScheduleImplCopyWithImpl(
      _$JobScheduleImpl _value, $Res Function(_$JobScheduleImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? jobType = null,
    Object? cronExpression = null,
    Object? enabled = null,
    Object? description = freezed,
    Object? lastRun = freezed,
    Object? nextRun = freezed,
    Object? createdAt = null,
  }) {
    return _then(_$JobScheduleImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      jobType: null == jobType
          ? _value.jobType
          : jobType // ignore: cast_nullable_to_non_nullable
              as String,
      cronExpression: null == cronExpression
          ? _value.cronExpression
          : cronExpression // ignore: cast_nullable_to_non_nullable
              as String,
      enabled: null == enabled
          ? _value.enabled
          : enabled // ignore: cast_nullable_to_non_nullable
              as bool,
      description: freezed == description
          ? _value.description
          : description // ignore: cast_nullable_to_non_nullable
              as String?,
      lastRun: freezed == lastRun
          ? _value.lastRun
          : lastRun // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      nextRun: freezed == nextRun
          ? _value.nextRun
          : nextRun // ignore: cast_nullable_to_non_nullable
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
class _$JobScheduleImpl implements _JobSchedule {
  const _$JobScheduleImpl(
      {required this.id,
      required this.jobType,
      required this.cronExpression,
      required this.enabled,
      this.description,
      this.lastRun,
      this.nextRun,
      required this.createdAt});

  factory _$JobScheduleImpl.fromJson(Map<String, dynamic> json) =>
      _$$JobScheduleImplFromJson(json);

  @override
  final int id;
  @override
  final String jobType;
  @override
  final String cronExpression;
  @override
  final bool enabled;
  @override
  final String? description;
  @override
  final DateTime? lastRun;
  @override
  final DateTime? nextRun;
  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'JobSchedule(id: $id, jobType: $jobType, cronExpression: $cronExpression, enabled: $enabled, description: $description, lastRun: $lastRun, nextRun: $nextRun, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$JobScheduleImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.jobType, jobType) || other.jobType == jobType) &&
            (identical(other.cronExpression, cronExpression) ||
                other.cronExpression == cronExpression) &&
            (identical(other.enabled, enabled) || other.enabled == enabled) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.lastRun, lastRun) || other.lastRun == lastRun) &&
            (identical(other.nextRun, nextRun) || other.nextRun == nextRun) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, id, jobType, cronExpression,
      enabled, description, lastRun, nextRun, createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$JobScheduleImplCopyWith<_$JobScheduleImpl> get copyWith =>
      __$$JobScheduleImplCopyWithImpl<_$JobScheduleImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$JobScheduleImplToJson(
      this,
    );
  }
}

abstract class _JobSchedule implements JobSchedule {
  const factory _JobSchedule(
      {required final int id,
      required final String jobType,
      required final String cronExpression,
      required final bool enabled,
      final String? description,
      final DateTime? lastRun,
      final DateTime? nextRun,
      required final DateTime createdAt}) = _$JobScheduleImpl;

  factory _JobSchedule.fromJson(Map<String, dynamic> json) =
      _$JobScheduleImpl.fromJson;

  @override
  int get id;
  @override
  String get jobType;
  @override
  String get cronExpression;
  @override
  bool get enabled;
  @override
  String? get description;
  @override
  DateTime? get lastRun;
  @override
  DateTime? get nextRun;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$JobScheduleImplCopyWith<_$JobScheduleImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

DataPipeline _$DataPipelineFromJson(Map<String, dynamic> json) {
  return _DataPipeline.fromJson(json);
}

/// @nodoc
mixin _$DataPipeline {
  int get id => throw _privateConstructorUsedError;
  String get name => throw _privateConstructorUsedError;
  String get sourceType => throw _privateConstructorUsedError;
  String get destinationType => throw _privateConstructorUsedError;
  String get status => throw _privateConstructorUsedError;
  bool get isActive => throw _privateConstructorUsedError;
  String? get description => throw _privateConstructorUsedError;
  String? get schedule => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;
  DateTime? get lastRun => throw _privateConstructorUsedError;
  DateTime? get lastSuccess => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $DataPipelineCopyWith<DataPipeline> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $DataPipelineCopyWith<$Res> {
  factory $DataPipelineCopyWith(
          DataPipeline value, $Res Function(DataPipeline) then) =
      _$DataPipelineCopyWithImpl<$Res, DataPipeline>;
  @useResult
  $Res call(
      {int id,
      String name,
      String sourceType,
      String destinationType,
      String status,
      bool isActive,
      String? description,
      String? schedule,
      DateTime createdAt,
      DateTime? lastRun,
      DateTime? lastSuccess});
}

/// @nodoc
class _$DataPipelineCopyWithImpl<$Res, $Val extends DataPipeline>
    implements $DataPipelineCopyWith<$Res> {
  _$DataPipelineCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? sourceType = null,
    Object? destinationType = null,
    Object? status = null,
    Object? isActive = null,
    Object? description = freezed,
    Object? schedule = freezed,
    Object? createdAt = null,
    Object? lastRun = freezed,
    Object? lastSuccess = freezed,
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
      sourceType: null == sourceType
          ? _value.sourceType
          : sourceType // ignore: cast_nullable_to_non_nullable
              as String,
      destinationType: null == destinationType
          ? _value.destinationType
          : destinationType // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      isActive: null == isActive
          ? _value.isActive
          : isActive // ignore: cast_nullable_to_non_nullable
              as bool,
      description: freezed == description
          ? _value.description
          : description // ignore: cast_nullable_to_non_nullable
              as String?,
      schedule: freezed == schedule
          ? _value.schedule
          : schedule // ignore: cast_nullable_to_non_nullable
              as String?,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
      lastRun: freezed == lastRun
          ? _value.lastRun
          : lastRun // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      lastSuccess: freezed == lastSuccess
          ? _value.lastSuccess
          : lastSuccess // ignore: cast_nullable_to_non_nullable
              as DateTime?,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$DataPipelineImplCopyWith<$Res>
    implements $DataPipelineCopyWith<$Res> {
  factory _$$DataPipelineImplCopyWith(
          _$DataPipelineImpl value, $Res Function(_$DataPipelineImpl) then) =
      __$$DataPipelineImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String name,
      String sourceType,
      String destinationType,
      String status,
      bool isActive,
      String? description,
      String? schedule,
      DateTime createdAt,
      DateTime? lastRun,
      DateTime? lastSuccess});
}

/// @nodoc
class __$$DataPipelineImplCopyWithImpl<$Res>
    extends _$DataPipelineCopyWithImpl<$Res, _$DataPipelineImpl>
    implements _$$DataPipelineImplCopyWith<$Res> {
  __$$DataPipelineImplCopyWithImpl(
      _$DataPipelineImpl _value, $Res Function(_$DataPipelineImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? sourceType = null,
    Object? destinationType = null,
    Object? status = null,
    Object? isActive = null,
    Object? description = freezed,
    Object? schedule = freezed,
    Object? createdAt = null,
    Object? lastRun = freezed,
    Object? lastSuccess = freezed,
  }) {
    return _then(_$DataPipelineImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      name: null == name
          ? _value.name
          : name // ignore: cast_nullable_to_non_nullable
              as String,
      sourceType: null == sourceType
          ? _value.sourceType
          : sourceType // ignore: cast_nullable_to_non_nullable
              as String,
      destinationType: null == destinationType
          ? _value.destinationType
          : destinationType // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      isActive: null == isActive
          ? _value.isActive
          : isActive // ignore: cast_nullable_to_non_nullable
              as bool,
      description: freezed == description
          ? _value.description
          : description // ignore: cast_nullable_to_non_nullable
              as String?,
      schedule: freezed == schedule
          ? _value.schedule
          : schedule // ignore: cast_nullable_to_non_nullable
              as String?,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
      lastRun: freezed == lastRun
          ? _value.lastRun
          : lastRun // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      lastSuccess: freezed == lastSuccess
          ? _value.lastSuccess
          : lastSuccess // ignore: cast_nullable_to_non_nullable
              as DateTime?,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$DataPipelineImpl implements _DataPipeline {
  const _$DataPipelineImpl(
      {required this.id,
      required this.name,
      required this.sourceType,
      required this.destinationType,
      required this.status,
      required this.isActive,
      this.description,
      this.schedule,
      required this.createdAt,
      this.lastRun,
      this.lastSuccess});

  factory _$DataPipelineImpl.fromJson(Map<String, dynamic> json) =>
      _$$DataPipelineImplFromJson(json);

  @override
  final int id;
  @override
  final String name;
  @override
  final String sourceType;
  @override
  final String destinationType;
  @override
  final String status;
  @override
  final bool isActive;
  @override
  final String? description;
  @override
  final String? schedule;
  @override
  final DateTime createdAt;
  @override
  final DateTime? lastRun;
  @override
  final DateTime? lastSuccess;

  @override
  String toString() {
    return 'DataPipeline(id: $id, name: $name, sourceType: $sourceType, destinationType: $destinationType, status: $status, isActive: $isActive, description: $description, schedule: $schedule, createdAt: $createdAt, lastRun: $lastRun, lastSuccess: $lastSuccess)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$DataPipelineImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.sourceType, sourceType) ||
                other.sourceType == sourceType) &&
            (identical(other.destinationType, destinationType) ||
                other.destinationType == destinationType) &&
            (identical(other.status, status) || other.status == status) &&
            (identical(other.isActive, isActive) ||
                other.isActive == isActive) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.schedule, schedule) ||
                other.schedule == schedule) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt) &&
            (identical(other.lastRun, lastRun) || other.lastRun == lastRun) &&
            (identical(other.lastSuccess, lastSuccess) ||
                other.lastSuccess == lastSuccess));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      name,
      sourceType,
      destinationType,
      status,
      isActive,
      description,
      schedule,
      createdAt,
      lastRun,
      lastSuccess);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$DataPipelineImplCopyWith<_$DataPipelineImpl> get copyWith =>
      __$$DataPipelineImplCopyWithImpl<_$DataPipelineImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$DataPipelineImplToJson(
      this,
    );
  }
}

abstract class _DataPipeline implements DataPipeline {
  const factory _DataPipeline(
      {required final int id,
      required final String name,
      required final String sourceType,
      required final String destinationType,
      required final String status,
      required final bool isActive,
      final String? description,
      final String? schedule,
      required final DateTime createdAt,
      final DateTime? lastRun,
      final DateTime? lastSuccess}) = _$DataPipelineImpl;

  factory _DataPipeline.fromJson(Map<String, dynamic> json) =
      _$DataPipelineImpl.fromJson;

  @override
  int get id;
  @override
  String get name;
  @override
  String get sourceType;
  @override
  String get destinationType;
  @override
  String get status;
  @override
  bool get isActive;
  @override
  String? get description;
  @override
  String? get schedule;
  @override
  DateTime get createdAt;
  @override
  DateTime? get lastRun;
  @override
  DateTime? get lastSuccess;
  @override
  @JsonKey(ignore: true)
  _$$DataPipelineImplCopyWith<_$DataPipelineImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

PipelineExecution _$PipelineExecutionFromJson(Map<String, dynamic> json) {
  return _PipelineExecution.fromJson(json);
}

/// @nodoc
mixin _$PipelineExecution {
  int get id => throw _privateConstructorUsedError;
  int get pipelineId => throw _privateConstructorUsedError;
  String get status => throw _privateConstructorUsedError;
  int get recordsProcessed => throw _privateConstructorUsedError;
  int get recordsFailed => throw _privateConstructorUsedError;
  int? get executionTimeMs => throw _privateConstructorUsedError;
  DateTime get startedAt => throw _privateConstructorUsedError;
  DateTime? get completedAt => throw _privateConstructorUsedError;
  String? get errorMessage => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $PipelineExecutionCopyWith<PipelineExecution> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $PipelineExecutionCopyWith<$Res> {
  factory $PipelineExecutionCopyWith(
          PipelineExecution value, $Res Function(PipelineExecution) then) =
      _$PipelineExecutionCopyWithImpl<$Res, PipelineExecution>;
  @useResult
  $Res call(
      {int id,
      int pipelineId,
      String status,
      int recordsProcessed,
      int recordsFailed,
      int? executionTimeMs,
      DateTime startedAt,
      DateTime? completedAt,
      String? errorMessage});
}

/// @nodoc
class _$PipelineExecutionCopyWithImpl<$Res, $Val extends PipelineExecution>
    implements $PipelineExecutionCopyWith<$Res> {
  _$PipelineExecutionCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? pipelineId = null,
    Object? status = null,
    Object? recordsProcessed = null,
    Object? recordsFailed = null,
    Object? executionTimeMs = freezed,
    Object? startedAt = null,
    Object? completedAt = freezed,
    Object? errorMessage = freezed,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      pipelineId: null == pipelineId
          ? _value.pipelineId
          : pipelineId // ignore: cast_nullable_to_non_nullable
              as int,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      recordsProcessed: null == recordsProcessed
          ? _value.recordsProcessed
          : recordsProcessed // ignore: cast_nullable_to_non_nullable
              as int,
      recordsFailed: null == recordsFailed
          ? _value.recordsFailed
          : recordsFailed // ignore: cast_nullable_to_non_nullable
              as int,
      executionTimeMs: freezed == executionTimeMs
          ? _value.executionTimeMs
          : executionTimeMs // ignore: cast_nullable_to_non_nullable
              as int?,
      startedAt: null == startedAt
          ? _value.startedAt
          : startedAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
      completedAt: freezed == completedAt
          ? _value.completedAt
          : completedAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      errorMessage: freezed == errorMessage
          ? _value.errorMessage
          : errorMessage // ignore: cast_nullable_to_non_nullable
              as String?,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$PipelineExecutionImplCopyWith<$Res>
    implements $PipelineExecutionCopyWith<$Res> {
  factory _$$PipelineExecutionImplCopyWith(_$PipelineExecutionImpl value,
          $Res Function(_$PipelineExecutionImpl) then) =
      __$$PipelineExecutionImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int pipelineId,
      String status,
      int recordsProcessed,
      int recordsFailed,
      int? executionTimeMs,
      DateTime startedAt,
      DateTime? completedAt,
      String? errorMessage});
}

/// @nodoc
class __$$PipelineExecutionImplCopyWithImpl<$Res>
    extends _$PipelineExecutionCopyWithImpl<$Res, _$PipelineExecutionImpl>
    implements _$$PipelineExecutionImplCopyWith<$Res> {
  __$$PipelineExecutionImplCopyWithImpl(_$PipelineExecutionImpl _value,
      $Res Function(_$PipelineExecutionImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? pipelineId = null,
    Object? status = null,
    Object? recordsProcessed = null,
    Object? recordsFailed = null,
    Object? executionTimeMs = freezed,
    Object? startedAt = null,
    Object? completedAt = freezed,
    Object? errorMessage = freezed,
  }) {
    return _then(_$PipelineExecutionImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      pipelineId: null == pipelineId
          ? _value.pipelineId
          : pipelineId // ignore: cast_nullable_to_non_nullable
              as int,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      recordsProcessed: null == recordsProcessed
          ? _value.recordsProcessed
          : recordsProcessed // ignore: cast_nullable_to_non_nullable
              as int,
      recordsFailed: null == recordsFailed
          ? _value.recordsFailed
          : recordsFailed // ignore: cast_nullable_to_non_nullable
              as int,
      executionTimeMs: freezed == executionTimeMs
          ? _value.executionTimeMs
          : executionTimeMs // ignore: cast_nullable_to_non_nullable
              as int?,
      startedAt: null == startedAt
          ? _value.startedAt
          : startedAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
      completedAt: freezed == completedAt
          ? _value.completedAt
          : completedAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      errorMessage: freezed == errorMessage
          ? _value.errorMessage
          : errorMessage // ignore: cast_nullable_to_non_nullable
              as String?,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$PipelineExecutionImpl implements _PipelineExecution {
  const _$PipelineExecutionImpl(
      {required this.id,
      required this.pipelineId,
      required this.status,
      required this.recordsProcessed,
      required this.recordsFailed,
      this.executionTimeMs,
      required this.startedAt,
      this.completedAt,
      this.errorMessage});

  factory _$PipelineExecutionImpl.fromJson(Map<String, dynamic> json) =>
      _$$PipelineExecutionImplFromJson(json);

  @override
  final int id;
  @override
  final int pipelineId;
  @override
  final String status;
  @override
  final int recordsProcessed;
  @override
  final int recordsFailed;
  @override
  final int? executionTimeMs;
  @override
  final DateTime startedAt;
  @override
  final DateTime? completedAt;
  @override
  final String? errorMessage;

  @override
  String toString() {
    return 'PipelineExecution(id: $id, pipelineId: $pipelineId, status: $status, recordsProcessed: $recordsProcessed, recordsFailed: $recordsFailed, executionTimeMs: $executionTimeMs, startedAt: $startedAt, completedAt: $completedAt, errorMessage: $errorMessage)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$PipelineExecutionImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.pipelineId, pipelineId) ||
                other.pipelineId == pipelineId) &&
            (identical(other.status, status) || other.status == status) &&
            (identical(other.recordsProcessed, recordsProcessed) ||
                other.recordsProcessed == recordsProcessed) &&
            (identical(other.recordsFailed, recordsFailed) ||
                other.recordsFailed == recordsFailed) &&
            (identical(other.executionTimeMs, executionTimeMs) ||
                other.executionTimeMs == executionTimeMs) &&
            (identical(other.startedAt, startedAt) ||
                other.startedAt == startedAt) &&
            (identical(other.completedAt, completedAt) ||
                other.completedAt == completedAt) &&
            (identical(other.errorMessage, errorMessage) ||
                other.errorMessage == errorMessage));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      pipelineId,
      status,
      recordsProcessed,
      recordsFailed,
      executionTimeMs,
      startedAt,
      completedAt,
      errorMessage);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$PipelineExecutionImplCopyWith<_$PipelineExecutionImpl> get copyWith =>
      __$$PipelineExecutionImplCopyWithImpl<_$PipelineExecutionImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$PipelineExecutionImplToJson(
      this,
    );
  }
}

abstract class _PipelineExecution implements PipelineExecution {
  const factory _PipelineExecution(
      {required final int id,
      required final int pipelineId,
      required final String status,
      required final int recordsProcessed,
      required final int recordsFailed,
      final int? executionTimeMs,
      required final DateTime startedAt,
      final DateTime? completedAt,
      final String? errorMessage}) = _$PipelineExecutionImpl;

  factory _PipelineExecution.fromJson(Map<String, dynamic> json) =
      _$PipelineExecutionImpl.fromJson;

  @override
  int get id;
  @override
  int get pipelineId;
  @override
  String get status;
  @override
  int get recordsProcessed;
  @override
  int get recordsFailed;
  @override
  int? get executionTimeMs;
  @override
  DateTime get startedAt;
  @override
  DateTime? get completedAt;
  @override
  String? get errorMessage;
  @override
  @JsonKey(ignore: true)
  _$$PipelineExecutionImplCopyWith<_$PipelineExecutionImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

PipelineStage _$PipelineStageFromJson(Map<String, dynamic> json) {
  return _PipelineStage.fromJson(json);
}

/// @nodoc
mixin _$PipelineStage {
  int get id => throw _privateConstructorUsedError;
  int get pipelineId => throw _privateConstructorUsedError;
  String get stageName => throw _privateConstructorUsedError;
  int get stageOrder => throw _privateConstructorUsedError;
  String get stageType => throw _privateConstructorUsedError;
  Map<String, dynamic> get config => throw _privateConstructorUsedError;
  String get status => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $PipelineStageCopyWith<PipelineStage> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $PipelineStageCopyWith<$Res> {
  factory $PipelineStageCopyWith(
          PipelineStage value, $Res Function(PipelineStage) then) =
      _$PipelineStageCopyWithImpl<$Res, PipelineStage>;
  @useResult
  $Res call(
      {int id,
      int pipelineId,
      String stageName,
      int stageOrder,
      String stageType,
      Map<String, dynamic> config,
      String status,
      DateTime createdAt});
}

/// @nodoc
class _$PipelineStageCopyWithImpl<$Res, $Val extends PipelineStage>
    implements $PipelineStageCopyWith<$Res> {
  _$PipelineStageCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? pipelineId = null,
    Object? stageName = null,
    Object? stageOrder = null,
    Object? stageType = null,
    Object? config = null,
    Object? status = null,
    Object? createdAt = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      pipelineId: null == pipelineId
          ? _value.pipelineId
          : pipelineId // ignore: cast_nullable_to_non_nullable
              as int,
      stageName: null == stageName
          ? _value.stageName
          : stageName // ignore: cast_nullable_to_non_nullable
              as String,
      stageOrder: null == stageOrder
          ? _value.stageOrder
          : stageOrder // ignore: cast_nullable_to_non_nullable
              as int,
      stageType: null == stageType
          ? _value.stageType
          : stageType // ignore: cast_nullable_to_non_nullable
              as String,
      config: null == config
          ? _value.config
          : config // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
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
abstract class _$$PipelineStageImplCopyWith<$Res>
    implements $PipelineStageCopyWith<$Res> {
  factory _$$PipelineStageImplCopyWith(
          _$PipelineStageImpl value, $Res Function(_$PipelineStageImpl) then) =
      __$$PipelineStageImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int pipelineId,
      String stageName,
      int stageOrder,
      String stageType,
      Map<String, dynamic> config,
      String status,
      DateTime createdAt});
}

/// @nodoc
class __$$PipelineStageImplCopyWithImpl<$Res>
    extends _$PipelineStageCopyWithImpl<$Res, _$PipelineStageImpl>
    implements _$$PipelineStageImplCopyWith<$Res> {
  __$$PipelineStageImplCopyWithImpl(
      _$PipelineStageImpl _value, $Res Function(_$PipelineStageImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? pipelineId = null,
    Object? stageName = null,
    Object? stageOrder = null,
    Object? stageType = null,
    Object? config = null,
    Object? status = null,
    Object? createdAt = null,
  }) {
    return _then(_$PipelineStageImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      pipelineId: null == pipelineId
          ? _value.pipelineId
          : pipelineId // ignore: cast_nullable_to_non_nullable
              as int,
      stageName: null == stageName
          ? _value.stageName
          : stageName // ignore: cast_nullable_to_non_nullable
              as String,
      stageOrder: null == stageOrder
          ? _value.stageOrder
          : stageOrder // ignore: cast_nullable_to_non_nullable
              as int,
      stageType: null == stageType
          ? _value.stageType
          : stageType // ignore: cast_nullable_to_non_nullable
              as String,
      config: null == config
          ? _value._config
          : config // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
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
class _$PipelineStageImpl implements _PipelineStage {
  const _$PipelineStageImpl(
      {required this.id,
      required this.pipelineId,
      required this.stageName,
      required this.stageOrder,
      required this.stageType,
      required final Map<String, dynamic> config,
      required this.status,
      required this.createdAt})
      : _config = config;

  factory _$PipelineStageImpl.fromJson(Map<String, dynamic> json) =>
      _$$PipelineStageImplFromJson(json);

  @override
  final int id;
  @override
  final int pipelineId;
  @override
  final String stageName;
  @override
  final int stageOrder;
  @override
  final String stageType;
  final Map<String, dynamic> _config;
  @override
  Map<String, dynamic> get config {
    if (_config is EqualUnmodifiableMapView) return _config;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(_config);
  }

  @override
  final String status;
  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'PipelineStage(id: $id, pipelineId: $pipelineId, stageName: $stageName, stageOrder: $stageOrder, stageType: $stageType, config: $config, status: $status, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$PipelineStageImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.pipelineId, pipelineId) ||
                other.pipelineId == pipelineId) &&
            (identical(other.stageName, stageName) ||
                other.stageName == stageName) &&
            (identical(other.stageOrder, stageOrder) ||
                other.stageOrder == stageOrder) &&
            (identical(other.stageType, stageType) ||
                other.stageType == stageType) &&
            const DeepCollectionEquality().equals(other._config, _config) &&
            (identical(other.status, status) || other.status == status) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      pipelineId,
      stageName,
      stageOrder,
      stageType,
      const DeepCollectionEquality().hash(_config),
      status,
      createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$PipelineStageImplCopyWith<_$PipelineStageImpl> get copyWith =>
      __$$PipelineStageImplCopyWithImpl<_$PipelineStageImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$PipelineStageImplToJson(
      this,
    );
  }
}

abstract class _PipelineStage implements PipelineStage {
  const factory _PipelineStage(
      {required final int id,
      required final int pipelineId,
      required final String stageName,
      required final int stageOrder,
      required final String stageType,
      required final Map<String, dynamic> config,
      required final String status,
      required final DateTime createdAt}) = _$PipelineStageImpl;

  factory _PipelineStage.fromJson(Map<String, dynamic> json) =
      _$PipelineStageImpl.fromJson;

  @override
  int get id;
  @override
  int get pipelineId;
  @override
  String get stageName;
  @override
  int get stageOrder;
  @override
  String get stageType;
  @override
  Map<String, dynamic> get config;
  @override
  String get status;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$PipelineStageImplCopyWith<_$PipelineStageImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

CacheEntry _$CacheEntryFromJson(Map<String, dynamic> json) {
  return _CacheEntry.fromJson(json);
}

/// @nodoc
mixin _$CacheEntry {
  String get cacheKey => throw _privateConstructorUsedError;
  Map<String, dynamic> get cacheValue => throw _privateConstructorUsedError;
  String get strategy => throw _privateConstructorUsedError;
  int? get ttlSeconds => throw _privateConstructorUsedError;
  int get hitCount => throw _privateConstructorUsedError;
  int? get sizeBytes => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;
  DateTime? get expiresAt => throw _privateConstructorUsedError;

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
      {String cacheKey,
      Map<String, dynamic> cacheValue,
      String strategy,
      int? ttlSeconds,
      int hitCount,
      int? sizeBytes,
      DateTime createdAt,
      DateTime? expiresAt});
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
    Object? cacheKey = null,
    Object? cacheValue = null,
    Object? strategy = null,
    Object? ttlSeconds = freezed,
    Object? hitCount = null,
    Object? sizeBytes = freezed,
    Object? createdAt = null,
    Object? expiresAt = freezed,
  }) {
    return _then(_value.copyWith(
      cacheKey: null == cacheKey
          ? _value.cacheKey
          : cacheKey // ignore: cast_nullable_to_non_nullable
              as String,
      cacheValue: null == cacheValue
          ? _value.cacheValue
          : cacheValue // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      strategy: null == strategy
          ? _value.strategy
          : strategy // ignore: cast_nullable_to_non_nullable
              as String,
      ttlSeconds: freezed == ttlSeconds
          ? _value.ttlSeconds
          : ttlSeconds // ignore: cast_nullable_to_non_nullable
              as int?,
      hitCount: null == hitCount
          ? _value.hitCount
          : hitCount // ignore: cast_nullable_to_non_nullable
              as int,
      sizeBytes: freezed == sizeBytes
          ? _value.sizeBytes
          : sizeBytes // ignore: cast_nullable_to_non_nullable
              as int?,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
      expiresAt: freezed == expiresAt
          ? _value.expiresAt
          : expiresAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
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
      {String cacheKey,
      Map<String, dynamic> cacheValue,
      String strategy,
      int? ttlSeconds,
      int hitCount,
      int? sizeBytes,
      DateTime createdAt,
      DateTime? expiresAt});
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
    Object? cacheKey = null,
    Object? cacheValue = null,
    Object? strategy = null,
    Object? ttlSeconds = freezed,
    Object? hitCount = null,
    Object? sizeBytes = freezed,
    Object? createdAt = null,
    Object? expiresAt = freezed,
  }) {
    return _then(_$CacheEntryImpl(
      cacheKey: null == cacheKey
          ? _value.cacheKey
          : cacheKey // ignore: cast_nullable_to_non_nullable
              as String,
      cacheValue: null == cacheValue
          ? _value._cacheValue
          : cacheValue // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>,
      strategy: null == strategy
          ? _value.strategy
          : strategy // ignore: cast_nullable_to_non_nullable
              as String,
      ttlSeconds: freezed == ttlSeconds
          ? _value.ttlSeconds
          : ttlSeconds // ignore: cast_nullable_to_non_nullable
              as int?,
      hitCount: null == hitCount
          ? _value.hitCount
          : hitCount // ignore: cast_nullable_to_non_nullable
              as int,
      sizeBytes: freezed == sizeBytes
          ? _value.sizeBytes
          : sizeBytes // ignore: cast_nullable_to_non_nullable
              as int?,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
      expiresAt: freezed == expiresAt
          ? _value.expiresAt
          : expiresAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$CacheEntryImpl implements _CacheEntry {
  const _$CacheEntryImpl(
      {required this.cacheKey,
      required final Map<String, dynamic> cacheValue,
      required this.strategy,
      this.ttlSeconds,
      required this.hitCount,
      this.sizeBytes,
      required this.createdAt,
      this.expiresAt})
      : _cacheValue = cacheValue;

  factory _$CacheEntryImpl.fromJson(Map<String, dynamic> json) =>
      _$$CacheEntryImplFromJson(json);

  @override
  final String cacheKey;
  final Map<String, dynamic> _cacheValue;
  @override
  Map<String, dynamic> get cacheValue {
    if (_cacheValue is EqualUnmodifiableMapView) return _cacheValue;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(_cacheValue);
  }

  @override
  final String strategy;
  @override
  final int? ttlSeconds;
  @override
  final int hitCount;
  @override
  final int? sizeBytes;
  @override
  final DateTime createdAt;
  @override
  final DateTime? expiresAt;

  @override
  String toString() {
    return 'CacheEntry(cacheKey: $cacheKey, cacheValue: $cacheValue, strategy: $strategy, ttlSeconds: $ttlSeconds, hitCount: $hitCount, sizeBytes: $sizeBytes, createdAt: $createdAt, expiresAt: $expiresAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$CacheEntryImpl &&
            (identical(other.cacheKey, cacheKey) ||
                other.cacheKey == cacheKey) &&
            const DeepCollectionEquality()
                .equals(other._cacheValue, _cacheValue) &&
            (identical(other.strategy, strategy) ||
                other.strategy == strategy) &&
            (identical(other.ttlSeconds, ttlSeconds) ||
                other.ttlSeconds == ttlSeconds) &&
            (identical(other.hitCount, hitCount) ||
                other.hitCount == hitCount) &&
            (identical(other.sizeBytes, sizeBytes) ||
                other.sizeBytes == sizeBytes) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt) &&
            (identical(other.expiresAt, expiresAt) ||
                other.expiresAt == expiresAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      cacheKey,
      const DeepCollectionEquality().hash(_cacheValue),
      strategy,
      ttlSeconds,
      hitCount,
      sizeBytes,
      createdAt,
      expiresAt);

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
      {required final String cacheKey,
      required final Map<String, dynamic> cacheValue,
      required final String strategy,
      final int? ttlSeconds,
      required final int hitCount,
      final int? sizeBytes,
      required final DateTime createdAt,
      final DateTime? expiresAt}) = _$CacheEntryImpl;

  factory _CacheEntry.fromJson(Map<String, dynamic> json) =
      _$CacheEntryImpl.fromJson;

  @override
  String get cacheKey;
  @override
  Map<String, dynamic> get cacheValue;
  @override
  String get strategy;
  @override
  int? get ttlSeconds;
  @override
  int get hitCount;
  @override
  int? get sizeBytes;
  @override
  DateTime get createdAt;
  @override
  DateTime? get expiresAt;
  @override
  @JsonKey(ignore: true)
  _$$CacheEntryImplCopyWith<_$CacheEntryImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

CacheMetrics _$CacheMetricsFromJson(Map<String, dynamic> json) {
  return _CacheMetrics.fromJson(json);
}

/// @nodoc
mixin _$CacheMetrics {
  int get totalRequests => throw _privateConstructorUsedError;
  int get totalHits => throw _privateConstructorUsedError;
  int get totalMisses => throw _privateConstructorUsedError;
  double get averageResponseTimeMs => throw _privateConstructorUsedError;
  double get memoryUsageMb => throw _privateConstructorUsedError;
  int get evictionCount => throw _privateConstructorUsedError;
  DateTime get measuredAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $CacheMetricsCopyWith<CacheMetrics> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $CacheMetricsCopyWith<$Res> {
  factory $CacheMetricsCopyWith(
          CacheMetrics value, $Res Function(CacheMetrics) then) =
      _$CacheMetricsCopyWithImpl<$Res, CacheMetrics>;
  @useResult
  $Res call(
      {int totalRequests,
      int totalHits,
      int totalMisses,
      double averageResponseTimeMs,
      double memoryUsageMb,
      int evictionCount,
      DateTime measuredAt});
}

/// @nodoc
class _$CacheMetricsCopyWithImpl<$Res, $Val extends CacheMetrics>
    implements $CacheMetricsCopyWith<$Res> {
  _$CacheMetricsCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? totalRequests = null,
    Object? totalHits = null,
    Object? totalMisses = null,
    Object? averageResponseTimeMs = null,
    Object? memoryUsageMb = null,
    Object? evictionCount = null,
    Object? measuredAt = null,
  }) {
    return _then(_value.copyWith(
      totalRequests: null == totalRequests
          ? _value.totalRequests
          : totalRequests // ignore: cast_nullable_to_non_nullable
              as int,
      totalHits: null == totalHits
          ? _value.totalHits
          : totalHits // ignore: cast_nullable_to_non_nullable
              as int,
      totalMisses: null == totalMisses
          ? _value.totalMisses
          : totalMisses // ignore: cast_nullable_to_non_nullable
              as int,
      averageResponseTimeMs: null == averageResponseTimeMs
          ? _value.averageResponseTimeMs
          : averageResponseTimeMs // ignore: cast_nullable_to_non_nullable
              as double,
      memoryUsageMb: null == memoryUsageMb
          ? _value.memoryUsageMb
          : memoryUsageMb // ignore: cast_nullable_to_non_nullable
              as double,
      evictionCount: null == evictionCount
          ? _value.evictionCount
          : evictionCount // ignore: cast_nullable_to_non_nullable
              as int,
      measuredAt: null == measuredAt
          ? _value.measuredAt
          : measuredAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$CacheMetricsImplCopyWith<$Res>
    implements $CacheMetricsCopyWith<$Res> {
  factory _$$CacheMetricsImplCopyWith(
          _$CacheMetricsImpl value, $Res Function(_$CacheMetricsImpl) then) =
      __$$CacheMetricsImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int totalRequests,
      int totalHits,
      int totalMisses,
      double averageResponseTimeMs,
      double memoryUsageMb,
      int evictionCount,
      DateTime measuredAt});
}

/// @nodoc
class __$$CacheMetricsImplCopyWithImpl<$Res>
    extends _$CacheMetricsCopyWithImpl<$Res, _$CacheMetricsImpl>
    implements _$$CacheMetricsImplCopyWith<$Res> {
  __$$CacheMetricsImplCopyWithImpl(
      _$CacheMetricsImpl _value, $Res Function(_$CacheMetricsImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? totalRequests = null,
    Object? totalHits = null,
    Object? totalMisses = null,
    Object? averageResponseTimeMs = null,
    Object? memoryUsageMb = null,
    Object? evictionCount = null,
    Object? measuredAt = null,
  }) {
    return _then(_$CacheMetricsImpl(
      totalRequests: null == totalRequests
          ? _value.totalRequests
          : totalRequests // ignore: cast_nullable_to_non_nullable
              as int,
      totalHits: null == totalHits
          ? _value.totalHits
          : totalHits // ignore: cast_nullable_to_non_nullable
              as int,
      totalMisses: null == totalMisses
          ? _value.totalMisses
          : totalMisses // ignore: cast_nullable_to_non_nullable
              as int,
      averageResponseTimeMs: null == averageResponseTimeMs
          ? _value.averageResponseTimeMs
          : averageResponseTimeMs // ignore: cast_nullable_to_non_nullable
              as double,
      memoryUsageMb: null == memoryUsageMb
          ? _value.memoryUsageMb
          : memoryUsageMb // ignore: cast_nullable_to_non_nullable
              as double,
      evictionCount: null == evictionCount
          ? _value.evictionCount
          : evictionCount // ignore: cast_nullable_to_non_nullable
              as int,
      measuredAt: null == measuredAt
          ? _value.measuredAt
          : measuredAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$CacheMetricsImpl implements _CacheMetrics {
  const _$CacheMetricsImpl(
      {required this.totalRequests,
      required this.totalHits,
      required this.totalMisses,
      required this.averageResponseTimeMs,
      required this.memoryUsageMb,
      required this.evictionCount,
      required this.measuredAt});

  factory _$CacheMetricsImpl.fromJson(Map<String, dynamic> json) =>
      _$$CacheMetricsImplFromJson(json);

  @override
  final int totalRequests;
  @override
  final int totalHits;
  @override
  final int totalMisses;
  @override
  final double averageResponseTimeMs;
  @override
  final double memoryUsageMb;
  @override
  final int evictionCount;
  @override
  final DateTime measuredAt;

  @override
  String toString() {
    return 'CacheMetrics(totalRequests: $totalRequests, totalHits: $totalHits, totalMisses: $totalMisses, averageResponseTimeMs: $averageResponseTimeMs, memoryUsageMb: $memoryUsageMb, evictionCount: $evictionCount, measuredAt: $measuredAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$CacheMetricsImpl &&
            (identical(other.totalRequests, totalRequests) ||
                other.totalRequests == totalRequests) &&
            (identical(other.totalHits, totalHits) ||
                other.totalHits == totalHits) &&
            (identical(other.totalMisses, totalMisses) ||
                other.totalMisses == totalMisses) &&
            (identical(other.averageResponseTimeMs, averageResponseTimeMs) ||
                other.averageResponseTimeMs == averageResponseTimeMs) &&
            (identical(other.memoryUsageMb, memoryUsageMb) ||
                other.memoryUsageMb == memoryUsageMb) &&
            (identical(other.evictionCount, evictionCount) ||
                other.evictionCount == evictionCount) &&
            (identical(other.measuredAt, measuredAt) ||
                other.measuredAt == measuredAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      totalRequests,
      totalHits,
      totalMisses,
      averageResponseTimeMs,
      memoryUsageMb,
      evictionCount,
      measuredAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$CacheMetricsImplCopyWith<_$CacheMetricsImpl> get copyWith =>
      __$$CacheMetricsImplCopyWithImpl<_$CacheMetricsImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$CacheMetricsImplToJson(
      this,
    );
  }
}

abstract class _CacheMetrics implements CacheMetrics {
  const factory _CacheMetrics(
      {required final int totalRequests,
      required final int totalHits,
      required final int totalMisses,
      required final double averageResponseTimeMs,
      required final double memoryUsageMb,
      required final int evictionCount,
      required final DateTime measuredAt}) = _$CacheMetricsImpl;

  factory _CacheMetrics.fromJson(Map<String, dynamic> json) =
      _$CacheMetricsImpl.fromJson;

  @override
  int get totalRequests;
  @override
  int get totalHits;
  @override
  int get totalMisses;
  @override
  double get averageResponseTimeMs;
  @override
  double get memoryUsageMb;
  @override
  int get evictionCount;
  @override
  DateTime get measuredAt;
  @override
  @JsonKey(ignore: true)
  _$$CacheMetricsImplCopyWith<_$CacheMetricsImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

APIDocumentation _$APIDocumentationFromJson(Map<String, dynamic> json) {
  return _APIDocumentation.fromJson(json);
}

/// @nodoc
mixin _$APIDocumentation {
  int get id => throw _privateConstructorUsedError;
  String get name => throw _privateConstructorUsedError;
  String get format => throw _privateConstructorUsedError;
  String get version => throw _privateConstructorUsedError;
  String? get description => throw _privateConstructorUsedError;
  String? get basePath => throw _privateConstructorUsedError;
  List<String> get servers => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;
  DateTime get updatedAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $APIDocumentationCopyWith<APIDocumentation> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $APIDocumentationCopyWith<$Res> {
  factory $APIDocumentationCopyWith(
          APIDocumentation value, $Res Function(APIDocumentation) then) =
      _$APIDocumentationCopyWithImpl<$Res, APIDocumentation>;
  @useResult
  $Res call(
      {int id,
      String name,
      String format,
      String version,
      String? description,
      String? basePath,
      List<String> servers,
      DateTime createdAt,
      DateTime updatedAt});
}

/// @nodoc
class _$APIDocumentationCopyWithImpl<$Res, $Val extends APIDocumentation>
    implements $APIDocumentationCopyWith<$Res> {
  _$APIDocumentationCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? format = null,
    Object? version = null,
    Object? description = freezed,
    Object? basePath = freezed,
    Object? servers = null,
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
      format: null == format
          ? _value.format
          : format // ignore: cast_nullable_to_non_nullable
              as String,
      version: null == version
          ? _value.version
          : version // ignore: cast_nullable_to_non_nullable
              as String,
      description: freezed == description
          ? _value.description
          : description // ignore: cast_nullable_to_non_nullable
              as String?,
      basePath: freezed == basePath
          ? _value.basePath
          : basePath // ignore: cast_nullable_to_non_nullable
              as String?,
      servers: null == servers
          ? _value.servers
          : servers // ignore: cast_nullable_to_non_nullable
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
abstract class _$$APIDocumentationImplCopyWith<$Res>
    implements $APIDocumentationCopyWith<$Res> {
  factory _$$APIDocumentationImplCopyWith(_$APIDocumentationImpl value,
          $Res Function(_$APIDocumentationImpl) then) =
      __$$APIDocumentationImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String name,
      String format,
      String version,
      String? description,
      String? basePath,
      List<String> servers,
      DateTime createdAt,
      DateTime updatedAt});
}

/// @nodoc
class __$$APIDocumentationImplCopyWithImpl<$Res>
    extends _$APIDocumentationCopyWithImpl<$Res, _$APIDocumentationImpl>
    implements _$$APIDocumentationImplCopyWith<$Res> {
  __$$APIDocumentationImplCopyWithImpl(_$APIDocumentationImpl _value,
      $Res Function(_$APIDocumentationImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? format = null,
    Object? version = null,
    Object? description = freezed,
    Object? basePath = freezed,
    Object? servers = null,
    Object? createdAt = null,
    Object? updatedAt = null,
  }) {
    return _then(_$APIDocumentationImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      name: null == name
          ? _value.name
          : name // ignore: cast_nullable_to_non_nullable
              as String,
      format: null == format
          ? _value.format
          : format // ignore: cast_nullable_to_non_nullable
              as String,
      version: null == version
          ? _value.version
          : version // ignore: cast_nullable_to_non_nullable
              as String,
      description: freezed == description
          ? _value.description
          : description // ignore: cast_nullable_to_non_nullable
              as String?,
      basePath: freezed == basePath
          ? _value.basePath
          : basePath // ignore: cast_nullable_to_non_nullable
              as String?,
      servers: null == servers
          ? _value._servers
          : servers // ignore: cast_nullable_to_non_nullable
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
class _$APIDocumentationImpl implements _APIDocumentation {
  const _$APIDocumentationImpl(
      {required this.id,
      required this.name,
      required this.format,
      required this.version,
      this.description,
      this.basePath,
      required final List<String> servers,
      required this.createdAt,
      required this.updatedAt})
      : _servers = servers;

  factory _$APIDocumentationImpl.fromJson(Map<String, dynamic> json) =>
      _$$APIDocumentationImplFromJson(json);

  @override
  final int id;
  @override
  final String name;
  @override
  final String format;
  @override
  final String version;
  @override
  final String? description;
  @override
  final String? basePath;
  final List<String> _servers;
  @override
  List<String> get servers {
    if (_servers is EqualUnmodifiableListView) return _servers;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_servers);
  }

  @override
  final DateTime createdAt;
  @override
  final DateTime updatedAt;

  @override
  String toString() {
    return 'APIDocumentation(id: $id, name: $name, format: $format, version: $version, description: $description, basePath: $basePath, servers: $servers, createdAt: $createdAt, updatedAt: $updatedAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$APIDocumentationImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.format, format) || other.format == format) &&
            (identical(other.version, version) || other.version == version) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.basePath, basePath) ||
                other.basePath == basePath) &&
            const DeepCollectionEquality().equals(other._servers, _servers) &&
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
      format,
      version,
      description,
      basePath,
      const DeepCollectionEquality().hash(_servers),
      createdAt,
      updatedAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$APIDocumentationImplCopyWith<_$APIDocumentationImpl> get copyWith =>
      __$$APIDocumentationImplCopyWithImpl<_$APIDocumentationImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$APIDocumentationImplToJson(
      this,
    );
  }
}

abstract class _APIDocumentation implements APIDocumentation {
  const factory _APIDocumentation(
      {required final int id,
      required final String name,
      required final String format,
      required final String version,
      final String? description,
      final String? basePath,
      required final List<String> servers,
      required final DateTime createdAt,
      required final DateTime updatedAt}) = _$APIDocumentationImpl;

  factory _APIDocumentation.fromJson(Map<String, dynamic> json) =
      _$APIDocumentationImpl.fromJson;

  @override
  int get id;
  @override
  String get name;
  @override
  String get format;
  @override
  String get version;
  @override
  String? get description;
  @override
  String? get basePath;
  @override
  List<String> get servers;
  @override
  DateTime get createdAt;
  @override
  DateTime get updatedAt;
  @override
  @JsonKey(ignore: true)
  _$$APIDocumentationImplCopyWith<_$APIDocumentationImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

APIEndpoint _$APIEndpointFromJson(Map<String, dynamic> json) {
  return _APIEndpoint.fromJson(json);
}

/// @nodoc
mixin _$APIEndpoint {
  int get id => throw _privateConstructorUsedError;
  String get path => throw _privateConstructorUsedError;
  String get method => throw _privateConstructorUsedError;
  String? get summary => throw _privateConstructorUsedError;
  String? get description => throw _privateConstructorUsedError;
  Map<String, dynamic>? get parameters => throw _privateConstructorUsedError;
  Map<String, dynamic>? get requestSchema => throw _privateConstructorUsedError;
  Map<String, dynamic>? get responseSchema =>
      throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $APIEndpointCopyWith<APIEndpoint> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $APIEndpointCopyWith<$Res> {
  factory $APIEndpointCopyWith(
          APIEndpoint value, $Res Function(APIEndpoint) then) =
      _$APIEndpointCopyWithImpl<$Res, APIEndpoint>;
  @useResult
  $Res call(
      {int id,
      String path,
      String method,
      String? summary,
      String? description,
      Map<String, dynamic>? parameters,
      Map<String, dynamic>? requestSchema,
      Map<String, dynamic>? responseSchema,
      DateTime createdAt});
}

/// @nodoc
class _$APIEndpointCopyWithImpl<$Res, $Val extends APIEndpoint>
    implements $APIEndpointCopyWith<$Res> {
  _$APIEndpointCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? path = null,
    Object? method = null,
    Object? summary = freezed,
    Object? description = freezed,
    Object? parameters = freezed,
    Object? requestSchema = freezed,
    Object? responseSchema = freezed,
    Object? createdAt = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      path: null == path
          ? _value.path
          : path // ignore: cast_nullable_to_non_nullable
              as String,
      method: null == method
          ? _value.method
          : method // ignore: cast_nullable_to_non_nullable
              as String,
      summary: freezed == summary
          ? _value.summary
          : summary // ignore: cast_nullable_to_non_nullable
              as String?,
      description: freezed == description
          ? _value.description
          : description // ignore: cast_nullable_to_non_nullable
              as String?,
      parameters: freezed == parameters
          ? _value.parameters
          : parameters // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>?,
      requestSchema: freezed == requestSchema
          ? _value.requestSchema
          : requestSchema // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>?,
      responseSchema: freezed == responseSchema
          ? _value.responseSchema
          : responseSchema // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>?,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$APIEndpointImplCopyWith<$Res>
    implements $APIEndpointCopyWith<$Res> {
  factory _$$APIEndpointImplCopyWith(
          _$APIEndpointImpl value, $Res Function(_$APIEndpointImpl) then) =
      __$$APIEndpointImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String path,
      String method,
      String? summary,
      String? description,
      Map<String, dynamic>? parameters,
      Map<String, dynamic>? requestSchema,
      Map<String, dynamic>? responseSchema,
      DateTime createdAt});
}

/// @nodoc
class __$$APIEndpointImplCopyWithImpl<$Res>
    extends _$APIEndpointCopyWithImpl<$Res, _$APIEndpointImpl>
    implements _$$APIEndpointImplCopyWith<$Res> {
  __$$APIEndpointImplCopyWithImpl(
      _$APIEndpointImpl _value, $Res Function(_$APIEndpointImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? path = null,
    Object? method = null,
    Object? summary = freezed,
    Object? description = freezed,
    Object? parameters = freezed,
    Object? requestSchema = freezed,
    Object? responseSchema = freezed,
    Object? createdAt = null,
  }) {
    return _then(_$APIEndpointImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      path: null == path
          ? _value.path
          : path // ignore: cast_nullable_to_non_nullable
              as String,
      method: null == method
          ? _value.method
          : method // ignore: cast_nullable_to_non_nullable
              as String,
      summary: freezed == summary
          ? _value.summary
          : summary // ignore: cast_nullable_to_non_nullable
              as String?,
      description: freezed == description
          ? _value.description
          : description // ignore: cast_nullable_to_non_nullable
              as String?,
      parameters: freezed == parameters
          ? _value._parameters
          : parameters // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>?,
      requestSchema: freezed == requestSchema
          ? _value._requestSchema
          : requestSchema // ignore: cast_nullable_to_non_nullable
              as Map<String, dynamic>?,
      responseSchema: freezed == responseSchema
          ? _value._responseSchema
          : responseSchema // ignore: cast_nullable_to_non_nullable
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
class _$APIEndpointImpl implements _APIEndpoint {
  const _$APIEndpointImpl(
      {required this.id,
      required this.path,
      required this.method,
      this.summary,
      this.description,
      final Map<String, dynamic>? parameters,
      final Map<String, dynamic>? requestSchema,
      final Map<String, dynamic>? responseSchema,
      required this.createdAt})
      : _parameters = parameters,
        _requestSchema = requestSchema,
        _responseSchema = responseSchema;

  factory _$APIEndpointImpl.fromJson(Map<String, dynamic> json) =>
      _$$APIEndpointImplFromJson(json);

  @override
  final int id;
  @override
  final String path;
  @override
  final String method;
  @override
  final String? summary;
  @override
  final String? description;
  final Map<String, dynamic>? _parameters;
  @override
  Map<String, dynamic>? get parameters {
    final value = _parameters;
    if (value == null) return null;
    if (_parameters is EqualUnmodifiableMapView) return _parameters;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(value);
  }

  final Map<String, dynamic>? _requestSchema;
  @override
  Map<String, dynamic>? get requestSchema {
    final value = _requestSchema;
    if (value == null) return null;
    if (_requestSchema is EqualUnmodifiableMapView) return _requestSchema;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(value);
  }

  final Map<String, dynamic>? _responseSchema;
  @override
  Map<String, dynamic>? get responseSchema {
    final value = _responseSchema;
    if (value == null) return null;
    if (_responseSchema is EqualUnmodifiableMapView) return _responseSchema;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(value);
  }

  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'APIEndpoint(id: $id, path: $path, method: $method, summary: $summary, description: $description, parameters: $parameters, requestSchema: $requestSchema, responseSchema: $responseSchema, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$APIEndpointImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.path, path) || other.path == path) &&
            (identical(other.method, method) || other.method == method) &&
            (identical(other.summary, summary) || other.summary == summary) &&
            (identical(other.description, description) ||
                other.description == description) &&
            const DeepCollectionEquality()
                .equals(other._parameters, _parameters) &&
            const DeepCollectionEquality()
                .equals(other._requestSchema, _requestSchema) &&
            const DeepCollectionEquality()
                .equals(other._responseSchema, _responseSchema) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      path,
      method,
      summary,
      description,
      const DeepCollectionEquality().hash(_parameters),
      const DeepCollectionEquality().hash(_requestSchema),
      const DeepCollectionEquality().hash(_responseSchema),
      createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$APIEndpointImplCopyWith<_$APIEndpointImpl> get copyWith =>
      __$$APIEndpointImplCopyWithImpl<_$APIEndpointImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$APIEndpointImplToJson(
      this,
    );
  }
}

abstract class _APIEndpoint implements APIEndpoint {
  const factory _APIEndpoint(
      {required final int id,
      required final String path,
      required final String method,
      final String? summary,
      final String? description,
      final Map<String, dynamic>? parameters,
      final Map<String, dynamic>? requestSchema,
      final Map<String, dynamic>? responseSchema,
      required final DateTime createdAt}) = _$APIEndpointImpl;

  factory _APIEndpoint.fromJson(Map<String, dynamic> json) =
      _$APIEndpointImpl.fromJson;

  @override
  int get id;
  @override
  String get path;
  @override
  String get method;
  @override
  String? get summary;
  @override
  String? get description;
  @override
  Map<String, dynamic>? get parameters;
  @override
  Map<String, dynamic>? get requestSchema;
  @override
  Map<String, dynamic>? get responseSchema;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$APIEndpointImplCopyWith<_$APIEndpointImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

APIUsageMetrics _$APIUsageMetricsFromJson(Map<String, dynamic> json) {
  return _APIUsageMetrics.fromJson(json);
}

/// @nodoc
mixin _$APIUsageMetrics {
  String get endpoint => throw _privateConstructorUsedError;
  String get method => throw _privateConstructorUsedError;
  int get callCount => throw _privateConstructorUsedError;
  int get errorCount => throw _privateConstructorUsedError;
  double get averageResponseTimeMs => throw _privateConstructorUsedError;
  double get maxResponseTimeMs => throw _privateConstructorUsedError;
  double get minResponseTimeMs => throw _privateConstructorUsedError;
  DateTime get measuredAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $APIUsageMetricsCopyWith<APIUsageMetrics> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $APIUsageMetricsCopyWith<$Res> {
  factory $APIUsageMetricsCopyWith(
          APIUsageMetrics value, $Res Function(APIUsageMetrics) then) =
      _$APIUsageMetricsCopyWithImpl<$Res, APIUsageMetrics>;
  @useResult
  $Res call(
      {String endpoint,
      String method,
      int callCount,
      int errorCount,
      double averageResponseTimeMs,
      double maxResponseTimeMs,
      double minResponseTimeMs,
      DateTime measuredAt});
}

/// @nodoc
class _$APIUsageMetricsCopyWithImpl<$Res, $Val extends APIUsageMetrics>
    implements $APIUsageMetricsCopyWith<$Res> {
  _$APIUsageMetricsCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? endpoint = null,
    Object? method = null,
    Object? callCount = null,
    Object? errorCount = null,
    Object? averageResponseTimeMs = null,
    Object? maxResponseTimeMs = null,
    Object? minResponseTimeMs = null,
    Object? measuredAt = null,
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
      callCount: null == callCount
          ? _value.callCount
          : callCount // ignore: cast_nullable_to_non_nullable
              as int,
      errorCount: null == errorCount
          ? _value.errorCount
          : errorCount // ignore: cast_nullable_to_non_nullable
              as int,
      averageResponseTimeMs: null == averageResponseTimeMs
          ? _value.averageResponseTimeMs
          : averageResponseTimeMs // ignore: cast_nullable_to_non_nullable
              as double,
      maxResponseTimeMs: null == maxResponseTimeMs
          ? _value.maxResponseTimeMs
          : maxResponseTimeMs // ignore: cast_nullable_to_non_nullable
              as double,
      minResponseTimeMs: null == minResponseTimeMs
          ? _value.minResponseTimeMs
          : minResponseTimeMs // ignore: cast_nullable_to_non_nullable
              as double,
      measuredAt: null == measuredAt
          ? _value.measuredAt
          : measuredAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$APIUsageMetricsImplCopyWith<$Res>
    implements $APIUsageMetricsCopyWith<$Res> {
  factory _$$APIUsageMetricsImplCopyWith(_$APIUsageMetricsImpl value,
          $Res Function(_$APIUsageMetricsImpl) then) =
      __$$APIUsageMetricsImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {String endpoint,
      String method,
      int callCount,
      int errorCount,
      double averageResponseTimeMs,
      double maxResponseTimeMs,
      double minResponseTimeMs,
      DateTime measuredAt});
}

/// @nodoc
class __$$APIUsageMetricsImplCopyWithImpl<$Res>
    extends _$APIUsageMetricsCopyWithImpl<$Res, _$APIUsageMetricsImpl>
    implements _$$APIUsageMetricsImplCopyWith<$Res> {
  __$$APIUsageMetricsImplCopyWithImpl(
      _$APIUsageMetricsImpl _value, $Res Function(_$APIUsageMetricsImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? endpoint = null,
    Object? method = null,
    Object? callCount = null,
    Object? errorCount = null,
    Object? averageResponseTimeMs = null,
    Object? maxResponseTimeMs = null,
    Object? minResponseTimeMs = null,
    Object? measuredAt = null,
  }) {
    return _then(_$APIUsageMetricsImpl(
      endpoint: null == endpoint
          ? _value.endpoint
          : endpoint // ignore: cast_nullable_to_non_nullable
              as String,
      method: null == method
          ? _value.method
          : method // ignore: cast_nullable_to_non_nullable
              as String,
      callCount: null == callCount
          ? _value.callCount
          : callCount // ignore: cast_nullable_to_non_nullable
              as int,
      errorCount: null == errorCount
          ? _value.errorCount
          : errorCount // ignore: cast_nullable_to_non_nullable
              as int,
      averageResponseTimeMs: null == averageResponseTimeMs
          ? _value.averageResponseTimeMs
          : averageResponseTimeMs // ignore: cast_nullable_to_non_nullable
              as double,
      maxResponseTimeMs: null == maxResponseTimeMs
          ? _value.maxResponseTimeMs
          : maxResponseTimeMs // ignore: cast_nullable_to_non_nullable
              as double,
      minResponseTimeMs: null == minResponseTimeMs
          ? _value.minResponseTimeMs
          : minResponseTimeMs // ignore: cast_nullable_to_non_nullable
              as double,
      measuredAt: null == measuredAt
          ? _value.measuredAt
          : measuredAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$APIUsageMetricsImpl implements _APIUsageMetrics {
  const _$APIUsageMetricsImpl(
      {required this.endpoint,
      required this.method,
      required this.callCount,
      required this.errorCount,
      required this.averageResponseTimeMs,
      required this.maxResponseTimeMs,
      required this.minResponseTimeMs,
      required this.measuredAt});

  factory _$APIUsageMetricsImpl.fromJson(Map<String, dynamic> json) =>
      _$$APIUsageMetricsImplFromJson(json);

  @override
  final String endpoint;
  @override
  final String method;
  @override
  final int callCount;
  @override
  final int errorCount;
  @override
  final double averageResponseTimeMs;
  @override
  final double maxResponseTimeMs;
  @override
  final double minResponseTimeMs;
  @override
  final DateTime measuredAt;

  @override
  String toString() {
    return 'APIUsageMetrics(endpoint: $endpoint, method: $method, callCount: $callCount, errorCount: $errorCount, averageResponseTimeMs: $averageResponseTimeMs, maxResponseTimeMs: $maxResponseTimeMs, minResponseTimeMs: $minResponseTimeMs, measuredAt: $measuredAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$APIUsageMetricsImpl &&
            (identical(other.endpoint, endpoint) ||
                other.endpoint == endpoint) &&
            (identical(other.method, method) || other.method == method) &&
            (identical(other.callCount, callCount) ||
                other.callCount == callCount) &&
            (identical(other.errorCount, errorCount) ||
                other.errorCount == errorCount) &&
            (identical(other.averageResponseTimeMs, averageResponseTimeMs) ||
                other.averageResponseTimeMs == averageResponseTimeMs) &&
            (identical(other.maxResponseTimeMs, maxResponseTimeMs) ||
                other.maxResponseTimeMs == maxResponseTimeMs) &&
            (identical(other.minResponseTimeMs, minResponseTimeMs) ||
                other.minResponseTimeMs == minResponseTimeMs) &&
            (identical(other.measuredAt, measuredAt) ||
                other.measuredAt == measuredAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      endpoint,
      method,
      callCount,
      errorCount,
      averageResponseTimeMs,
      maxResponseTimeMs,
      minResponseTimeMs,
      measuredAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$APIUsageMetricsImplCopyWith<_$APIUsageMetricsImpl> get copyWith =>
      __$$APIUsageMetricsImplCopyWithImpl<_$APIUsageMetricsImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$APIUsageMetricsImplToJson(
      this,
    );
  }
}

abstract class _APIUsageMetrics implements APIUsageMetrics {
  const factory _APIUsageMetrics(
      {required final String endpoint,
      required final String method,
      required final int callCount,
      required final int errorCount,
      required final double averageResponseTimeMs,
      required final double maxResponseTimeMs,
      required final double minResponseTimeMs,
      required final DateTime measuredAt}) = _$APIUsageMetricsImpl;

  factory _APIUsageMetrics.fromJson(Map<String, dynamic> json) =
      _$APIUsageMetricsImpl.fromJson;

  @override
  String get endpoint;
  @override
  String get method;
  @override
  int get callCount;
  @override
  int get errorCount;
  @override
  double get averageResponseTimeMs;
  @override
  double get maxResponseTimeMs;
  @override
  double get minResponseTimeMs;
  @override
  DateTime get measuredAt;
  @override
  @JsonKey(ignore: true)
  _$$APIUsageMetricsImplCopyWith<_$APIUsageMetricsImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

PlatformMetrics _$PlatformMetricsFromJson(Map<String, dynamic> json) {
  return _PlatformMetrics.fromJson(json);
}

/// @nodoc
mixin _$PlatformMetrics {
  int get activeWebSocketConnections => throw _privateConstructorUsedError;
  int get pendingBackgroundJobs => throw _privateConstructorUsedError;
  int get runningPipelines => throw _privateConstructorUsedError;
  int get totalCacheSize => throw _privateConstructorUsedError;
  double get cacheHitRate => throw _privateConstructorUsedError;
  double get apiAverageResponseTime => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $PlatformMetricsCopyWith<PlatformMetrics> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $PlatformMetricsCopyWith<$Res> {
  factory $PlatformMetricsCopyWith(
          PlatformMetrics value, $Res Function(PlatformMetrics) then) =
      _$PlatformMetricsCopyWithImpl<$Res, PlatformMetrics>;
  @useResult
  $Res call(
      {int activeWebSocketConnections,
      int pendingBackgroundJobs,
      int runningPipelines,
      int totalCacheSize,
      double cacheHitRate,
      double apiAverageResponseTime});
}

/// @nodoc
class _$PlatformMetricsCopyWithImpl<$Res, $Val extends PlatformMetrics>
    implements $PlatformMetricsCopyWith<$Res> {
  _$PlatformMetricsCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? activeWebSocketConnections = null,
    Object? pendingBackgroundJobs = null,
    Object? runningPipelines = null,
    Object? totalCacheSize = null,
    Object? cacheHitRate = null,
    Object? apiAverageResponseTime = null,
  }) {
    return _then(_value.copyWith(
      activeWebSocketConnections: null == activeWebSocketConnections
          ? _value.activeWebSocketConnections
          : activeWebSocketConnections // ignore: cast_nullable_to_non_nullable
              as int,
      pendingBackgroundJobs: null == pendingBackgroundJobs
          ? _value.pendingBackgroundJobs
          : pendingBackgroundJobs // ignore: cast_nullable_to_non_nullable
              as int,
      runningPipelines: null == runningPipelines
          ? _value.runningPipelines
          : runningPipelines // ignore: cast_nullable_to_non_nullable
              as int,
      totalCacheSize: null == totalCacheSize
          ? _value.totalCacheSize
          : totalCacheSize // ignore: cast_nullable_to_non_nullable
              as int,
      cacheHitRate: null == cacheHitRate
          ? _value.cacheHitRate
          : cacheHitRate // ignore: cast_nullable_to_non_nullable
              as double,
      apiAverageResponseTime: null == apiAverageResponseTime
          ? _value.apiAverageResponseTime
          : apiAverageResponseTime // ignore: cast_nullable_to_non_nullable
              as double,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$PlatformMetricsImplCopyWith<$Res>
    implements $PlatformMetricsCopyWith<$Res> {
  factory _$$PlatformMetricsImplCopyWith(_$PlatformMetricsImpl value,
          $Res Function(_$PlatformMetricsImpl) then) =
      __$$PlatformMetricsImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int activeWebSocketConnections,
      int pendingBackgroundJobs,
      int runningPipelines,
      int totalCacheSize,
      double cacheHitRate,
      double apiAverageResponseTime});
}

/// @nodoc
class __$$PlatformMetricsImplCopyWithImpl<$Res>
    extends _$PlatformMetricsCopyWithImpl<$Res, _$PlatformMetricsImpl>
    implements _$$PlatformMetricsImplCopyWith<$Res> {
  __$$PlatformMetricsImplCopyWithImpl(
      _$PlatformMetricsImpl _value, $Res Function(_$PlatformMetricsImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? activeWebSocketConnections = null,
    Object? pendingBackgroundJobs = null,
    Object? runningPipelines = null,
    Object? totalCacheSize = null,
    Object? cacheHitRate = null,
    Object? apiAverageResponseTime = null,
  }) {
    return _then(_$PlatformMetricsImpl(
      activeWebSocketConnections: null == activeWebSocketConnections
          ? _value.activeWebSocketConnections
          : activeWebSocketConnections // ignore: cast_nullable_to_non_nullable
              as int,
      pendingBackgroundJobs: null == pendingBackgroundJobs
          ? _value.pendingBackgroundJobs
          : pendingBackgroundJobs // ignore: cast_nullable_to_non_nullable
              as int,
      runningPipelines: null == runningPipelines
          ? _value.runningPipelines
          : runningPipelines // ignore: cast_nullable_to_non_nullable
              as int,
      totalCacheSize: null == totalCacheSize
          ? _value.totalCacheSize
          : totalCacheSize // ignore: cast_nullable_to_non_nullable
              as int,
      cacheHitRate: null == cacheHitRate
          ? _value.cacheHitRate
          : cacheHitRate // ignore: cast_nullable_to_non_nullable
              as double,
      apiAverageResponseTime: null == apiAverageResponseTime
          ? _value.apiAverageResponseTime
          : apiAverageResponseTime // ignore: cast_nullable_to_non_nullable
              as double,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$PlatformMetricsImpl implements _PlatformMetrics {
  const _$PlatformMetricsImpl(
      {required this.activeWebSocketConnections,
      required this.pendingBackgroundJobs,
      required this.runningPipelines,
      required this.totalCacheSize,
      required this.cacheHitRate,
      required this.apiAverageResponseTime});

  factory _$PlatformMetricsImpl.fromJson(Map<String, dynamic> json) =>
      _$$PlatformMetricsImplFromJson(json);

  @override
  final int activeWebSocketConnections;
  @override
  final int pendingBackgroundJobs;
  @override
  final int runningPipelines;
  @override
  final int totalCacheSize;
  @override
  final double cacheHitRate;
  @override
  final double apiAverageResponseTime;

  @override
  String toString() {
    return 'PlatformMetrics(activeWebSocketConnections: $activeWebSocketConnections, pendingBackgroundJobs: $pendingBackgroundJobs, runningPipelines: $runningPipelines, totalCacheSize: $totalCacheSize, cacheHitRate: $cacheHitRate, apiAverageResponseTime: $apiAverageResponseTime)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$PlatformMetricsImpl &&
            (identical(other.activeWebSocketConnections,
                    activeWebSocketConnections) ||
                other.activeWebSocketConnections ==
                    activeWebSocketConnections) &&
            (identical(other.pendingBackgroundJobs, pendingBackgroundJobs) ||
                other.pendingBackgroundJobs == pendingBackgroundJobs) &&
            (identical(other.runningPipelines, runningPipelines) ||
                other.runningPipelines == runningPipelines) &&
            (identical(other.totalCacheSize, totalCacheSize) ||
                other.totalCacheSize == totalCacheSize) &&
            (identical(other.cacheHitRate, cacheHitRate) ||
                other.cacheHitRate == cacheHitRate) &&
            (identical(other.apiAverageResponseTime, apiAverageResponseTime) ||
                other.apiAverageResponseTime == apiAverageResponseTime));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      activeWebSocketConnections,
      pendingBackgroundJobs,
      runningPipelines,
      totalCacheSize,
      cacheHitRate,
      apiAverageResponseTime);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$PlatformMetricsImplCopyWith<_$PlatformMetricsImpl> get copyWith =>
      __$$PlatformMetricsImplCopyWithImpl<_$PlatformMetricsImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$PlatformMetricsImplToJson(
      this,
    );
  }
}

abstract class _PlatformMetrics implements PlatformMetrics {
  const factory _PlatformMetrics(
      {required final int activeWebSocketConnections,
      required final int pendingBackgroundJobs,
      required final int runningPipelines,
      required final int totalCacheSize,
      required final double cacheHitRate,
      required final double apiAverageResponseTime}) = _$PlatformMetricsImpl;

  factory _PlatformMetrics.fromJson(Map<String, dynamic> json) =
      _$PlatformMetricsImpl.fromJson;

  @override
  int get activeWebSocketConnections;
  @override
  int get pendingBackgroundJobs;
  @override
  int get runningPipelines;
  @override
  int get totalCacheSize;
  @override
  double get cacheHitRate;
  @override
  double get apiAverageResponseTime;
  @override
  @JsonKey(ignore: true)
  _$$PlatformMetricsImplCopyWith<_$PlatformMetricsImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

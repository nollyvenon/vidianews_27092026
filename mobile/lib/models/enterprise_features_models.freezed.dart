// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'enterprise_features_models.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
    'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models');

AuditLog _$AuditLogFromJson(Map<String, dynamic> json) {
  return _AuditLog.fromJson(json);
}

/// @nodoc
mixin _$AuditLog {
  int get id => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  String get action => throw _privateConstructorUsedError;
  String? get resourceType => throw _privateConstructorUsedError;
  int? get resourceId => throw _privateConstructorUsedError;
  String? get status => throw _privateConstructorUsedError;
  String? get ipAddress => throw _privateConstructorUsedError;
  String? get severity => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

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
      int userId,
      String action,
      String? resourceType,
      int? resourceId,
      String? status,
      String? ipAddress,
      String? severity,
      DateTime createdAt});
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
    Object? userId = null,
    Object? action = null,
    Object? resourceType = freezed,
    Object? resourceId = freezed,
    Object? status = freezed,
    Object? ipAddress = freezed,
    Object? severity = freezed,
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
      action: null == action
          ? _value.action
          : action // ignore: cast_nullable_to_non_nullable
              as String,
      resourceType: freezed == resourceType
          ? _value.resourceType
          : resourceType // ignore: cast_nullable_to_non_nullable
              as String?,
      resourceId: freezed == resourceId
          ? _value.resourceId
          : resourceId // ignore: cast_nullable_to_non_nullable
              as int?,
      status: freezed == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String?,
      ipAddress: freezed == ipAddress
          ? _value.ipAddress
          : ipAddress // ignore: cast_nullable_to_non_nullable
              as String?,
      severity: freezed == severity
          ? _value.severity
          : severity // ignore: cast_nullable_to_non_nullable
              as String?,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
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
      int userId,
      String action,
      String? resourceType,
      int? resourceId,
      String? status,
      String? ipAddress,
      String? severity,
      DateTime createdAt});
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
    Object? userId = null,
    Object? action = null,
    Object? resourceType = freezed,
    Object? resourceId = freezed,
    Object? status = freezed,
    Object? ipAddress = freezed,
    Object? severity = freezed,
    Object? createdAt = null,
  }) {
    return _then(_$AuditLogImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      action: null == action
          ? _value.action
          : action // ignore: cast_nullable_to_non_nullable
              as String,
      resourceType: freezed == resourceType
          ? _value.resourceType
          : resourceType // ignore: cast_nullable_to_non_nullable
              as String?,
      resourceId: freezed == resourceId
          ? _value.resourceId
          : resourceId // ignore: cast_nullable_to_non_nullable
              as int?,
      status: freezed == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String?,
      ipAddress: freezed == ipAddress
          ? _value.ipAddress
          : ipAddress // ignore: cast_nullable_to_non_nullable
              as String?,
      severity: freezed == severity
          ? _value.severity
          : severity // ignore: cast_nullable_to_non_nullable
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
class _$AuditLogImpl implements _AuditLog {
  const _$AuditLogImpl(
      {required this.id,
      required this.userId,
      required this.action,
      this.resourceType,
      this.resourceId,
      this.status,
      this.ipAddress,
      this.severity,
      required this.createdAt});

  factory _$AuditLogImpl.fromJson(Map<String, dynamic> json) =>
      _$$AuditLogImplFromJson(json);

  @override
  final int id;
  @override
  final int userId;
  @override
  final String action;
  @override
  final String? resourceType;
  @override
  final int? resourceId;
  @override
  final String? status;
  @override
  final String? ipAddress;
  @override
  final String? severity;
  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'AuditLog(id: $id, userId: $userId, action: $action, resourceType: $resourceType, resourceId: $resourceId, status: $status, ipAddress: $ipAddress, severity: $severity, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$AuditLogImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.action, action) || other.action == action) &&
            (identical(other.resourceType, resourceType) ||
                other.resourceType == resourceType) &&
            (identical(other.resourceId, resourceId) ||
                other.resourceId == resourceId) &&
            (identical(other.status, status) || other.status == status) &&
            (identical(other.ipAddress, ipAddress) ||
                other.ipAddress == ipAddress) &&
            (identical(other.severity, severity) ||
                other.severity == severity) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, id, userId, action, resourceType,
      resourceId, status, ipAddress, severity, createdAt);

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
      required final int userId,
      required final String action,
      final String? resourceType,
      final int? resourceId,
      final String? status,
      final String? ipAddress,
      final String? severity,
      required final DateTime createdAt}) = _$AuditLogImpl;

  factory _AuditLog.fromJson(Map<String, dynamic> json) =
      _$AuditLogImpl.fromJson;

  @override
  int get id;
  @override
  int get userId;
  @override
  String get action;
  @override
  String? get resourceType;
  @override
  int? get resourceId;
  @override
  String? get status;
  @override
  String? get ipAddress;
  @override
  String? get severity;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$AuditLogImplCopyWith<_$AuditLogImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

AccessControl _$AccessControlFromJson(Map<String, dynamic> json) {
  return _AccessControl.fromJson(json);
}

/// @nodoc
mixin _$AccessControl {
  int get id => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  String get resourceType => throw _privateConstructorUsedError;
  int get resourceId => throw _privateConstructorUsedError;
  String get accessLevel => throw _privateConstructorUsedError;
  List<String> get permissions => throw _privateConstructorUsedError;
  int? get grantedBy => throw _privateConstructorUsedError;
  DateTime get grantedAt => throw _privateConstructorUsedError;
  DateTime? get expiresAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $AccessControlCopyWith<AccessControl> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $AccessControlCopyWith<$Res> {
  factory $AccessControlCopyWith(
          AccessControl value, $Res Function(AccessControl) then) =
      _$AccessControlCopyWithImpl<$Res, AccessControl>;
  @useResult
  $Res call(
      {int id,
      int userId,
      String resourceType,
      int resourceId,
      String accessLevel,
      List<String> permissions,
      int? grantedBy,
      DateTime grantedAt,
      DateTime? expiresAt});
}

/// @nodoc
class _$AccessControlCopyWithImpl<$Res, $Val extends AccessControl>
    implements $AccessControlCopyWith<$Res> {
  _$AccessControlCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? resourceType = null,
    Object? resourceId = null,
    Object? accessLevel = null,
    Object? permissions = null,
    Object? grantedBy = freezed,
    Object? grantedAt = null,
    Object? expiresAt = freezed,
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
      resourceType: null == resourceType
          ? _value.resourceType
          : resourceType // ignore: cast_nullable_to_non_nullable
              as String,
      resourceId: null == resourceId
          ? _value.resourceId
          : resourceId // ignore: cast_nullable_to_non_nullable
              as int,
      accessLevel: null == accessLevel
          ? _value.accessLevel
          : accessLevel // ignore: cast_nullable_to_non_nullable
              as String,
      permissions: null == permissions
          ? _value.permissions
          : permissions // ignore: cast_nullable_to_non_nullable
              as List<String>,
      grantedBy: freezed == grantedBy
          ? _value.grantedBy
          : grantedBy // ignore: cast_nullable_to_non_nullable
              as int?,
      grantedAt: null == grantedAt
          ? _value.grantedAt
          : grantedAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
      expiresAt: freezed == expiresAt
          ? _value.expiresAt
          : expiresAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$AccessControlImplCopyWith<$Res>
    implements $AccessControlCopyWith<$Res> {
  factory _$$AccessControlImplCopyWith(
          _$AccessControlImpl value, $Res Function(_$AccessControlImpl) then) =
      __$$AccessControlImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int userId,
      String resourceType,
      int resourceId,
      String accessLevel,
      List<String> permissions,
      int? grantedBy,
      DateTime grantedAt,
      DateTime? expiresAt});
}

/// @nodoc
class __$$AccessControlImplCopyWithImpl<$Res>
    extends _$AccessControlCopyWithImpl<$Res, _$AccessControlImpl>
    implements _$$AccessControlImplCopyWith<$Res> {
  __$$AccessControlImplCopyWithImpl(
      _$AccessControlImpl _value, $Res Function(_$AccessControlImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? resourceType = null,
    Object? resourceId = null,
    Object? accessLevel = null,
    Object? permissions = null,
    Object? grantedBy = freezed,
    Object? grantedAt = null,
    Object? expiresAt = freezed,
  }) {
    return _then(_$AccessControlImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      resourceType: null == resourceType
          ? _value.resourceType
          : resourceType // ignore: cast_nullable_to_non_nullable
              as String,
      resourceId: null == resourceId
          ? _value.resourceId
          : resourceId // ignore: cast_nullable_to_non_nullable
              as int,
      accessLevel: null == accessLevel
          ? _value.accessLevel
          : accessLevel // ignore: cast_nullable_to_non_nullable
              as String,
      permissions: null == permissions
          ? _value._permissions
          : permissions // ignore: cast_nullable_to_non_nullable
              as List<String>,
      grantedBy: freezed == grantedBy
          ? _value.grantedBy
          : grantedBy // ignore: cast_nullable_to_non_nullable
              as int?,
      grantedAt: null == grantedAt
          ? _value.grantedAt
          : grantedAt // ignore: cast_nullable_to_non_nullable
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
class _$AccessControlImpl implements _AccessControl {
  const _$AccessControlImpl(
      {required this.id,
      required this.userId,
      required this.resourceType,
      required this.resourceId,
      required this.accessLevel,
      required final List<String> permissions,
      this.grantedBy,
      required this.grantedAt,
      this.expiresAt})
      : _permissions = permissions;

  factory _$AccessControlImpl.fromJson(Map<String, dynamic> json) =>
      _$$AccessControlImplFromJson(json);

  @override
  final int id;
  @override
  final int userId;
  @override
  final String resourceType;
  @override
  final int resourceId;
  @override
  final String accessLevel;
  final List<String> _permissions;
  @override
  List<String> get permissions {
    if (_permissions is EqualUnmodifiableListView) return _permissions;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_permissions);
  }

  @override
  final int? grantedBy;
  @override
  final DateTime grantedAt;
  @override
  final DateTime? expiresAt;

  @override
  String toString() {
    return 'AccessControl(id: $id, userId: $userId, resourceType: $resourceType, resourceId: $resourceId, accessLevel: $accessLevel, permissions: $permissions, grantedBy: $grantedBy, grantedAt: $grantedAt, expiresAt: $expiresAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$AccessControlImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.resourceType, resourceType) ||
                other.resourceType == resourceType) &&
            (identical(other.resourceId, resourceId) ||
                other.resourceId == resourceId) &&
            (identical(other.accessLevel, accessLevel) ||
                other.accessLevel == accessLevel) &&
            const DeepCollectionEquality()
                .equals(other._permissions, _permissions) &&
            (identical(other.grantedBy, grantedBy) ||
                other.grantedBy == grantedBy) &&
            (identical(other.grantedAt, grantedAt) ||
                other.grantedAt == grantedAt) &&
            (identical(other.expiresAt, expiresAt) ||
                other.expiresAt == expiresAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      userId,
      resourceType,
      resourceId,
      accessLevel,
      const DeepCollectionEquality().hash(_permissions),
      grantedBy,
      grantedAt,
      expiresAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$AccessControlImplCopyWith<_$AccessControlImpl> get copyWith =>
      __$$AccessControlImplCopyWithImpl<_$AccessControlImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$AccessControlImplToJson(
      this,
    );
  }
}

abstract class _AccessControl implements AccessControl {
  const factory _AccessControl(
      {required final int id,
      required final int userId,
      required final String resourceType,
      required final int resourceId,
      required final String accessLevel,
      required final List<String> permissions,
      final int? grantedBy,
      required final DateTime grantedAt,
      final DateTime? expiresAt}) = _$AccessControlImpl;

  factory _AccessControl.fromJson(Map<String, dynamic> json) =
      _$AccessControlImpl.fromJson;

  @override
  int get id;
  @override
  int get userId;
  @override
  String get resourceType;
  @override
  int get resourceId;
  @override
  String get accessLevel;
  @override
  List<String> get permissions;
  @override
  int? get grantedBy;
  @override
  DateTime get grantedAt;
  @override
  DateTime? get expiresAt;
  @override
  @JsonKey(ignore: true)
  _$$AccessControlImplCopyWith<_$AccessControlImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

RoleAssignment _$RoleAssignmentFromJson(Map<String, dynamic> json) {
  return _RoleAssignment.fromJson(json);
}

/// @nodoc
mixin _$RoleAssignment {
  int get id => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  String get role => throw _privateConstructorUsedError;
  List<String> get permissions => throw _privateConstructorUsedError;
  bool get canEditContent => throw _privateConstructorUsedError;
  bool get canDeleteContent => throw _privateConstructorUsedError;
  bool get canManageUsers => throw _privateConstructorUsedError;
  bool get canAccessAnalytics => throw _privateConstructorUsedError;
  bool get canAccessAdmin => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $RoleAssignmentCopyWith<RoleAssignment> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $RoleAssignmentCopyWith<$Res> {
  factory $RoleAssignmentCopyWith(
          RoleAssignment value, $Res Function(RoleAssignment) then) =
      _$RoleAssignmentCopyWithImpl<$Res, RoleAssignment>;
  @useResult
  $Res call(
      {int id,
      int userId,
      String role,
      List<String> permissions,
      bool canEditContent,
      bool canDeleteContent,
      bool canManageUsers,
      bool canAccessAnalytics,
      bool canAccessAdmin,
      DateTime createdAt});
}

/// @nodoc
class _$RoleAssignmentCopyWithImpl<$Res, $Val extends RoleAssignment>
    implements $RoleAssignmentCopyWith<$Res> {
  _$RoleAssignmentCopyWithImpl(this._value, this._then);

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
    Object? canEditContent = null,
    Object? canDeleteContent = null,
    Object? canManageUsers = null,
    Object? canAccessAnalytics = null,
    Object? canAccessAdmin = null,
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
      canEditContent: null == canEditContent
          ? _value.canEditContent
          : canEditContent // ignore: cast_nullable_to_non_nullable
              as bool,
      canDeleteContent: null == canDeleteContent
          ? _value.canDeleteContent
          : canDeleteContent // ignore: cast_nullable_to_non_nullable
              as bool,
      canManageUsers: null == canManageUsers
          ? _value.canManageUsers
          : canManageUsers // ignore: cast_nullable_to_non_nullable
              as bool,
      canAccessAnalytics: null == canAccessAnalytics
          ? _value.canAccessAnalytics
          : canAccessAnalytics // ignore: cast_nullable_to_non_nullable
              as bool,
      canAccessAdmin: null == canAccessAdmin
          ? _value.canAccessAdmin
          : canAccessAdmin // ignore: cast_nullable_to_non_nullable
              as bool,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$RoleAssignmentImplCopyWith<$Res>
    implements $RoleAssignmentCopyWith<$Res> {
  factory _$$RoleAssignmentImplCopyWith(_$RoleAssignmentImpl value,
          $Res Function(_$RoleAssignmentImpl) then) =
      __$$RoleAssignmentImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int userId,
      String role,
      List<String> permissions,
      bool canEditContent,
      bool canDeleteContent,
      bool canManageUsers,
      bool canAccessAnalytics,
      bool canAccessAdmin,
      DateTime createdAt});
}

/// @nodoc
class __$$RoleAssignmentImplCopyWithImpl<$Res>
    extends _$RoleAssignmentCopyWithImpl<$Res, _$RoleAssignmentImpl>
    implements _$$RoleAssignmentImplCopyWith<$Res> {
  __$$RoleAssignmentImplCopyWithImpl(
      _$RoleAssignmentImpl _value, $Res Function(_$RoleAssignmentImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? role = null,
    Object? permissions = null,
    Object? canEditContent = null,
    Object? canDeleteContent = null,
    Object? canManageUsers = null,
    Object? canAccessAnalytics = null,
    Object? canAccessAdmin = null,
    Object? createdAt = null,
  }) {
    return _then(_$RoleAssignmentImpl(
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
      canEditContent: null == canEditContent
          ? _value.canEditContent
          : canEditContent // ignore: cast_nullable_to_non_nullable
              as bool,
      canDeleteContent: null == canDeleteContent
          ? _value.canDeleteContent
          : canDeleteContent // ignore: cast_nullable_to_non_nullable
              as bool,
      canManageUsers: null == canManageUsers
          ? _value.canManageUsers
          : canManageUsers // ignore: cast_nullable_to_non_nullable
              as bool,
      canAccessAnalytics: null == canAccessAnalytics
          ? _value.canAccessAnalytics
          : canAccessAnalytics // ignore: cast_nullable_to_non_nullable
              as bool,
      canAccessAdmin: null == canAccessAdmin
          ? _value.canAccessAdmin
          : canAccessAdmin // ignore: cast_nullable_to_non_nullable
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
class _$RoleAssignmentImpl implements _RoleAssignment {
  const _$RoleAssignmentImpl(
      {required this.id,
      required this.userId,
      required this.role,
      required final List<String> permissions,
      required this.canEditContent,
      required this.canDeleteContent,
      required this.canManageUsers,
      required this.canAccessAnalytics,
      required this.canAccessAdmin,
      required this.createdAt})
      : _permissions = permissions;

  factory _$RoleAssignmentImpl.fromJson(Map<String, dynamic> json) =>
      _$$RoleAssignmentImplFromJson(json);

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
  final bool canEditContent;
  @override
  final bool canDeleteContent;
  @override
  final bool canManageUsers;
  @override
  final bool canAccessAnalytics;
  @override
  final bool canAccessAdmin;
  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'RoleAssignment(id: $id, userId: $userId, role: $role, permissions: $permissions, canEditContent: $canEditContent, canDeleteContent: $canDeleteContent, canManageUsers: $canManageUsers, canAccessAnalytics: $canAccessAnalytics, canAccessAdmin: $canAccessAdmin, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$RoleAssignmentImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.role, role) || other.role == role) &&
            const DeepCollectionEquality()
                .equals(other._permissions, _permissions) &&
            (identical(other.canEditContent, canEditContent) ||
                other.canEditContent == canEditContent) &&
            (identical(other.canDeleteContent, canDeleteContent) ||
                other.canDeleteContent == canDeleteContent) &&
            (identical(other.canManageUsers, canManageUsers) ||
                other.canManageUsers == canManageUsers) &&
            (identical(other.canAccessAnalytics, canAccessAnalytics) ||
                other.canAccessAnalytics == canAccessAnalytics) &&
            (identical(other.canAccessAdmin, canAccessAdmin) ||
                other.canAccessAdmin == canAccessAdmin) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      userId,
      role,
      const DeepCollectionEquality().hash(_permissions),
      canEditContent,
      canDeleteContent,
      canManageUsers,
      canAccessAnalytics,
      canAccessAdmin,
      createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$RoleAssignmentImplCopyWith<_$RoleAssignmentImpl> get copyWith =>
      __$$RoleAssignmentImplCopyWithImpl<_$RoleAssignmentImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$RoleAssignmentImplToJson(
      this,
    );
  }
}

abstract class _RoleAssignment implements RoleAssignment {
  const factory _RoleAssignment(
      {required final int id,
      required final int userId,
      required final String role,
      required final List<String> permissions,
      required final bool canEditContent,
      required final bool canDeleteContent,
      required final bool canManageUsers,
      required final bool canAccessAnalytics,
      required final bool canAccessAdmin,
      required final DateTime createdAt}) = _$RoleAssignmentImpl;

  factory _RoleAssignment.fromJson(Map<String, dynamic> json) =
      _$RoleAssignmentImpl.fromJson;

  @override
  int get id;
  @override
  int get userId;
  @override
  String get role;
  @override
  List<String> get permissions;
  @override
  bool get canEditContent;
  @override
  bool get canDeleteContent;
  @override
  bool get canManageUsers;
  @override
  bool get canAccessAnalytics;
  @override
  bool get canAccessAdmin;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$RoleAssignmentImplCopyWith<_$RoleAssignmentImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

ModerationItem _$ModerationItemFromJson(Map<String, dynamic> json) {
  return _ModerationItem.fromJson(json);
}

/// @nodoc
mixin _$ModerationItem {
  int get id => throw _privateConstructorUsedError;
  int get contentId => throw _privateConstructorUsedError;
  String get contentType => throw _privateConstructorUsedError;
  String get status => throw _privateConstructorUsedError;
  String? get reason => throw _privateConstructorUsedError;
  List<String> get flags => throw _privateConstructorUsedError;
  double get confidenceScore => throw _privateConstructorUsedError;
  int? get assignedTo => throw _privateConstructorUsedError;
  int? get reviewedBy => throw _privateConstructorUsedError;
  DateTime? get reviewedAt => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $ModerationItemCopyWith<ModerationItem> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $ModerationItemCopyWith<$Res> {
  factory $ModerationItemCopyWith(
          ModerationItem value, $Res Function(ModerationItem) then) =
      _$ModerationItemCopyWithImpl<$Res, ModerationItem>;
  @useResult
  $Res call(
      {int id,
      int contentId,
      String contentType,
      String status,
      String? reason,
      List<String> flags,
      double confidenceScore,
      int? assignedTo,
      int? reviewedBy,
      DateTime? reviewedAt,
      DateTime createdAt});
}

/// @nodoc
class _$ModerationItemCopyWithImpl<$Res, $Val extends ModerationItem>
    implements $ModerationItemCopyWith<$Res> {
  _$ModerationItemCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? contentId = null,
    Object? contentType = null,
    Object? status = null,
    Object? reason = freezed,
    Object? flags = null,
    Object? confidenceScore = null,
    Object? assignedTo = freezed,
    Object? reviewedBy = freezed,
    Object? reviewedAt = freezed,
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
      contentType: null == contentType
          ? _value.contentType
          : contentType // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      reason: freezed == reason
          ? _value.reason
          : reason // ignore: cast_nullable_to_non_nullable
              as String?,
      flags: null == flags
          ? _value.flags
          : flags // ignore: cast_nullable_to_non_nullable
              as List<String>,
      confidenceScore: null == confidenceScore
          ? _value.confidenceScore
          : confidenceScore // ignore: cast_nullable_to_non_nullable
              as double,
      assignedTo: freezed == assignedTo
          ? _value.assignedTo
          : assignedTo // ignore: cast_nullable_to_non_nullable
              as int?,
      reviewedBy: freezed == reviewedBy
          ? _value.reviewedBy
          : reviewedBy // ignore: cast_nullable_to_non_nullable
              as int?,
      reviewedAt: freezed == reviewedAt
          ? _value.reviewedAt
          : reviewedAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$ModerationItemImplCopyWith<$Res>
    implements $ModerationItemCopyWith<$Res> {
  factory _$$ModerationItemImplCopyWith(_$ModerationItemImpl value,
          $Res Function(_$ModerationItemImpl) then) =
      __$$ModerationItemImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int contentId,
      String contentType,
      String status,
      String? reason,
      List<String> flags,
      double confidenceScore,
      int? assignedTo,
      int? reviewedBy,
      DateTime? reviewedAt,
      DateTime createdAt});
}

/// @nodoc
class __$$ModerationItemImplCopyWithImpl<$Res>
    extends _$ModerationItemCopyWithImpl<$Res, _$ModerationItemImpl>
    implements _$$ModerationItemImplCopyWith<$Res> {
  __$$ModerationItemImplCopyWithImpl(
      _$ModerationItemImpl _value, $Res Function(_$ModerationItemImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? contentId = null,
    Object? contentType = null,
    Object? status = null,
    Object? reason = freezed,
    Object? flags = null,
    Object? confidenceScore = null,
    Object? assignedTo = freezed,
    Object? reviewedBy = freezed,
    Object? reviewedAt = freezed,
    Object? createdAt = null,
  }) {
    return _then(_$ModerationItemImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      contentId: null == contentId
          ? _value.contentId
          : contentId // ignore: cast_nullable_to_non_nullable
              as int,
      contentType: null == contentType
          ? _value.contentType
          : contentType // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      reason: freezed == reason
          ? _value.reason
          : reason // ignore: cast_nullable_to_non_nullable
              as String?,
      flags: null == flags
          ? _value._flags
          : flags // ignore: cast_nullable_to_non_nullable
              as List<String>,
      confidenceScore: null == confidenceScore
          ? _value.confidenceScore
          : confidenceScore // ignore: cast_nullable_to_non_nullable
              as double,
      assignedTo: freezed == assignedTo
          ? _value.assignedTo
          : assignedTo // ignore: cast_nullable_to_non_nullable
              as int?,
      reviewedBy: freezed == reviewedBy
          ? _value.reviewedBy
          : reviewedBy // ignore: cast_nullable_to_non_nullable
              as int?,
      reviewedAt: freezed == reviewedAt
          ? _value.reviewedAt
          : reviewedAt // ignore: cast_nullable_to_non_nullable
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
class _$ModerationItemImpl implements _ModerationItem {
  const _$ModerationItemImpl(
      {required this.id,
      required this.contentId,
      required this.contentType,
      required this.status,
      this.reason,
      required final List<String> flags,
      required this.confidenceScore,
      this.assignedTo,
      this.reviewedBy,
      this.reviewedAt,
      required this.createdAt})
      : _flags = flags;

  factory _$ModerationItemImpl.fromJson(Map<String, dynamic> json) =>
      _$$ModerationItemImplFromJson(json);

  @override
  final int id;
  @override
  final int contentId;
  @override
  final String contentType;
  @override
  final String status;
  @override
  final String? reason;
  final List<String> _flags;
  @override
  List<String> get flags {
    if (_flags is EqualUnmodifiableListView) return _flags;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_flags);
  }

  @override
  final double confidenceScore;
  @override
  final int? assignedTo;
  @override
  final int? reviewedBy;
  @override
  final DateTime? reviewedAt;
  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'ModerationItem(id: $id, contentId: $contentId, contentType: $contentType, status: $status, reason: $reason, flags: $flags, confidenceScore: $confidenceScore, assignedTo: $assignedTo, reviewedBy: $reviewedBy, reviewedAt: $reviewedAt, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$ModerationItemImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.contentId, contentId) ||
                other.contentId == contentId) &&
            (identical(other.contentType, contentType) ||
                other.contentType == contentType) &&
            (identical(other.status, status) || other.status == status) &&
            (identical(other.reason, reason) || other.reason == reason) &&
            const DeepCollectionEquality().equals(other._flags, _flags) &&
            (identical(other.confidenceScore, confidenceScore) ||
                other.confidenceScore == confidenceScore) &&
            (identical(other.assignedTo, assignedTo) ||
                other.assignedTo == assignedTo) &&
            (identical(other.reviewedBy, reviewedBy) ||
                other.reviewedBy == reviewedBy) &&
            (identical(other.reviewedAt, reviewedAt) ||
                other.reviewedAt == reviewedAt) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      contentId,
      contentType,
      status,
      reason,
      const DeepCollectionEquality().hash(_flags),
      confidenceScore,
      assignedTo,
      reviewedBy,
      reviewedAt,
      createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$ModerationItemImplCopyWith<_$ModerationItemImpl> get copyWith =>
      __$$ModerationItemImplCopyWithImpl<_$ModerationItemImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$ModerationItemImplToJson(
      this,
    );
  }
}

abstract class _ModerationItem implements ModerationItem {
  const factory _ModerationItem(
      {required final int id,
      required final int contentId,
      required final String contentType,
      required final String status,
      final String? reason,
      required final List<String> flags,
      required final double confidenceScore,
      final int? assignedTo,
      final int? reviewedBy,
      final DateTime? reviewedAt,
      required final DateTime createdAt}) = _$ModerationItemImpl;

  factory _ModerationItem.fromJson(Map<String, dynamic> json) =
      _$ModerationItemImpl.fromJson;

  @override
  int get id;
  @override
  int get contentId;
  @override
  String get contentType;
  @override
  String get status;
  @override
  String? get reason;
  @override
  List<String> get flags;
  @override
  double get confidenceScore;
  @override
  int? get assignedTo;
  @override
  int? get reviewedBy;
  @override
  DateTime? get reviewedAt;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$ModerationItemImplCopyWith<_$ModerationItemImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

ComplianceCheckResult _$ComplianceCheckResultFromJson(
    Map<String, dynamic> json) {
  return _ComplianceCheckResult.fromJson(json);
}

/// @nodoc
mixin _$ComplianceCheckResult {
  bool get isCompliant => throw _privateConstructorUsedError;
  List<Map<String, dynamic>> get violations =>
      throw _privateConstructorUsedError;
  int get violationCount => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $ComplianceCheckResultCopyWith<ComplianceCheckResult> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $ComplianceCheckResultCopyWith<$Res> {
  factory $ComplianceCheckResultCopyWith(ComplianceCheckResult value,
          $Res Function(ComplianceCheckResult) then) =
      _$ComplianceCheckResultCopyWithImpl<$Res, ComplianceCheckResult>;
  @useResult
  $Res call(
      {bool isCompliant,
      List<Map<String, dynamic>> violations,
      int violationCount});
}

/// @nodoc
class _$ComplianceCheckResultCopyWithImpl<$Res,
        $Val extends ComplianceCheckResult>
    implements $ComplianceCheckResultCopyWith<$Res> {
  _$ComplianceCheckResultCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? isCompliant = null,
    Object? violations = null,
    Object? violationCount = null,
  }) {
    return _then(_value.copyWith(
      isCompliant: null == isCompliant
          ? _value.isCompliant
          : isCompliant // ignore: cast_nullable_to_non_nullable
              as bool,
      violations: null == violations
          ? _value.violations
          : violations // ignore: cast_nullable_to_non_nullable
              as List<Map<String, dynamic>>,
      violationCount: null == violationCount
          ? _value.violationCount
          : violationCount // ignore: cast_nullable_to_non_nullable
              as int,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$ComplianceCheckResultImplCopyWith<$Res>
    implements $ComplianceCheckResultCopyWith<$Res> {
  factory _$$ComplianceCheckResultImplCopyWith(
          _$ComplianceCheckResultImpl value,
          $Res Function(_$ComplianceCheckResultImpl) then) =
      __$$ComplianceCheckResultImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {bool isCompliant,
      List<Map<String, dynamic>> violations,
      int violationCount});
}

/// @nodoc
class __$$ComplianceCheckResultImplCopyWithImpl<$Res>
    extends _$ComplianceCheckResultCopyWithImpl<$Res,
        _$ComplianceCheckResultImpl>
    implements _$$ComplianceCheckResultImplCopyWith<$Res> {
  __$$ComplianceCheckResultImplCopyWithImpl(_$ComplianceCheckResultImpl _value,
      $Res Function(_$ComplianceCheckResultImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? isCompliant = null,
    Object? violations = null,
    Object? violationCount = null,
  }) {
    return _then(_$ComplianceCheckResultImpl(
      isCompliant: null == isCompliant
          ? _value.isCompliant
          : isCompliant // ignore: cast_nullable_to_non_nullable
              as bool,
      violations: null == violations
          ? _value._violations
          : violations // ignore: cast_nullable_to_non_nullable
              as List<Map<String, dynamic>>,
      violationCount: null == violationCount
          ? _value.violationCount
          : violationCount // ignore: cast_nullable_to_non_nullable
              as int,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$ComplianceCheckResultImpl implements _ComplianceCheckResult {
  const _$ComplianceCheckResultImpl(
      {required this.isCompliant,
      required final List<Map<String, dynamic>> violations,
      required this.violationCount})
      : _violations = violations;

  factory _$ComplianceCheckResultImpl.fromJson(Map<String, dynamic> json) =>
      _$$ComplianceCheckResultImplFromJson(json);

  @override
  final bool isCompliant;
  final List<Map<String, dynamic>> _violations;
  @override
  List<Map<String, dynamic>> get violations {
    if (_violations is EqualUnmodifiableListView) return _violations;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_violations);
  }

  @override
  final int violationCount;

  @override
  String toString() {
    return 'ComplianceCheckResult(isCompliant: $isCompliant, violations: $violations, violationCount: $violationCount)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$ComplianceCheckResultImpl &&
            (identical(other.isCompliant, isCompliant) ||
                other.isCompliant == isCompliant) &&
            const DeepCollectionEquality()
                .equals(other._violations, _violations) &&
            (identical(other.violationCount, violationCount) ||
                other.violationCount == violationCount));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, isCompliant,
      const DeepCollectionEquality().hash(_violations), violationCount);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$ComplianceCheckResultImplCopyWith<_$ComplianceCheckResultImpl>
      get copyWith => __$$ComplianceCheckResultImplCopyWithImpl<
          _$ComplianceCheckResultImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$ComplianceCheckResultImplToJson(
      this,
    );
  }
}

abstract class _ComplianceCheckResult implements ComplianceCheckResult {
  const factory _ComplianceCheckResult(
      {required final bool isCompliant,
      required final List<Map<String, dynamic>> violations,
      required final int violationCount}) = _$ComplianceCheckResultImpl;

  factory _ComplianceCheckResult.fromJson(Map<String, dynamic> json) =
      _$ComplianceCheckResultImpl.fromJson;

  @override
  bool get isCompliant;
  @override
  List<Map<String, dynamic>> get violations;
  @override
  int get violationCount;
  @override
  @JsonKey(ignore: true)
  _$$ComplianceCheckResultImplCopyWith<_$ComplianceCheckResultImpl>
      get copyWith => throw _privateConstructorUsedError;
}

RateLimitStatus _$RateLimitStatusFromJson(Map<String, dynamic> json) {
  return _RateLimitStatus.fromJson(json);
}

/// @nodoc
mixin _$RateLimitStatus {
  bool get limited => throw _privateConstructorUsedError;
  int? get minuteRemaining => throw _privateConstructorUsedError;
  int? get hourRemaining => throw _privateConstructorUsedError;
  int? get dayRemaining => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $RateLimitStatusCopyWith<RateLimitStatus> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $RateLimitStatusCopyWith<$Res> {
  factory $RateLimitStatusCopyWith(
          RateLimitStatus value, $Res Function(RateLimitStatus) then) =
      _$RateLimitStatusCopyWithImpl<$Res, RateLimitStatus>;
  @useResult
  $Res call(
      {bool limited,
      int? minuteRemaining,
      int? hourRemaining,
      int? dayRemaining});
}

/// @nodoc
class _$RateLimitStatusCopyWithImpl<$Res, $Val extends RateLimitStatus>
    implements $RateLimitStatusCopyWith<$Res> {
  _$RateLimitStatusCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? limited = null,
    Object? minuteRemaining = freezed,
    Object? hourRemaining = freezed,
    Object? dayRemaining = freezed,
  }) {
    return _then(_value.copyWith(
      limited: null == limited
          ? _value.limited
          : limited // ignore: cast_nullable_to_non_nullable
              as bool,
      minuteRemaining: freezed == minuteRemaining
          ? _value.minuteRemaining
          : minuteRemaining // ignore: cast_nullable_to_non_nullable
              as int?,
      hourRemaining: freezed == hourRemaining
          ? _value.hourRemaining
          : hourRemaining // ignore: cast_nullable_to_non_nullable
              as int?,
      dayRemaining: freezed == dayRemaining
          ? _value.dayRemaining
          : dayRemaining // ignore: cast_nullable_to_non_nullable
              as int?,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$RateLimitStatusImplCopyWith<$Res>
    implements $RateLimitStatusCopyWith<$Res> {
  factory _$$RateLimitStatusImplCopyWith(_$RateLimitStatusImpl value,
          $Res Function(_$RateLimitStatusImpl) then) =
      __$$RateLimitStatusImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {bool limited,
      int? minuteRemaining,
      int? hourRemaining,
      int? dayRemaining});
}

/// @nodoc
class __$$RateLimitStatusImplCopyWithImpl<$Res>
    extends _$RateLimitStatusCopyWithImpl<$Res, _$RateLimitStatusImpl>
    implements _$$RateLimitStatusImplCopyWith<$Res> {
  __$$RateLimitStatusImplCopyWithImpl(
      _$RateLimitStatusImpl _value, $Res Function(_$RateLimitStatusImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? limited = null,
    Object? minuteRemaining = freezed,
    Object? hourRemaining = freezed,
    Object? dayRemaining = freezed,
  }) {
    return _then(_$RateLimitStatusImpl(
      limited: null == limited
          ? _value.limited
          : limited // ignore: cast_nullable_to_non_nullable
              as bool,
      minuteRemaining: freezed == minuteRemaining
          ? _value.minuteRemaining
          : minuteRemaining // ignore: cast_nullable_to_non_nullable
              as int?,
      hourRemaining: freezed == hourRemaining
          ? _value.hourRemaining
          : hourRemaining // ignore: cast_nullable_to_non_nullable
              as int?,
      dayRemaining: freezed == dayRemaining
          ? _value.dayRemaining
          : dayRemaining // ignore: cast_nullable_to_non_nullable
              as int?,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$RateLimitStatusImpl implements _RateLimitStatus {
  const _$RateLimitStatusImpl(
      {required this.limited,
      this.minuteRemaining,
      this.hourRemaining,
      this.dayRemaining});

  factory _$RateLimitStatusImpl.fromJson(Map<String, dynamic> json) =>
      _$$RateLimitStatusImplFromJson(json);

  @override
  final bool limited;
  @override
  final int? minuteRemaining;
  @override
  final int? hourRemaining;
  @override
  final int? dayRemaining;

  @override
  String toString() {
    return 'RateLimitStatus(limited: $limited, minuteRemaining: $minuteRemaining, hourRemaining: $hourRemaining, dayRemaining: $dayRemaining)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$RateLimitStatusImpl &&
            (identical(other.limited, limited) || other.limited == limited) &&
            (identical(other.minuteRemaining, minuteRemaining) ||
                other.minuteRemaining == minuteRemaining) &&
            (identical(other.hourRemaining, hourRemaining) ||
                other.hourRemaining == hourRemaining) &&
            (identical(other.dayRemaining, dayRemaining) ||
                other.dayRemaining == dayRemaining));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType, limited, minuteRemaining, hourRemaining, dayRemaining);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$RateLimitStatusImplCopyWith<_$RateLimitStatusImpl> get copyWith =>
      __$$RateLimitStatusImplCopyWithImpl<_$RateLimitStatusImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$RateLimitStatusImplToJson(
      this,
    );
  }
}

abstract class _RateLimitStatus implements RateLimitStatus {
  const factory _RateLimitStatus(
      {required final bool limited,
      final int? minuteRemaining,
      final int? hourRemaining,
      final int? dayRemaining}) = _$RateLimitStatusImpl;

  factory _RateLimitStatus.fromJson(Map<String, dynamic> json) =
      _$RateLimitStatusImpl.fromJson;

  @override
  bool get limited;
  @override
  int? get minuteRemaining;
  @override
  int? get hourRemaining;
  @override
  int? get dayRemaining;
  @override
  @JsonKey(ignore: true)
  _$$RateLimitStatusImplCopyWith<_$RateLimitStatusImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

NotificationPreference _$NotificationPreferenceFromJson(
    Map<String, dynamic> json) {
  return _NotificationPreference.fromJson(json);
}

/// @nodoc
mixin _$NotificationPreference {
  int get id => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  bool get emailEnabled => throw _privateConstructorUsedError;
  bool get pushEnabled => throw _privateConstructorUsedError;
  bool get smsEnabled => throw _privateConstructorUsedError;
  bool get inAppEnabled => throw _privateConstructorUsedError;
  String get frequency => throw _privateConstructorUsedError;
  String? get doNotDisturbStart => throw _privateConstructorUsedError;
  String? get doNotDisturbEnd => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $NotificationPreferenceCopyWith<NotificationPreference> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $NotificationPreferenceCopyWith<$Res> {
  factory $NotificationPreferenceCopyWith(NotificationPreference value,
          $Res Function(NotificationPreference) then) =
      _$NotificationPreferenceCopyWithImpl<$Res, NotificationPreference>;
  @useResult
  $Res call(
      {int id,
      int userId,
      bool emailEnabled,
      bool pushEnabled,
      bool smsEnabled,
      bool inAppEnabled,
      String frequency,
      String? doNotDisturbStart,
      String? doNotDisturbEnd,
      DateTime createdAt});
}

/// @nodoc
class _$NotificationPreferenceCopyWithImpl<$Res,
        $Val extends NotificationPreference>
    implements $NotificationPreferenceCopyWith<$Res> {
  _$NotificationPreferenceCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? emailEnabled = null,
    Object? pushEnabled = null,
    Object? smsEnabled = null,
    Object? inAppEnabled = null,
    Object? frequency = null,
    Object? doNotDisturbStart = freezed,
    Object? doNotDisturbEnd = freezed,
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
      emailEnabled: null == emailEnabled
          ? _value.emailEnabled
          : emailEnabled // ignore: cast_nullable_to_non_nullable
              as bool,
      pushEnabled: null == pushEnabled
          ? _value.pushEnabled
          : pushEnabled // ignore: cast_nullable_to_non_nullable
              as bool,
      smsEnabled: null == smsEnabled
          ? _value.smsEnabled
          : smsEnabled // ignore: cast_nullable_to_non_nullable
              as bool,
      inAppEnabled: null == inAppEnabled
          ? _value.inAppEnabled
          : inAppEnabled // ignore: cast_nullable_to_non_nullable
              as bool,
      frequency: null == frequency
          ? _value.frequency
          : frequency // ignore: cast_nullable_to_non_nullable
              as String,
      doNotDisturbStart: freezed == doNotDisturbStart
          ? _value.doNotDisturbStart
          : doNotDisturbStart // ignore: cast_nullable_to_non_nullable
              as String?,
      doNotDisturbEnd: freezed == doNotDisturbEnd
          ? _value.doNotDisturbEnd
          : doNotDisturbEnd // ignore: cast_nullable_to_non_nullable
              as String?,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$NotificationPreferenceImplCopyWith<$Res>
    implements $NotificationPreferenceCopyWith<$Res> {
  factory _$$NotificationPreferenceImplCopyWith(
          _$NotificationPreferenceImpl value,
          $Res Function(_$NotificationPreferenceImpl) then) =
      __$$NotificationPreferenceImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int userId,
      bool emailEnabled,
      bool pushEnabled,
      bool smsEnabled,
      bool inAppEnabled,
      String frequency,
      String? doNotDisturbStart,
      String? doNotDisturbEnd,
      DateTime createdAt});
}

/// @nodoc
class __$$NotificationPreferenceImplCopyWithImpl<$Res>
    extends _$NotificationPreferenceCopyWithImpl<$Res,
        _$NotificationPreferenceImpl>
    implements _$$NotificationPreferenceImplCopyWith<$Res> {
  __$$NotificationPreferenceImplCopyWithImpl(
      _$NotificationPreferenceImpl _value,
      $Res Function(_$NotificationPreferenceImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? emailEnabled = null,
    Object? pushEnabled = null,
    Object? smsEnabled = null,
    Object? inAppEnabled = null,
    Object? frequency = null,
    Object? doNotDisturbStart = freezed,
    Object? doNotDisturbEnd = freezed,
    Object? createdAt = null,
  }) {
    return _then(_$NotificationPreferenceImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      emailEnabled: null == emailEnabled
          ? _value.emailEnabled
          : emailEnabled // ignore: cast_nullable_to_non_nullable
              as bool,
      pushEnabled: null == pushEnabled
          ? _value.pushEnabled
          : pushEnabled // ignore: cast_nullable_to_non_nullable
              as bool,
      smsEnabled: null == smsEnabled
          ? _value.smsEnabled
          : smsEnabled // ignore: cast_nullable_to_non_nullable
              as bool,
      inAppEnabled: null == inAppEnabled
          ? _value.inAppEnabled
          : inAppEnabled // ignore: cast_nullable_to_non_nullable
              as bool,
      frequency: null == frequency
          ? _value.frequency
          : frequency // ignore: cast_nullable_to_non_nullable
              as String,
      doNotDisturbStart: freezed == doNotDisturbStart
          ? _value.doNotDisturbStart
          : doNotDisturbStart // ignore: cast_nullable_to_non_nullable
              as String?,
      doNotDisturbEnd: freezed == doNotDisturbEnd
          ? _value.doNotDisturbEnd
          : doNotDisturbEnd // ignore: cast_nullable_to_non_nullable
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
class _$NotificationPreferenceImpl implements _NotificationPreference {
  const _$NotificationPreferenceImpl(
      {required this.id,
      required this.userId,
      required this.emailEnabled,
      required this.pushEnabled,
      required this.smsEnabled,
      required this.inAppEnabled,
      required this.frequency,
      this.doNotDisturbStart,
      this.doNotDisturbEnd,
      required this.createdAt});

  factory _$NotificationPreferenceImpl.fromJson(Map<String, dynamic> json) =>
      _$$NotificationPreferenceImplFromJson(json);

  @override
  final int id;
  @override
  final int userId;
  @override
  final bool emailEnabled;
  @override
  final bool pushEnabled;
  @override
  final bool smsEnabled;
  @override
  final bool inAppEnabled;
  @override
  final String frequency;
  @override
  final String? doNotDisturbStart;
  @override
  final String? doNotDisturbEnd;
  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'NotificationPreference(id: $id, userId: $userId, emailEnabled: $emailEnabled, pushEnabled: $pushEnabled, smsEnabled: $smsEnabled, inAppEnabled: $inAppEnabled, frequency: $frequency, doNotDisturbStart: $doNotDisturbStart, doNotDisturbEnd: $doNotDisturbEnd, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$NotificationPreferenceImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.emailEnabled, emailEnabled) ||
                other.emailEnabled == emailEnabled) &&
            (identical(other.pushEnabled, pushEnabled) ||
                other.pushEnabled == pushEnabled) &&
            (identical(other.smsEnabled, smsEnabled) ||
                other.smsEnabled == smsEnabled) &&
            (identical(other.inAppEnabled, inAppEnabled) ||
                other.inAppEnabled == inAppEnabled) &&
            (identical(other.frequency, frequency) ||
                other.frequency == frequency) &&
            (identical(other.doNotDisturbStart, doNotDisturbStart) ||
                other.doNotDisturbStart == doNotDisturbStart) &&
            (identical(other.doNotDisturbEnd, doNotDisturbEnd) ||
                other.doNotDisturbEnd == doNotDisturbEnd) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      userId,
      emailEnabled,
      pushEnabled,
      smsEnabled,
      inAppEnabled,
      frequency,
      doNotDisturbStart,
      doNotDisturbEnd,
      createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$NotificationPreferenceImplCopyWith<_$NotificationPreferenceImpl>
      get copyWith => __$$NotificationPreferenceImplCopyWithImpl<
          _$NotificationPreferenceImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$NotificationPreferenceImplToJson(
      this,
    );
  }
}

abstract class _NotificationPreference implements NotificationPreference {
  const factory _NotificationPreference(
      {required final int id,
      required final int userId,
      required final bool emailEnabled,
      required final bool pushEnabled,
      required final bool smsEnabled,
      required final bool inAppEnabled,
      required final String frequency,
      final String? doNotDisturbStart,
      final String? doNotDisturbEnd,
      required final DateTime createdAt}) = _$NotificationPreferenceImpl;

  factory _NotificationPreference.fromJson(Map<String, dynamic> json) =
      _$NotificationPreferenceImpl.fromJson;

  @override
  int get id;
  @override
  int get userId;
  @override
  bool get emailEnabled;
  @override
  bool get pushEnabled;
  @override
  bool get smsEnabled;
  @override
  bool get inAppEnabled;
  @override
  String get frequency;
  @override
  String? get doNotDisturbStart;
  @override
  String? get doNotDisturbEnd;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$NotificationPreferenceImplCopyWith<_$NotificationPreferenceImpl>
      get copyWith => throw _privateConstructorUsedError;
}

Notification _$NotificationFromJson(Map<String, dynamic> json) {
  return _Notification.fromJson(json);
}

/// @nodoc
mixin _$Notification {
  int get id => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  String get notificationType => throw _privateConstructorUsedError;
  String get title => throw _privateConstructorUsedError;
  String get message => throw _privateConstructorUsedError;
  bool get read => throw _privateConstructorUsedError;
  DateTime? get readAt => throw _privateConstructorUsedError;
  String? get actionUrl => throw _privateConstructorUsedError;
  String? get source => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $NotificationCopyWith<Notification> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $NotificationCopyWith<$Res> {
  factory $NotificationCopyWith(
          Notification value, $Res Function(Notification) then) =
      _$NotificationCopyWithImpl<$Res, Notification>;
  @useResult
  $Res call(
      {int id,
      int userId,
      String notificationType,
      String title,
      String message,
      bool read,
      DateTime? readAt,
      String? actionUrl,
      String? source,
      DateTime createdAt});
}

/// @nodoc
class _$NotificationCopyWithImpl<$Res, $Val extends Notification>
    implements $NotificationCopyWith<$Res> {
  _$NotificationCopyWithImpl(this._value, this._then);

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
    Object? message = null,
    Object? read = null,
    Object? readAt = freezed,
    Object? actionUrl = freezed,
    Object? source = freezed,
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
      message: null == message
          ? _value.message
          : message // ignore: cast_nullable_to_non_nullable
              as String,
      read: null == read
          ? _value.read
          : read // ignore: cast_nullable_to_non_nullable
              as bool,
      readAt: freezed == readAt
          ? _value.readAt
          : readAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      actionUrl: freezed == actionUrl
          ? _value.actionUrl
          : actionUrl // ignore: cast_nullable_to_non_nullable
              as String?,
      source: freezed == source
          ? _value.source
          : source // ignore: cast_nullable_to_non_nullable
              as String?,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$NotificationImplCopyWith<$Res>
    implements $NotificationCopyWith<$Res> {
  factory _$$NotificationImplCopyWith(
          _$NotificationImpl value, $Res Function(_$NotificationImpl) then) =
      __$$NotificationImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int userId,
      String notificationType,
      String title,
      String message,
      bool read,
      DateTime? readAt,
      String? actionUrl,
      String? source,
      DateTime createdAt});
}

/// @nodoc
class __$$NotificationImplCopyWithImpl<$Res>
    extends _$NotificationCopyWithImpl<$Res, _$NotificationImpl>
    implements _$$NotificationImplCopyWith<$Res> {
  __$$NotificationImplCopyWithImpl(
      _$NotificationImpl _value, $Res Function(_$NotificationImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? notificationType = null,
    Object? title = null,
    Object? message = null,
    Object? read = null,
    Object? readAt = freezed,
    Object? actionUrl = freezed,
    Object? source = freezed,
    Object? createdAt = null,
  }) {
    return _then(_$NotificationImpl(
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
      message: null == message
          ? _value.message
          : message // ignore: cast_nullable_to_non_nullable
              as String,
      read: null == read
          ? _value.read
          : read // ignore: cast_nullable_to_non_nullable
              as bool,
      readAt: freezed == readAt
          ? _value.readAt
          : readAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      actionUrl: freezed == actionUrl
          ? _value.actionUrl
          : actionUrl // ignore: cast_nullable_to_non_nullable
              as String?,
      source: freezed == source
          ? _value.source
          : source // ignore: cast_nullable_to_non_nullable
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
class _$NotificationImpl implements _Notification {
  const _$NotificationImpl(
      {required this.id,
      required this.userId,
      required this.notificationType,
      required this.title,
      required this.message,
      required this.read,
      this.readAt,
      this.actionUrl,
      this.source,
      required this.createdAt});

  factory _$NotificationImpl.fromJson(Map<String, dynamic> json) =>
      _$$NotificationImplFromJson(json);

  @override
  final int id;
  @override
  final int userId;
  @override
  final String notificationType;
  @override
  final String title;
  @override
  final String message;
  @override
  final bool read;
  @override
  final DateTime? readAt;
  @override
  final String? actionUrl;
  @override
  final String? source;
  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'Notification(id: $id, userId: $userId, notificationType: $notificationType, title: $title, message: $message, read: $read, readAt: $readAt, actionUrl: $actionUrl, source: $source, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$NotificationImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.notificationType, notificationType) ||
                other.notificationType == notificationType) &&
            (identical(other.title, title) || other.title == title) &&
            (identical(other.message, message) || other.message == message) &&
            (identical(other.read, read) || other.read == read) &&
            (identical(other.readAt, readAt) || other.readAt == readAt) &&
            (identical(other.actionUrl, actionUrl) ||
                other.actionUrl == actionUrl) &&
            (identical(other.source, source) || other.source == source) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, id, userId, notificationType,
      title, message, read, readAt, actionUrl, source, createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$NotificationImplCopyWith<_$NotificationImpl> get copyWith =>
      __$$NotificationImplCopyWithImpl<_$NotificationImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$NotificationImplToJson(
      this,
    );
  }
}

abstract class _Notification implements Notification {
  const factory _Notification(
      {required final int id,
      required final int userId,
      required final String notificationType,
      required final String title,
      required final String message,
      required final bool read,
      final DateTime? readAt,
      final String? actionUrl,
      final String? source,
      required final DateTime createdAt}) = _$NotificationImpl;

  factory _Notification.fromJson(Map<String, dynamic> json) =
      _$NotificationImpl.fromJson;

  @override
  int get id;
  @override
  int get userId;
  @override
  String get notificationType;
  @override
  String get title;
  @override
  String get message;
  @override
  bool get read;
  @override
  DateTime? get readAt;
  @override
  String? get actionUrl;
  @override
  String? get source;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$NotificationImplCopyWith<_$NotificationImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

AlertConfiguration _$AlertConfigurationFromJson(Map<String, dynamic> json) {
  return _AlertConfiguration.fromJson(json);
}

/// @nodoc
mixin _$AlertConfiguration {
  int get id => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  String get alertType => throw _privateConstructorUsedError;
  String get condition => throw _privateConstructorUsedError;
  double? get threshold => throw _privateConstructorUsedError;
  bool get enabled => throw _privateConstructorUsedError;
  List<String> get notificationChannels => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $AlertConfigurationCopyWith<AlertConfiguration> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $AlertConfigurationCopyWith<$Res> {
  factory $AlertConfigurationCopyWith(
          AlertConfiguration value, $Res Function(AlertConfiguration) then) =
      _$AlertConfigurationCopyWithImpl<$Res, AlertConfiguration>;
  @useResult
  $Res call(
      {int id,
      int userId,
      String alertType,
      String condition,
      double? threshold,
      bool enabled,
      List<String> notificationChannels,
      DateTime createdAt});
}

/// @nodoc
class _$AlertConfigurationCopyWithImpl<$Res, $Val extends AlertConfiguration>
    implements $AlertConfigurationCopyWith<$Res> {
  _$AlertConfigurationCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? alertType = null,
    Object? condition = null,
    Object? threshold = freezed,
    Object? enabled = null,
    Object? notificationChannels = null,
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
      alertType: null == alertType
          ? _value.alertType
          : alertType // ignore: cast_nullable_to_non_nullable
              as String,
      condition: null == condition
          ? _value.condition
          : condition // ignore: cast_nullable_to_non_nullable
              as String,
      threshold: freezed == threshold
          ? _value.threshold
          : threshold // ignore: cast_nullable_to_non_nullable
              as double?,
      enabled: null == enabled
          ? _value.enabled
          : enabled // ignore: cast_nullable_to_non_nullable
              as bool,
      notificationChannels: null == notificationChannels
          ? _value.notificationChannels
          : notificationChannels // ignore: cast_nullable_to_non_nullable
              as List<String>,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$AlertConfigurationImplCopyWith<$Res>
    implements $AlertConfigurationCopyWith<$Res> {
  factory _$$AlertConfigurationImplCopyWith(_$AlertConfigurationImpl value,
          $Res Function(_$AlertConfigurationImpl) then) =
      __$$AlertConfigurationImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int userId,
      String alertType,
      String condition,
      double? threshold,
      bool enabled,
      List<String> notificationChannels,
      DateTime createdAt});
}

/// @nodoc
class __$$AlertConfigurationImplCopyWithImpl<$Res>
    extends _$AlertConfigurationCopyWithImpl<$Res, _$AlertConfigurationImpl>
    implements _$$AlertConfigurationImplCopyWith<$Res> {
  __$$AlertConfigurationImplCopyWithImpl(_$AlertConfigurationImpl _value,
      $Res Function(_$AlertConfigurationImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? alertType = null,
    Object? condition = null,
    Object? threshold = freezed,
    Object? enabled = null,
    Object? notificationChannels = null,
    Object? createdAt = null,
  }) {
    return _then(_$AlertConfigurationImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      alertType: null == alertType
          ? _value.alertType
          : alertType // ignore: cast_nullable_to_non_nullable
              as String,
      condition: null == condition
          ? _value.condition
          : condition // ignore: cast_nullable_to_non_nullable
              as String,
      threshold: freezed == threshold
          ? _value.threshold
          : threshold // ignore: cast_nullable_to_non_nullable
              as double?,
      enabled: null == enabled
          ? _value.enabled
          : enabled // ignore: cast_nullable_to_non_nullable
              as bool,
      notificationChannels: null == notificationChannels
          ? _value._notificationChannels
          : notificationChannels // ignore: cast_nullable_to_non_nullable
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
class _$AlertConfigurationImpl implements _AlertConfiguration {
  const _$AlertConfigurationImpl(
      {required this.id,
      required this.userId,
      required this.alertType,
      required this.condition,
      this.threshold,
      required this.enabled,
      required final List<String> notificationChannels,
      required this.createdAt})
      : _notificationChannels = notificationChannels;

  factory _$AlertConfigurationImpl.fromJson(Map<String, dynamic> json) =>
      _$$AlertConfigurationImplFromJson(json);

  @override
  final int id;
  @override
  final int userId;
  @override
  final String alertType;
  @override
  final String condition;
  @override
  final double? threshold;
  @override
  final bool enabled;
  final List<String> _notificationChannels;
  @override
  List<String> get notificationChannels {
    if (_notificationChannels is EqualUnmodifiableListView)
      return _notificationChannels;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_notificationChannels);
  }

  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'AlertConfiguration(id: $id, userId: $userId, alertType: $alertType, condition: $condition, threshold: $threshold, enabled: $enabled, notificationChannels: $notificationChannels, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$AlertConfigurationImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.alertType, alertType) ||
                other.alertType == alertType) &&
            (identical(other.condition, condition) ||
                other.condition == condition) &&
            (identical(other.threshold, threshold) ||
                other.threshold == threshold) &&
            (identical(other.enabled, enabled) || other.enabled == enabled) &&
            const DeepCollectionEquality()
                .equals(other._notificationChannels, _notificationChannels) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      userId,
      alertType,
      condition,
      threshold,
      enabled,
      const DeepCollectionEquality().hash(_notificationChannels),
      createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$AlertConfigurationImplCopyWith<_$AlertConfigurationImpl> get copyWith =>
      __$$AlertConfigurationImplCopyWithImpl<_$AlertConfigurationImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$AlertConfigurationImplToJson(
      this,
    );
  }
}

abstract class _AlertConfiguration implements AlertConfiguration {
  const factory _AlertConfiguration(
      {required final int id,
      required final int userId,
      required final String alertType,
      required final String condition,
      final double? threshold,
      required final bool enabled,
      required final List<String> notificationChannels,
      required final DateTime createdAt}) = _$AlertConfigurationImpl;

  factory _AlertConfiguration.fromJson(Map<String, dynamic> json) =
      _$AlertConfigurationImpl.fromJson;

  @override
  int get id;
  @override
  int get userId;
  @override
  String get alertType;
  @override
  String get condition;
  @override
  double? get threshold;
  @override
  bool get enabled;
  @override
  List<String> get notificationChannels;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$AlertConfigurationImplCopyWith<_$AlertConfigurationImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

AdvancedReport _$AdvancedReportFromJson(Map<String, dynamic> json) {
  return _AdvancedReport.fromJson(json);
}

/// @nodoc
mixin _$AdvancedReport {
  int get id => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  String get name => throw _privateConstructorUsedError;
  String get reportType => throw _privateConstructorUsedError;
  String get format => throw _privateConstructorUsedError;
  String get status => throw _privateConstructorUsedError;
  DateTime? get generatedAt => throw _privateConstructorUsedError;
  DateTime? get expiresAt => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $AdvancedReportCopyWith<AdvancedReport> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $AdvancedReportCopyWith<$Res> {
  factory $AdvancedReportCopyWith(
          AdvancedReport value, $Res Function(AdvancedReport) then) =
      _$AdvancedReportCopyWithImpl<$Res, AdvancedReport>;
  @useResult
  $Res call(
      {int id,
      int userId,
      String name,
      String reportType,
      String format,
      String status,
      DateTime? generatedAt,
      DateTime? expiresAt,
      DateTime createdAt});
}

/// @nodoc
class _$AdvancedReportCopyWithImpl<$Res, $Val extends AdvancedReport>
    implements $AdvancedReportCopyWith<$Res> {
  _$AdvancedReportCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? name = null,
    Object? reportType = null,
    Object? format = null,
    Object? status = null,
    Object? generatedAt = freezed,
    Object? expiresAt = freezed,
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
      name: null == name
          ? _value.name
          : name // ignore: cast_nullable_to_non_nullable
              as String,
      reportType: null == reportType
          ? _value.reportType
          : reportType // ignore: cast_nullable_to_non_nullable
              as String,
      format: null == format
          ? _value.format
          : format // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      generatedAt: freezed == generatedAt
          ? _value.generatedAt
          : generatedAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      expiresAt: freezed == expiresAt
          ? _value.expiresAt
          : expiresAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$AdvancedReportImplCopyWith<$Res>
    implements $AdvancedReportCopyWith<$Res> {
  factory _$$AdvancedReportImplCopyWith(_$AdvancedReportImpl value,
          $Res Function(_$AdvancedReportImpl) then) =
      __$$AdvancedReportImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int userId,
      String name,
      String reportType,
      String format,
      String status,
      DateTime? generatedAt,
      DateTime? expiresAt,
      DateTime createdAt});
}

/// @nodoc
class __$$AdvancedReportImplCopyWithImpl<$Res>
    extends _$AdvancedReportCopyWithImpl<$Res, _$AdvancedReportImpl>
    implements _$$AdvancedReportImplCopyWith<$Res> {
  __$$AdvancedReportImplCopyWithImpl(
      _$AdvancedReportImpl _value, $Res Function(_$AdvancedReportImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? name = null,
    Object? reportType = null,
    Object? format = null,
    Object? status = null,
    Object? generatedAt = freezed,
    Object? expiresAt = freezed,
    Object? createdAt = null,
  }) {
    return _then(_$AdvancedReportImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      name: null == name
          ? _value.name
          : name // ignore: cast_nullable_to_non_nullable
              as String,
      reportType: null == reportType
          ? _value.reportType
          : reportType // ignore: cast_nullable_to_non_nullable
              as String,
      format: null == format
          ? _value.format
          : format // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      generatedAt: freezed == generatedAt
          ? _value.generatedAt
          : generatedAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      expiresAt: freezed == expiresAt
          ? _value.expiresAt
          : expiresAt // ignore: cast_nullable_to_non_nullable
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
class _$AdvancedReportImpl implements _AdvancedReport {
  const _$AdvancedReportImpl(
      {required this.id,
      required this.userId,
      required this.name,
      required this.reportType,
      required this.format,
      required this.status,
      this.generatedAt,
      this.expiresAt,
      required this.createdAt});

  factory _$AdvancedReportImpl.fromJson(Map<String, dynamic> json) =>
      _$$AdvancedReportImplFromJson(json);

  @override
  final int id;
  @override
  final int userId;
  @override
  final String name;
  @override
  final String reportType;
  @override
  final String format;
  @override
  final String status;
  @override
  final DateTime? generatedAt;
  @override
  final DateTime? expiresAt;
  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'AdvancedReport(id: $id, userId: $userId, name: $name, reportType: $reportType, format: $format, status: $status, generatedAt: $generatedAt, expiresAt: $expiresAt, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$AdvancedReportImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.reportType, reportType) ||
                other.reportType == reportType) &&
            (identical(other.format, format) || other.format == format) &&
            (identical(other.status, status) || other.status == status) &&
            (identical(other.generatedAt, generatedAt) ||
                other.generatedAt == generatedAt) &&
            (identical(other.expiresAt, expiresAt) ||
                other.expiresAt == expiresAt) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, id, userId, name, reportType,
      format, status, generatedAt, expiresAt, createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$AdvancedReportImplCopyWith<_$AdvancedReportImpl> get copyWith =>
      __$$AdvancedReportImplCopyWithImpl<_$AdvancedReportImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$AdvancedReportImplToJson(
      this,
    );
  }
}

abstract class _AdvancedReport implements AdvancedReport {
  const factory _AdvancedReport(
      {required final int id,
      required final int userId,
      required final String name,
      required final String reportType,
      required final String format,
      required final String status,
      final DateTime? generatedAt,
      final DateTime? expiresAt,
      required final DateTime createdAt}) = _$AdvancedReportImpl;

  factory _AdvancedReport.fromJson(Map<String, dynamic> json) =
      _$AdvancedReportImpl.fromJson;

  @override
  int get id;
  @override
  int get userId;
  @override
  String get name;
  @override
  String get reportType;
  @override
  String get format;
  @override
  String get status;
  @override
  DateTime? get generatedAt;
  @override
  DateTime? get expiresAt;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$AdvancedReportImplCopyWith<_$AdvancedReportImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

ReportTemplate _$ReportTemplateFromJson(Map<String, dynamic> json) {
  return _ReportTemplate.fromJson(json);
}

/// @nodoc
mixin _$ReportTemplate {
  int get id => throw _privateConstructorUsedError;
  String get name => throw _privateConstructorUsedError;
  String get reportType => throw _privateConstructorUsedError;
  List<String> get sections => throw _privateConstructorUsedError;
  String get format => throw _privateConstructorUsedError;
  String? get description => throw _privateConstructorUsedError;
  String? get schedule => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $ReportTemplateCopyWith<ReportTemplate> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $ReportTemplateCopyWith<$Res> {
  factory $ReportTemplateCopyWith(
          ReportTemplate value, $Res Function(ReportTemplate) then) =
      _$ReportTemplateCopyWithImpl<$Res, ReportTemplate>;
  @useResult
  $Res call(
      {int id,
      String name,
      String reportType,
      List<String> sections,
      String format,
      String? description,
      String? schedule,
      DateTime createdAt});
}

/// @nodoc
class _$ReportTemplateCopyWithImpl<$Res, $Val extends ReportTemplate>
    implements $ReportTemplateCopyWith<$Res> {
  _$ReportTemplateCopyWithImpl(this._value, this._then);

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
    Object? sections = null,
    Object? format = null,
    Object? description = freezed,
    Object? schedule = freezed,
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
      reportType: null == reportType
          ? _value.reportType
          : reportType // ignore: cast_nullable_to_non_nullable
              as String,
      sections: null == sections
          ? _value.sections
          : sections // ignore: cast_nullable_to_non_nullable
              as List<String>,
      format: null == format
          ? _value.format
          : format // ignore: cast_nullable_to_non_nullable
              as String,
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
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$ReportTemplateImplCopyWith<$Res>
    implements $ReportTemplateCopyWith<$Res> {
  factory _$$ReportTemplateImplCopyWith(_$ReportTemplateImpl value,
          $Res Function(_$ReportTemplateImpl) then) =
      __$$ReportTemplateImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String name,
      String reportType,
      List<String> sections,
      String format,
      String? description,
      String? schedule,
      DateTime createdAt});
}

/// @nodoc
class __$$ReportTemplateImplCopyWithImpl<$Res>
    extends _$ReportTemplateCopyWithImpl<$Res, _$ReportTemplateImpl>
    implements _$$ReportTemplateImplCopyWith<$Res> {
  __$$ReportTemplateImplCopyWithImpl(
      _$ReportTemplateImpl _value, $Res Function(_$ReportTemplateImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? reportType = null,
    Object? sections = null,
    Object? format = null,
    Object? description = freezed,
    Object? schedule = freezed,
    Object? createdAt = null,
  }) {
    return _then(_$ReportTemplateImpl(
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
      sections: null == sections
          ? _value._sections
          : sections // ignore: cast_nullable_to_non_nullable
              as List<String>,
      format: null == format
          ? _value.format
          : format // ignore: cast_nullable_to_non_nullable
              as String,
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
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$ReportTemplateImpl implements _ReportTemplate {
  const _$ReportTemplateImpl(
      {required this.id,
      required this.name,
      required this.reportType,
      required final List<String> sections,
      required this.format,
      this.description,
      this.schedule,
      required this.createdAt})
      : _sections = sections;

  factory _$ReportTemplateImpl.fromJson(Map<String, dynamic> json) =>
      _$$ReportTemplateImplFromJson(json);

  @override
  final int id;
  @override
  final String name;
  @override
  final String reportType;
  final List<String> _sections;
  @override
  List<String> get sections {
    if (_sections is EqualUnmodifiableListView) return _sections;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_sections);
  }

  @override
  final String format;
  @override
  final String? description;
  @override
  final String? schedule;
  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'ReportTemplate(id: $id, name: $name, reportType: $reportType, sections: $sections, format: $format, description: $description, schedule: $schedule, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$ReportTemplateImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.reportType, reportType) ||
                other.reportType == reportType) &&
            const DeepCollectionEquality().equals(other._sections, _sections) &&
            (identical(other.format, format) || other.format == format) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.schedule, schedule) ||
                other.schedule == schedule) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      name,
      reportType,
      const DeepCollectionEquality().hash(_sections),
      format,
      description,
      schedule,
      createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$ReportTemplateImplCopyWith<_$ReportTemplateImpl> get copyWith =>
      __$$ReportTemplateImplCopyWithImpl<_$ReportTemplateImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$ReportTemplateImplToJson(
      this,
    );
  }
}

abstract class _ReportTemplate implements ReportTemplate {
  const factory _ReportTemplate(
      {required final int id,
      required final String name,
      required final String reportType,
      required final List<String> sections,
      required final String format,
      final String? description,
      final String? schedule,
      required final DateTime createdAt}) = _$ReportTemplateImpl;

  factory _ReportTemplate.fromJson(Map<String, dynamic> json) =
      _$ReportTemplateImpl.fromJson;

  @override
  int get id;
  @override
  String get name;
  @override
  String get reportType;
  @override
  List<String> get sections;
  @override
  String get format;
  @override
  String? get description;
  @override
  String? get schedule;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$ReportTemplateImplCopyWith<_$ReportTemplateImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

ScheduledReport _$ScheduledReportFromJson(Map<String, dynamic> json) {
  return _ScheduledReport.fromJson(json);
}

/// @nodoc
mixin _$ScheduledReport {
  int get id => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  String get name => throw _privateConstructorUsedError;
  String get cronExpression => throw _privateConstructorUsedError;
  bool get enabled => throw _privateConstructorUsedError;
  DateTime? get lastRun => throw _privateConstructorUsedError;
  DateTime? get nextRun => throw _privateConstructorUsedError;
  List<String> get recipientEmails => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $ScheduledReportCopyWith<ScheduledReport> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $ScheduledReportCopyWith<$Res> {
  factory $ScheduledReportCopyWith(
          ScheduledReport value, $Res Function(ScheduledReport) then) =
      _$ScheduledReportCopyWithImpl<$Res, ScheduledReport>;
  @useResult
  $Res call(
      {int id,
      int userId,
      String name,
      String cronExpression,
      bool enabled,
      DateTime? lastRun,
      DateTime? nextRun,
      List<String> recipientEmails,
      DateTime createdAt});
}

/// @nodoc
class _$ScheduledReportCopyWithImpl<$Res, $Val extends ScheduledReport>
    implements $ScheduledReportCopyWith<$Res> {
  _$ScheduledReportCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? name = null,
    Object? cronExpression = null,
    Object? enabled = null,
    Object? lastRun = freezed,
    Object? nextRun = freezed,
    Object? recipientEmails = null,
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
      name: null == name
          ? _value.name
          : name // ignore: cast_nullable_to_non_nullable
              as String,
      cronExpression: null == cronExpression
          ? _value.cronExpression
          : cronExpression // ignore: cast_nullable_to_non_nullable
              as String,
      enabled: null == enabled
          ? _value.enabled
          : enabled // ignore: cast_nullable_to_non_nullable
              as bool,
      lastRun: freezed == lastRun
          ? _value.lastRun
          : lastRun // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      nextRun: freezed == nextRun
          ? _value.nextRun
          : nextRun // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      recipientEmails: null == recipientEmails
          ? _value.recipientEmails
          : recipientEmails // ignore: cast_nullable_to_non_nullable
              as List<String>,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$ScheduledReportImplCopyWith<$Res>
    implements $ScheduledReportCopyWith<$Res> {
  factory _$$ScheduledReportImplCopyWith(_$ScheduledReportImpl value,
          $Res Function(_$ScheduledReportImpl) then) =
      __$$ScheduledReportImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int userId,
      String name,
      String cronExpression,
      bool enabled,
      DateTime? lastRun,
      DateTime? nextRun,
      List<String> recipientEmails,
      DateTime createdAt});
}

/// @nodoc
class __$$ScheduledReportImplCopyWithImpl<$Res>
    extends _$ScheduledReportCopyWithImpl<$Res, _$ScheduledReportImpl>
    implements _$$ScheduledReportImplCopyWith<$Res> {
  __$$ScheduledReportImplCopyWithImpl(
      _$ScheduledReportImpl _value, $Res Function(_$ScheduledReportImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? name = null,
    Object? cronExpression = null,
    Object? enabled = null,
    Object? lastRun = freezed,
    Object? nextRun = freezed,
    Object? recipientEmails = null,
    Object? createdAt = null,
  }) {
    return _then(_$ScheduledReportImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      name: null == name
          ? _value.name
          : name // ignore: cast_nullable_to_non_nullable
              as String,
      cronExpression: null == cronExpression
          ? _value.cronExpression
          : cronExpression // ignore: cast_nullable_to_non_nullable
              as String,
      enabled: null == enabled
          ? _value.enabled
          : enabled // ignore: cast_nullable_to_non_nullable
              as bool,
      lastRun: freezed == lastRun
          ? _value.lastRun
          : lastRun // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      nextRun: freezed == nextRun
          ? _value.nextRun
          : nextRun // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      recipientEmails: null == recipientEmails
          ? _value._recipientEmails
          : recipientEmails // ignore: cast_nullable_to_non_nullable
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
class _$ScheduledReportImpl implements _ScheduledReport {
  const _$ScheduledReportImpl(
      {required this.id,
      required this.userId,
      required this.name,
      required this.cronExpression,
      required this.enabled,
      this.lastRun,
      this.nextRun,
      required final List<String> recipientEmails,
      required this.createdAt})
      : _recipientEmails = recipientEmails;

  factory _$ScheduledReportImpl.fromJson(Map<String, dynamic> json) =>
      _$$ScheduledReportImplFromJson(json);

  @override
  final int id;
  @override
  final int userId;
  @override
  final String name;
  @override
  final String cronExpression;
  @override
  final bool enabled;
  @override
  final DateTime? lastRun;
  @override
  final DateTime? nextRun;
  final List<String> _recipientEmails;
  @override
  List<String> get recipientEmails {
    if (_recipientEmails is EqualUnmodifiableListView) return _recipientEmails;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_recipientEmails);
  }

  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'ScheduledReport(id: $id, userId: $userId, name: $name, cronExpression: $cronExpression, enabled: $enabled, lastRun: $lastRun, nextRun: $nextRun, recipientEmails: $recipientEmails, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$ScheduledReportImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.cronExpression, cronExpression) ||
                other.cronExpression == cronExpression) &&
            (identical(other.enabled, enabled) || other.enabled == enabled) &&
            (identical(other.lastRun, lastRun) || other.lastRun == lastRun) &&
            (identical(other.nextRun, nextRun) || other.nextRun == nextRun) &&
            const DeepCollectionEquality()
                .equals(other._recipientEmails, _recipientEmails) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      userId,
      name,
      cronExpression,
      enabled,
      lastRun,
      nextRun,
      const DeepCollectionEquality().hash(_recipientEmails),
      createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$ScheduledReportImplCopyWith<_$ScheduledReportImpl> get copyWith =>
      __$$ScheduledReportImplCopyWithImpl<_$ScheduledReportImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$ScheduledReportImplToJson(
      this,
    );
  }
}

abstract class _ScheduledReport implements ScheduledReport {
  const factory _ScheduledReport(
      {required final int id,
      required final int userId,
      required final String name,
      required final String cronExpression,
      required final bool enabled,
      final DateTime? lastRun,
      final DateTime? nextRun,
      required final List<String> recipientEmails,
      required final DateTime createdAt}) = _$ScheduledReportImpl;

  factory _ScheduledReport.fromJson(Map<String, dynamic> json) =
      _$ScheduledReportImpl.fromJson;

  @override
  int get id;
  @override
  int get userId;
  @override
  String get name;
  @override
  String get cronExpression;
  @override
  bool get enabled;
  @override
  DateTime? get lastRun;
  @override
  DateTime? get nextRun;
  @override
  List<String> get recipientEmails;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$ScheduledReportImplCopyWith<_$ScheduledReportImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

ExportJob _$ExportJobFromJson(Map<String, dynamic> json) {
  return _ExportJob.fromJson(json);
}

/// @nodoc
mixin _$ExportJob {
  int get id => throw _privateConstructorUsedError;
  int get userId => throw _privateConstructorUsedError;
  String get exportType => throw _privateConstructorUsedError;
  String get format => throw _privateConstructorUsedError;
  String get status => throw _privateConstructorUsedError;
  int get progress => throw _privateConstructorUsedError;
  int get recordCount => throw _privateConstructorUsedError;
  DateTime? get startedAt => throw _privateConstructorUsedError;
  DateTime? get completedAt => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $ExportJobCopyWith<ExportJob> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $ExportJobCopyWith<$Res> {
  factory $ExportJobCopyWith(ExportJob value, $Res Function(ExportJob) then) =
      _$ExportJobCopyWithImpl<$Res, ExportJob>;
  @useResult
  $Res call(
      {int id,
      int userId,
      String exportType,
      String format,
      String status,
      int progress,
      int recordCount,
      DateTime? startedAt,
      DateTime? completedAt,
      DateTime createdAt});
}

/// @nodoc
class _$ExportJobCopyWithImpl<$Res, $Val extends ExportJob>
    implements $ExportJobCopyWith<$Res> {
  _$ExportJobCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? exportType = null,
    Object? format = null,
    Object? status = null,
    Object? progress = null,
    Object? recordCount = null,
    Object? startedAt = freezed,
    Object? completedAt = freezed,
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
      exportType: null == exportType
          ? _value.exportType
          : exportType // ignore: cast_nullable_to_non_nullable
              as String,
      format: null == format
          ? _value.format
          : format // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      progress: null == progress
          ? _value.progress
          : progress // ignore: cast_nullable_to_non_nullable
              as int,
      recordCount: null == recordCount
          ? _value.recordCount
          : recordCount // ignore: cast_nullable_to_non_nullable
              as int,
      startedAt: freezed == startedAt
          ? _value.startedAt
          : startedAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      completedAt: freezed == completedAt
          ? _value.completedAt
          : completedAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$ExportJobImplCopyWith<$Res>
    implements $ExportJobCopyWith<$Res> {
  factory _$$ExportJobImplCopyWith(
          _$ExportJobImpl value, $Res Function(_$ExportJobImpl) then) =
      __$$ExportJobImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      int userId,
      String exportType,
      String format,
      String status,
      int progress,
      int recordCount,
      DateTime? startedAt,
      DateTime? completedAt,
      DateTime createdAt});
}

/// @nodoc
class __$$ExportJobImplCopyWithImpl<$Res>
    extends _$ExportJobCopyWithImpl<$Res, _$ExportJobImpl>
    implements _$$ExportJobImplCopyWith<$Res> {
  __$$ExportJobImplCopyWithImpl(
      _$ExportJobImpl _value, $Res Function(_$ExportJobImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? exportType = null,
    Object? format = null,
    Object? status = null,
    Object? progress = null,
    Object? recordCount = null,
    Object? startedAt = freezed,
    Object? completedAt = freezed,
    Object? createdAt = null,
  }) {
    return _then(_$ExportJobImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      userId: null == userId
          ? _value.userId
          : userId // ignore: cast_nullable_to_non_nullable
              as int,
      exportType: null == exportType
          ? _value.exportType
          : exportType // ignore: cast_nullable_to_non_nullable
              as String,
      format: null == format
          ? _value.format
          : format // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      progress: null == progress
          ? _value.progress
          : progress // ignore: cast_nullable_to_non_nullable
              as int,
      recordCount: null == recordCount
          ? _value.recordCount
          : recordCount // ignore: cast_nullable_to_non_nullable
              as int,
      startedAt: freezed == startedAt
          ? _value.startedAt
          : startedAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      completedAt: freezed == completedAt
          ? _value.completedAt
          : completedAt // ignore: cast_nullable_to_non_nullable
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
class _$ExportJobImpl implements _ExportJob {
  const _$ExportJobImpl(
      {required this.id,
      required this.userId,
      required this.exportType,
      required this.format,
      required this.status,
      required this.progress,
      required this.recordCount,
      this.startedAt,
      this.completedAt,
      required this.createdAt});

  factory _$ExportJobImpl.fromJson(Map<String, dynamic> json) =>
      _$$ExportJobImplFromJson(json);

  @override
  final int id;
  @override
  final int userId;
  @override
  final String exportType;
  @override
  final String format;
  @override
  final String status;
  @override
  final int progress;
  @override
  final int recordCount;
  @override
  final DateTime? startedAt;
  @override
  final DateTime? completedAt;
  @override
  final DateTime createdAt;

  @override
  String toString() {
    return 'ExportJob(id: $id, userId: $userId, exportType: $exportType, format: $format, status: $status, progress: $progress, recordCount: $recordCount, startedAt: $startedAt, completedAt: $completedAt, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$ExportJobImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.exportType, exportType) ||
                other.exportType == exportType) &&
            (identical(other.format, format) || other.format == format) &&
            (identical(other.status, status) || other.status == status) &&
            (identical(other.progress, progress) ||
                other.progress == progress) &&
            (identical(other.recordCount, recordCount) ||
                other.recordCount == recordCount) &&
            (identical(other.startedAt, startedAt) ||
                other.startedAt == startedAt) &&
            (identical(other.completedAt, completedAt) ||
                other.completedAt == completedAt) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, id, userId, exportType, format,
      status, progress, recordCount, startedAt, completedAt, createdAt);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$ExportJobImplCopyWith<_$ExportJobImpl> get copyWith =>
      __$$ExportJobImplCopyWithImpl<_$ExportJobImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$ExportJobImplToJson(
      this,
    );
  }
}

abstract class _ExportJob implements ExportJob {
  const factory _ExportJob(
      {required final int id,
      required final int userId,
      required final String exportType,
      required final String format,
      required final String status,
      required final int progress,
      required final int recordCount,
      final DateTime? startedAt,
      final DateTime? completedAt,
      required final DateTime createdAt}) = _$ExportJobImpl;

  factory _ExportJob.fromJson(Map<String, dynamic> json) =
      _$ExportJobImpl.fromJson;

  @override
  int get id;
  @override
  int get userId;
  @override
  String get exportType;
  @override
  String get format;
  @override
  String get status;
  @override
  int get progress;
  @override
  int get recordCount;
  @override
  DateTime? get startedAt;
  @override
  DateTime? get completedAt;
  @override
  DateTime get createdAt;
  @override
  @JsonKey(ignore: true)
  _$$ExportJobImplCopyWith<_$ExportJobImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

SecurityStats _$SecurityStatsFromJson(Map<String, dynamic> json) {
  return _SecurityStats.fromJson(json);
}

/// @nodoc
mixin _$SecurityStats {
  int get totalAuditLogs => throw _privateConstructorUsedError;
  int get moderationItemsPending => throw _privateConstructorUsedError;
  int get recentThrottles => throw _privateConstructorUsedError;
  int get unreadNotifications => throw _privateConstructorUsedError;
  int get activeAlerts => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $SecurityStatsCopyWith<SecurityStats> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $SecurityStatsCopyWith<$Res> {
  factory $SecurityStatsCopyWith(
          SecurityStats value, $Res Function(SecurityStats) then) =
      _$SecurityStatsCopyWithImpl<$Res, SecurityStats>;
  @useResult
  $Res call(
      {int totalAuditLogs,
      int moderationItemsPending,
      int recentThrottles,
      int unreadNotifications,
      int activeAlerts});
}

/// @nodoc
class _$SecurityStatsCopyWithImpl<$Res, $Val extends SecurityStats>
    implements $SecurityStatsCopyWith<$Res> {
  _$SecurityStatsCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? totalAuditLogs = null,
    Object? moderationItemsPending = null,
    Object? recentThrottles = null,
    Object? unreadNotifications = null,
    Object? activeAlerts = null,
  }) {
    return _then(_value.copyWith(
      totalAuditLogs: null == totalAuditLogs
          ? _value.totalAuditLogs
          : totalAuditLogs // ignore: cast_nullable_to_non_nullable
              as int,
      moderationItemsPending: null == moderationItemsPending
          ? _value.moderationItemsPending
          : moderationItemsPending // ignore: cast_nullable_to_non_nullable
              as int,
      recentThrottles: null == recentThrottles
          ? _value.recentThrottles
          : recentThrottles // ignore: cast_nullable_to_non_nullable
              as int,
      unreadNotifications: null == unreadNotifications
          ? _value.unreadNotifications
          : unreadNotifications // ignore: cast_nullable_to_non_nullable
              as int,
      activeAlerts: null == activeAlerts
          ? _value.activeAlerts
          : activeAlerts // ignore: cast_nullable_to_non_nullable
              as int,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$SecurityStatsImplCopyWith<$Res>
    implements $SecurityStatsCopyWith<$Res> {
  factory _$$SecurityStatsImplCopyWith(
          _$SecurityStatsImpl value, $Res Function(_$SecurityStatsImpl) then) =
      __$$SecurityStatsImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int totalAuditLogs,
      int moderationItemsPending,
      int recentThrottles,
      int unreadNotifications,
      int activeAlerts});
}

/// @nodoc
class __$$SecurityStatsImplCopyWithImpl<$Res>
    extends _$SecurityStatsCopyWithImpl<$Res, _$SecurityStatsImpl>
    implements _$$SecurityStatsImplCopyWith<$Res> {
  __$$SecurityStatsImplCopyWithImpl(
      _$SecurityStatsImpl _value, $Res Function(_$SecurityStatsImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? totalAuditLogs = null,
    Object? moderationItemsPending = null,
    Object? recentThrottles = null,
    Object? unreadNotifications = null,
    Object? activeAlerts = null,
  }) {
    return _then(_$SecurityStatsImpl(
      totalAuditLogs: null == totalAuditLogs
          ? _value.totalAuditLogs
          : totalAuditLogs // ignore: cast_nullable_to_non_nullable
              as int,
      moderationItemsPending: null == moderationItemsPending
          ? _value.moderationItemsPending
          : moderationItemsPending // ignore: cast_nullable_to_non_nullable
              as int,
      recentThrottles: null == recentThrottles
          ? _value.recentThrottles
          : recentThrottles // ignore: cast_nullable_to_non_nullable
              as int,
      unreadNotifications: null == unreadNotifications
          ? _value.unreadNotifications
          : unreadNotifications // ignore: cast_nullable_to_non_nullable
              as int,
      activeAlerts: null == activeAlerts
          ? _value.activeAlerts
          : activeAlerts // ignore: cast_nullable_to_non_nullable
              as int,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$SecurityStatsImpl implements _SecurityStats {
  const _$SecurityStatsImpl(
      {required this.totalAuditLogs,
      required this.moderationItemsPending,
      required this.recentThrottles,
      required this.unreadNotifications,
      required this.activeAlerts});

  factory _$SecurityStatsImpl.fromJson(Map<String, dynamic> json) =>
      _$$SecurityStatsImplFromJson(json);

  @override
  final int totalAuditLogs;
  @override
  final int moderationItemsPending;
  @override
  final int recentThrottles;
  @override
  final int unreadNotifications;
  @override
  final int activeAlerts;

  @override
  String toString() {
    return 'SecurityStats(totalAuditLogs: $totalAuditLogs, moderationItemsPending: $moderationItemsPending, recentThrottles: $recentThrottles, unreadNotifications: $unreadNotifications, activeAlerts: $activeAlerts)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$SecurityStatsImpl &&
            (identical(other.totalAuditLogs, totalAuditLogs) ||
                other.totalAuditLogs == totalAuditLogs) &&
            (identical(other.moderationItemsPending, moderationItemsPending) ||
                other.moderationItemsPending == moderationItemsPending) &&
            (identical(other.recentThrottles, recentThrottles) ||
                other.recentThrottles == recentThrottles) &&
            (identical(other.unreadNotifications, unreadNotifications) ||
                other.unreadNotifications == unreadNotifications) &&
            (identical(other.activeAlerts, activeAlerts) ||
                other.activeAlerts == activeAlerts));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      totalAuditLogs,
      moderationItemsPending,
      recentThrottles,
      unreadNotifications,
      activeAlerts);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$SecurityStatsImplCopyWith<_$SecurityStatsImpl> get copyWith =>
      __$$SecurityStatsImplCopyWithImpl<_$SecurityStatsImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$SecurityStatsImplToJson(
      this,
    );
  }
}

abstract class _SecurityStats implements SecurityStats {
  const factory _SecurityStats(
      {required final int totalAuditLogs,
      required final int moderationItemsPending,
      required final int recentThrottles,
      required final int unreadNotifications,
      required final int activeAlerts}) = _$SecurityStatsImpl;

  factory _SecurityStats.fromJson(Map<String, dynamic> json) =
      _$SecurityStatsImpl.fromJson;

  @override
  int get totalAuditLogs;
  @override
  int get moderationItemsPending;
  @override
  int get recentThrottles;
  @override
  int get unreadNotifications;
  @override
  int get activeAlerts;
  @override
  @JsonKey(ignore: true)
  _$$SecurityStatsImplCopyWith<_$SecurityStatsImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

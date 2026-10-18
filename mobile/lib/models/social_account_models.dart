// Messages, followers, notifications, privacy settings and premium status for the signed-in user.

class DirectMessage {
  final int id;
  final int senderId;
  final String content;
  final bool isRead;

  const DirectMessage({required this.id, required this.senderId, required this.content, required this.isRead});

  factory DirectMessage.fromJson(Map<String, dynamic> json) => DirectMessage(
        id: json['id'] as int,
        senderId: json['sender_id'] as int,
        content: json['content'] as String,
        isRead: json['is_read'] as bool? ?? false,
      );
}

class Follower {
  final int id;
  final int followerId;
  final int followingId;
  final String? followerName;
  final DateTime? followedAt;

  const Follower({
    required this.id,
    required this.followerId,
    required this.followingId,
    this.followerName,
    this.followedAt,
  });

  factory Follower.fromJson(Map<String, dynamic> json) => Follower(
        id: json['id'] as int,
        followerId: json['follower_id'] as int,
        followingId: json['following_id'] as int,
        followerName: json['follower_name'] as String?,
        followedAt: json['created_at'] is String ? DateTime.tryParse(json['created_at'] as String) : null,
      );
}

class AppNotification {
  final int id;
  final String title;
  final String message;
  final bool isRead;
  final DateTime? createdAt;

  const AppNotification({
    required this.id,
    required this.title,
    required this.message,
    required this.isRead,
    this.createdAt,
  });

  factory AppNotification.fromJson(Map<String, dynamic> json) => AppNotification(
        id: json['id'] as int,
        title: json['title'] as String,
        message: json['message'] as String,
        isRead: json['is_read'] as bool? ?? json['read'] as bool? ?? false,
        createdAt: json['created_at'] is String ? DateTime.tryParse(json['created_at'] as String) : null,
      );
}

class PrivacySettings {
  final String profileVisibility;
  final String contentVisibility;
  final bool allowAnalytics;
  final bool allowMarketing;

  const PrivacySettings({
    required this.profileVisibility,
    required this.contentVisibility,
    required this.allowAnalytics,
    required this.allowMarketing,
  });

  factory PrivacySettings.fromJson(Map<String, dynamic> json) => PrivacySettings(
        profileVisibility: json['profile_visibility'] as String,
        contentVisibility: json['content_visibility'] as String,
        allowAnalytics: json['allow_analytics'] as bool,
        allowMarketing: json['allow_marketing'] as bool,
      );
}

class ConsentEntry {
  final int id;
  final String consentType;
  final bool granted;
  final String? version;

  const ConsentEntry({required this.id, required this.consentType, required this.granted, this.version});

  factory ConsentEntry.fromJson(Map<String, dynamic> json) => ConsentEntry(
        id: json['id'] as int,
        consentType: json['consent_type'] as String,
        granted: json['granted'] as bool,
        version: json['version'] as String?,
      );
}

class PremiumStatus {
  final bool isPremium;
  final List<String> features;

  const PremiumStatus({required this.isPremium, this.features = const []});

  factory PremiumStatus.fromJson(Map<String, dynamic> json) => PremiumStatus(
        isPremium: json['is_premium'] as bool,
        features: (json['features'] as List<dynamic>?)?.cast<String>() ?? const [],
      );
}

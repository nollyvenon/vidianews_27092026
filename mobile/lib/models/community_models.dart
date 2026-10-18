// Comments, push devices and notification logs, and outbound webhooks for the signed-in user.

class ContentComment {
  final int id;
  final int userId;
  final int contentId;
  final String text;
  final String status;
  final DateTime? createdAt;

  const ContentComment({
    required this.id,
    required this.userId,
    required this.contentId,
    required this.text,
    required this.status,
    this.createdAt,
  });

  factory ContentComment.fromJson(Map<String, dynamic> json) => ContentComment(
        id: json['id'] as int,
        userId: json['user_id'] as int,
        contentId: json['content_id'] as int,
        text: json['text'] as String,
        status: json['status'] as String? ?? 'published',
        createdAt: json['created_at'] is String ? DateTime.tryParse(json['created_at'] as String) : null,
      );
}

class PushDevice {
  final int id;
  final String deviceToken;
  final String platform;
  final String? deviceName;
  final DateTime? lastActive;

  const PushDevice({
    required this.id,
    required this.deviceToken,
    required this.platform,
    this.deviceName,
    this.lastActive,
  });

  factory PushDevice.fromJson(Map<String, dynamic> json) => PushDevice(
        id: json['id'] as int,
        deviceToken: json['device_token'] as String,
        platform: json['platform'] as String,
        deviceName: json['device_name'] as String?,
        lastActive: json['last_active'] is String ? DateTime.tryParse(json['last_active'] as String) : null,
      );
}

class NotificationLog {
  final int id;
  final String notificationType;
  final String title;
  final String body;
  final String status;
  final DateTime? createdAt;

  const NotificationLog({
    required this.id,
    required this.notificationType,
    required this.title,
    required this.body,
    required this.status,
    this.createdAt,
  });

  factory NotificationLog.fromJson(Map<String, dynamic> json) => NotificationLog(
        id: json['id'] as int,
        notificationType: json['notification_type'] as String,
        title: json['title'] as String,
        body: json['body'] as String? ?? '',
        status: json['status'] as String,
        createdAt: json['created_at'] is String ? DateTime.tryParse(json['created_at'] as String) : null,
      );
}

class OutboundWebhook {
  final int id;
  final String url;
  final String? description;
  final List<String> events;
  final bool isActive;

  const OutboundWebhook({
    required this.id,
    required this.url,
    this.description,
    required this.events,
    required this.isActive,
  });

  factory OutboundWebhook.fromJson(Map<String, dynamic> json) => OutboundWebhook(
        id: json['id'] as int,
        url: json['url'] as String,
        description: json['description'] as String?,
        events: (json['events'] as List<dynamic>? ?? const []).cast<String>(),
        isActive: json['is_active'] as bool? ?? true,
      );
}

class WebhookEventType {
  final String event;
  final String description;

  const WebhookEventType({required this.event, required this.description});

  factory WebhookEventType.fromJson(Map<String, dynamic> json) => WebhookEventType(
        event: json['event'] as String,
        description: json['description'] as String? ?? '',
      );
}

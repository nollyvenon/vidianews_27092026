// Creators, recommendations, trending topics, search results, video processing, live streams,
// partnerships and documentation.

class CreatorProfile {
  final int id;
  final int userId;
  final String? bio;
  final int followers;
  final bool isVerified;

  const CreatorProfile({
    required this.id,
    required this.userId,
    this.bio,
    required this.followers,
    required this.isVerified,
  });

  factory CreatorProfile.fromJson(Map<String, dynamic> json) => CreatorProfile(
        id: json['id'] as int,
        userId: json['user_id'] as int,
        bio: json['bio'] as String?,
        followers: json['followers'] as int? ?? 0,
        isVerified: json['is_verified'] as bool? ?? false,
      );
}

class Recommendation {
  final int id;
  final int contentId;
  final String title;
  final String? creator;
  final int views;
  final String? reason;

  const Recommendation({
    required this.id,
    required this.contentId,
    required this.title,
    this.creator,
    required this.views,
    this.reason,
  });

  factory Recommendation.fromJson(Map<String, dynamic> json) => Recommendation(
        id: json['id'] as int,
        contentId: json['content_id'] as int,
        title: json['title'] as String,
        creator: json['creator'] as String?,
        views: json['views'] as int? ?? 0,
        reason: json['reason'] as String?,
      );
}

class TrendingTopic {
  final int id;
  final String topic;
  final int mentionCount;

  const TrendingTopic({required this.id, required this.topic, required this.mentionCount});

  factory TrendingTopic.fromJson(Map<String, dynamic> json) => TrendingTopic(
        id: json['id'] as int,
        topic: json['topic'] as String,
        mentionCount: json['mention_count'] as int? ?? 0,
      );
}

class SearchResult {
  final int id;
  final String resourceType;
  final int resourceId;
  final String title;
  final String? content;

  const SearchResult({
    required this.id,
    required this.resourceType,
    required this.resourceId,
    required this.title,
    this.content,
  });

  factory SearchResult.fromJson(Map<String, dynamic> json) => SearchResult(
        id: json['id'] as int,
        resourceType: json['resource_type'] as String,
        resourceId: json['resource_id'] as int,
        title: json['title'] as String,
        content: json['content'] as String?,
      );
}

class VideoJob {
  final int contentId;
  final String title;
  final String status;
  final int progress;

  const VideoJob({required this.contentId, required this.title, required this.status, required this.progress});

  factory VideoJob.fromJson(Map<String, dynamic> json) => VideoJob(
        contentId: json['content_id'] as int,
        title: json['title'] as String,
        status: json['status'] as String,
        progress: (json['progress'] as num?)?.round() ?? 0,
      );
}

class ActiveStream {
  final int id;
  final String title;
  final int viewers;

  const ActiveStream({required this.id, required this.title, required this.viewers});

  factory ActiveStream.fromJson(Map<String, dynamic> json) => ActiveStream(
        id: json['id'] as int,
        title: json['title'] as String,
        viewers: json['viewers'] as int? ?? 0,
      );
}

class Partnership {
  final int id;
  final String type;
  final String status;

  const Partnership({required this.id, required this.type, required this.status});

  factory Partnership.fromJson(Map<String, dynamic> json) => Partnership(
        id: json['id'] as int,
        type: json['type'] as String,
        status: json['status'] as String,
      );
}

class Doc {
  final int id;
  final String title;
  final String slug;
  final String docType;
  final int views;
  final String version;

  const Doc({
    required this.id,
    required this.title,
    required this.slug,
    required this.docType,
    required this.views,
    required this.version,
  });

  factory Doc.fromJson(Map<String, dynamic> json) => Doc(
        id: json['id'] as int,
        title: json['title'] as String,
        slug: json['slug'] as String,
        docType: json['doc_type'] as String,
        views: json['views'] as int? ?? 0,
        version: json['version'] as String? ?? '',
      );
}

class ApiReference {
  final int id;
  final String method;
  final String endpoint;

  const ApiReference({required this.id, required this.method, required this.endpoint});

  factory ApiReference.fromJson(Map<String, dynamic> json) => ApiReference(
        id: json['id'] as int,
        method: json['method'] as String,
        endpoint: json['endpoint'] as String,
      );
}

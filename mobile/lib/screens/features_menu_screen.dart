// Every feature screen in the app, grouped by area, so each one can be opened from the home screen.

import 'package:flutter/material.dart';
import 'package:aether_cms/screens/activity/activity_screen.dart';
import 'package:aether_cms/screens/admin/admin_screen.dart';
import 'package:aether_cms/screens/advanced_features/ab_testing_screen.dart';
import 'package:aether_cms/screens/advanced_features/cohorts_screen.dart';
import 'package:aether_cms/screens/advanced_features/insights_screen.dart';
import 'package:aether_cms/screens/advanced_features/predictions_screen.dart';
import 'package:aether_cms/screens/advanced_features/recommendations_screen.dart' as advanced_recommendations;
import 'package:aether_cms/screens/advanced_features/retention_screen.dart';
import 'package:aether_cms/screens/advanced_platform/api_docs_screen.dart';
import 'package:aether_cms/screens/advanced_platform/jobs_screen.dart';
import 'package:aether_cms/screens/advanced_platform/performance_screen.dart';
import 'package:aether_cms/screens/advanced_platform/pipelines_screen.dart';
import 'package:aether_cms/screens/ai/monitoring_screen.dart' as ai_monitoring;
import 'package:aether_cms/screens/alerts_screen.dart';
import 'package:aether_cms/screens/analytics/analytics_main_screen.dart';
import 'package:aether_cms/screens/analytics/analytics_screen.dart' as analytics_detail;
import 'package:aether_cms/screens/analytics/behavior_tracking_screen.dart';
import 'package:aether_cms/screens/analytics/search_analytics_screen.dart';
import 'package:aether_cms/screens/analytics/system_health_screen.dart';
import 'package:aether_cms/screens/analytics_dashboard_screen.dart';
import 'package:aether_cms/screens/analytics_screen.dart' as analytics_overview;
import 'package:aether_cms/screens/api_versions_screen.dart';
import 'package:aether_cms/screens/audit_screen.dart';
import 'package:aether_cms/screens/billing_screen.dart';
import 'package:aether_cms/screens/cache_screen.dart';
import 'package:aether_cms/screens/community_screen.dart';
import 'package:aether_cms/screens/compliance_screen.dart';
import 'package:aether_cms/screens/comments_screen.dart';
import 'package:aether_cms/screens/content/content_list_screen.dart';
import 'package:aether_cms/screens/content_quality/brand_voice_screen.dart';
import 'package:aether_cms/screens/content_quality/calendar_screen.dart';
import 'package:aether_cms/screens/content_quality/content_quality_screen.dart';
import 'package:aether_cms/screens/content_quality/plagiarism_screen.dart';
import 'package:aether_cms/screens/content_quality/proofreading_screen.dart';
import 'package:aether_cms/screens/content_quality/readability_screen.dart';
import 'package:aether_cms/screens/creator_screen.dart';
import 'package:aether_cms/screens/discover_screen.dart';
import 'package:aether_cms/screens/docs_screen.dart';
import 'package:aether_cms/screens/ecommerce/addresses_screen.dart';
import 'package:aether_cms/screens/ecommerce/order_tracking_screen.dart';
import 'package:aether_cms/screens/ecommerce/products_screen.dart';
import 'package:aether_cms/screens/ecommerce/wishlists_screen.dart';
import 'package:aether_cms/screens/enterprise_features/moderation_screen.dart' as enterprise_moderation;
import 'package:aether_cms/screens/enterprise_features/reports_screen.dart' as enterprise_reports;
import 'package:aether_cms/screens/enterprise_features/security_screen.dart' as enterprise_security;
import 'package:aether_cms/screens/errors_screen.dart';
import 'package:aether_cms/screens/features_screen.dart';
import 'package:aether_cms/screens/followers_screen.dart';
import 'package:aether_cms/screens/gamification_screen.dart';
import 'package:aether_cms/screens/graphql_screen.dart';
import 'package:aether_cms/screens/integrations_screen.dart';
import 'package:aether_cms/screens/invoices_screen.dart';
import 'package:aether_cms/screens/livestream_screen.dart';
import 'package:aether_cms/screens/localization_screen.dart';
import 'package:aether_cms/screens/logs_screen.dart';
import 'package:aether_cms/screens/marketplace_screen.dart';
import 'package:aether_cms/screens/memberships/memberships_screen.dart';
import 'package:aether_cms/screens/messages_screen.dart';
import 'package:aether_cms/screens/moderation_screen.dart' as moderation;
import 'package:aether_cms/screens/monitoring_screen.dart';
import 'package:aether_cms/screens/notifications_center_screen.dart';
import 'package:aether_cms/screens/partnerships_screen.dart';
import 'package:aether_cms/screens/premium_screen.dart';
import 'package:aether_cms/screens/privacy_screen.dart';
import 'package:aether_cms/screens/publishing_distribution/publishing_distribution_screen.dart';
import 'package:aether_cms/screens/push_notifications_screen.dart';
import 'package:aether_cms/screens/quota_screen.dart';
import 'package:aether_cms/widgets/current_user_builder.dart';
import 'package:aether_cms/screens/realtime_screen.dart';
import 'package:aether_cms/screens/recommendations_screen.dart' as discover_recommendations;
import 'package:aether_cms/screens/reports_screen.dart' as reports;
import 'package:aether_cms/screens/search_screen.dart';
import 'package:aether_cms/screens/security_screen.dart' as security;
import 'package:aether_cms/screens/settings/settings_screen.dart';
import 'package:aether_cms/screens/subscriptions_screen.dart';
import 'package:aether_cms/screens/testing_screen.dart';
import 'package:aether_cms/screens/user_management/campaigns_screen.dart';
import 'package:aether_cms/screens/user_management/preferences_screen.dart';
import 'package:aether_cms/screens/user_management/segments_screen.dart';
import 'package:aether_cms/screens/user_management/subscriber_screen.dart';
import 'package:aether_cms/screens/user_management/user_management_screen.dart';
import 'package:aether_cms/screens/video_processing_screen.dart';
import 'package:aether_cms/screens/webhooks_screen.dart';

class _Feature {
  final String title;
  final String subtitle;
  final WidgetBuilder builder;

  const _Feature(this.title, this.subtitle, this.builder);
}

class _Section {
  final String heading;
  final List<_Feature> features;

  const _Section(this.heading, this.features);
}

final List<_Section> _sections = [
  _Section('Account & social', [
    _Feature('Activity', 'Your recent actions', (_) => ActivityScreen()),
    _Feature('Alerts', 'Notifications addressed to you', (_) => AlertsScreen()),
    _Feature('Notifications', 'Notices from the platform', (_) => NotificationsCenterScreen()),
    _Feature('Push notifications', 'Delivery of push messages', (_) => PushNotificationsScreen()),
    _Feature('Followers', 'People who follow you', (_) => CurrentUserBuilder(builder: (context, userId) => FollowersScreen(userId: userId))),
    _Feature('Messages', 'Your conversations', (_) => CurrentUserBuilder(builder: (context, userId) => MessagesScreen(currentUserId: userId))),
    _Feature('Community', 'Discussions and groups', (_) => CommunityScreen()),
    _Feature('Privacy', 'Consents and your data', (_) => PrivacyScreen()),
    _Feature('Premium', 'Plans and benefits', (_) => PremiumScreen()),
    _Feature('Subscriptions', 'Your subscriptions', (_) => SubscriptionsScreen()),
    _Feature('Invoices', 'Invoices and payments', (_) => InvoicesScreen()),
    _Feature('Billing', 'Plan and billing details', (_) => BillingScreen()),
    _Feature('Usage & quotas', 'Your API usage against limits', (_) => QuotaScreen()),
    _Feature('Memberships', 'Membership programmes', (_) => MembershipsScreen()),
    _Feature('Settings', 'Account settings', (_) => SettingsScreen()),
  ]),
  _Section('Shop', [
    _Feature('Products', 'Browse the catalogue', (_) => ProductsScreen()),
    _Feature('Wishlists', 'Saved products', (_) => WishlistsScreen()),
    _Feature('Shipping addresses', 'Where your orders go', (_) => AddressesScreen()),
    _Feature('Order tracking', 'Shipments and returns', (_) => OrderTrackingScreen()),
  ]),
  _Section('Content & AI', [
    _Feature('Content', 'Videos and articles', (_) => ContentListScreen()),
    _Feature('Comments', 'Discussion on a piece of content', (_) => CommentsLookupScreen()),
    _Feature('Creator', 'Your creator profile', (_) => CreatorScreen()),
    _Feature('Discover', 'Trending and recommended', (_) => DiscoverScreen()),
    _Feature('Recommendations', 'Suggested content', (_) => discover_recommendations.RecommendationsScreen()),
    _Feature('Search', 'Find content', (_) => SearchScreen()),
    _Feature('Video processing', 'Encoding status', (_) => VideoProcessingScreen()),
    _Feature('Livestream', 'Live broadcasts', (_) => LivestreamScreen()),
    _Feature('Marketplace', 'Listings', (_) => MarketplaceScreen()),
    _Feature('Partnerships', 'Partner programmes', (_) => PartnershipsScreen()),
    _Feature('Gamification', 'Points and badges', (_) => GamificationScreen()),
    _Feature('Localization', 'Languages and translations', (_) => LocalizationScreen()),
    _Feature('Docs', 'Documentation', (_) => DocsScreen()),
    _Feature('GraphQL', 'Query the API', (_) => GraphQLScreen()),
    _Feature('Content quality', 'Quality scores', (_) => ContentQualityScreen()),
    _Feature('Brand voice', 'Tone checks', (_) => BrandVoiceScreen()),
    _Feature('Content calendar', 'Publishing schedule', (_) => ContentCalendarScreen()),
    _Feature('Plagiarism', 'Originality checks', (_) => PlagiarismScreen()),
    _Feature('Proofreading', 'Grammar and spelling', (_) => ProofreadingScreen()),
    _Feature('Readability', 'Reading level', (_) => ReadabilityScreen()),
    _Feature('Publishing & distribution', 'Channels and schedules', (_) => PublishingDistributionScreen()),
  ]),
  _Section('Analytics & reports', [
    _Feature('Analytics', 'Metrics overview', (_) => AnalyticsMainScreen()),
    _Feature('Analytics dashboard', 'Revenue and engagement', (_) => AnalyticsDashboardScreen()),
    _Feature('Analytics summary', 'Views and subscribers', (_) => analytics_overview.AnalyticsScreen()),
    _Feature('Analytics detail', 'Detailed analytics', (_) => analytics_detail.AnalyticsScreen()),
    _Feature('Behaviour tracking', 'How people use the app', (_) => BehaviorTrackingScreen()),
    _Feature('Search analytics', 'What people search for', (_) => SearchAnalyticsScreen()),
    _Feature('System health', 'Platform health', (_) => SystemHealthScreen()),
    _Feature('Reports', 'Your reports', (_) => reports.ReportsScreen()),
    _Feature('Report center', 'Scheduled and exported reports', (_) => CurrentUserBuilder(builder: (context, userId) => enterprise_reports.ReportsScreen(userId: userId))),
  ]),
  _Section('Advanced features', [
    _Feature('A/B testing', 'Experiments', (_) => ABTestingScreen()),
    _Feature('Cohorts', 'Retention groups', (_) => CohortsScreen()),
    _Feature('Insights', 'Automated insights', (_) => InsightsScreen()),
    _Feature('Predictions', 'Forecasts', (_) => PredictionsScreen()),
    _Feature('Advanced recommendations', 'Personalised suggestions', (_) => advanced_recommendations.RecommendationsScreen()),
    _Feature('Retention', 'Returning users', (_) => RetentionScreen()),
    _Feature('Features', 'Feature flags', (_) => FeaturesScreen()),
    _Feature('Integrations', 'Connected services', (_) => IntegrationsScreen()),
    _Feature('Webhooks', 'Outbound webhooks', (_) => WebhooksScreen()),
    _Feature('Testing', 'Test suites', (_) => TestingScreen()),
    _Feature('Realtime', 'Live events and presence', (_) => RealtimeScreen()),
    _Feature('Jobs', 'Background jobs', (_) => JobsScreen()),
    _Feature('Performance', 'Response times', (_) => PerformanceScreen()),
    _Feature('Data pipelines', 'Pipelines and their runs', (_) => PipelinesScreen()),
    _Feature('API usage', 'Endpoint usage', (_) => APIDocsScreen()),
    _Feature('API versions', 'Endpoint versions', (_) => APIVersionsScreen()),
    _Feature('Cache', 'Cache performance', (_) => CacheScreen()),
    _Feature('Logs', 'Activity logs', (_) => LogsScreen()),
    _Feature('Errors', 'Unresolved errors', (_) => ErrorsScreen()),
    _Feature('Monitoring', 'Health checks and alerts', (_) => MonitoringScreen()),
    _Feature('AI monitoring', 'Assistant health', (_) => ai_monitoring.MonitoringScreen()),
    _Feature('Audit', 'Audit trail', (_) => AuditScreen()),
  ]),
  _Section('Security & moderation', [
    _Feature('Security', 'Access and sign-in', (_) => security.SecurityScreen()),
    _Feature('Security controls', 'Rate limits and access', (_) => CurrentUserBuilder(builder: (context, userId) => enterprise_security.SecurityScreen(userId: userId))),
    _Feature('Moderation', 'Review queue', (_) => moderation.ModerationScreen()),
    _Feature('Moderation controls', 'Compliance and review', (_) => enterprise_moderation.ModerationScreen()),
    _Feature('Compliance', 'Rules and checks', (_) => ComplianceScreen()),
  ]),
  _Section('Users & administration', [
    _Feature('User management', 'Users and API keys', (_) => UserManagementScreen()),
    _Feature('Campaigns', 'Email campaigns', (_) => CampaignsScreen()),
    _Feature('Segments', 'Audience segments', (_) => SegmentsScreen()),
    _Feature('Subscribers', 'Subscriber overview', (_) => SubscriberScreen()),
    _Feature('Preferences', 'Communication preferences', (_) => PreferencesScreen()),
    _Feature('Administration', 'Administrator tools', (_) => AdminScreen()),
  ]),
];

/// Every feature screen in the app, grouped by area.
class FeaturesMenuScreen extends StatelessWidget {
  const FeaturesMenuScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('All features')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          for (final section in _sections) ...[
            Padding(
              padding: const EdgeInsets.only(top: 12, bottom: 4),
              child: Text(section.heading, style: Theme.of(context).textTheme.titleMedium),
            ),
            for (final feature in section.features)
              ListTile(
                key: Key('feature-${feature.title}'),
                contentPadding: EdgeInsets.zero,
                title: Text(feature.title),
                subtitle: Text(feature.subtitle),
                trailing: const Icon(Icons.chevron_right),
                onTap: () => Navigator.of(context).push(MaterialPageRoute<void>(builder: feature.builder)),
              ),
          ],
        ],
      ),
    );
  }
}

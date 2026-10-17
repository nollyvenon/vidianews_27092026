// Social login models (provider list, admin configuration, token response).

class SocialProvider {
  final String provider;
  final String displayName;

  const SocialProvider({required this.provider, required this.displayName});

  factory SocialProvider.fromJson(Map<String, dynamic> json) => SocialProvider(
        provider: json['provider'] as String,
        displayName: json['display_name'] as String,
      );
}

class SocialProviderAdmin {
  final String provider;
  final String displayName;
  final bool enabled;
  final String? clientId;
  final bool clientSecretSet;
  final String? redirectUri;
  final String scopes;

  const SocialProviderAdmin({
    required this.provider,
    required this.displayName,
    required this.enabled,
    required this.clientId,
    required this.clientSecretSet,
    required this.redirectUri,
    required this.scopes,
  });

  factory SocialProviderAdmin.fromJson(Map<String, dynamic> json) => SocialProviderAdmin(
        provider: json['provider'] as String,
        displayName: json['display_name'] as String,
        enabled: json['enabled'] as bool,
        clientId: json['client_id'] as String?,
        clientSecretSet: json['client_secret_set'] as bool,
        redirectUri: json['redirect_uri'] as String?,
        scopes: (json['scopes'] as String?) ?? '',
      );
}

/// Body for PUT /admin/social-providers/{provider}. A null [clientSecret] keeps the stored secret.
class SocialProviderUpdate {
  final bool enabled;
  final String clientId;
  final String? clientSecret;
  final String redirectUri;
  final String scopes;

  const SocialProviderUpdate({
    required this.enabled,
    required this.clientId,
    this.clientSecret,
    required this.redirectUri,
    required this.scopes,
  });

  Map<String, dynamic> toJson() => {
        'enabled': enabled,
        'client_id': clientId,
        'redirect_uri': redirectUri,
        'scopes': scopes,
        if (clientSecret != null && clientSecret!.isNotEmpty) 'client_secret': clientSecret,
      };
}

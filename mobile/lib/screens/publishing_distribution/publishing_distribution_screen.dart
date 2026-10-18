// Publishing and distribution is an administration tool. It is used from the web dashboard, not the mobile app.

import 'package:flutter/material.dart';
import 'package:aether_cms/widgets/web_only_notice.dart';

class PublishingDistributionScreen extends StatelessWidget {
  const PublishingDistributionScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) => const WebOnlyNotice(title: 'Publishing and distribution');
}

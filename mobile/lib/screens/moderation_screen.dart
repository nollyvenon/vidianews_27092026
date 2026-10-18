// Moderation is an administration tool. It is used from the web dashboard, not the mobile app.

import 'package:flutter/material.dart';
import 'package:aether_cms/widgets/web_only_notice.dart';

class ModerationScreen extends StatelessWidget {
  const ModerationScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) => const WebOnlyNotice(title: 'Moderation');
}

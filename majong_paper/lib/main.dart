import 'package:flutter/material.dart';
import 'package:majong_paper/pages/top_page.dart';
import 'package:majong_paper/theme/app_theme.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '麻雀記録',
      theme: appTheme,
      home: const TopPage(),
    );
  }
}
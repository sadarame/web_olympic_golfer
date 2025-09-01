import 'package:flutter/material.dart';

class WoodBackground extends StatelessWidget {
  final Widget child;
  const WoodBackground({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    return Container(
      child: child,
    );
  }
}

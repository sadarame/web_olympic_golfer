import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

final appTheme = ThemeData(
  appBarTheme: const AppBarTheme(
    backgroundColor: Color(0xFF2E7D32), // Lighter Green
    foregroundColor: Color(0xFFFFFDE7), // Light Cream
  ),
  textTheme: GoogleFonts.yuseiMagicTextTheme().apply(
    bodyColor: const Color(0xFFFFFDE7),
    displayColor: const Color(0xFFFFFDE7),
  ),
  elevatedButtonTheme: ElevatedButtonThemeData(
    style: ElevatedButton.styleFrom(
      backgroundColor: const Color(0xFFC62828), // Dark Red
      foregroundColor: Colors.white,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(8),
      ),
    ),
  ),
  textButtonTheme: TextButtonThemeData(
    style: TextButton.styleFrom(
      foregroundColor: const Color(0xFFFFD700), // Gold
    ),
  ),
  bottomNavigationBarTheme: const BottomNavigationBarThemeData(
    backgroundColor: Color(0xFF2E7D32),
    selectedItemColor: Color(0xFFFFD700), // Gold
    unselectedItemColor: Color(0xFFFFFDE7),
  ),
  visualDensity: VisualDensity.adaptivePlatformDensity,
);

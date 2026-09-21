import 'package:flutter/material.dart';
import 'package:haven_mobile/screens/login_screen.dart';

void main() {
  runApp(const HavenApp());
}

class HavenApp extends StatelessWidget {
  const HavenApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'HAVEN',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFFff2e63),
          primary: const Color(0xFFff2e63),
          secondary: const Color(0xFF7c3aed),
          surface: const Color(0xFFFFF7FA),
        ),
        scaffoldBackgroundColor: const Color(0xFFFFF7FA),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFFff2e63),
          foregroundColor: Colors.white,
          elevation: 0,
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: const Color(0xFFff2e63),
            foregroundColor: Colors.white,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
          ),
        ),
      ),
      home: const LoginScreen(),
    );
  }
}

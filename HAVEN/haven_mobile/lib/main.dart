import 'package:flutter/material.dart';
import 'package:haven_mobile/screens/calculator_screen.dart';

void main() {
  runApp(HavenApp());
}

class HavenApp extends StatelessWidget {
  const HavenApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Calculator',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.grey,
      ),
      // Starts as a calculator
      home: CalculatorScreen(),
    );
  }
}

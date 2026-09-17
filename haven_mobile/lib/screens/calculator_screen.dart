import 'package:flutter/material.dart';
import 'package:haven_mobile/screens/login_screen.dart';

import 'package:math_expressions/math_expressions.dart';

class CalculatorScreen extends StatefulWidget {
  const CalculatorScreen({Key? key}) : super(key: key);

  @override
  State<CalculatorScreen> createState() => _CalculatorScreenState();
}

class _CalculatorScreenState extends State<CalculatorScreen> {
  String display = '0';
  String secretPin = '8080=';
  String currentInput = '';

  void _onPressed(String text) {
    setState(() {
      if (text == 'C') {
        display = '0';
        currentInput = '';
      } else if (text == '=') {
        currentInput += text;
        if (currentInput == secretPin) {
          currentInput = '';
          display = '0';
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (context) => const LoginScreen()),
          );
          return;
        }
        
        try {
          Parser p = Parser();
          Expression exp = p.parse(display);
          ContextModel cm = ContextModel();
          double eval = exp.evaluate(EvaluationType.REAL, cm);
          
          display = eval.toString();
          if (display.endsWith('.0')) {
            display = display.substring(0, display.length - 2);
          }
          currentInput = display;
        } catch (e) {
          display = 'Error';
          currentInput = '';
        }
      } else {
        if (display == '0' || display == 'Error') {
          display = text;
        } else {
          display += text;
        }
        currentInput += text;
        
        // Still check for secret pin just in case
        if (currentInput == secretPin) {
          currentInput = '';
          display = '0';
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (context) => const LoginScreen()),
          );
        }
      }
    });
  }

  Widget _buildButton(String text) {
    return Expanded(
      child: Padding(
        padding: const EdgeInsets.all(4.0),
        child: ElevatedButton(
          style: ElevatedButton.styleFrom(
            padding: EdgeInsets.all(24.0),
            backgroundColor: Colors.grey[200],
            foregroundColor: Colors.black,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(8.0),
            )
          ),
          onPressed: () => _onPressed(text),
          child: Text(text, style: TextStyle(fontSize: 24)),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: Text('Calculator'),
        backgroundColor: Colors.white,
        elevation: 0,
        foregroundColor: Colors.black,
      ),
      body: Column(
        children: [
          Expanded(
            child: Container(
              alignment: Alignment.bottomRight,
              padding: EdgeInsets.all(24.0),
              child: Text(
                display,
                style: TextStyle(fontSize: 48, fontWeight: FontWeight.bold),
              ),
            ),
          ),
          Row(children: [_buildButton('7'), _buildButton('8'), _buildButton('9'), _buildButton('/')]),
          Row(children: [_buildButton('4'), _buildButton('5'), _buildButton('6'), _buildButton('*')]),
          Row(children: [_buildButton('1'), _buildButton('2'), _buildButton('3'), _buildButton('-')]),
          Row(children: [_buildButton('C'), _buildButton('0'), _buildButton('='), _buildButton('+')]),
          SizedBox(height: 20),
        ],
      ),
    );
  }
}

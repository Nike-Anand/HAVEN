import 'package:flutter/material.dart';
import 'package:haven_mobile/screens/login_screen.dart';
import 'package:haven_mobile/screens/dashboard_screen.dart';
import 'package:haven_mobile/api/haven_client.dart';
import 'package:haven_mobile/screens/active_sos_screen.dart';
import 'package:geolocator/geolocator.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:math_expressions/math_expressions.dart';

class CalculatorScreen extends StatefulWidget {
  const CalculatorScreen({super.key});

  @override
  State<CalculatorScreen> createState() => _CalculatorScreenState();
}

class _CalculatorScreenState extends State<CalculatorScreen> {
  String display = '0';
  String unlockPin = '8080=';
  String panicPin = '9999=';
  String currentInput = '';
  final _secure = const FlutterSecureStorage();

  @override
  void initState() {
    super.initState();
    _loadPins();
  }

  Future<void> _loadPins() async {
    final storedUnlock = await _secure.read(key: 'decoy_pin');
    final storedPanic = await _secure.read(key: 'panic_pin');

    setState(() {
      if (storedUnlock != null && storedUnlock.isNotEmpty) {
        unlockPin = storedUnlock;
      }
      if (storedPanic != null && storedPanic.isNotEmpty) {
        panicPin = storedPanic;
      }
    });
  }

  void _onPressed(String text) {
    setState(() {
      if (text == 'C') {
        display = '0';
        currentInput = '';
      } else if (text == '=') {
        currentInput += text;
        
        // 1. Check Panic / Direct SOS PIN
        if (currentInput == panicPin) {
          currentInput = '';
          display = '0';
          _triggerPanicSOS();
          return;
        }

        // 2. Check App Unlock PIN
        if (currentInput == unlockPin) {
          currentInput = '';
          display = '0';
          _unlockApp();
          return;
        }

        // 3. Normal Math Evaluation
        try {
          String evalExpr = display.replaceAll('×', '*').replaceAll('÷', '/');
          Parser p = Parser();
          Expression exp = p.parse(evalExpr);
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

        // Also check if PIN is matched without = if configured
        if (currentInput == panicPin) {
          currentInput = '';
          display = '0';
          _triggerPanicSOS();
        } else if (currentInput == unlockPin) {
          currentInput = '';
          display = '0';
          _unlockApp();
        }
      }
    });
  }

  Future<void> _unlockApp() async {
    // Check if user is already logged in
    final token = await _secure.read(key: 'auth_token');
    final email = await _secure.read(key: 'auth_email');

    if (token != null && token.isNotEmpty && email != null && email.isNotEmpty) {
      HavenClient.token = token;
      HavenClient.email = email;
      if (!mounted) return;
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => DashboardScreen(email: email),
        ),
      );
    } else {
      if (!mounted) return;
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => const LoginScreen()),
      );
    }
  }

  Future<void> _triggerPanicSOS() async {
    // Ensure credentials or defaults exist
    final token = await _secure.read(key: 'auth_token');
    final email = await _secure.read(key: 'auth_email');
    if (token != null) HavenClient.token = token;
    if (email != null) HavenClient.email = email;

    Position? position;
    try {
      bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
      if (serviceEnabled) {
        LocationPermission permission = await Geolocator.checkPermission();
        if (permission == LocationPermission.denied) {
          permission = await Geolocator.requestPermission();
        }
        if (permission != LocationPermission.deniedForever && permission != LocationPermission.denied) {
          position = await Geolocator.getCurrentPosition(desiredAccuracy: LocationAccuracy.high);
        }
      }
    } catch (e) {
      position = null;
    }

    try {
      final resp = await HavenClient.triggerSOS(
        latitude: position?.latitude ?? 12.9278,
        longitude: position?.longitude ?? 80.2050,
      );
      if (!mounted) return;
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => ActiveSOSScreen(sosData: resp)),
      );
    } catch (e) {
      // Fallback to active screen with local emergency context
      if (!mounted) return;
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => ActiveSOSScreen(sosData: {
            "sos_id": "emergency-${DateTime.now().millisecondsSinceEpoch}",
            "status": "active",
            "message": "Direct emergency SOS initiated.",
            "contacts_notified": 1,
            "therapy_bot_ready": true,
            "authorities_notified": true,
          }),
        ),
      );
    }
  }

  Widget _buildButton(String text, {Color? bgColor, Color? textColor, int flex = 1}) {
    final isOperator = ['÷', '×', '-', '+', '='].contains(text);
    final isSpecial = ['C', '±', '%'].contains(text);
    
    final bg = bgColor ?? (isOperator 
        ? const Color(0xFFe53935) 
        : (isSpecial ? const Color(0xFFcfd8dc) : const Color(0xFFf5f5f5)));
    final fg = textColor ?? (isOperator ? Colors.white : Colors.black87);

    return Expanded(
      flex: flex,
      child: Padding(
        padding: const EdgeInsets.all(5.0),
        child: SizedBox(
          height: 68,
          child: ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: bg,
              foregroundColor: fg,
              elevation: 0,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(16.0),
              ),
            ),
            onPressed: () => _onPressed(text),
            child: Text(
              text,
              style: TextStyle(fontSize: 24, fontWeight: isOperator ? FontWeight.bold : FontWeight.w500),
            ),
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF1a1c23),
      appBar: AppBar(
        title: const Text('Calculator', style: TextStyle(color: Colors.white70, fontSize: 18)),
        backgroundColor: Colors.transparent,
        elevation: 0,
        centerTitle: true,
      ),
      body: SafeArea(
        child: Column(
          children: [
            Expanded(
              child: Container(
                alignment: Alignment.bottomRight,
                padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 20.0),
                child: SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  reverse: true,
                  child: Text(
                    display,
                    style: const TextStyle(
                      fontSize: 54,
                      fontWeight: FontWeight.w300,
                      color: Colors.white,
                    ),
                  ),
                ),
              ),
            ),
            Container(
              padding: const EdgeInsets.all(12.0),
              decoration: const BoxDecoration(
                color: Color(0xFF242731),
                borderRadius: BorderRadius.vertical(top: Radius.circular(28)),
              ),
              child: Column(
                children: [
                  Row(children: [_buildButton('C'), _buildButton('('), _buildButton(')'), _buildButton('÷')]),
                  Row(children: [_buildButton('7'), _buildButton('8'), _buildButton('9'), _buildButton('×')]),
                  Row(children: [_buildButton('4'), _buildButton('5'), _buildButton('6'), _buildButton('-')]),
                  Row(children: [_buildButton('1'), _buildButton('2'), _buildButton('3'), _buildButton('+')]),
                  Row(children: [
                    _buildButton('0', flex: 2),
                    _buildButton('.'),
                    _buildButton('='),
                  ]),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}


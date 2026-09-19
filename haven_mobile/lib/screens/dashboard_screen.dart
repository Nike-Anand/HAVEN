import 'dart:async';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:record/record.dart';
import 'package:sensors_plus/sensors_plus.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:haven_mobile/api/haven_client.dart';
import 'package:haven_mobile/api/offline_manager.dart';
import 'package:haven_mobile/screens/active_sos_screen.dart';
import 'package:haven_mobile/screens/therapy_screen.dart';
import 'package:haven_mobile/screens/legal_screen.dart';
import 'package:haven_mobile/screens/contacts_screen.dart';
import 'package:haven_mobile/screens/vault_screen.dart';

class DashboardScreen extends StatefulWidget {
  final String email;

  const DashboardScreen({super.key, required this.email});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  bool _isLoading = false;
  final AudioRecorder _audioRecorder = AudioRecorder();
  
  // Timer State
  bool _timerActive = false;
  int _timerDuration = 30;

  // Shake State
  StreamSubscription<UserAccelerometerEvent>? _shakeSubscription;
  DateTime _lastShakeTime = DateTime.now();
  int _shakeCount = 0;

  // Speech State
  stt.SpeechToText _speech = stt.SpeechToText();
  bool _isListening = false;

  @override
  void initState() {
    super.initState();
    OfflineManager.startMonitoring();
    _initShakeDetector();
    _initSpeech();
  }

  void _initShakeDetector() {
    _shakeSubscription = userAccelerometerEventStream().listen((UserAccelerometerEvent event) {
      double acceleration = event.x.abs() + event.y.abs() + event.z.abs();
      if (acceleration > 20) {
        final now = DateTime.now();
        if (now.difference(_lastShakeTime).inSeconds < 2) {
          _shakeCount++;
        } else {
          _shakeCount = 1;
        }
        _lastShakeTime = now;

        if (_shakeCount >= 3) {
          _shakeCount = 0;
          if (!_isLoading) {
            _triggerSOS();
          }
        }
      }
    });
  }

  Future<void> _initSpeech() async {
    await _speech.initialize();
  }

  void _toggleListening() async {
    if (_isListening) {
      _speech.stop();
      setState(() => _isListening = false);
    } else {
      bool available = await _speech.initialize();
      if (available) {
        setState(() => _isListening = true);
        _speech.listen(onResult: (val) {
          if (val.recognizedWords.toUpperCase().contains('HAVEN HELP')) {
            _speech.stop();
            setState(() => _isListening = false);
            if (!_isLoading) {
              _triggerSOS();
            }
          }
        });
      }
    }
  }

  void _toggleTimer() async {
    if (_timerActive) {
      try {
        await HavenClient.cancelSafetyTimer();
        setState(() => _timerActive = false);
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Safety Timer Cancelled!')),
          );
        }
      } catch (e) {
        debugPrint(e.toString());
      }
    } else {
      try {
        await HavenClient.startSafetyTimer(_timerDuration);
        setState(() => _timerActive = true);
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Safety Timer Started for $_timerDuration minutes!')),
          );
        }
      } catch (e) {
        debugPrint(e.toString());
      }
    }
  }

  @override
  void dispose() {
    _audioRecorder.dispose();
    _shakeSubscription?.cancel();
    _speech.cancel();
    super.dispose();
  }

  Future<Position?> _determinePosition() async {
    bool serviceEnabled;
    LocationPermission permission;

    serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) return null;

    permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) return null;
    }
    
    if (permission == LocationPermission.deniedForever) return null;

    return await Geolocator.getCurrentPosition();
  }

  Future<void> _startAudioRecording(String sosId) async {
    if (await _audioRecorder.hasPermission()) {
      final path = 'sos_audio_${DateTime.now().millisecondsSinceEpoch}.m4a';
      await _audioRecorder.start(const RecordConfig(), path: path);
      
      Timer(const Duration(seconds: 30), () async {
        final filePath = await _audioRecorder.stop();
        if (filePath != null) {
          try {
            final bytes = await File(filePath).readAsBytes();
            await HavenClient.uploadSOSAudio(sosId, bytes, 'audio_clip.m4a');
          } catch (e) {
            debugPrint("Failed to upload audio: $e");
          }
        }
      });
    }
  }

  Future<void> _triggerSOS() async {
    setState(() {
      _isLoading = true;
    });

    Position? position;
    try {
      position = await _determinePosition();
    } catch (e) {
      debugPrint("Could not fetch location: $e");
    }

    try {
      final response = await HavenClient.triggerSOS(
        latitude: position?.latitude,
        longitude: position?.longitude,
      );
      
      if (mounted) {
        _startAudioRecording(response['sos_id']);

        Navigator.pushReplacement(
          context,
          MaterialPageRoute(
            builder: (context) => ActiveSOSScreen(sosData: response),
          ),
        );
      }
    } catch (e) {
      await OfflineManager.queueSOS(position?.latitude, position?.longitude);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Network error. SOS queued and will trigger when online!'),
            backgroundColor: Colors.orange,
            duration: Duration(seconds: 5),
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  void _onNavTapped(int index) {
    if (index == 1) {
      Navigator.push(context, MaterialPageRoute(builder: (context) => const TherapyScreen()));
    } else if (index == 2) {
      Navigator.push(context, MaterialPageRoute(builder: (context) => const LegalScreen()));
    } else if (index == 3) {
      Navigator.push(context, MaterialPageRoute(builder: (context) => const ContactsScreen()));
    } else if (index == 4) {
      Navigator.push(context, MaterialPageRoute(builder: (context) => const VaultScreen()));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('HAVEN Safety'),
        backgroundColor: const Color(0xFF1f2d3d),
        foregroundColor: Colors.white,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              'Press in case of emergency',
              style: TextStyle(fontSize: 18, color: Colors.grey),
            ),
            const SizedBox(height: 40),
            GestureDetector(
              onTap: _isLoading ? null : _triggerSOS,
              child: Container(
                width: 250,
                height: 250,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: const Color(0xFFc62828),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.red.withOpacity(0.4),
                      spreadRadius: 10,
                      blurRadius: 20,
                    ),
                  ],
                ),
                child: Center(
                  child: _isLoading
                      ? const CircularProgressIndicator(color: Colors.white)
                      : const Text(
                          'SOS',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 72,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                ),
              ),
            ),
            const SizedBox(height: 40),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton.icon(
                  onPressed: _toggleTimer,
                  icon: Icon(_timerActive ? Icons.timer_off : Icons.timer),
                  label: Text(_timerActive ? 'Cancel Timer' : 'Safety Timer (30m)'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: _timerActive ? Colors.green : Colors.blueGrey,
                    foregroundColor: Colors.white,
                  ),
                ),
                ElevatedButton.icon(
                  onPressed: _toggleListening,
                  icon: Icon(_isListening ? Icons.mic : Icons.mic_off),
                  label: Text(_isListening ? 'Listening...' : 'Wake Word'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: _isListening ? Colors.redAccent : Colors.blueGrey,
                    foregroundColor: Colors.white,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 10),
            const Text(
              "Or quickly shake phone 3 times to trigger SOS",
              style: TextStyle(color: Colors.grey, fontSize: 12),
            )
          ],
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: 0,
        selectedItemColor: const Color(0xFFc62828),
        unselectedItemColor: Colors.grey,
        onTap: _onNavTapped,
        type: BottomNavigationBarType.fixed,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.chat), label: 'Therapy'),
          BottomNavigationBarItem(icon: Icon(Icons.gavel), label: 'Legal'),
          BottomNavigationBarItem(icon: Icon(Icons.people), label: 'Contacts'),
          BottomNavigationBarItem(icon: Icon(Icons.security), label: 'Vault'),
        ],
      ),
    );
  }
}


import 'dart:async';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:record/record.dart';
import 'package:haven_mobile/api/haven_client.dart';
import 'package:haven_mobile/api/offline_manager.dart';
import 'package:haven_mobile/screens/active_sos_screen.dart';
import 'package:haven_mobile/screens/therapy_screen.dart';
import 'package:haven_mobile/screens/legal_screen.dart';
import 'package:haven_mobile/screens/contacts_screen.dart';
import 'package:haven_mobile/screens/vault_screen.dart';

class DashboardScreen extends StatefulWidget {
  final String email;

  const DashboardScreen({Key? key, required this.email}) : super(key: key);

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  bool _isLoading = false;
  final AudioRecorder _audioRecorder = AudioRecorder();

  @override
  void initState() {
    super.initState();
    OfflineManager.startMonitoring();
  }

  @override
  void dispose() {
    _audioRecorder.dispose();
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
      // Record to a temporary file
      final path = 'sos_audio_${DateTime.now().millisecondsSinceEpoch}.m4a';
      await _audioRecorder.start(const RecordConfig(), path: path);
      
      // Stop after 30 seconds and upload
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
        // Start recording in background
        _startAudioRecording(response['sos_id']);

        Navigator.pushReplacement(
          context,
          MaterialPageRoute(
            builder: (context) => ActiveSOSScreen(sosData: response),
          ),
        );
      }
    } catch (e) {
      // Offline fallback
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

import 'dart:async';
import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:haven_mobile/api/haven_client.dart';
import 'package:haven_mobile/screens/dashboard_screen.dart';

class ActiveSOSScreen extends StatefulWidget {
  final Map<String, dynamic> sosData;

  const ActiveSOSScreen({super.key, required this.sosData});

  @override
  State<ActiveSOSScreen> createState() => _ActiveSOSScreenState();
}

class _ActiveSOSScreenState extends State<ActiveSOSScreen> {
  bool _isCancelling = false;
  StreamSubscription<Position>? _positionStream;

  @override
  void initState() {
    super.initState();
    _startLiveTracking();
  }

  void _startLiveTracking() {
    final locationSettings = const LocationSettings(
      accuracy: LocationAccuracy.high,
      distanceFilter: 5, // Update if they move 5 meters
    );
    
    _positionStream = Geolocator.getPositionStream(locationSettings: locationSettings).listen((Position? position) {
      if (position != null) {
        HavenClient.streamLocation(
          widget.sosData['sos_id'], 
          position.latitude, 
          position.longitude
        ).catchError((e) => debugPrint("Live tracking failed: $e"));
      }
    });
  }

  @override
  void dispose() {
    _positionStream?.cancel();
    super.dispose();
  }

  Future<void> _cancelSOS() async {
    setState(() {
      _isCancelling = true;
    });

    try {
      await HavenClient.cancelSOS(widget.sosData['sos_id']);
      if (mounted) {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(
            builder: (context) => DashboardScreen(email: HavenClient.email ?? ''),
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to cancel SOS: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isCancelling = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF1f2d3d),
      appBar: AppBar(
        title: const Text('ACTIVE SOS'),
        backgroundColor: Colors.red,
        foregroundColor: Colors.white,
        automaticallyImplyLeading: false,
      ),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          children: [
            const Icon(Icons.warning_amber_rounded, size: 100, color: Colors.redAccent),
            const SizedBox(height: 20),
            const Text(
              'EMERGENCY ALERT ACTIVE',
              style: TextStyle(
                color: Colors.white,
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 10),
            Text(
              widget.sosData['message'] ?? 'Help is on the way.',
              style: const TextStyle(color: Colors.white70, fontSize: 16),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 40),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.white10,
                borderRadius: BorderRadius.circular(8),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text('Contacts Notified:', style: TextStyle(color: Colors.white, fontSize: 18)),
                  Text(
                    '${widget.sosData['contacts_notified']}',
                    style: const TextStyle(color: Colors.redAccent, fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                ],
              ),
            ),
            const Spacer(),
            SizedBox(
              width: double.infinity,
              height: 60,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.white10,
                  foregroundColor: Colors.white,
                ),
                onPressed: _isCancelling ? null : _cancelSOS,
                child: _isCancelling 
                  ? const CircularProgressIndicator(color: Colors.white)
                  : const Text('CANCEL SOS', style: TextStyle(fontSize: 18)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

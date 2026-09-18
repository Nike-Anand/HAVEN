import 'dart:async';
import 'package:flutter/material.dart';
import 'package:socket_io_client/socket_io_client.dart' as IO;
import 'package:haven_mobile/api/haven_client.dart';
import 'package:geolocator/geolocator.dart';
import 'package:url_launcher/url_launcher.dart';

class ResponderDashboard extends StatefulWidget {
  const ResponderDashboard({super.key});

  @override
  State<ResponderDashboard> createState() => _ResponderDashboardState();
}

class _ResponderDashboardState extends State<ResponderDashboard> {
  IO.Socket? _socket;
  List<Map<String, dynamic>> _alerts = [];
  Map<String, dynamic>? _selected;
  Map<String, dynamic>? _routeData;
  bool _isLoading = false;
  bool _isRouting = false;
  Position? _myPosition;
  Timer? _pollTimer;

  @override
  void initState() {
    super.initState();
    _fetchMyPosition();
    _loadActiveAlerts();
    _initSocket();
    _pollTimer = Timer.periodic(const Duration(seconds: 5), (_) => _loadActiveAlerts());
  }

  @override
  void dispose() {
    _pollTimer?.cancel();
    _socket?.dispose();
    super.dispose();
  }

  Future<void> _fetchMyPosition() async {
    try {
      bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
      if (serviceEnabled) {
        LocationPermission permission = await Geolocator.checkPermission();
        if (permission == LocationPermission.denied) {
          permission = await Geolocator.requestPermission();
        }
        if (permission != LocationPermission.denied && permission != LocationPermission.deniedForever) {
          final pos = await Geolocator.getCurrentPosition(desiredAccuracy: LocationAccuracy.high);
          if (mounted) setState(() => _myPosition = pos);
        }
      }
    } catch (_) {}
  }

  Future<void> _loadActiveAlerts() async {
    try {
      final list = await HavenClient.getActiveSOS();
      if (mounted) {
        setState(() {
          _alerts = list.map((e) => Map<String, dynamic>.from(e)).toList();
        });
      }
    } catch (e) {
      debugPrint('Failed to load active alerts: $e');
    }
  }

  void _initSocket() {
    if (HavenClient.token == null) return;
    try {
      _socket = IO.io(HavenClient.baseUrl, <String, dynamic>{
        'transports': ['websocket'],
        'auth': {'token': HavenClient.token},
      });

      _socket?.on('connect', (_) {
        debugPrint('Responder socket connected');
      });

      _socket?.on('sos_alert', (data) {
        if (mounted) {
          setState(() {
            _alerts.insert(0, Map<String, dynamic>.from(data));
          });
        }
      });

      _socket?.on('sos_location_update', (data) {
        final sosId = data['sos_id'];
        if (mounted) {
          setState(() {
            final idx = _alerts.indexWhere((e) => e['sos_id'] == sosId);
            if (idx != -1) {
              _alerts[idx] = {..._alerts[idx], ...Map<String, dynamic>.from(data)};
            }
          });
          if (_selected != null && _selected!['sos_id'] == sosId) {
            _selected = {..._selected!, ...Map<String, dynamic>.from(data)};
            _fetchRoute(_selected!['latitude'], _selected!['longitude']);
          }
        }
      });
    } catch (e) {
      debugPrint('Socket init error: $e');
    }
  }

  Future<void> _fetchRoute(double destLat, double destLng) async {
    setState(() => _isRouting = true);
    try {
      final origLat = _myPosition?.latitude ?? 12.9249;
      final origLng = _myPosition?.longitude ?? 80.2000;
      final data = await HavenClient.getDirections(origLat, origLng, destLat, destLng);
      if (mounted) {
        setState(() {
          _routeData = data;
        });
      }
    } catch (e) {
      debugPrint('Route fetch error: $e');
    } finally {
      if (mounted) setState(() => _isRouting = false);
    }
  }

  Future<void> _acknowledge(String code) async {
    if (_selected == null) return;
    try {
      await HavenClient.respondToSOS(_selected!['sos_id'], "responder_b", code);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Response "$code" sent to victim & team!'),
            backgroundColor: Colors.green,
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to send status: $e'), backgroundColor: Colors.red),
        );
      }
    }
  }

  Future<void> _openExternalMap(double lat, double lng) async {
    final uri = Uri.parse('https://www.google.com/maps/dir/?api=1&destination=$lat,$lng');
    try {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    } catch (_) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Could not open external maps')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        title: const Text('Emergency Responder View', style: TextStyle(fontWeight: FontWeight.bold)),
        backgroundColor: const Color(0xFF1E293B),
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _loadActiveAlerts,
          ),
        ],
      ),
      body: Row(
        children: [
          // Left column / List of active SOS alerts
          Expanded(
            flex: _selected == null ? 1 : 1,
            child: _alerts.isEmpty
                ? Center(
                    child: Padding(
                      padding: const EdgeInsets.all(24.0),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: const [
                          Icon(Icons.shield_outlined, size: 72, color: Colors.blueGrey),
                          SizedBox(height: 16),
                          Text(
                            'No Active SOS Alerts',
                            style: TextStyle(fontSize: 20, color: Colors.white, fontWeight: FontWeight.bold),
                          ),
                          SizedBox(height: 8),
                          Text(
                            'When a user (Person A) triggers an SOS, live location & navigation route will appear here immediately.',
                            textAlign: TextAlign.center,
                            style: TextStyle(color: Colors.white60),
                          ),
                        ],
                      ),
                    ),
                  )
                : ListView.builder(
                    itemCount: _alerts.length,
                    itemBuilder: (context, idx) {
                      final a = _alerts[idx];
                      final isSelected = _selected?['sos_id'] == a['sos_id'];
                      return Card(
                        margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                        color: isSelected ? const Color(0xFF334155) : const Color(0xFF1E293B),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                          side: BorderSide(
                            color: isSelected ? const Color(0xFFEF4444) : Colors.transparent,
                            width: 2,
                          ),
                        ),
                        child: ListTile(
                          contentPadding: const EdgeInsets.all(12),
                          leading: Container(
                            padding: const EdgeInsets.all(10),
                            decoration: BoxDecoration(
                              color: const Color(0xFFEF4444).withOpacity(0.2),
                              shape: BoxShape.circle,
                            ),
                            child: const Icon(Icons.warning_rounded, color: Color(0xFFEF4444), size: 28),
                          ),
                          title: Text(
                            a['user_email'] ?? 'Person In Distress',
                            style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16),
                          ),
                          subtitle: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const SizedBox(height: 4),
                              Text('GPS: ${a['latitude']?.toStringAsFixed(4)}, ${a['longitude']?.toStringAsFixed(4)}',
                                  style: const TextStyle(color: Colors.white70, fontSize: 13)),
                              const SizedBox(height: 2),
                              Text('Status: ${a['status']?.toUpperCase() ?? "ACTIVE"} • Severity: ${a['severity'] ?? "CRITICAL"}',
                                  style: const TextStyle(color: Color(0xFFF87171), fontSize: 12, fontWeight: FontWeight.w600)),
                            ],
                          ),
                          trailing: ElevatedButton(
                            style: ElevatedButton.styleFrom(
                              backgroundColor: const Color(0xFFDC2626),
                              foregroundColor: Colors.white,
                              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                            ),
                            onPressed: () {
                              setState(() => _selected = a);
                              _fetchRoute(a['latitude'], a['longitude']);
                            },
                            child: const Text('ROUTE'),
                          ),
                        ),
                      );
                    },
                  ),
          ),

          // Right pane / Route & Navigation details when an alert is selected
          if (_selected != null)
            Expanded(
              flex: 1,
              child: Container(
                decoration: const BoxDecoration(
                  color: Color(0xFF1E293B),
                  border: Border(left: BorderSide(color: Color(0xFF334155), width: 1)),
                ),
                child: SingleChildScrollView(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text(
                            'Rescue Navigation Route',
                            style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
                          ),
                          IconButton(
                            icon: const Icon(Icons.close, color: Colors.white70),
                            onPressed: () => setState(() => _selected = null),
                          ),
                        ],
                      ),
                      const Divider(color: Color(0xFF334155)),
                      
                      // Distress Details Card
                      Container(
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: const Color(0xFF0F172A),
                          borderRadius: BorderRadius.circular(10),
                          border: Border.all(color: const Color(0xFFEF4444).withOpacity(0.4)),
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('Distress Target: ${_selected!['user_email']}',
                                style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                            const SizedBox(height: 4),
                            Text('Victim Coordinates: ${_selected!['latitude']}, ${_selected!['longitude']}',
                                style: const TextStyle(color: Colors.white70, fontSize: 13)),
                            if (_routeData != null) ...[
                              const SizedBox(height: 8),
                              Row(
                                children: [
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                    decoration: BoxDecoration(
                                      color: Colors.blue.withOpacity(0.2),
                                      borderRadius: BorderRadius.circular(6),
                                    ),
                                    child: Text(
                                      'Distance: ${((_routeData!['distance'] ?? 0) / 1000).toStringAsFixed(2)} km',
                                      style: const TextStyle(color: Colors.lightBlueAccent, fontWeight: FontWeight.bold),
                                    ),
                                  ),
                                  const SizedBox(width: 8),
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                    decoration: BoxDecoration(
                                      color: Colors.green.withOpacity(0.2),
                                      borderRadius: BorderRadius.circular(6),
                                    ),
                                    child: Text(
                                      'Est. Time: ${((_routeData!['duration'] ?? 0) / 60).toStringAsFixed(0)} mins',
                                      style: const TextStyle(color: Colors.greenAccent, fontWeight: FontWeight.bold),
                                    ),
                                  ),
                                ],
                              ),
                            ]
                          ],
                        ),
                      ),
                      const SizedBox(height: 16),

                      // Action Buttons
                      Row(
                        children: [
                          Expanded(
                            child: ElevatedButton.icon(
                              style: ElevatedButton.styleFrom(
                                backgroundColor: const Color(0xFF10B981),
                                foregroundColor: Colors.white,
                                padding: const EdgeInsets.symmetric(vertical: 12),
                              ),
                              onPressed: () => _acknowledge('ON_WAY'),
                              icon: const Icon(Icons.directions_run),
                              label: const Text("I'm On My Way"),
                            ),
                          ),
                          const SizedBox(width: 8),
                          Expanded(
                            child: ElevatedButton.icon(
                              style: ElevatedButton.styleFrom(
                                backgroundColor: const Color(0xFF2563EB),
                                foregroundColor: Colors.white,
                                padding: const EdgeInsets.symmetric(vertical: 12),
                              ),
                              onPressed: () => _openExternalMap(_selected!['latitude'], _selected!['longitude']),
                              icon: const Icon(Icons.map),
                              label: const Text('Open in Maps'),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 16),

                      const Text('Turn-by-Turn Route Steps:',
                          style: TextStyle(color: Colors.white70, fontWeight: FontWeight.bold, fontSize: 14)),
                      const SizedBox(height: 8),

                      if (_isRouting)
                        const Center(child: Padding(padding: EdgeInsets.all(20), child: CircularProgressIndicator()))
                      else if (_routeData != null && _routeData!['steps'] != null)
                        ...(_routeData!['steps'] as List).asMap().entries.map((entry) {
                          return Container(
                            margin: const EdgeInsets.only(bottom: 6),
                            padding: const EdgeInsets.all(10),
                            decoration: BoxDecoration(
                              color: const Color(0xFF0F172A),
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: Row(
                              children: [
                                CircleAvatar(
                                  radius: 12,
                                  backgroundColor: const Color(0xFF3B82F6),
                                  child: Text('${entry.key + 1}',
                                      style: const TextStyle(fontSize: 11, color: Colors.white, fontWeight: FontWeight.bold)),
                                ),
                                const SizedBox(width: 10),
                                Expanded(
                                  child: Text(
                                    entry.value.toString(),
                                    style: const TextStyle(color: Colors.white, fontSize: 13),
                                  ),
                                ),
                              ],
                            ),
                          );
                        })
                      else
                        const Text('Calculating route directions...', style: TextStyle(color: Colors.white54)),
                    ],
                  ),
                ),
              ),
            ),
        ],
      ),
    );
  }
}


import 'package:flutter/material.dart';
import 'package:socket_io_client/socket_io_client.dart' as IO;
import 'package:haven_mobile/api/haven_client.dart';
import 'package:geolocator/geolocator.dart';
import 'package:mapbox_gl/mapbox_gl.dart';
import 'package:haven_mobile/api/config.dart';

// Responder Dashboard scaffold. This screen will list incoming SOS alerts and
// display a Mapbox map when MAPBOX_TOKEN is configured. Currently a UI
// scaffold that will be wired to the realtime Socket.IO client.

class ResponderDashboard extends StatefulWidget {
  const ResponderDashboard({super.key});

  @override
  State<ResponderDashboard> createState() => _ResponderDashboardState();
}

class _ResponderDashboardState extends State<ResponderDashboard> {
  // TODO: Connect to Socket.IO server using socket_io_client and listen for
  // `sos_alert` and `sos_location_update` events. When MAPBOX_TOKEN is present,
  // show the Mapbox map and draw routing from responder -> sos location.
  IO.Socket? _socket;
  final List<Map<String, dynamic>> _alerts = [];
  Map<String, dynamic>? _selected;
  MapboxMapController? _mapController;
  List<Line> _lines = [];

  @override
  void initState() {
    super.initState();
    _initSocket();
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
        setState(() {
          _alerts.insert(0, Map<String, dynamic>.from(data));
        });
      });

      _socket?.on('sos_location_update', (data) {
        final sosId = data['sos_id'];
        setState(() {
          final idx = _alerts.indexWhere((e) => e['sos_id'] == sosId);
          if (idx != -1) {
            _alerts[idx] = {..._alerts[idx], ...Map<String, dynamic>.from(data)};
          }
        });
        if (_selected != null && _selected!['sos_id'] == sosId && _mapController != null) {
          _mapController!.animateCamera(CameraUpdate.newLatLng(LatLng(data['latitude'], data['longitude'])));
          // Optionally fetch new route
          _fetchRoute(_selected!['latitude'], _selected!['longitude']);
        }
      });

      _socket?.on('disconnect', (_) {
        debugPrint('Responder socket disconnected');
      });
    } catch (e) {
      debugPrint('Socket init failed: $e');
    }
  }

  Future<void> _fetchRoute(double destLat, double destLng) async {
    try {
      final pos = await Geolocator.getCurrentPosition();
      final data = await HavenClient.getDirections(pos.latitude, pos.longitude, destLat, destLng);
      final geom = data['geometry'];
      if (geom != null && geom['coordinates'] != null && _mapController != null) {
        final coords = (geom['coordinates'] as List).map((c) => LatLng(c[1], c[0])).toList();
        // Remove existing lines
        for (final l in _lines) {
          await _mapController!.removeLine(l);
        }
        _lines.clear();
        final line = await _mapController!.addLine(LineOptions(
          geometry: coords,
          lineColor: "#ff0000",
          lineWidth: 4.0,
          lineOpacity: 0.9,
        ));
        _lines.add(line);
        // Fit camera to route
        if (coords.isNotEmpty) {
          await _mapController!.animateCamera(CameraUpdate.newLatLng(coords[(coords.length / 2).floor()]));
        }
      }
    } catch (e) {
      debugPrint('Route fetch failed: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Responder Dashboard'),
      ),
      body: Column(
        children: [
          Expanded(
            child: _alerts.isEmpty
                ? Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: const [
                        Icon(Icons.location_on, size: 72, color: Colors.redAccent),
                        SizedBox(height: 16),
                        Text('No active alerts', style: TextStyle(fontSize: 18)),
                        SizedBox(height: 8),
                        Text('When an SOS arrives it will appear here with live location.'),
                      ],
                    ),
                  )
                : ListView.builder(
                    itemCount: _alerts.length,
                    itemBuilder: (context, idx) {
                      final a = _alerts[idx];
                      return ListTile(
                        leading: const Icon(Icons.warning_amber_rounded, color: Colors.redAccent),
                        title: Text('SOS ${a['sos_id']?.toString().substring(0,8) ?? ''}'),
                        subtitle: Text('${a['latitude']}, ${a['longitude']}'),
                        trailing: Text(a['severity'] ?? ''),
                        onTap: () {
                          setState(() {
                            _selected = a;
                          });
                        },
                      );
                    },
                  ),
          ),
          if (_selected != null && Config.MAPBOX_TOKEN.isNotEmpty)
            SizedBox(
              height: 300,
              child: MapboxMap(
                accessToken: Config.MAPBOX_TOKEN,
                initialCameraPosition: CameraPosition(
                  target: LatLng(_selected!['latitude'] ?? 0.0, _selected!['longitude'] ?? 0.0),
                  zoom: 14.0,
                ),
                onMapCreated: (controller) {
                  _mapController = controller;
                },
              ),
            )
          else if (_selected != null)
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Text('Select MAPBOX_TOKEN in api/config.dart to view the map'),
            )
        ],
      ),
    );
  }
}

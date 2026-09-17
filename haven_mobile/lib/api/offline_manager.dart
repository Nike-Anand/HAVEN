import 'dart:convert';
import 'dart:async';
import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:haven_mobile/api/haven_client.dart';

class OfflineManager {
  static const String queueKey = 'offline_sos_queue';
  
  static Future<void> queueSOS(double? lat, double? lng) async {
    final prefs = await SharedPreferences.getInstance();
    final queue = prefs.getStringList(queueKey) ?? [];
    
    final payload = {
      'latitude': lat,
      'longitude': lng,
      'timestamp': DateTime.now().toIso8601String(),
    };
    
    queue.add(jsonEncode(payload));
    await prefs.setStringList(queueKey, queue);
  }

  static Future<void> syncQueue() async {
    final prefs = await SharedPreferences.getInstance();
    final queue = prefs.getStringList(queueKey) ?? [];
    
    if (queue.isEmpty) return;

    List<String> failedQueue = [];

    for (String item in queue) {
      final payload = jsonDecode(item);
      try {
        await HavenClient.triggerSOS(
          latitude: payload['latitude'],
          longitude: payload['longitude']
        );
      } catch (e) {
        // If it fails again, keep it in the queue
        failedQueue.add(item);
      }
    }

    await prefs.setStringList(queueKey, failedQueue);
  }

  static void startMonitoring() {
    Connectivity().onConnectivityChanged.listen((List<ConnectivityResult> results) {
      // Modern connectivity_plus returns a list, if any result is not none, we try syncing
      if (!results.contains(ConnectivityResult.none)) {
        syncQueue();
      }
    });
  }
}

import 'dart:convert';
import 'package:http/http.dart' as http;

class HavenClient {
  static const String baseUrl = 'http://127.0.0.1:8000';
  static String? token;
  static String? email;

  static Future<Map<String, dynamic>> triggerSOS() async {
    final response = await http.post(
      Uri.parse('$baseUrl/sos/trigger'),
      headers: {
        'Content-Type': 'application/json',
        if (token != null) 'Authorization': 'Bearer $token',
      },
      body: jsonEncode({
        "location": {
          "latitude": 19.0760,
          "longitude": 72.8777,
          "address": "Mobile Device Location"
        },
        "severity": "critical"
      }),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to trigger SOS');
    }
  }

  static Future<Map<String, dynamic>> cancelSOS(String sosId) async {
    final response = await http.post(
      Uri.parse('$baseUrl/sos/$sosId/cancel'),
      headers: {
        'Content-Type': 'application/json',
        if (token != null) 'Authorization': 'Bearer $token',
      },
      body: jsonEncode({"reason": "False alarm from mobile"}),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to cancel SOS');
    }
  }
}

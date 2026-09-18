import 'dart:convert';
import 'package:http/http.dart' as http;

class HavenClient {
  static const String baseUrl = 'http://127.0.0.1:8000';
  static String? token;
  static String? email;

  static Future<Map<String, dynamic>> triggerSOS({double? latitude, double? longitude}) async {
    final response = await http.post(
      Uri.parse('$baseUrl/sos/trigger'),
      headers: {
        'Content-Type': 'application/json',
        if (token != null) 'Authorization': 'Bearer $token',
      },
      body: jsonEncode({
        "location": {
          "latitude": latitude ?? 19.0760,
          "longitude": longitude ?? 72.8777,
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

  static Future<void> uploadSOSAudio(String sosId, List<int> audioBytes, String filename) async {
    var request = http.MultipartRequest('POST', Uri.parse('$baseUrl/sos/$sosId/audio'));
    
    if (token != null) {
      request.headers['Authorization'] = 'Bearer $token';
    }

    request.files.add(http.MultipartFile.fromBytes(
      'file',
      audioBytes,
      filename: filename,
    ));

    var streamedResponse = await request.send();
    var response = await http.Response.fromStream(streamedResponse);

    if (response.statusCode != 200) {
      throw Exception('Failed to upload audio: ${response.body}');
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

  static Future<Map<String, dynamic>> startSafetyTimer(int durationMinutes) async {
    final response = await http.post(
      Uri.parse('$baseUrl/sos/timer/start'),
      headers: {
        'Content-Type': 'application/json',
        if (token != null) 'Authorization': 'Bearer $token',
      },
      body: jsonEncode({"duration_minutes": durationMinutes}),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to start safety timer');
    }
  }

  static Future<Map<String, dynamic>> cancelSafetyTimer() async {
    final response = await http.post(
      Uri.parse('$baseUrl/sos/timer/cancel'),
      headers: {
        'Content-Type': 'application/json',
        if (token != null) 'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to cancel safety timer');
    }
  }

  static Future<void> streamLocation(String sosId, double latitude, double longitude) async {
    final response = await http.post(
      Uri.parse('$baseUrl/sos/$sosId/location'),
      headers: {
        'Content-Type': 'application/json',
        if (token != null) 'Authorization': 'Bearer $token',
      },
      body: jsonEncode({
        "latitude": latitude,
        "longitude": longitude
      }),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to stream location');
    }
  }

  static Future<Map<String, dynamic>> sendTherapyMessage(String message, {String language = 'en'}) async {
    final response = await http.post(
      Uri.parse('$baseUrl/therapy/send-message'),
      headers: {
        'Content-Type': 'application/json',
        if (token != null) 'Authorization': 'Bearer $token',
      },
      body: jsonEncode({"message": message, "language": language}),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to send therapy message');
    }
  }

  static Future<Map<String, dynamic>> askLegalQuestion(String query, {String language = 'en'}) async {
    final response = await http.post(
      Uri.parse('$baseUrl/legal/ask'),
      headers: {
        'Content-Type': 'application/json',
        if (token != null) 'Authorization': 'Bearer $token',
      },
      body: jsonEncode({"query": query, "language": language}),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to get legal guidance');
    }
  }

  static Future<List<dynamic>> getContacts() async {
    final response = await http.get(
      Uri.parse('$baseUrl/contacts/'),
      headers: {
        if (token != null) 'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['contacts'] ?? [];
    } else {
      throw Exception('Failed to load contacts');
    }
  }

  static Future<Map<String, dynamic>> addContact(String name, String phone, String relationship, {int priority = 2}) async {
    final response = await http.post(
      Uri.parse('$baseUrl/contacts/add'),
      headers: {
        'Content-Type': 'application/json',
        if (token != null) 'Authorization': 'Bearer $token',
      },
      body: jsonEncode({
        "name": name,
        "phone": phone,
        "relationship": relationship,
        "priority": priority
      }),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to add contact');
    }
  }

  static Future<List<int>> hideDataInImage(List<int> imageBytes, String secretText) async {
    var request = http.MultipartRequest('POST', Uri.parse('$baseUrl/stegano/hide'));
    
    if (token != null) {
      request.headers['Authorization'] = 'Bearer $token';
    }

    request.fields['secret_text'] = secretText;
    request.files.add(http.MultipartFile.fromBytes(
      'file',
      imageBytes,
      filename: 'upload.png',
    ));

    var streamedResponse = await request.send();
    var response = await http.Response.fromStream(streamedResponse);

    if (response.statusCode == 200) {
      return response.bodyBytes;
    } else {
      throw Exception('Failed to hide data: ${response.body}');
    }
  }

  static Future<String> extractDataFromImage(List<int> imageBytes) async {
    var request = http.MultipartRequest('POST', Uri.parse('$baseUrl/stegano/extract'));
    
    if (token != null) {
      request.headers['Authorization'] = 'Bearer $token';
    }

    request.files.add(http.MultipartFile.fromBytes(
      'file',
      imageBytes,
      filename: 'upload.png',
    ));

    var streamedResponse = await request.send();
    var response = await http.Response.fromStream(streamedResponse);

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['secret_text'] ?? '';
    } else {
      throw Exception('Failed to extract data: ${response.body}');
    }
  }

  static Future<Map<String, dynamic>> getDirections(double origLat, double origLng, double destLat, double destLng) async {
    final response = await http.get(
      Uri.parse('$baseUrl/maps/directions?orig_lat=$origLat&orig_lng=$origLng&dest_lat=$destLat&dest_lng=$destLng'),
      headers: {
        if (token != null) 'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to get directions: ${response.statusCode}');
    }
  }
}

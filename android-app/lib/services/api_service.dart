import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../models/user.dart';
import '../models/chat_session.dart';
import '../models/chat_message.dart';

class ApiService {
  // Change this to your server IP when testing on physical device
  // Use 10.0.2.2 for Android emulator to access localhost
  // Use your computer's IP for physical device (same WiFi network)
  static const String baseUrl = 'http://192.168.29.246:8000';

  String? _token;

  void setToken(String? token) {
    _token = token;
  }

  Map<String, String> get _headers {
    final headers = <String, String>{
      'Content-Type': 'application/json',
    };
    if (_token != null) {
      headers['Authorization'] = 'Bearer $_token';
    }
    return headers;
  }

  // ============== Auth ==============

  Future<Map<String, dynamic>> signup(String email, String username, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/auth/signup'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'email': email,
        'username': username,
        'password': password,
      }),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Signup failed');
    }
  }

  Future<Map<String, dynamic>> login(String email, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'email': email,
        'password': password,
      }),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Login failed');
    }
  }

  Future<User> getMe() async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/auth/me'),
      headers: _headers,
    );

    if (response.statusCode == 200) {
      return User.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to get user');
    }
  }

  // ============== Sessions ==============

  Future<List<ChatSession>> getSessions() async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/sessions'),
      headers: _headers,
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((json) => ChatSession.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load sessions');
    }
  }

  Future<Map<String, dynamic>> getSession(String sessionId) async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/sessions/$sessionId'),
      headers: _headers,
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load session');
    }
  }

  Future<ChatSession> createSession({String title = 'New Chat'}) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/sessions'),
      headers: _headers,
      body: jsonEncode({'title': title}),
    );

    if (response.statusCode == 200) {
      return ChatSession.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to create session');
    }
  }

  Future<void> deleteSession(String sessionId) async {
    final response = await http.delete(
      Uri.parse('$baseUrl/api/sessions/$sessionId'),
      headers: _headers,
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to delete session');
    }
  }

  // ============== Chat ==============

  Future<Map<String, dynamic>> askText(String question, {String? sessionId}) async {
    final body = <String, dynamic>{'question': question};
    if (sessionId != null) {
      body['session_id'] = sessionId;
    }

    final response = await http.post(
      Uri.parse('$baseUrl/api/ask/text/detailed'),
      headers: _headers,
      body: jsonEncode(body),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to get response');
    }
  }

  Future<Map<String, dynamic>> askVoice(File audioFile, {String? sessionId}) async {
    final request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/api/ask/voice/detailed'),
    );

    if (_token != null) {
      request.headers['Authorization'] = 'Bearer $_token';
    }

    if (sessionId != null) {
      request.fields['session_id'] = sessionId;
    }

    request.files.add(await http.MultipartFile.fromPath(
      'audio',
      audioFile.path,
      filename: 'recording.wav',
    ));

    final streamedResponse = await request.send();
    final response = await http.Response.fromStream(streamedResponse);

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to process audio');
    }
  }

  // ============== TTS ==============

  Future<List<int>> textToSpeech(String text) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/tts'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'question': text}),
    );

    if (response.statusCode == 200) {
      return response.bodyBytes;
    } else {
      throw Exception('Failed to generate speech');
    }
  }
}

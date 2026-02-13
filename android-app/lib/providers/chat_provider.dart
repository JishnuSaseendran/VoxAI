import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:path_provider/path_provider.dart';
import 'package:audioplayers/audioplayers.dart';
import '../models/chat_session.dart';
import '../models/chat_message.dart';
import '../services/api_service.dart';

enum ChatStatus { idle, recording, transcribing, routing, processing, generating, complete, error }

class ChatProvider with ChangeNotifier {
  ApiService? _apiService;

  List<ChatSession> _sessions = [];
  ChatSession? _currentSession;
  List<ChatMessage> _messages = [];
  ChatStatus _status = ChatStatus.idle;
  String? _error;
  String? _currentAgent;
  bool _isLoadingSessions = false;

  final AudioPlayer _audioPlayer = AudioPlayer();
  bool _isPlayingAudio = false;
  String? _playingMessageId;

  List<ChatSession> get sessions => _sessions;
  ChatSession? get currentSession => _currentSession;
  List<ChatMessage> get messages => _messages;
  ChatStatus get status => _status;
  String? get error => _error;
  String? get currentAgent => _currentAgent;
  bool get isLoadingSessions => _isLoadingSessions;
  bool get isPlayingAudio => _isPlayingAudio;
  String? get playingMessageId => _playingMessageId;

  bool get isProcessing =>
      _status != ChatStatus.idle &&
      _status != ChatStatus.complete &&
      _status != ChatStatus.error;

  void setApiService(ApiService apiService) {
    _apiService = apiService;
  }

  Future<void> loadSessions() async {
    if (_apiService == null) return;

    _isLoadingSessions = true;
    notifyListeners();

    try {
      _sessions = await _apiService!.getSessions();
      _isLoadingSessions = false;
      notifyListeners();
    } catch (e) {
      _isLoadingSessions = false;
      _error = e.toString();
      notifyListeners();
    }
  }

  Future<void> selectSession(String sessionId) async {
    if (_apiService == null) return;

    try {
      final data = await _apiService!.getSession(sessionId);
      _currentSession = ChatSession.fromJson(data);
      _messages = (data['messages'] as List)
          .map((m) => ChatMessage.fromJson(m))
          .toList();
      _status = ChatStatus.idle;
      _error = null;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      notifyListeners();
    }
  }

  void startNewChat() {
    _currentSession = null;
    _messages = [];
    _status = ChatStatus.idle;
    _error = null;
    _currentAgent = null;
    notifyListeners();
  }

  Future<void> deleteSession(String sessionId) async {
    if (_apiService == null) return;

    try {
      await _apiService!.deleteSession(sessionId);
      _sessions.removeWhere((s) => s.id == sessionId);

      if (_currentSession?.id == sessionId) {
        startNewChat();
      }

      notifyListeners();
    } catch (e) {
      _error = e.toString();
      notifyListeners();
    }
  }

  Future<void> sendTextMessage(String question) async {
    if (_apiService == null || question.trim().isEmpty) return;

    _status = ChatStatus.routing;
    _error = null;
    notifyListeners();

    try {
      final result = await _apiService!.askText(
        question,
        sessionId: _currentSession?.id,
      );

      _status = ChatStatus.processing;
      _currentAgent = result['agent_used'];
      notifyListeners();

      await Future.delayed(const Duration(milliseconds: 300));

      _status = ChatStatus.generating;
      notifyListeners();

      await Future.delayed(const Duration(milliseconds: 200));

      // Handle new session
      if (result['session_id'] != null && _currentSession == null) {
        final newSession = ChatSession(
          id: result['session_id'],
          title: result['session_title'] ?? question.substring(0, question.length > 50 ? 50 : question.length),
          createdAt: DateTime.now(),
          updatedAt: DateTime.now(),
        );
        _currentSession = newSession;
        _sessions.insert(0, newSession);
      }

      // Add messages
      _messages.add(ChatMessage(
        id: 'user-${DateTime.now().millisecondsSinceEpoch}',
        role: 'user',
        content: question,
        createdAt: DateTime.now(),
      ));

      _messages.add(ChatMessage(
        id: result['message_id'] ?? 'assistant-${DateTime.now().millisecondsSinceEpoch}',
        role: 'assistant',
        content: result['answer'],
        queryType: result['query_type'],
        agentUsed: result['agent_used'],
        plan: result['plan'] != null ? List<String>.from(result['plan']) : null,
        createdAt: DateTime.now(),
      ));

      _status = ChatStatus.complete;
      notifyListeners();
    } catch (e) {
      _status = ChatStatus.error;
      _error = e.toString().replaceFirst('Exception: ', '');
      notifyListeners();
    }
  }

  Future<void> sendVoiceMessage(File audioFile) async {
    if (_apiService == null) return;

    _status = ChatStatus.transcribing;
    _error = null;
    notifyListeners();

    try {
      final result = await _apiService!.askVoice(
        audioFile,
        sessionId: _currentSession?.id,
      );

      _status = ChatStatus.routing;
      notifyListeners();

      await Future.delayed(const Duration(milliseconds: 200));

      _status = ChatStatus.processing;
      _currentAgent = result['agent_used'];
      notifyListeners();

      await Future.delayed(const Duration(milliseconds: 300));

      _status = ChatStatus.generating;
      notifyListeners();

      await Future.delayed(const Duration(milliseconds: 200));

      // Handle new session
      if (result['session_id'] != null && _currentSession == null) {
        final newSession = ChatSession(
          id: result['session_id'],
          title: result['session_title'] ?? result['question'].substring(0, result['question'].length > 50 ? 50 : result['question'].length),
          createdAt: DateTime.now(),
          updatedAt: DateTime.now(),
        );
        _currentSession = newSession;
        _sessions.insert(0, newSession);
      }

      // Add messages
      _messages.add(ChatMessage(
        id: 'user-${DateTime.now().millisecondsSinceEpoch}',
        role: 'user',
        content: result['question'],
        createdAt: DateTime.now(),
      ));

      _messages.add(ChatMessage(
        id: result['message_id'] ?? 'assistant-${DateTime.now().millisecondsSinceEpoch}',
        role: 'assistant',
        content: result['answer'],
        queryType: result['query_type'],
        agentUsed: result['agent_used'],
        plan: result['plan'] != null ? List<String>.from(result['plan']) : null,
        createdAt: DateTime.now(),
      ));

      _status = ChatStatus.complete;
      notifyListeners();
    } catch (e) {
      _status = ChatStatus.error;
      _error = e.toString().replaceFirst('Exception: ', '');
      notifyListeners();
    }
  }

  Future<void> playMessage(String messageId, String content) async {
    if (_apiService == null) return;

    if (_isPlayingAudio && _playingMessageId == messageId) {
      await stopAudio();
      return;
    }

    await stopAudio();

    _isPlayingAudio = true;
    _playingMessageId = messageId;
    notifyListeners();

    try {
      final audioBytes = await _apiService!.textToSpeech(content);

      final tempDir = await getTemporaryDirectory();
      final tempFile = File('${tempDir.path}/tts_$messageId.mp3');
      await tempFile.writeAsBytes(audioBytes);

      _audioPlayer.onPlayerComplete.listen((_) {
        _isPlayingAudio = false;
        _playingMessageId = null;
        notifyListeners();
      });

      await _audioPlayer.play(DeviceFileSource(tempFile.path));
    } catch (e) {
      _isPlayingAudio = false;
      _playingMessageId = null;
      _error = 'Failed to play audio';
      notifyListeners();
    }
  }

  Future<void> stopAudio() async {
    await _audioPlayer.stop();
    _isPlayingAudio = false;
    _playingMessageId = null;
    notifyListeners();
  }

  void clearError() {
    _error = null;
    _status = ChatStatus.idle;
    notifyListeners();
  }

  void reset() {
    _sessions = [];
    _currentSession = null;
    _messages = [];
    _status = ChatStatus.idle;
    _error = null;
    _currentAgent = null;
    notifyListeners();
  }

  @override
  void dispose() {
    _audioPlayer.dispose();
    super.dispose();
  }
}

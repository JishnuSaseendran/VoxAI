class ChatMessage {
  final String id;
  final String role; // 'user' or 'assistant'
  final String content;
  final String? queryType;
  final String? agentUsed;
  final List<String>? plan;
  final DateTime createdAt;

  ChatMessage({
    required this.id,
    required this.role,
    required this.content,
    this.queryType,
    this.agentUsed,
    this.plan,
    required this.createdAt,
  });

  factory ChatMessage.fromJson(Map<String, dynamic> json) {
    return ChatMessage(
      id: json['id'] ?? '',
      role: json['role'] ?? 'user',
      content: json['content'] ?? '',
      queryType: json['query_type'],
      agentUsed: json['agent_used'],
      plan: json['plan'] != null ? List<String>.from(json['plan']) : null,
      createdAt: DateTime.parse(json['created_at'] ?? DateTime.now().toIso8601String()),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'role': role,
      'content': content,
      'query_type': queryType,
      'agent_used': agentUsed,
      'plan': plan,
      'created_at': createdAt.toIso8601String(),
    };
  }

  bool get isUser => role == 'user';
  bool get isAssistant => role == 'assistant';
}

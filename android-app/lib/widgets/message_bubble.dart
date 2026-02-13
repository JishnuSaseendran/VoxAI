import 'package:flutter/material.dart';
import '../models/chat_message.dart';

class MessageBubble extends StatelessWidget {
  final ChatMessage message;
  final bool isPlaying;
  final VoidCallback onPlay;
  final VoidCallback onStop;

  const MessageBubble({
    super.key,
    required this.message,
    required this.isPlaying,
    required this.onPlay,
    required this.onStop,
  });

  Color _getAgentColor(String? agent) {
    switch (agent) {
      case 'coding':
        return const Color(0xFFF39C12);
      case 'grammar':
        return const Color(0xFF9B59B6);
      case 'research':
        return const Color(0xFF1ABC9C);
      case 'planning':
        return const Color(0xFFE74C3C);
      case 'creative':
        return const Color(0xFFE91E63);
      case 'math':
        return const Color(0xFF3498DB);
      case 'conversation':
        return const Color(0xFF27AE60);
      default:
        return const Color(0xFF667EEA);
    }
  }

  String _getAgentIcon(String? agent) {
    switch (agent) {
      case 'coding':
        return '💻';
      case 'grammar':
        return '✏️';
      case 'research':
        return '🔍';
      case 'planning':
        return '📋';
      case 'creative':
        return '🎨';
      case 'math':
        return '🔢';
      case 'conversation':
        return '💬';
      default:
        return '💡';
    }
  }

  @override
  Widget build(BuildContext context) {
    final isUser = message.isUser;

    return Padding(
      padding: EdgeInsets.only(
        left: isUser ? 48 : 0,
        right: isUser ? 0 : 48,
        bottom: 12,
      ),
      child: Column(
        crossAxisAlignment: isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start,
        children: [
          // Agent badge for assistant messages
          if (!isUser && message.agentUsed != null) ...[
            Container(
              margin: const EdgeInsets.only(bottom: 4, left: 4),
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
              decoration: BoxDecoration(
                color: _getAgentColor(message.agentUsed).withOpacity(0.1),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    _getAgentIcon(message.agentUsed),
                    style: const TextStyle(fontSize: 12),
                  ),
                  const SizedBox(width: 4),
                  Text(
                    message.agentUsed!.substring(0, 1).toUpperCase() +
                        message.agentUsed!.substring(1),
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.w600,
                      color: _getAgentColor(message.agentUsed),
                    ),
                  ),
                ],
              ),
            ),
          ],

          // Message bubble
          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: isUser
                  ? const Color(0xFF667EEA)
                  : Theme.of(context).colorScheme.surfaceContainerHighest,
              borderRadius: BorderRadius.only(
                topLeft: const Radius.circular(16),
                topRight: const Radius.circular(16),
                bottomLeft: Radius.circular(isUser ? 16 : 4),
                bottomRight: Radius.circular(isUser ? 4 : 16),
              ),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.05),
                  blurRadius: 5,
                  offset: const Offset(0, 2),
                ),
              ],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  message.content,
                  style: TextStyle(
                    color: isUser ? Colors.white : null,
                    height: 1.4,
                  ),
                ),

                // Play button for assistant messages
                if (!isUser) ...[
                  const SizedBox(height: 10),
                  Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      InkWell(
                        onTap: isPlaying ? onStop : onPlay,
                        borderRadius: BorderRadius.circular(16),
                        child: Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: 12,
                            vertical: 6,
                          ),
                          decoration: BoxDecoration(
                            color: isPlaying
                                ? Colors.red.withOpacity(0.1)
                                : const Color(0xFF27AE60).withOpacity(0.1),
                            borderRadius: BorderRadius.circular(16),
                          ),
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Icon(
                                isPlaying ? Icons.stop : Icons.play_arrow,
                                size: 16,
                                color: isPlaying ? Colors.red : const Color(0xFF27AE60),
                              ),
                              const SizedBox(width: 4),
                              Text(
                                isPlaying ? 'Stop' : 'Play',
                                style: TextStyle(
                                  fontSize: 12,
                                  fontWeight: FontWeight.w600,
                                  color: isPlaying ? Colors.red : const Color(0xFF27AE60),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ],
            ),
          ),

          // Time
          Padding(
            padding: const EdgeInsets.only(top: 4, left: 4, right: 4),
            child: Text(
              '${message.createdAt.hour.toString().padLeft(2, '0')}:${message.createdAt.minute.toString().padLeft(2, '0')}',
              style: TextStyle(
                fontSize: 11,
                color: Colors.grey[500],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

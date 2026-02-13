import 'package:flutter/material.dart';
import '../providers/chat_provider.dart';

class StatusIndicator extends StatelessWidget {
  final ChatStatus status;
  final String? agentName;

  const StatusIndicator({
    super.key,
    required this.status,
    this.agentName,
  });

  String _getStatusText() {
    switch (status) {
      case ChatStatus.recording:
        return 'Recording audio...';
      case ChatStatus.transcribing:
        return 'Transcribing speech...';
      case ChatStatus.routing:
        return 'Router analyzing query...';
      case ChatStatus.processing:
        if (agentName != null) {
          final name = agentName!.substring(0, 1).toUpperCase() + agentName!.substring(1);
          return '$name agent processing...';
        }
        return 'Processing...';
      case ChatStatus.generating:
        return 'Generating response...';
      default:
        return 'Processing...';
    }
  }

  IconData _getStatusIcon() {
    switch (status) {
      case ChatStatus.recording:
        return Icons.mic;
      case ChatStatus.transcribing:
        return Icons.text_fields;
      case ChatStatus.routing:
        return Icons.alt_route;
      case ChatStatus.processing:
        return Icons.settings;
      case ChatStatus.generating:
        return Icons.chat_bubble_outline;
      default:
        return Icons.hourglass_empty;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [Color(0xFF667EEA), Color(0xFF764BA2)],
        ),
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: const Color(0xFF667EEA).withOpacity(0.3),
            blurRadius: 8,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Row(
        children: [
          SizedBox(
            width: 24,
            height: 24,
            child: CircularProgressIndicator(
              strokeWidth: 2,
              valueColor: AlwaysStoppedAnimation<Color>(
                Colors.white.withOpacity(0.9),
              ),
            ),
          ),
          const SizedBox(width: 12),
          Icon(
            _getStatusIcon(),
            color: Colors.white,
            size: 20,
          ),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              _getStatusText(),
              style: const TextStyle(
                color: Colors.white,
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
        ],
      ),
    );
  }
}

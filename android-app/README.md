# VoxAI Android App

A Flutter-based mobile app for the VoxAI multi-agent AI voice assistant, with authentication, session-based chat, voice input, and text-to-speech playback.

## Features

- User authentication (login/signup with JWT)
- Chat with AI using text or voice
- Session-based chat history with drawer navigation
- AI-generated session titles
- Text-to-speech playback for responses
- Agent badges showing which AI handled the query
- Real-time processing status indicators

## Prerequisites

1. **Flutter SDK** (3.0.0 or higher)
   ```bash
   # Install Flutter: https://docs.flutter.dev/get-started/install
   flutter --version
   ```

2. **Android Studio** or **VS Code** with Flutter extensions

3. **Backend server** running on your machine or network

## Setup

### 1. Install Flutter Dependencies

```bash
cd android-app
flutter pub get
```

### 2. Configure API URL

Edit `lib/services/api_service.dart` and update the `baseUrl`:

```dart
// For Android Emulator (accessing localhost)
static const String baseUrl = 'http://10.0.2.2:8000';

// For physical device (use your computer's IP)
static const String baseUrl = 'http://192.168.1.xxx:8000';
```

### 3. Run the App

```bash
# Run on connected device/emulator
flutter run

# Build APK
flutter build apk

# Build release APK
flutter build apk --release
```

## Project Structure

```
android-app/
├── lib/
│   ├── main.dart              # App entry point with Provider setup
│   ├── models/
│   │   ├── user.dart          # User model (id, email, username)
│   │   ├── chat_session.dart  # Session model (id, title, timestamps)
│   │   └── chat_message.dart  # Message model (role, content, agent)
│   ├── providers/
│   │   ├── auth_provider.dart # Auth state (login, signup, token, auto-login)
│   │   └── chat_provider.dart # Chat state (sessions, messages, queries)
│   ├── services/
│   │   └── api_service.dart   # HTTP client for all backend API calls
│   ├── screens/
│   │   ├── splash_screen.dart # Loading screen with auto-login check
│   │   ├── login_screen.dart  # Login/signup screen
│   │   └── home_screen.dart   # Main chat screen
│   └── widgets/
│       ├── chat_drawer.dart     # Session sidebar drawer
│       ├── message_bubble.dart  # Chat message with agent badge & TTS
│       └── status_indicator.dart # Processing status display
├── assets/
│   └── icon/                  # App icon assets
├── android/                   # Android native configuration
├── pubspec.yaml               # Dependencies
└── README.md
```

## Features Overview

### Authentication
- Email/password signup and login
- JWT token stored locally via SharedPreferences
- Auto-login on app restart

### Chat Interface
- Text input with send button
- Voice recording with microphone button (via flutter_sound)
- Real-time processing status indicators
- Agent badges showing which AI handled the query

### Session Management
- Drawer with all chat sessions
- AI-generated session titles
- Swipe to delete sessions
- Tap to switch between sessions

### Audio Features
- Voice recording for queries (flutter_sound)
- Text-to-speech playback for responses (audioplayers)
- Play/stop controls on each message

## Permissions

The app requires:
- `INTERNET` - API communication
- `RECORD_AUDIO` - Voice input
- `WRITE_EXTERNAL_STORAGE` - Audio file storage
- `READ_EXTERNAL_STORAGE` - Audio file access

## Dependencies

| Package | Purpose |
|---------|---------|
| `provider` | State management |
| `http` | HTTP client |
| `shared_preferences` | Local token storage |
| `flutter_sound` | Audio recording |
| `audioplayers` | Audio playback |
| `path_provider` | File system access |
| `permission_handler` | Runtime permissions |
| `cupertino_icons` | iOS-style icons |

## Troubleshooting

### "Connection refused" error
- Make sure the backend server is running
- Check the API URL in `api_service.dart`
- For physical devices, use your computer's local IP (not localhost)
- For emulator, use `10.0.2.2` instead of `localhost`

### Microphone not working
- Grant microphone permission in app settings
- Check if another app is using the microphone

### App crashes on startup
- Run `flutter clean && flutter pub get`
- Check Android SDK version compatibility

## Building for Release

```bash
# Generate release APK
flutter build apk --release

# The APK will be at:
# build/app/outputs/flutter-apk/app-release.apk
```

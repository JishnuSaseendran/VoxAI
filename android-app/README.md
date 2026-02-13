# Voice Assistant Android App

A Flutter-based Android app for the Voice Assistant multi-agent AI system.

## Features

- User authentication (login/signup)
- Chat with AI using text or voice
- Session-based chat history
- AI-generated session titles
- Text-to-speech playback for responses
- Multiple specialized AI agents

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
│   ├── main.dart              # App entry point
│   ├── models/
│   │   ├── user.dart          # User model
│   │   ├── chat_session.dart  # Session model
│   │   └── chat_message.dart  # Message model
│   ├── providers/
│   │   ├── auth_provider.dart # Authentication state
│   │   └── chat_provider.dart # Chat state
│   ├── services/
│   │   └── api_service.dart   # API client
│   ├── screens/
│   │   ├── splash_screen.dart # Loading screen
│   │   ├── login_screen.dart  # Auth screen
│   │   └── home_screen.dart   # Main chat screen
│   └── widgets/
│       ├── chat_drawer.dart   # Session sidebar
│       ├── message_bubble.dart # Chat messages
│       └── status_indicator.dart # Processing status
├── android/                   # Android configuration
├── pubspec.yaml              # Dependencies
└── README.md
```

## Features Overview

### Authentication
- Email/password signup and login
- JWT token stored locally
- Auto-login on app restart

### Chat Interface
- Text input with send button
- Voice recording with microphone button
- Real-time processing status indicators
- Agent badges showing which AI handled the query

### Session Management
- Drawer with all chat sessions
- AI-generated session titles
- Swipe to delete sessions
- Tap to switch between sessions

### Audio Features
- Voice recording for queries
- Text-to-speech playback for responses
- Play/stop controls on each message

## Permissions

The app requires:
- `INTERNET` - API communication
- `RECORD_AUDIO` - Voice input
- `WRITE_EXTERNAL_STORAGE` - Audio file storage
- `READ_EXTERNAL_STORAGE` - Audio file access

## Troubleshooting

### "Connection refused" error
- Make sure the backend server is running
- Check the API URL in `api_service.dart`
- For physical devices, use your computer's local IP (not localhost)

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

## Dependencies

- `provider` - State management
- `http` - HTTP client
- `shared_preferences` - Local storage
- `record` - Audio recording
- `audioplayers` - Audio playback
- `path_provider` - File system access
- `permission_handler` - Runtime permissions

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_inappwebview/flutter_inappwebview.dart';

/// 游戏是 ES Modules，file:// 打不开。用应用内 localhost 托管 assets/game。
final _server = InAppLocalhostServer(port: 18080, documentRoot: 'assets/game');

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await SystemChrome.setEnabledSystemUIMode(SystemUiMode.edgeToEdge);
  await _server.start();
  runApp(const LuluApp());
}

class LuluApp extends StatelessWidget {
  const LuluApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '噜噜练习',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF3B6BFF)),
        useMaterial3: true,
      ),
      home: const GamePage(),
    );
  }
}

class GamePage extends StatefulWidget {
  const GamePage({super.key});

  @override
  State<GamePage> createState() => _GamePageState();
}

class _GamePageState extends State<GamePage> {
  var _loading = true;
  String? _error;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF3B6BFF),
      body: Stack(
        children: [
          InAppWebView(
            initialUrlRequest: URLRequest(
              url: WebUri('http://127.0.0.1:${_server.port}/'),
            ),
            initialSettings: InAppWebViewSettings(
              javaScriptEnabled: true,
              mediaPlaybackRequiresUserGesture: false,
              allowsInlineMediaPlayback: true,
              supportZoom: false,
              verticalScrollBarEnabled: false,
              horizontalScrollBarEnabled: false,
              transparentBackground: true,
              useWideViewPort: true,
              loadWithOverviewMode: true,
            ),
            onLoadStop: (_, _) => setState(() => _loading = false),
            onReceivedError: (_, _, error) {
              setState(() {
                _loading = false;
                _error = error.description;
              });
            },
          ),
          if (_loading)
            const Center(
              child: CircularProgressIndicator(color: Colors.white),
            ),
          if (_error != null)
            Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Text(
                  '游戏没打开：$_error',
                  textAlign: TextAlign.center,
                  style: const TextStyle(color: Colors.white),
                ),
              ),
            ),
        ],
      ),
    );
  }
}

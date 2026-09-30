import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_inappwebview/flutter_inappwebview.dart';

/// 游戏是 ES Modules，file:// 打不开，而且 Android WebView 对 file 下的
/// 模块脚本会直接拦截。用应用内 localhost 托管 assets/game。
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
  InAppWebViewController? _web;
  var _loading = true;
  String? _error;

  Future<void> _openGame() async {
    final web = _web;
    if (web == null) return;
    setState(() {
      _loading = true;
      _error = null;
    });
    await web.loadUrl(
      urlRequest: URLRequest(url: WebUri('http://127.0.0.1:${_server.port}/')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFFFF8EC),
      body: Stack(
        children: [
          InAppWebView(
            initialSettings: InAppWebViewSettings(
              javaScriptEnabled: true,
              domStorageEnabled: true,
              databaseEnabled: true,
              mediaPlaybackRequiresUserGesture: false,
              allowsInlineMediaPlayback: true,
              // 角色和标题星星都是脚本画进 SVG 的。关掉文件访问，
              // 避免 WebView 把 localhost 当成不安全来源，拦掉模块脚本。
              allowFileAccess: false,
              allowFileAccessFromFileURLs: false,
              allowUniversalAccessFromFileURLs: false,
              mixedContentMode: MixedContentMode.MIXED_CONTENT_NEVER_ALLOW,
              supportZoom: false,
              verticalScrollBarEnabled: false,
              horizontalScrollBarEnabled: false,
              transparentBackground: true,
              useWideViewPort: true,
              loadWithOverviewMode: false,
              useShouldOverrideUrlLoading: true,
            ),
            onWebViewCreated: (controller) {
              _web = controller;
              _openGame();
            },
            shouldOverrideUrlLoading: (controller, action) async {
              final url = action.request.url;
              if (url != null &&
                  (url.host == '127.0.0.1' || url.host == 'localhost')) {
                return NavigationActionPolicy.ALLOW;
              }
              return NavigationActionPolicy.CANCEL;
            },
            onLoadStop: (_, _) => setState(() => _loading = false),
            onReceivedError: (_, request, error) {
              if (request.isForMainFrame != true) return;
              setState(() {
                _loading = false;
                _error = error.description;
              });
            },
            onConsoleMessage: (_, message) {
              debugPrint('game: ${message.message}');
            },
          ),
          if (_loading)
            const ColoredBox(
              color: Color(0xFFFFF8EC),
              child: Center(
                child: CircularProgressIndicator(color: Color(0xFF3B6BFF)),
              ),
            ),
          if (_error != null)
            ColoredBox(
              color: const Color(0xFFFFF8EC),
              child: Center(
                child: Padding(
                  padding: const EdgeInsets.all(24),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        '游戏没打开：$_error',
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 16),
                      FilledButton(
                        onPressed: _openGame,
                        child: const Text('再试一次'),
                      ),
                    ],
                  ),
                ),
              ),
            ),
        ],
      ),
    );
  }
}

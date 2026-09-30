import 'package:flutter_test/flutter_test.dart';
import 'package:lulu_drill/main.dart';

void main() {
  testWidgets('shell shows the game page', (WidgetTester tester) async {
    await tester.pumpWidget(const LuluApp());
    expect(find.byType(GamePage), findsOneWidget);
  });
}

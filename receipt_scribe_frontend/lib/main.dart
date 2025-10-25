import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'screens/dashboard_screen.dart';
import 'screens/upload_screen.dart';
import 'providers/expense_provider.dart';

void main() {
  runApp(const ReceiptScribeApp());
}

class ReceiptScribeApp extends StatelessWidget {
  const ReceiptScribeApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => ExpenseProvider(),
      child: MaterialApp(
        title: 'ReceiptScribe',
        theme: ThemeData(
          primarySwatch: Colors.blue,
          useMaterial3: true,
        ),
        home: const DashboardScreen(),
        routes: {
          '/upload': (context) => const UploadScreen(),
        },
      ),
    );
  }
}
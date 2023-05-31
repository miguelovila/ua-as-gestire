import 'package:flutter/material.dart';
import 'package:gestire/welcome.dart';

void main() {
  runApp(const MainApp());
}

class MainApp extends StatelessWidget {
  const MainApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        debugShowCheckedModeBanner: false,
        title: 'Gestire',
        theme: ThemeData(
            useMaterial3: true,
            colorSchemeSeed: Colors.lightGreen,
            brightness: Brightness.light),
        darkTheme: ThemeData(
            useMaterial3: true,
            colorSchemeSeed: Colors.lightGreen,
            brightness: Brightness.dark),
        home: const Welcome());
  }
}

import 'package:flutter/material.dart';

class Rooms extends StatefulWidget {
  const Rooms({Key? key}) : super(key: key);

  @override
  _RoomsState createState() => _RoomsState();
}

class _RoomsState extends State<Rooms> {
  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(
        child: Column(
          children: [
            Text('Rooms'),
            TextField(
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Room',
                helperText: 'Example: DEI-1.1',
              ),
            )
          ],
        ),
      ),
    );
  }
}

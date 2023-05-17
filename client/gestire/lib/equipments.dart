import 'package:flutter/material.dart';

class Equipments extends StatefulWidget {
  const Equipments({Key? key}) : super(key: key);

  @override
  _EquipmentsState createState() => _EquipmentsState();
}

class _EquipmentsState extends State<Equipments> {
  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(
        child: Column(
          children: [
            Text('Equipments'),
            TextField(
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Equipment',
                helperText: 'Example: DEI-1.1',
              ),
            )
          ],
        ),
      ),
    );
  }
}

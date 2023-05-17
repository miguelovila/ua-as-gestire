import 'package:flutter/material.dart';
import 'package:gestire/rooms.dart';
import 'package:gestire/equipments.dart';
import 'package:gestire/records.dart';
import 'package:gestire/settings.dart';

class Dashboard extends StatefulWidget {
  const Dashboard({Key? key}) : super(key: key);

  @override
  _DashboardState createState() => _DashboardState();
}

class _DashboardState extends State<Dashboard> {
  int currentPage = 0;
  late PageController pageController;

  @override
  void initState() {
    super.initState();
    pageController = PageController(initialPage: currentPage);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: PageView(
          controller: pageController,
          onPageChanged: (int index) {
            setState(() {
              currentPage = index;
            });
          },
          children: const [
            Rooms(),
            Equipments(),
            Records(),
            Settings(),
          ],
        ),
        bottomNavigationBar: NavigationBar(
          selectedIndex: currentPage,
          onDestinationSelected: (int index) {
            setState(() {
              currentPage = index;
              pageController.animateToPage(currentPage,
                  duration: const Duration(milliseconds: 300),
                  curve: Curves.ease);
            });
          },
          destinations: destinations.map(
            (Destination destination) {
              return NavigationDestination(
                label: destination.label,
                icon: destination.icon,
                selectedIcon: destination.selectedIcon,
                tooltip: destination.label,
              );
            },
          ).toList(),
        ));
  }
}

class Destination {
  const Destination(this.label, this.icon, this.selectedIcon);
  final String label;
  final Widget icon;
  final Widget selectedIcon;
}

const List<Destination> destinations = <Destination>[
  Destination(
      'Rooms', Icon(Icons.meeting_room_outlined), Icon(Icons.meeting_room)),
  Destination('Equipments', Icon(Icons.home_repair_service_outlined),
      Icon(Icons.home_repair_service)),
  Destination('Records', Icon(Icons.history_outlined), Icon(Icons.history)),
  Destination('Settings', Icon(Icons.settings_outlined), Icon(Icons.settings)),
];

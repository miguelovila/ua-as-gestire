import 'package:flutter/material.dart';

class Dashboard extends StatefulWidget {
  const Dashboard({super.key});

  @override
  State<Dashboard> createState() => _DashboardState();
}

class _DashboardState extends State<Dashboard> {
  int screenIndex = 0;
  late bool showNavigationDrawer;

  void handleScreenChanged(int selectedScreen) {
    setState(() {
      screenIndex = selectedScreen;
    });
  }

  Widget buildBottomNavigation() {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: <Widget>[
            Text('Page Index =  $screenIndex'),
          ],
        ),
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: screenIndex,
        onDestinationSelected: (int index) {
          setState(() {
            screenIndex = index;
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
      ),
    );
  }

  Widget buildRailNavigation(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Row(
          children: <Widget>[
            NavigationRail(
              groupAlignment: 0.0,
              labelType: NavigationRailLabelType.all,
              selectedIndex: screenIndex,
              useIndicator: true,
              elevation: 10,
              onDestinationSelected: (int index) {
                setState(() {
                  screenIndex = index;
                });
              },
              minWidth: 100,
              destinations: destinations.map(
                (Destination destination) {
                  return NavigationRailDestination(
                    label: Text(destination.label),
                    icon: destination.icon,
                    selectedIcon: destination.selectedIcon,
                  );
                },
              ).toList(),
            ),
            const VerticalDivider(thickness: 1, width: 1),
          ],
        ),
      ),
    );
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    showNavigationDrawer = MediaQuery.of(context).size.width >= 700;
  }

  @override
  Widget build(BuildContext context) {
    return showNavigationDrawer
        ? buildRailNavigation(context)
        : buildBottomNavigation();
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

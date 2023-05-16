import 'package:flutter/material.dart';

class Dashboard extends StatefulWidget {
  const Dashboard({super.key});

  @override
  State<Dashboard> createState() => _DashboardState();
}

class _DashboardState extends State<Dashboard> {
  final GlobalKey<ScaffoldState> scaffoldKey = GlobalKey<ScaffoldState>();

  int screenIndex = 0;
  late bool showNavigationDrawer;

  void handleScreenChanged(int selectedScreen) {
    setState(() {
      screenIndex = selectedScreen;
    });
  }

  void openDrawer() {
    scaffoldKey.currentState!.openEndDrawer();
  }

  Widget buildBottomNavigation() {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: <Widget>[
            Text('Page Indexs =  $screenIndex'),
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
          (ExampleDestination destination) {
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
        key: scaffoldKey,
        body: SafeArea(
          bottom: false,
          top: false,
          child: Row(
            children: <Widget>[
              SizedBox(
                width: 150,
                child: NavigationDrawer(
                  onDestinationSelected: handleScreenChanged,
                  selectedIndex: screenIndex,
                  children: <Widget>[
                    ...destinations.map(
                      (ExampleDestination destination) {
                        return NavigationDrawerDestination(
                          label: Text(destination.label),
                          icon: destination.icon,
                          selectedIcon: destination.selectedIcon,
                        );
                      },
                    ),
                  ],
                ),
              ),
              const VerticalDivider(thickness: 0, width: 0),
            ],
          ),
        ));
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

class ExampleDestination {
  const ExampleDestination(this.label, this.icon, this.selectedIcon);

  final String label;
  final Widget icon;
  final Widget selectedIcon;
}

const List<ExampleDestination> destinations = <ExampleDestination>[
  ExampleDestination(
      'page 0', Icon(Icons.widgets_outlined), Icon(Icons.widgets)),
  ExampleDestination(
      'page 1', Icon(Icons.format_paint_outlined), Icon(Icons.format_paint)),
  ExampleDestination(
      'page 2', Icon(Icons.text_snippet_outlined), Icon(Icons.text_snippet)),
  ExampleDestination(
      'page 3', Icon(Icons.invert_colors_on_outlined), Icon(Icons.opacity)),
];

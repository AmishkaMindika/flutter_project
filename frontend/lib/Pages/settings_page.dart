import 'package:flutter/material.dart';

import '../style/colour.dart';
import 'about_page.dart';
import 'help_page.dart';


class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  bool notificationEnable = false; //state for notifications

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [AppColors.green_1,AppColors.green_2],
            begin: const FractionalOffset(0.0, 0.4),
            end: Alignment.topRight,
          ),
        ),
        child: Column(
          children: [
            Container(
              padding: const EdgeInsets.only(top: 30,left: 20,right: 20),
              width: MediaQuery.of(context).size.width,
              height: 100,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  SizedBox(height: 20,),
                  Align(
                    alignment: Alignment.centerLeft,
                    child: Text(
                      "Settings",
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 30,
                        color: AppColors.textMain,
                      ),
                    ),
                  )
                ],
              ),
            ),
            Expanded(
              child: Container(
                decoration: BoxDecoration(
                  color: AppColors.background,
                  borderRadius: BorderRadius.only(
                    topRight: Radius.circular(20),
                    topLeft: Radius.circular(20),
                  ),
                ),
                child: ListView(
                  padding: EdgeInsets.all(10),
                  children: [
                    ListTile(
                      leading: Icon(
                        Icons.account_circle_outlined,
                        color: AppColors.green_1,
                      ),
                      title: Text(
                        "Account",
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 20,
                        ),
                      ),
                      subtitle: Text(
                        "Manage your account settings"
                      ),
                      onTap: (){}, //Add Account Page settings
                    ),
                    Divider(),
                    ListTile(
                      leading: Icon(
                        Icons.notifications,
                        color: AppColors.green_1,
                      ),
                      title: Text(
                        "Notifications",
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 20,
                        ),
                      ),
                      subtitle: Text(
                        "Manage notification preferences",
                      ),
                      trailing: Switch(
                        value: notificationEnable,
                        onChanged: (bool value){
                          setState(() {
                            notificationEnable =value;
                          });
                        },
                      ),
                    ),
                    Divider(),
                    ListTile(
                      leading: Icon(
                        Icons.info_outline_rounded,
                      ),
                      title: Text(
                        "About",
                        style: TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 20,
                        ),
                      ),
                      subtitle: Text(
                        "App Information"
                      ),
                      onTap: (){
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => AboutPage()),
                        );
                      },
                    ),
                    Divider(),
                    ListTile(
                      leading: Icon(
                        Icons.question_mark_rounded
                      ),
                      title: Text(
                        "Help",
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 20,
                        ),
                      ),
                      subtitle: Text(
                          "Contact for Support"
                      ),
                      onTap: (){
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => HelpPage()),
                        );
                      },
                    ),
                  ],
                ),
              ),
            )
          ],
        ),
      ),
    );
  }
}

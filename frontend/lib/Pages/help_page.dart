import 'package:flutter/material.dart';
// import 'package:url_launcher/url_launcher.dart';
import '../style/colour.dart';

class HelpPage extends StatefulWidget {
  const HelpPage({super.key});

  @override
  State<HelpPage> createState() => _HelpPageState();
}

class _HelpPageState extends State<HelpPage> {
  //Launch Url code starts here
  // void launchURL(String url) async{
  //   final Uri uri = Uri.parse(url);
  //   if(!await launchUrl(uri,mode: LaunchMode.externalApplication)){
  //     throw "Could not launch $url";
  //   }
  // }
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
              padding: const EdgeInsets.only(top: 30, right: 20,left: 20),
              width: MediaQuery.of(context).size.width,
              height: 100,
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 10),
                child: Row(
                  children: [
                    GestureDetector(
                      onTap: (){
                        Navigator.pop(context);
                      },
                       child: Icon(
                        Icons.arrow_back_ios,
                        size: 25,
                        color: AppColors.textMain,
                      ),
                    ),
                    const SizedBox(width: 10,),
                    Text(
                      "Help Center",
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 30,
                        color: AppColors.textMain,
                      ),
                    ),
                  ],
                ),
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
                  children: [
                    ExpansionTile(
                      leading: Icon(
                        Icons.support_agent_rounded,
                        color: AppColors.green_1,
                        size: 30,
                      ),
                      //Added Email for contact and support in this drop down menu
                      title: Text(
                        "Contacts",
                        style: TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      children: [
                        ListTile(
                          title: Text(
                            "Email"
                          ),
                          leading: Icon(
                            Icons.email_rounded,
                            color: AppColors.green_1,
                          ),
                        ),
                      ],
                    ),
                    Divider(),
                    ExpansionTile(
                      leading: Icon(
                        Icons.face_6_rounded,
                        color: AppColors.green_1,
                        size: 30,
                      ),
                      //Added Social Media Links to this drop down menu
                      title: Text(
                        "Social Media",
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 20,
                        ),
                      ),
                      children: [
                        ListTile(
                          title: Text(
                            "Instagram",
                          ),
                          leading: Icon(
                            Icons.camera_alt_rounded
                          ),
                          //onTap: ()=> launchURL("https://www.instagram.com/p/DFvTzwFycFF/?utm_source=ig_web_copy_link"),
                        ),
                        ListTile(
                          title: Text(
                            "Youtube",
                          ),
                          leading: Icon(
                            Icons.video_camera_back,
                          ),
                          //onTap: ()=> launchURL("https://www.youtube.com/@SocialEase-e2l"),
                        ),
                        ListTile(
                          title: Text(
                            "Website",
                          ),
                          leading: Icon(
                            Icons.web,
                          ),
                          //onTap: ()=> launchURL("http://socialease.netlify.app/"),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

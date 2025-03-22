import 'package:flutter/material.dart';


import '../style/colour.dart';

class AboutPage extends StatefulWidget {
  const AboutPage({super.key});

  @override
  State<AboutPage> createState() => _AboutPageState();
}

class _AboutPageState extends State<AboutPage> {
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
                      "About Us",
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
                child: Padding(
                  padding: const EdgeInsets.all(20),
                  child: SingleChildScrollView(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          "Welcome to Social Ease",
                          style: TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                            color: AppColors.green_5,
                          ),
                        ),
                        const SizedBox(height: 10,),
                        Text(
                          "At Social Ease we believe that everyone deserves the confidence to express themselves "
                          "clearly and effectively, no matter the situation.Our app is designed for individual who struggle "
                          "with speaking in front of others whether in social settings,professional environments, or even casual conversation "
                          "We specifically focus on introverts and those who find it challenging to articulate their thoughts with confidence "
                          "when given the opportunity",
                          style: TextStyle(
                            fontSize: 15,
                            color: AppColors.textSub,
                          ),
                        ),
                        const SizedBox(height: 10,),
                        Text(
                          "Our Mission",
                          style: TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                            color: AppColors.green_5,
                          ),
                        ),
                        const SizedBox(height: 10,),
                        Text(
                          "Our goal is to create a supportive,structured and engaging leaning environment where "
                          "users can develop their speaking skills at their own pace."
                          "We aim to :",
                          style: TextStyle(
                            fontSize: 15,
                            color: AppColors.textSub,
                          ),
                        ),
                       const SizedBox(height: 5,),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            bulletPoint("Help individuals overcome the fear of public speaking."),
                            bulletPoint("Provide structured exercises that encourage gradual progress."),
                            bulletPoint("Foster self-expression through interactive and immersive activities."),
                            bulletPoint("Offer constructive feedback that builds confidence over time."),
                          ],
                        ),
                        const SizedBox(height: 10,),
                        Text(
                          "Why We Created This App",
                          style: TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                            color: AppColors.green_5,
                          ),
                        ),
                        const SizedBox(height: 10,),
                        Text(
                          "We understand how intimidating it can be to speak up, especially when confidence feels out of reach, "
                          "Many people have great ideas but struggle to voice them due to anxiety, self-doubt, "
                          "or lack of practice. Our team has designed this app to provide a safe and structured space where users "
                          "can grow at their own pace, free from judgment.",
                          style: TextStyle(
                            fontSize: 15,
                            color: AppColors.textSub,
                          ),
                        ),
                        const SizedBox(height: 10,),
                        Text(
                          "Who Is This App For",
                          style: TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                            color: AppColors.green_5,
                          ),
                        ),
                        const SizedBox(height: 10,),
                        Text(
                          "Whether you're a student preparing for presentations, a professional aiming to communication with impact,or "
                          "someone who simply wants to be more confident in daily conversations, Social is built to support you",
                          style: TextStyle(
                            fontSize: 15,
                            color: AppColors.textSub,
                          ),
                        ),
                        const SizedBox(height: 10,),
                        Text(
                          "Thank you for for using our app and supporting the Social Ease Team",
                          style: TextStyle(
                            fontSize: 15,
                            color: AppColors.textSub
                          ),
                        )
                      ],
                    )
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
  Widget bulletPoint (String text) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 3),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
              "• ",
            style: TextStyle(
              fontSize: 15,
              fontWeight: FontWeight.bold
            ),
          ),
          Expanded(
            child: Text(
              text,
              style: TextStyle(
                fontWeight: FontWeight.w500,
                fontSize: 15,
                color: AppColors.textSub,
              ),
            ),
          )
        ],
      ),
    );
  }
}

import 'package:flutter/material.dart';
import 'package:frontend_part_2/style/colour.dart';
import 'package:frontend_part_2/style/progress_chart.dart';


class ProgressTrackingPage extends StatefulWidget {
  const ProgressTrackingPage({super.key});

  @override
  State<ProgressTrackingPage> createState() => _ProgressTrackingPageState();
}

class _ProgressTrackingPageState extends State<ProgressTrackingPage> {
  List<double> progressData = [40,50,70,30,85,60,90];
  @override
  Widget build(BuildContext context) {
   return Scaffold(
     body: Container(
       decoration: BoxDecoration(
         gradient: LinearGradient(
           colors: [AppColors.green_1, AppColors.green_2],
           begin: const FractionalOffset(0.0, 0.4),
           end: Alignment.topLeft,
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
                 const SizedBox(height: 20,),
                 Align(
                   alignment: Alignment.centerLeft,
                   child: Text(
                     "Progress Branch",
                     style: TextStyle(
                       fontSize: 30,
                       color: AppColors.textMain,
                       fontWeight: FontWeight.bold,
                     ),
                   ),
                 ),
               ],
             ),
           ),
           Expanded(
             child: Container(
               decoration: BoxDecoration(
                 color: AppColors.background,
                 borderRadius: const BorderRadius.only(
                   topLeft: Radius.circular(20),
                   topRight: Radius.circular(20),
                 ),
               ),
               child: Column(
                 children: [
                   const SizedBox(height: 20,),
                   const Text(
                     "Your Weekly Progress",
                     style: TextStyle(
                       fontSize: 18,
                       fontWeight: FontWeight.bold,
                       color: AppColors.green_1,
                     ),
                   ),
                   ProgressChart(
                       progressData: progressData
                   ),
                   const SizedBox(height: 20,),
                   Text(
                     "Average : ${(progressData.reduce((a,b) => a + b / progressData.length).toStringAsFixed(1))}%",
                     style: TextStyle(
                       fontSize: 16,
                       fontWeight: FontWeight.bold,
                       color: AppColors.green_1
                     ),
                   )
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




import 'package:flutter/material.dart';

class ProgressChart extends StatefulWidget {
  final List<double> progressData;

  const ProgressChart({super.key, required this.progressData});

  @override
  ProgressChartState createState() => ProgressChartState();
}

class ProgressChartState extends State<ProgressChart> {
  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 350,
      child: Padding(
        padding: const EdgeInsets.only(left: 10, right: 20, top: 15),
        child: LineChart(
          LineChartData(
            gridData: FlGridData(
              show: true,
              drawVerticalLine: false,
              horizontalInterval: 10,
            ),
            titlesData: FlTitlesData(
              leftTitles: AxisTitles(
                sideTitles: SideTitles(
                  showTitles: true,
                  reservedSize: 40,
                  interval: 20,
                  getTitlesWidget: (value, meta) => Padding(
                    padding: const EdgeInsets.only(left: 10),
                    child: Text(
                      value.toInt().toString(),
                      style: TextStyle(
                        color: Colors.green, // Replace with AppColors.green_1
                      ),
                    ),
                  ),
                ),
              ),
              rightTitles: const AxisTitles(
                sideTitles: SideTitles(showTitles: false),
              ),
              topTitles: const AxisTitles(
                sideTitles: SideTitles(showTitles: false),
              ),
              bottomTitles: AxisTitles(
                sideTitles: SideTitles(
                  showTitles: true,
                  interval: 1,
                  getTitlesWidget: (value, meta) {
                    const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
                    if (value >= 0 && value < days.length) {
                      return Text(
                        days[value.toInt()],
                        style: TextStyle(
                          color: Colors.green, // Replace with AppColors.green_1
                        ),
                      );
                    }
                    return const Text("");
                  },
                ),
              ),
            ),
            borderData: FlBorderData(show: true),
            lineBarsData: [
              LineChartBarData(
                spots: List.generate(
                  widget.progressData.length,
                      (index) => FlSpot(index.toDouble(), widget.progressData[index]),
                ),
                isCurved: true,
                color: Colors.green, // Replace with AppColors.green_1
                barWidth: 3,
                dotData: FlDotData(show: true),
                belowBarData: BarAreaData(
                  show: true,
                  gradient: LinearGradient(
                    colors: [
                      Colors.green.withOpacity(0.4), // Replace with AppColors.green_2
                      Colors.green.withOpacity(0.1), // Replace with AppColors.green_3
                    ],
                    begin: Alignment.topCenter,
                    end: Alignment.bottomCenter,
                  ),
                ),
              ),
            ],
            minX: 0,
            maxX: 6,
            minY: 0,
            maxY: 100,
          ),
        ),
      ),
    );
  }

  LineChart(lineChartData) {}
}




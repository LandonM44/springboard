import 'dart:convert';
import 'package:http/http.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:clima_weather/services/location.dart';
import 'package:flutter/material.dart';

class NetworkHelper {
  NetworkHelper(this.url);

  final String url;

  Future getData() async {
    Response response = await get(Uri.parse(url));

    if (response.statusCode == 200) {
      String data = response.body;

      return jsonDecode(data);
    } else {
      print(response.statusCode);
    }
  }

  Future fetchWeatherData(lat, lon) async {
    Response response = await get(Uri.parse(
        'https://api.openweathermap.org/data/3.0/onecall?lat=$lat&lon=$lon&appid=d3d73c8595fb0ddaeaf3f00376096dd8&units=imperial'));
    //print(response.body);
    if (response.statusCode == 200) {
      String data = response.body;
      return jsonDecode(data);
    } else {
      print(response.statusCode);
      throw Exception('Failed to load weather data');
    }
  }
}
/*class NetworkHelper {
  NetworkHelper(this.url);

  final String url;


}*/

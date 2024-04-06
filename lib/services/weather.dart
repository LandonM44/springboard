import 'dart:convert';

import 'package:flutter/material.dart';
import 'location.dart';
import '../services/networking.dart';

const apiKey = 'e72ca729af228beabd5d20e3b7749713';
const openWeatherMapURL = 'https://api.openweathermap.org/data/2.5/weather';

class WeatherModel {
  int? cityLat;
  /*Future<dynamic> getCityWeather(String cityName) async {
    NetworkHelper networkHelper = NetworkHelper(
        'http://api.openweathermap.org/geo/1.0/direct?q=Newark,NJ,US&limit=5&appid=d3d73c8595fb0ddaeaf3f00376096dd8&units=imperial');

    var weatherData = await networkHelper.getData();
    cityLat = weatherData['lat'].toInt();
    print('/////////////////////////${cityLat}');
    print(weatherData);
    return weatherData;
  }*/

  Future<dynamic> getCityWeather(String cityName) async {
    NetworkHelper networkHelper = NetworkHelper(
        'http://api.openweathermap.org/geo/1.0/direct?q=$cityName&limit=5&appid=d3d73c8595fb0ddaeaf3f00376096dd8&units=imperial');

    var weatherData = await networkHelper.getData();

    // Assuming weatherData is a list of locations and you want to extract the first one
    if (weatherData.isNotEmpty) {
      var firstLocation = weatherData[0];
      double cityLat = firstLocation['lat'];
      double cityLon = firstLocation['lon'];

      print('//////////////////Latitude: $cityLat');
      print('Longitude: $cityLon');

      // Call fetchWeatherData with cityLat and cityLon
      var weatherDetails = await getWeather(cityLat, cityLon);

      // Use weatherDetails as needed
      print(weatherDetails);
      return weatherDetails;
    } else {
      print('No location found');
      return null;
    }
  }

  Future<dynamic> getLocationWeather() async {
    Location location = Location();
    await location.getCurrentLocation();

    NetworkHelper networkHelper = NetworkHelper(
        'https://api.openweathermap.org/data/3.0/onecall?lat=${location.latitude}&lon=${location.longitude}&appid=d3d73c8595fb0ddaeaf3f00376096dd8&units=imperial');

    var weatherData = await networkHelper.getData();
    return weatherData;
  }

  Future<dynamic> getWeather(double lat, double lon) async {
    NetworkHelper networkHelper = NetworkHelper(
        'https://api.openweathermap.org/data/3.0/onecall?lat=${lat}&lon=${lon}&appid=d3d73c8595fb0ddaeaf3f00376096dd8&units=imperial');

    var weatherData = await networkHelper.getData();
    //print(weatherData);
    return weatherData;
  }

  String getWeatherIcon(int condition) {
    if (condition < 300) {
      return '🌩';
    } else if (condition < 400) {
      return '🌧';
    } else if (condition < 600) {
      return '☔️';
    } else if (condition < 700) {
      return '☃️';
    } else if (condition < 800) {
      return '🌫';
    } else if (condition == 800) {
      return '☀️';
    } else if (condition <= 804) {
      return '☁️';
    } else {
      return '🤷‍';
    }
  }

  String getMessage(int temp) {
    if (temp > 70) {
      return 'It\'s 🍦 time';
    } else if (temp > 55) {
      return 'Time for shorts and 👕';
    } else if (temp < 40) {
      return 'You\'ll need 🧣 and 🧤';
    } else {
      return 'Bring a 🧥 just in case';
    }
  }
}

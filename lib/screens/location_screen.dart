import 'package:clima_weather/screens/city_screen.dart';
import 'package:flutter/material.dart';
import 'package:clima_weather/utilities/constants.dart';
import 'package:clima_weather/services/weather.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

class LocationScreen extends StatefulWidget {
  late final locationWeather;

  LocationScreen({this.locationWeather});
  @override
  _LocationScreenState createState() => _LocationScreenState();
}

class _LocationScreenState extends State<LocationScreen> {
  WeatherModel weather = WeatherModel();
  String? weatherMessage;
  String? weatherIcon;
  late int temperature;
  late int condition;
  late String cityName;
  bool isLoading = true;

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    updateUi(widget.locationWeather);
    print(widget.locationWeather);
  }

  void updateUi(dynamic weatherData) {
    if (weatherData == null) {
      setState(() {
        isLoading =
            false; // Set loading to false when data fetching is complete
        temperature = 0;
        weatherIcon = 'error';
        weatherMessage = "we are unable to get your weather data";
      });
      return;
    }
    double temp = weatherData['current']['temp'];
    setState(() {
      isLoading = false; // Set loading to false when data fetching is complete
      temperature = temp.toInt();
      condition = weatherData['current']['weather'][0]['id'];
      cityName = weatherData['timezone'];
      weatherIcon = weather.getWeatherIcon(condition);
      weatherMessage = weather.getMessage(temperature);
    });
  }

  /* void updateUi(dynamic weatherData) {
    if (weatherData == null) {
      temperature = 0;
      weatherIcon = 'error';
      weatherMessage = "we are unable to get your weather data";
      return;
    }
    double temp = weatherData['current']['temp'];
    temperature = temp.toInt();
    condition = weatherData['current']['weather'][0]['id'];
    cityName = weatherData['timezone'];
    weatherIcon = weather.getWeatherIcon(condition);
    weatherMessage = weather.getMessage(temperature);
  }*/

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        Scaffold(
          body: Container(
            decoration: BoxDecoration(
              image: DecorationImage(
                image: AssetImage('images/location_background.jpg'),
                fit: BoxFit.cover,
                colorFilter: ColorFilter.mode(
                    Colors.white.withOpacity(0.8), BlendMode.dstATop),
              ),
            ),
            constraints: BoxConstraints.expand(),
            child: SafeArea(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: <Widget>[
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: <Widget>[
                      TextButton(
                        onPressed: () async {
                          var weatherData = await weather.getLocationWeather();
                          updateUi(weatherData);
                          print(weatherData);
                        },
                        child: Icon(
                          Icons.near_me,
                          size: 50.0,
                        ),
                      ),
                      TextButton(
                        onPressed: () async {
                          var typedName = await Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) {
                                return CityScreen();
                              },
                            ),
                          );
                          if (typedName != null) {
                            var weatherInfo =
                                await weather.getCityWeather(typedName);
                            updateUi(weatherInfo);
                          }
                        },
                        child: Icon(
                          Icons.location_city,
                          size: 50.0,
                        ),
                      ),
                    ],
                  ),
                  Padding(
                    padding: EdgeInsets.only(left: 15.0),
                    child: Row(
                      children: <Widget>[
                        Text(
                          temperature.toString(),
                          style: kTempTextStyle,
                        ),
                        Text(
                          weatherIcon!,
                          style: kConditionTextStyle,
                        ),
                      ],
                    ),
                  ),
                  Padding(
                    padding: EdgeInsets.only(right: 15.0),
                    child: Text(
                      weatherMessage!,
                      textAlign: TextAlign.right,
                      style: kMessageTextStyle,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
        if (isLoading)
          Center(
            child: SpinKitWave(
              color: Colors.white,
              size: 50.0,
            ),
          ),
      ],
    );
  }
}

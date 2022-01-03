[![App running](https://github.com/IvanVnucec/rain_alert/actions/workflows/weather_check.yml/badge.svg?branch=master&event=schedule)](https://github.com/IvanVnucec/rain_alert/actions/workflows/weather_check.yml)

# rain_alert
You will not forget your umbrella anymore. :umbrella:

## About
Check every morning at 5 AM local time if it will be raining that day, if yes 
send an email with forecast message like this:
<html>
  <table>
    <tr>
        <th>Hour [h]</th>
        <th>Probability [%]</th>
    </tr>
    <tr>
        <td>6</td>
        <td id="CELL0">0</td>
    </tr>
    <tr>
        <td>7</td>
        <td id="CELL1">0</td>
    </tr>
    <tr>
        <td>8</td>
        <td id="CELL2">0</td>
    </tr>
    <tr>
        <td>9</td>
        <td id="CELL3">0</td>
    </tr>
    <tr>
        <td>10</td>
        <td id="CELL4">10</td>
    </tr>
    <tr>
        <td>11</td>
        <td id="CELL5">22</td>
    </tr>
    <tr>
        <td>12</td>
        <td id="CELL6">35</td>
    </tr>
    <tr>
        <td>13</td>
        <td id="CELL7">60</td>
    </tr>
    <tr>
        <td>14</td>
        <td id="CELL8">86</td>
    </tr>
    <tr>
        <td>15</td>
        <td id="CELL9">100</td>
    </tr>
    <tr>
        <td>16</td>
        <td id="CELL10">100</td>
    </tr>
    <tr>
        <td>17</td>
        <td id="CELL11">100</td>
    </tr>
    <tr>
        <td>18</td>
        <td id="CELL12">100</td>
    </tr>
    <tr>
        <td>19</td>
        <td id="CELL13">72</td>
    </tr>
    <tr>
        <td>20</td>
        <td id="CELL14">36</td>
    </tr>
    <tr>
        <td>21</td>
        <td id="CELL15">5</td>
    </tr>
    <tr>
        <td>22</td>
        <td id="CELL16">0</td>
    </tr>
    <tr>
        <td>23</td>
        <td id="CELL17">0</td>
    </tr>
  </table>
</html>

## Get started
0. Create Gmail account and enable the Less secure app access and also create an OpenWeather API Key.
1. Create `credentials/credentials.yaml` file and put Gmail and OpenWeather credentials from step 0.
```
senderEmail: <sender Gmail email>
senderPassword: <Gmail email password>
openWeatherApiKey: <OpenWeather API key>
```
2. Create `credentials/receivers.txt` file put in email subscribers. For example:
```
example1@email.com, Zagreb
example2@email.com, Berlin
example3@email.com, Milwaukee
example4@email.com, Mobile Alabama
example5@email.com, Nashville Tennessee
example6@email.com, Nashville Indiana
```
3. Run the app using Makefile as `make run`
4. (Recommended) You can schedule the script to run on GitHub servers like we did in 
[our GitHub Actions CI workflow](https://github.com/IvanVnucec/rain_alert/blob/master/.github/workflows/weather_check.yml). 
See the [Instructions](./.github/workflows/README.md) for more info.

## License
[MIT](LICENSE.md)

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h3 align="center">HMS</h3>

  <p align="center">
HMS is basic webapplication using flask. The Documentation is given with the code. You can use this for mini-project.
    <br />
    <a href="https://github.com/dhina016/HMS"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/dhina016/HMS/issues">Report Bug</a>
    ·
    <a href="https://github.com/dhina016/HMS/issues">Request Feature</a>
    .
    <a href="https://www.instagram.com/anintrovertinlove/">Instagram</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)



<!-- ABOUT THE PROJECT -->
## About The Project

![Product Name Screen Shot][product-screenshot]
  
HMS is a webapplication using flask. This retail banking is a mini project. You can
use this project for free. The Documentation is given with the code.If you like this project give stars..


### Built With

* [Bootsrap](https://getbootstrap.com/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Jinja](https://jinja.palletsprojects.com/en/2.11.x/)

<!-- GETTING STARTED -->
## Getting Started

Follow the installation steps to open project without error

### Installation
 
1. Download and extract the project
2. I'm using xampp, so you can also use it and Create the database
3. Upload or Import flask.sql in your database. 
4. Download python 3.x and install on your PC. My pc is 64bit so i installed Python3(64bit). Set environmental variable for both python and pip or else you get command not found.
5. I've used virtual environment. It's not necessary, but using virtual environment is preferable.  
Note: You can skip the 5th step if you don't want virtual environment  
(i) Make sure you've set your python path in environmental variable and then install 
```sh

python -m venv venv

```
(ii) I've already created. So now you want to activate it. I'm using windows. so I used CMD. Now open the cmd of your current project folder. My project folder is HMS.
```sh

D:\flask\HMS> cd venv/Scripts/activate

After venv is activated

(venv) D:\flask\HMS>

```
(iii) Once you can close the project, this command is user to open the venv again and for deactivation command also given.
```sh

D:\flask\HMS>workon venv

If not working again activate your venv

(venv) D:\flask\HMS>

For Deactivating,

D:\flask\HMS> cd venv/Scripts/deactivate

```
6. Install the following requirements by following command.
```sh

D:\flask\HMS> pip install -r requirements.txt

```
7. To run the the code, use this command 
```sh

D:\flask\HMS>python app.py

or

D:\flask\HMS>flask run

```

8. If you get any error, make sure you've done following things 
```sh

1. Python version should be 3.x.
2. Settingup Environment variables.
3. Installed all requirements without errors.
4. I am using 64 bit. If you are using 32 Bit google it and fix it.
5. Check the server is active or not.
6. Imported sql file.
7. Everything is done.
```
9. Admin Login.
```sh
url : http://127.0.0.1:5000/login
Username => admin,
Password => !1Qqwerty,

```

Credential at hosted site
* username = executive
* password = Exec@1
* username = desk
* password = Exec@1
* username = pharmacist
* password = Exec@1
<!-- USAGE EXAMPLES -->
## Usage

HMS is a webapp. This HMS is very simple to use.

<!-- TEAM -->
## Team

We created this project for TCS Case Study. Special thanks to my team!!
1. Gokul - https://github.com/gokulrv4399


<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/dhina016/HMS/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/dhina016/HMS](https://github.com/dhina016/HMS)




<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/dhina016/HMS.svg?style=flat-square
[contributors-url]: https://github.com/dhina016/HMS/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/dhina016/HMS.svg?style=flat-square
[forks-url]: https://github.com/dhina016/HMS/network/members
[stars-shield]: https://img.shields.io/github/stars/dhina016/HMS.svg?style=flat-square
[stars-url]: https://github.com/dhina016/HMS/stargazers
[issues-shield]: https://img.shields.io/github/issues/dhina016/HMS.svg?style=flat-square
[issues-url]: https://github.com/dhina016/HMS/issues
[license-shield]: https://img.shields.io/github/license/dhina016/HMS.svg?style=flat-square
[license-url]: https://github.com/dhina016/HMS/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/dhina016/
[ss1]: screenshot/ss1.PNG
[ss2]: screenshot/ss2.PNG
[ss3]: screenshot/ss3.PNG
[ss4]: screenshot/ss4.PNG
[ss5]: screenshot/ss5.PNG
[ss6]: screenshot/ss6.PNG
[ss7]: screenshot/ss7.PNG
[ss8]: screenshot/ss8.PNG
[ss9]: screenshot/ss9.PNG
[ss10]: screenshot/ss10.PNG
[ss11]: screenshot/ss11.PNG
[ss12]: screenshot/ss12.PNG
[ss13]: screenshot/ss13.PNG
[ss14]: screenshot/ss14.PNG
[ss15]: screenshot/ss15.PNG
[ss16]: screenshot/ss16.PNG
[ss17]: screenshot/ss17.PNG
[ss18]: screenshot/ss18.PNG
[ss19]: screenshot/ss19.PNG
[ss20]: screenshot/ss20.PNG
[ss21]: screenshot/ss21.PNG
=======
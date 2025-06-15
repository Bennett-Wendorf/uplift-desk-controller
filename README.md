<!--
*** This readme is inspired by the Best-README-Template available at https://github.com/othneildrew/Best-README-Template. Thanks to othneildrew for the inspiration!
-->


<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
<!-- [![Forks][forks-shield]][forks-url] -->



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h1 align="center">Uplift Desk Controller</h3>

  <p align="center">
    An unofficial Python library for control of Uplift standing desks over BLE.
    <br />
    <a href="https://github.com/Bennett-Wendorf/uplift-desk-controller"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Bennett-Wendorf/uplift-desk-controller/issues">Report Bug</a>
    ·
    <a href="https://github.com/Bennett-Wendorf/uplift-desk-controller/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#getting-started">Getting Started</a></li>
      <ul>
        <li><a href="#running-the-demo">Running the Demo</a></li>
      </ul>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

I'll say it again. This is an **UNOFFICIAL** library for control of Uplift Desk standing desks over Bluetooth Low Energy (BLE). For this library to work, you must have the [Uplift Bluetooth Adapter](https://www.upliftdesk.com/bluetooth-adapter-for-uplift-desk/?15775=12278) installed in a compatible desk. See their website for a better understanding of desk compatibility. 

Unfortunately, like the app, this controller is a bit limited in what can be controlled. As of v1, controls include moving to standing preset, moving to sitting preset, raising the desk, and lowering the desk. The desk's bluetooth protocol does not allow using the presets on your desk's advanced keypad (if installed). In addition, I've done my best to reverse engineer the bluetooth service that Uplift uses (with the help of a few other open source projects. See [Acknowledgements](#acknowledgements) for details), but there are a few characteristics that are still unknown. If you'd like to help add more functionality, see the [Contributing](#contributing) section below.

For now, it is also not possible to configure the desk settings such as name, presets, etc. through this controller. To use this project effectively, you'll want to first install the Uplift Desk app on iOS or Android and set up some of the basic settings (including sit and stand presets).

> Note: When using this project, no other device can be connected to the desk or it will be undiscoverable. This means that the Uplift Desk app needs to be either disconnected or closed for this application to work.

### Built With

This project is written in Python using the following libraries:
* [Python](https://www.python.org/)
* [Bleak](https://pypi.org/project/bleak/)
* For a full list of dependencies, see [Pipfile](https://github.com/Bennett-Wendorf/uplift-desk-controller/blob/main/Pipfile)

Each of their respective licenses apply to their binaries and their use in this project. Their licenses can be found at the links above.

<!-- Getting Started -->
## Getting Started
This project was built primarily for use in my [Home Assistant integration](https://github.com/Bennett-Wendorf/hass-uplift-desk), but you can also run it standalone. To make this easier, I created a demo application.

### Running the Demo
1. Clone the repository and open a terminal to it
2. Execute `pipenv install` to build a virtual environment and install the dependencies
3. Exeucte the demo with `pipenv run python demo.py`

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

If you find an issue in existing code, feel free to use the above procedure to generate a change, or open an [issue](https://github.com/Bennett-Wendorf/uplift-desk-controller/issues) for me to fix it.


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Bennett Wendorf - [Website](https://bennettwendorf.dev/) - bennett@bennettwendorf.dev

Project Link: [https://pypi.org/project/uplift-desk](https://pypi.org/project/uplift-desk)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Img Shields](https://shields.io)
* [https://github.com/william-r-s/desk_controller_uplift](https://github.com/william-r-s/desk_controller_uplift)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/bennett-Wendorf/NeuraViz.svg?style=flat&color=informational
[contributors-url]: https://github.com/Bennett-Wendorf/uplift-desk-controller/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/bennett-Wendorf/uplift-desk-controller.svg?style=flat
[forks-url]: https://github.com/Bennett-Wendorf/uplift-desk-controller/network/members
[stars-shield]: https://img.shields.io/github/stars/bennett-Wendorf/uplift-desk-controller.svg?style=flat&color=yellow
[stars-url]: https://github.com/Bennett-Wendorf/uplift-desk-controller/stargazers
[issues-shield]: https://img.shields.io/github/issues/bennett-Wendorf/uplift-desk-controller.svg?style=flat&color=red
[issues-url]: https://github.com/Bennett-Wendorf/uplift-desk-controller/issues
[license-shield]: https://img.shields.io/github/license/bennett-Wendorf/uplift-desk-controller.svg?style=flat
[license-url]: https://github.com/Bennett-Wendorf/uplift-desk-controller/blob/main/LICENSE

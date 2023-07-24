<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="APP IMAGE" width="80" height="80">
  </a>

  <h3 align="center">Juggling Tracker and Siteswap Extractor</h3>

  <p align="center">
    A project capable of performing ball detection and tracking in juggling videos on one hand, and extracting the executed siteswap on the other.
    <br />
    <br />
    <a href="https://github.com/AlejandroAlonsoG/tfg_jugglingTrackingSiteswap"><strong>Paper (still unpublished, check files)</strong></a>
    <br />
    <br />
    <a href="https://github.com/AlejandroAlonsoG/tfg_jugglingTrackingSiteswap">View Demo</a>
    ·
    <a href="https://github.com/AlejandroAlonsoG/tfg_jugglingTrackingSiteswap/issues">Report Bug</a>
    ·
    <a href="https://github.com/AlejandroAlonsoG/tfg_jugglingTrackingSiteswap/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

The project aims to develop a system capable of extracting juggling siteswaps from videos of jugglers performing their tricks. Siteswap is a widely used notation in juggling to describe patterns. However, there is currently no accessible application that can automatically extract the siteswap from juggling videos. The proposed system will try to address this gap.

The developed system performs well in ideal conditions, successfully identifying the siteswaps in approximately 77.27% of cases. While this level of accuracy may already be sufficient for experienced jugglers, future revisions could focus on improving the system's performance in less ideal video conditions. The ultimate goal is to create an application that can accurately identify complex siteswaps executed by skilled jugglers.

More detailed explanations can be found in the paper referenced at the beginning of this README or by contacting me directly.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Required dependencies can be found in the requirements.txt file.

### Installation

Not every necessary file is uploaded to the repository.

Once you have cloned it, you will have to prepare the directory as follows for it to work without any modifications:

- tfg_jugglingTrackingSiteswap
  - files
    - (this folder just as it is downloaded)
  - results
    - (this folder just as it is downloaded)
  - dataset
    - here goes all the videos from the dataset. By default, they are expected in a subfolder called tanda2 with the naming convention {ss}\_{color}\_{juggler}.mp4




With that and all dependencies installed, the application should work. If you encounter any problem, feel free to contact me.

<!-- USAGE EXAMPLES -->
## Usage

For the execution of the final system, it is enough to open a terminal in .../tfg_jugglingTrackingSiteswap and execute:

```bash
python3 files/final_system.py
```

Any tracking system can be executed on their own in a similar way as if they were main programs. The same thing goes with the tracking_visualizer.



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Alejandro Alonso - [@twitter](https://twitter.com/MelenalexYT) - alexalongarci@gmail.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

The base programs for the main tracking implementations came from

* [Stephen Meschke](https://github.com/smeschke/juggling)
* [Barton Chittenden](https://github.com/bartonski/juggling_detector)

The template of this README came from:
* [othneildrew](https://github.com/othneildrew/Best-README-Template/tree/master)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

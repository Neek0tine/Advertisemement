<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/neek0tine/Advertisemement) ![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/neek0tine/Advertisemement) ![GitHub License](https://img.shields.io/github/license/neek0tine/adveritsemement) ![Maintenance](https://img.shields.io/maintenance/yes/2024)
<div align="center">
  <a href="https://github.com/neek0tine/advertisemement">
    <img src="https://github.com/Neek0tine/Advertisemement/blob/main/graphics/banner-01.png" alt="Logo">
  </a>
</div>

# Advertisemement: The Digital Codebook
Adveritsemement (diambil dari penggabungan kata <i>Advertisement</i> dan <i>Meme</i>) adalah aplikasi berbasis web yang ditujukan sebagai _codebook_ digital untuk memudahkan proses pengodingan (_labelling_) konten multimedia dari sosial media Instagram. Berbeda dari cara knovensional yang menggunakan formulir koding yang berbentuk dokumen atau _spreadsheet_, Advertisemement mengintegrasikan basis data tempat penyimpanan data koding dengan sumber konten secara langsung di satu tempat. Selain sebagai pendukung kenyamanan dan kecepatan dalam proses koding, pembuatan aplikasi web juga membolehkan lebih dari satu koder untuk bekerja bersamaan di konten yang sama, memudahkan perhitungan Kappa yang alhasil akan memberikan hasil koding yang objektif dan akurat. 

<!-- GETTING STARTED -->
# Installation and Usage

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

# Screenshots
<div align="center">
  <a href="https://github.com/neek0tine/advertisemement">
    <img src="https://github.com/Neek0tine/Advertisemement/blob/main/graphics/login.png" alt="Logo">
  </a>
</div>

<div align="center">
  <a href="https://github.com/neek0tine/advertisemement">
    <img src="https://github.com/Neek0tine/Advertisemement/blob/main/graphics/main.png" alt="Logo">
  </a>
</div>

<div align="center">
  <a href="https://github.com/neek0tine/advertisemement">
    <img src="https://github.com/Neek0tine/Advertisemement/blob/main/graphics/main2.png" alt="Logo">
  </a>
</div>
<br>

## Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* MariaDB
* Python
* Folder containing 1000+ instagram psots as `Instaloader.post` objects
## Installation

1. Initiate a database system
2. Import the posts data from `Advertisemement.sql` and make changes to the `local_download_dir` column
3. Configure database connection in `backend/auth/config.py` and set `dbmodel.py` appropriately to your own.
4. Run `run.py` to start Flask server
<p align="right">(<a href="#readme-top">back to top</a>)</p>

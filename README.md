# meerkat_dev
Contains the configs and scripts required to run the Meerkat development environment.

System requirements:
-----------
You need to have Linux or Macos, `python 2.7` with `pip`, `passlib`, `git` (configured with your ssh key), `docker` and `docker-compose`

Get Started
-----------
1. Create folder to store the Meerkat Code base. e.g. /home/[user]/meerkat
2. Change directory into that folder. `cd /home/[user]/meerkat`
3. Git clone this repository:
   `git clone git@github.com:meerkat-code/meerkat_dev.git`
4. The development environment script `mk` is in the new meerkat_dev folder.
   It is recommended that you create a symlink to this script from your path:
   `ln -s /home/[user]/meerkat/meerkat_dev/mk /usr/local/bin/mk`
5. Run the setup process `mk setup`.
   *N.B* This will install only the demo country configs. If you have access to
   all country configs use `--all` option to install the complete development
   environment.
6. Use `mk -h` to read the script's documentation.



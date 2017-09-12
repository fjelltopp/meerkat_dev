# meerkat_dev
Contains the configs and scripts required to run the Meerkat development environment.

Get Started
-----------
1. Create folder to store the Meerkat Code base. e.g. /home/[user]/meerkat
2. Change directory into that folder. `cd /home/[user]/meerkat`
3. Git clone this repository:
   `git clone git@github.com:meerkat-code/meerkat_dev.git`
4. The development environment script `mk` is in the new meerkat_dev folder.
   It is recommended that you create a symlink to this script from your path:
   `symlink -l /usr/local/bin/mk /home/[user]/meerkat/meerkat_dev/mk`
5. Run the setup process `mk setup`.
6. Use `mk -h` to read the script's documentation.

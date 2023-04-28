apt-get -y install devscripts dh-make

mkdir -p hello-world/hello-world-0.0.1

cd hello-world/hello-world-0.0.1

cp /assets/hello-world.sh .

dh_make --indep --createorig

echo "hello-world.sh usr/bin/" > debian/install

dpkg-buildpackage
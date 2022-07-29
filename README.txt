cd /build
git clone https://github.com/brion/mtpng.git
cd mtpng
make
cp build/libmtpng.so /usr/local/lib/.

cd /build/pymtpng
swig -python mtpng.i

rm -f /io/wheelhouse/pymtpng*.whl
/opt/py/cp39-cp39/bin/pip wheel . --no-deps -w /io/wheelhouse 
auditwheel repair --only-plat --plat manylinux2014_x86_64 -w /io/wheelhouse /io/wheelhouse/pymtpng*.whl


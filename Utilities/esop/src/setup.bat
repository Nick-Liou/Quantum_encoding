

@REM Clone project fork (original code at https://github.com/hriener/easy)
git clone git@github.com:Nick-Liou/easy.git


cd easy 
mkdir build
cd build

cmake -DEASY_TEST=ON ..
cmake --build .

@REM Run tests
.\test\Debug\run_tests.exe
# Tecerator
 
Tecerator is an utility for creating competitive programming task packages, designed to be judge-independent, feature-rich and simple to use. 
See [example/](example/) for a small task definition.
The fields in desc.tex will be updated automatically if changed in manifest.py. 
To build a sio2 package, install tecerator(`pip3 install tecerator`) and run `python3 manifest.py build --target=sio2-staszic` in the package directory.
The package will be built in build/native/sio2-staszic/add.zip.
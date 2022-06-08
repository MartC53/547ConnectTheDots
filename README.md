# Android App
In order to run the android app the project must be built in android studio. The best way to run this app is to download the compressed file from this branch, extract it, and open the project in Android Studio. **The model is stored as a .pkl file**, for your security the .pkl file is not added to the build. To add the .pkl first run the model from the main branch of the repo then or copy the file to the following directory:

```
.
├── Project
│   └── ConnecttheDots
│       └── app
│         └── src
│           └── python
│             └── model.pkl
```
Re-sync the gradle files and rebuild the app. The app can then be evaluated using a virtual device in the device manager or installed on an android phone that has developer mode and usb debugging enabled.


This app was built using Android Studio Chipmunk and python 3.10 on linux. For virtualization a pixel 4a running release operating system was used. The build information is as follows
Build #AI-212.5712.43.2112.8512546, built on April 28, 2022
Runtime version: 11.0.12+0-b1504.28-7817840 amd64
VM: OpenJDK 64-Bit Server VM by JetBrains s.r.o.
Linux 5.17.5-76051705-generic
GC: G1 Young Generation, G1 Old Generation
Memory: 2048M
Cores: 8
Registry: external.system.auto.import.disabled=true

Current Desktop: pop:GNOME

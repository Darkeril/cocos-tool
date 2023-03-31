@echo off
set COCOS_CREATOR_PATH=%1
set COCOS_PRO_ROOT=%2

cd %COCOS_PRO_ROOT%/autobuild
echo Building test package...

echo Cocos Creator Path: %COCOS_CREATOR_PATH%
echo Cocos Project Root: %COCOS_PRO_ROOT%

robocopy "..\assets\bundle" "..\restemp\bundle" /E /MOVE > nul
move "..\assets\bundle.meta" "..\restemp"
echo setting
node reset_build_json_dev
echo setting done
echo start apk richmaster
%COCOS_CREATOR_PATH% --path ../ --build ../local/builder.json
echo cocos build succ
rmdir /s /q "..\richmasterbuildrelease\jsb-link\assets"
rmdir /s /q "..\richmasterbuildrelease\jsb-link\src"
rmdir /s /q "..\richmasterbuildrelease\jsb-link\frameworks\runtime-src\proj.android-studio\app\build\outputs\apk\release"
echo assets-del done
robocopy "..\build\jsb-link\assets" "..\richmasterbuildrelease\jsb-link\assets" /E /MOVE > nul
robocopy "..\build\jsb-link\src" "..\richmasterbuildrelease\jsb-link\src" /E /MOVE > nul
echo assets-copy done
call build-aab.bat
echo build aab apk succ
cd C:\work\gongsi\qyg\autobuild
node apk-copy
echo copy succ
robocopy "..\restemp\bundle" "..\assets\bundle" /E /MOVE > nul
move "..\restemp\bundle.meta" "..\assets"
echo all succ
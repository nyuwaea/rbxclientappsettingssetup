import os
import re

fpsTarget = 144
appSettings = '{\n\t"FFlagHandleAltEnterFullscreenManually": "False",\n\t"DFIntTaskSchedulerTargetFps": ' + str(fpsTarget) + '\n}'

userPath = os.getenv("APPDATA").rstrip("Roaming") + "\\Local\\Roblox\\Versions\\"
adminPath = os.getenv("ProgramFiles(x86)") + "\\Roblox\\Versions\\"

def init():
    path = userPath
    if not os.path.isdir(path):
        path = adminPath
        if not os.path.isdir(path):
            return

    versions = {}
    sortComplete = False

    for f in os.scandir(path):
        if os.path.isdir(f.path) and re.match("version-", f.name):
            versions[len(versions)] = {
                "dir": f,
                "ctime": int(os.path.getctime(f))
            }

    try:
        versions[0]
    except:
        return

    while not sortComplete:
        _arrayWrite = False

        for i in range(len(versions)):
            try:
                _current = versions[i]
                _next = versions[i + 1]
            except:
                break

            if _next["ctime"] > _current["ctime"]:
                versions[i] = _next
                versions[i + 1] = _current
                _arrayWrite = True

        sortComplete = not _arrayWrite

    latestVersionPath = versions[0]["dir"].path
    clientSettingsDir = latestVersionPath + "\\ClientSettings"
    clientAppSettingsFile = clientSettingsDir + "\\ClientAppSettings.json"

    if not os.path.isdir(clientSettingsDir):
        os.mkdir(clientSettingsDir)
    
    f = open(clientAppSettingsFile, "w")
    f.write(appSettings)

init()

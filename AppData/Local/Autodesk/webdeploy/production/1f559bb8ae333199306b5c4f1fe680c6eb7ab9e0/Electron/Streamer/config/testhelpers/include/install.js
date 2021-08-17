function DoInstall(appname, argsin) {
    var fso = WScript.CreateObject("Scripting.FileSystemObject");
    var shell = WScript.CreateObject("WScript.Shell");

    var base = fso.GetParentFolderName(WScript.ScriptFullName);
    var exe = fso.BuildPath(base, "Windows");
    exe = fso.BuildPath(exe, appname + " Client Downloader" + ".exe");

    var args = [];
    for (var i=0; i < argsin.Length; i++) {
        args.push(argsin(i));
    }

    var root = fso.BuildPath(fso.GetParentFolderName(base), "packages");
    root = root.replace(/\\/g, "/" );

    if (root.substr(0,2) == "//") {
        root = root.substr(1); // Strip the leading slash
    }
    var cmd = '"' + exe + '" -c "file:///' + root + '/"';
    if (args.length) {
        cmd += ' "' + args.join('" "') + '"';
    }

    shell.Run(cmd);
}

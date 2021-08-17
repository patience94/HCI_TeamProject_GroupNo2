var args = WScript.Arguments;
var fso = new ActiveXObject("Scripting.FileSystemObject");
var i;
for (i = 0; i != args.length; ++i)
	WScript.Echo(fso.GetFileVersion(args(i)));
